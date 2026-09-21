"""
Junta audio narrado + imágenes por bloque + música de fondo en el video final.

Usa ffmpeg directamente (sin moviepy): el zoom Ken Burns se hace con filtros
nativos de ffmpeg y el encoding con la GPU (h264_nvenc) si está disponible,
cayendo a libx264 por CPU si no. Cada bloque se renderiza como un segmento
independiente (varios en paralelo) y al final se concatenan sin re-encodear,
junto con la narración y la música.

Uso:
    python assemble_video.py output/audio_manifest.json output/visuals_manifest.json config.yaml
"""

import json
import random
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

ENCODER_ARGS = {
    # calidad ~ equivalente; nvenc usa la GPU (RTX), libx264 la CPU
    "nvenc": ["-c:v", "h264_nvenc", "-preset", "p4", "-tune", "hq", "-rc", "vbr", "-cq", "23", "-b:v", "0"],
    "libx264": ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"],
}


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def probe_duration(path: Path) -> float:
    out = run([
        FFPROBE, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ]).stdout.strip()
    return float(out)


def probe_audio_format(path: Path) -> tuple[int, int]:
    """(sample_rate, channels) del primer stream de audio."""
    out = run([
        FFPROBE, "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels",
        "-of", "csv=p=0", str(path),
    ]).stdout.strip()
    sr, ch = out.split(",")[:2]
    return int(sr), int(ch)


def check_audio_formats(paths: list[Path]) -> tuple[int, int]:
    """El concat demuxer exige que todos los WAV tengan el mismo formato. Si no,
    los bloques posteriores quedan corridos respecto al video sin ningún error.
    Mejor abortar acá con un mensaje claro."""
    formats = {}
    for p in paths:
        formats.setdefault(probe_audio_format(p), []).append(p.name)
    if len(formats) > 1:
        detail = "\n".join(f"  {sr} Hz / {ch} canal(es): {', '.join(names[:4])}"
                           f"{' ...' if len(names) > 4 else ''}"
                           for (sr, ch), names in formats.items())
        raise SystemExit(
            "[ERROR] Los WAV de narración no comparten formato (sample rate / canales):\n"
            f"{detail}\nBorra output/audio/ y cache/audio/ y vuelve a generar el audio."
        )
    return next(iter(formats))


def nvenc_available() -> bool:
    """Prueba encodear 1 frame con h264_nvenc; falla si no hay GPU NVIDIA/driver."""
    try:
        run([
            FFMPEG, "-v", "error", "-f", "lavfi", "-i", "color=black:s=256x256:d=0.1",
            "-frames:v", "1", "-c:v", "h264_nvenc", "-f", "null", "-",
        ])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def pick_encoder(cfg_encoder: str) -> str:
    if cfg_encoder == "auto":
        if nvenc_available():
            print("[encoder] h264_nvenc (GPU)")
            return "nvenc"
        print("[encoder] h264_nvenc no disponible, usando libx264 (CPU)")
        return "libx264"
    if cfg_encoder not in ENCODER_ARGS:
        raise SystemExit(f"video.encoder desconocido: {cfg_encoder!r} (usa auto | nvenc | libx264)")
    print(f"[encoder] {cfg_encoder} (forzado por config)")
    return cfg_encoder


def pick_random_music(folder_path: str, seed=None) -> Path | None:
    """Elige un mp3 al azar de la carpeta de música. Devuelve None si no hay ninguno."""
    folder = Path(folder_path)
    if not folder.exists():
        return None

    candidates = sorted(folder.glob("*.mp3"))  # sorted() para que el random sea reproducible con seed
    if not candidates:
        return None

    rng = random.Random(seed)  # si seed es None, usa entropía del sistema (distinto cada vez)
    return rng.choice(candidates)


# ---------------------------------------------------------------------------
# Capítulos de YouTube y registro de la música (van a output/fuentes.md)
# ---------------------------------------------------------------------------

AUTO_MARKER = "<!-- generado por assemble_video.py: de aquí para abajo se reescribe en cada corrida -->"
MIN_CHAPTER_SEC = 10.0   # YouTube exige capítulos de al menos 10 s (y mínimo 3, partiendo en 00:00)


def format_ts(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def chapter_name(block: dict) -> str:
    if block.get("title"):
        return block["title"]
    label = block.get("label") or block.get("tag") or block.get("slug", "")
    return label.strip().capitalize()


def build_chapters(blocks: list[dict]) -> list[tuple[float, str]]:
    """Un capítulo por cada cambio de (rótulo, titular). Las partes _p1/_p2 de una
    misma noticia y los [IMAGEN]/[GRÁFICO] que heredan el titular de su [PLACA]
    caen en el mismo capítulo. Capítulos más cortos que MIN_CHAPTER_SEC se
    absorben en el anterior."""
    raw, t = [], 0.0
    for a in blocks:
        key = (a.get("label"), a.get("title"))
        if not raw or key != raw[-1][0]:
            raw.append([key, chapter_name(a), t, 0.0])
        raw[-1][3] += float(a["duration_sec"])
        t += float(a["duration_sec"])

    chapters: list[list] = []
    for key, name, start, dur in raw:
        if chapters and dur < MIN_CHAPTER_SEC:
            chapters[-1][3] += dur          # se pega al anterior
            continue
        chapters.append([key, name, start, dur])
    # el primero siempre parte en 00:00 (si era corto, absorbe hacia adelante)
    if chapters:
        chapters[0][2] = 0.0
    return [(start, name) for _, name, start, _ in chapters]


def music_license(music_path: Path | None, folder: Path) -> str:
    """Busca la licencia de la pista en assets/music/licencias.yaml
    ({"archivo.mp3": "texto de licencia/atribución", "default": "..."})."""
    if music_path is None:
        return ""
    reg = folder / "licencias.yaml"
    if not reg.exists():
        return f"NO REGISTRADA — crea {reg} con la licencia/atribución de cada pista"
    data = yaml.safe_load(reg.read_text(encoding="utf-8")) or {}
    text = data.get(music_path.name) or data.get("default")
    return str(text).strip() if text else f"NO REGISTRADA — agrega '{music_path.name}' en {reg}"


def write_youtube_section(sources_path: Path, blocks: list[dict], music_path: Path | None,
                          music_folder: Path, music_start: float, seed) -> None:
    """Agrega (o reemplaza) al final de fuentes.md los capítulos y la pista usada.
    fuentes.md es el archivo que sobrevive a la limpieza: ahí queda la constancia."""
    lines = [AUTO_MARKER, "", "## Capítulos (pegar en la descripción de YouTube)", ""]
    chapters = build_chapters(blocks)
    for start, name in chapters:
        lines.append(f"{format_ts(start)} {name}")
    if len(chapters) < 3:
        lines += ["", "(YouTube solo activa capítulos con 3 o más; este episodio tiene "
                  f"{len(chapters)})"]
    lines += ["", "## Música de fondo", ""]
    if music_path is None:
        lines.append("- Sin música (no había mp3 en la carpeta).")
    else:
        lines += [
            f"- Pista: `{music_path.name}`",
            f"- Licencia / atribución: {music_license(music_path, music_folder)}",
            f"- Tramo usado: desde {format_ts(music_start)} de la pista"
            + (f" (music.seed: {seed})" if seed is not None else " (elección al azar, sin seed)"),
        ]
    lines.append("")

    existing = sources_path.read_text(encoding="utf-8") if sources_path.exists() else ""
    if AUTO_MARKER in existing:
        existing = existing[: existing.index(AUTO_MARKER)]
    body = existing.rstrip() + "\n\n" if existing.strip() else ""
    sources_path.write_text(body + "\n".join(lines), encoding="utf-8")
    print(f"[youtube] {len(chapters)} capítulos y registro de música → {sources_path}")


def segment_filter(n_frames: int, fps: int, resolution, ken_burns: bool, zoom: float) -> str:
    """Cadena de filtros ffmpeg para convertir UNA imagen fija en n_frames de video."""
    w, h = resolution
    chain = [
        # ajustar la imagen al lienzo (respeta aspecto, rellena con negro)
        f"scale={w}:{h}:force_original_aspect_ratio=decrease",
        f"pad={w}:{h}:-1:-1:color=black",
        # decodificar el PNG una sola vez y repetir el frame (mucho más rápido que -loop 1)
        "loop=loop=-1:size=1",
        f"fps={fps}",
        f"trim=end_frame={n_frames}",
        "setpts=PTS-STARTPTS",
    ]
    if ken_burns and n_frames > 1:
        # zoom lineal de 1.0 a `zoom` a lo largo del bloque; n = índice de frame
        chain += [
            f"scale=w='trunc(iw*(1+({zoom}-1)*n/{n_frames - 1})/2)*2':h=-2:eval=frame",
            f"crop={w}:{h}",
        ]
    chain.append("format=yuv420p")
    return ",".join(chain)


def render_segment(image_path: str, n_frames: int, out_path: Path, fps: int,
                   resolution, ken_burns: bool, zoom: float, encoder: str) -> Path:
    cmd = [
        FFMPEG, "-v", "error", "-y",
        "-i", image_path,
        "-vf", segment_filter(n_frames, fps, resolution, ken_burns, zoom),
        "-r", str(fps), "-an",
        *ENCODER_ARGS[encoder],
        str(out_path),
    ]
    run(cmd)
    return out_path


def write_concat_list(paths: list[Path], list_path: Path) -> None:
    lines = []
    for p in paths:
        escaped = str(p.resolve()).replace("'", r"'\''")
        lines.append(f"file '{escaped}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        print(
            "Uso: python assemble_video.py <audio_manifest.json> "
            "<visuals_manifest.json> <config.yaml>"
        )
        sys.exit(1)

    audio_manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    visuals_manifest = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    cfg = yaml.safe_load(Path(sys.argv[3]).read_text(encoding="utf-8"))

    resolution = tuple(cfg["video"]["resolution"])
    fps = int(cfg["video"]["fps"])
    ken_burns = cfg["visuals"]["ken_burns"]
    zoom = float(cfg["visuals"]["ken_burns_zoom"])
    encoder = pick_encoder(cfg["video"].get("encoder", "auto"))
    parallel_jobs = int(cfg["video"].get("parallel_jobs", 4))

    visuals_by_index = {v["index"]: v["image_path"] for v in visuals_manifest}
    blocks = sorted(audio_manifest, key=lambda x: x["index"])

    # Frames por bloque calculados sobre el tiempo acumulado, para que el redondeo
    # a frames enteros no vaya desfasando el video respecto a la narración.
    frame_counts = []
    t_acc = 0.0
    for a in blocks:
        start_f = round(t_acc * fps)
        t_acc += a["duration_sec"]
        end_f = round(t_acc * fps)
        frame_counts.append(max(1, end_f - start_f))
    total_duration = t_acc
    print(f"[video] {len(blocks)} bloques, {total_duration/60:.1f} min, {sum(frame_counts)} frames @ {fps} fps")

    output_path = Path(cfg["video"]["output_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="segments_", dir=output_path.parent) as tmp:
        tmp = Path(tmp)

        # 1) Renderizar cada bloque (imagen → video mudo) en paralelo
        def job(i_block):
            i, a = i_block
            seg = tmp / f"seg_{i:03d}.mp4"
            render_segment(
                visuals_by_index[a["index"]], frame_counts[i], seg,
                fps, resolution, ken_burns, zoom, encoder,
            )
            print(f"  [{i + 1}/{len(blocks)}] {a['slug']} ({a['duration_sec']:.1f}s)")
            return seg

        # Los bloques más largos van primero: si quedaran al final, los últimos
        # minutos del render correrían con un solo proceso y la GPU medio ociosa.
        order = sorted(range(len(blocks)), key=lambda i: -frame_counts[i])
        with ThreadPoolExecutor(max_workers=max(1, parallel_jobs)) as pool:
            done = dict(zip(order, pool.map(job, [(i, blocks[i]) for i in order])))
        segments = [done[i] for i in range(len(blocks))]

        audio_paths = [Path(a["audio_path"]) for a in blocks]
        sample_rate, _ = check_audio_formats(audio_paths)

        video_list = tmp / "video.txt"
        audio_list = tmp / "audio.txt"
        write_concat_list(segments, video_list)
        write_concat_list(audio_paths, audio_list)

        # 2) Concatenar segmentos (sin re-encodear) + narración + música
        cmd = [
            FFMPEG, "-v", "error", "-stats", "-y",
            "-f", "concat", "-safe", "0", "-i", str(video_list),   # 0: video
            "-f", "concat", "-safe", "0", "-i", str(audio_list),   # 1: narración
        ]
        music_cfg = cfg["music"]
        ducking = bool(music_cfg.get("ducking", True))
        music_folder = music_cfg["folder_path"]
        seed = music_cfg.get("seed")
        music_path = pick_random_music(music_folder, seed=seed)
        music_start = 0.0

        # loudnorm deja la voz a un volumen parejo y estándar (-16 LUFS, como YouTube).
        # Con ducking, la narración se duplica (asplit): una copia va a la mezcla y
        # la otra alimenta el sidechain, porque sidechaincompress la consume.
        nar_out = "asplit=2[nar][narsc]" if (ducking and music_path is not None) else "anull[nar]"
        afilters = [
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,"
            f"aformat=sample_rates={sample_rate}:channel_layouts=stereo,asetpts=PTS-STARTPTS,{nar_out}",
        ]

        if music_path is not None:
            print(f"[música] pista elegida al azar: {music_path.name}")
            music_duration = probe_duration(music_path)

            if music_duration <= total_duration:
                # la pista es más corta que el video (o de duración similar): se loopea completa
                cmd += ["-stream_loop", "-1", "-i", str(music_path)]          # 2: música
            else:
                # la pista es más larga (tus mp3 de ~1h): arranca en un punto al azar
                # dentro de ella en vez de repetir siempre el mismo comienzo.
                rng = random.Random(seed)
                music_start = rng.uniform(0, music_duration - total_duration)
                print(f"[música] arrancando en el segundo {music_start:.0f} de la pista")
                cmd += ["-ss", f"{music_start:.3f}", "-i", str(music_path)]  # 2: música

            fade_in = music_cfg["fade_in_sec"]
            fade_out = music_cfg["fade_out_sec"]
            music_chain = (
                f"[2:a]atrim=duration={total_duration:.3f},asetpts=PTS-STARTPTS,"
                f"aformat=sample_rates={sample_rate}:channel_layouts=stereo,"
                f"volume={music_cfg['volume_db']}dB,"
                f"afade=t=in:st=0:d={fade_in},"
                f"afade=t=out:st={max(0.0, total_duration - fade_out):.3f}:d={fade_out}"
            )
            if ducking:
                # sidechain: la música se comprime sola cuando hay voz y vuelve a
                # subir en las pausas. volume_db pasa a ser el nivel SIN voz.
                thr = float(music_cfg.get("duck_threshold", 0.05))
                ratio = float(music_cfg.get("duck_ratio", 8))
                attack = float(music_cfg.get("duck_attack_ms", 20))
                release = float(music_cfg.get("duck_release_ms", 400))
                afilters.append(music_chain + "[musraw]")
                afilters.append(
                    f"[musraw][narsc]sidechaincompress=threshold={thr}:ratio={ratio}:"
                    f"attack={attack}:release={release}[mus]"
                )
                print(f"[música] ducking activo (threshold={thr}, ratio={ratio}:1)")
            else:
                afilters.append(music_chain + "[mus]")
            afilters.append("[nar][mus]amix=inputs=2:duration=first:normalize=0[aout]")
        else:
            print(f"[aviso] No se encontraron archivos .mp3 en '{music_folder}'. "
                  "El video se genera solo con narración.")
            afilters.append("[nar]anull[aout]")

        cmd += [
            "-filter_complex", ";".join(afilters),
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-shortest",
            str(output_path),
        ]
        print("[video] concatenando y mezclando audio...")
        subprocess.run(cmd, check=True)

    write_youtube_section(output_path.parent / "fuentes.md", blocks, music_path,
                          Path(music_folder), music_start, seed)
    print(f"\nVideo final: {output_path}")


if __name__ == "__main__":
    main()

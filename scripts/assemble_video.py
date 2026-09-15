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

        video_list = tmp / "video.txt"
        audio_list = tmp / "audio.txt"
        write_concat_list(segments, video_list)
        write_concat_list([Path(a["audio_path"]) for a in blocks], audio_list)

        # 2) Concatenar segmentos (sin re-encodear) + narración + música
        cmd = [
            FFMPEG, "-v", "error", "-stats", "-y",
            "-f", "concat", "-safe", "0", "-i", str(video_list),   # 0: video
            "-f", "concat", "-safe", "0", "-i", str(audio_list),   # 1: narración
        ]
        # loudnorm deja la voz a un volumen parejo y estándar (-16 LUFS, como YouTube)
        afilters = [
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,"
            "aformat=sample_rates=44100:channel_layouts=stereo,asetpts=PTS-STARTPTS[nar]",
        ]

        music_folder = cfg["music"]["folder_path"]
        seed = cfg["music"].get("seed")
        music_path = pick_random_music(music_folder, seed=seed)

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
                start = rng.uniform(0, music_duration - total_duration)
                print(f"[música] arrancando en el segundo {start:.0f} de la pista")
                cmd += ["-ss", f"{start:.3f}", "-i", str(music_path)]       # 2: música

            fade_in = cfg["music"]["fade_in_sec"]
            fade_out = cfg["music"]["fade_out_sec"]
            afilters.append(
                f"[2:a]atrim=duration={total_duration:.3f},asetpts=PTS-STARTPTS,"
                f"aformat=sample_rates=44100:channel_layouts=stereo,"
                f"volume={cfg['music']['volume_db']}dB,"
                f"afade=t=in:st=0:d={fade_in},"
                f"afade=t=out:st={max(0.0, total_duration - fade_out):.3f}:d={fade_out}[mus]"
            )
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

    print(f"\nVideo final: {output_path}")


if __name__ == "__main__":
    main()

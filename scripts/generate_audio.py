"""
Genera el audio de narración para cada bloque del guion.

Motores disponibles (config.yaml → tts.engine, y la cadena tts.fallback_engines):
  - kokoro: Kokoro-82M local en la GPU (kokoro-onnx + onnxruntime-gpu). Voces en
            español: em_alex, em_santa (hombre), ef_dora (mujer). Sin internet.
  - edge:   voces neuronales de Microsoft vía edge-tts (gratis, necesita internet,
            cliente no oficial: puede dejar de funcionar cuando Microsoft cambia algo).
            Voces chilenas: es-CL-LorenzoNeural, es-CL-CatalinaNeural.
  - piper:  TTS local y offline (calidad más robótica). Último respaldo.
  - elevenlabs: pendiente de implementar.

Caché: cada bloque se guarda en cache/audio/<hash>.wav, donde el hash depende del
texto y de los parámetros de voz. Si el texto de un bloque no cambió, no se vuelve
a sintetizar; si cambias la voz o la velocidad, el hash cambia y se regenera solo.

Toda salida de TTS se normaliza al mismo formato (48 kHz, mono, PCM 16 bit)
apenas se sintetiza, sea cual sea el motor: así el concat de assemble_video.py
nunca mezcla sample rates.

Si el motor principal Y el de respaldo fallan en un bloque, no se aborta: se
genera un silencio de la duración estimada y el bloque queda marcado como
"failed" en el manifest, con la lista completa al final.

Uso:
    python generate_audio.py output/bloques.json output/audio/ config.yaml
"""

import asyncio
import hashlib
import json
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

import yaml

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

TARGET_SAMPLE_RATE = 48000
TARGET_CHANNELS = 1
AUDIO_FORMAT_VERSION = "v2-48k-mono"   # súbelo si cambias el formato: invalida el caché
WORDS_PER_SECOND = 2.6                  # para estimar la duración de un bloque fallido
DEFAULT_CACHE_DIR = "cache/audio"


def get_wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def normalize_wav(src: Path, dst: Path | None = None) -> None:
    """Convierte cualquier audio (wav/mp3, cualquier sample rate) al formato único
    del pipeline. Si dst es None, reemplaza src in-place."""
    out = dst if dst is not None else src.with_suffix(".norm.wav")
    subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-i", str(src),
         "-ar", str(TARGET_SAMPLE_RATE), "-ac", str(TARGET_CHANNELS), "-c:a", "pcm_s16le",
         str(out)],
        check=True,
    )
    if dst is None:
        out.replace(src)


def make_silence(out_path: Path, seconds: float) -> None:
    subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-f", "lavfi",
         "-i", f"anullsrc=r={TARGET_SAMPLE_RATE}:cl=mono",
         "-t", f"{seconds:.3f}", "-c:a", "pcm_s16le", str(out_path)],
        check=True,
    )


def pad_silence(src: Path, dst: Path, seconds: float) -> None:
    """Copia src a dst agregando `seconds` de silencio al final (para [PAUSA])."""
    subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-i", str(src),
         "-af", f"apad=pad_dur={seconds:.3f}",
         "-ar", str(TARGET_SAMPLE_RATE), "-ac", str(TARGET_CHANNELS), "-c:a", "pcm_s16le",
         str(dst)],
        check=True,
    )


def audio_key(text: str, engine: str, cfg: dict) -> str:
    """Hash del contenido + parámetros de voz. Mismo texto y misma voz → mismo archivo."""
    t = cfg["tts"]
    if engine == "kokoro":
        params = [Path(t.get("kokoro_model_path", "")).name, t.get("kokoro_voice"),
                  t.get("kokoro_speed"), t.get("kokoro_lang", "es")]
    elif engine == "edge":
        params = [t.get("edge_voice"), t.get("edge_rate"), t.get("edge_pitch")]
    elif engine == "piper":
        params = [Path(t.get("piper_model_path", "")).name, t.get("piper_speed"),
                  t.get("piper_sentence_silence")]
    else:
        params = [t.get(f"{engine}_voice_id")]
    payload = "|".join([AUDIO_FORMAT_VERSION, engine, *map(str, params), text])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def find_piper_model(configured_path: str) -> Path:
    """
    Devuelve la ruta real del modelo de Piper. Si la ruta configurada no
    existe, busca el mismo nombre de archivo en las carpetas donde
    `python -m piper.download_voices` suele dejarlo (cwd y ./models/).
    """
    configured = Path(configured_path)
    if configured.exists():
        return configured

    filename = configured.name  # ej. es_ES-davefx-medium.onnx
    candidate_dirs = [Path.cwd(), Path.cwd() / "models"]

    for d in candidate_dirs:
        candidate = d / filename
        if candidate.exists():
            print(
                f"[aviso] '{configured_path}' no existe, pero encontré '{candidate}'. "
                f"Usándolo. Tip: actualiza tts.piper_model_path en config.yaml a "
                f"'{candidate}' para que no vuelva a buscarlo."
            )
            return candidate

    searched = ", ".join(str(d / filename) for d in [configured.parent, *candidate_dirs])
    raise FileNotFoundError(
        f"No encontré el modelo de Piper '{filename}'. Busqué en: {searched}. "
        "Descárgalo con: python -m piper.download_voices --download-dir models "
        f"{configured.stem} y confirma que quedó en 'models/{filename}', "
        "o actualiza tts.piper_model_path en config.yaml apuntando a donde quedó."
    )


def synthesize_piper(text: str, out_path: Path, cfg: dict) -> None:
    """Llama al binario de Piper (lee texto por stdin, escribe WAV). El modelo
    *medium* sale a 22.050 Hz, por eso se normaliza al final."""
    model_path = find_piper_model(cfg["tts"]["piper_model_path"])
    raw = out_path.with_suffix(".piper.wav")

    # piper 1.x acepta flags con guion (--output-file); las versiones nuevas
    # también aceptan guion bajo, pero la forma con guion funciona en ambas.
    cmd = [
        "piper",
        "--model", str(model_path),
        "--output-file", str(raw),
        "--length-scale", str(1.0 / float(cfg["tts"].get("piper_speed", 1.0))),
        "--sentence-silence", str(cfg["tts"].get("piper_sentence_silence", 0.25)),
    ]
    try:
        subprocess.run(cmd, input=text.encode("utf-8"), check=True,
                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raw.unlink(missing_ok=True)
        detail = (e.stderr or b"").decode("utf-8", "replace").strip().splitlines()
        raise RuntimeError(f"piper falló: {detail[-1] if detail else e}") from e
    normalize_wav(raw, out_path)
    raw.unlink(missing_ok=True)


def synthesize_edge(text: str, out_path: Path, cfg: dict) -> None:
    """Voz neuronal de Microsoft (edge-tts). Genera mp3 y lo convierte a wav con ffmpeg."""
    import edge_tts  # import tardío: solo hace falta si se usa este motor

    tts_cfg = cfg["tts"]
    voice = tts_cfg.get("edge_voice", "es-CL-LorenzoNeural")
    rate = tts_cfg.get("edge_rate", "+0%")
    pitch = tts_cfg.get("edge_pitch", "+0Hz")
    tmp_mp3 = out_path.with_suffix(".tmp.mp3")

    async def _run():
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
        await communicate.save(str(tmp_mp3))

    # el servicio a veces corta la conexión: reintentar antes de rendirse
    attempts = int(tts_cfg.get("edge_retries", 3))
    for attempt in range(1, attempts + 1):
        try:
            asyncio.run(_run())
            break
        except Exception as e:  # noqa: BLE001 - cualquier fallo de red/servicio
            if attempt == attempts:
                tmp_mp3.unlink(missing_ok=True)
                raise
            print(f"  [edge] intento {attempt} falló ({type(e).__name__}: {e}), reintentando...")
            time.sleep(2 * attempt)

    normalize_wav(tmp_mp3, out_path)
    tmp_mp3.unlink(missing_ok=True)


_KOKORO = None  # el modelo se carga una vez por proceso (tarda ~1 s y pesa 300 MB)


def _load_kokoro(cfg: dict):
    global _KOKORO
    if _KOKORO is not None:
        return _KOKORO
    import onnxruntime as ort
    from kokoro_onnx import Kokoro

    t = cfg["tts"]
    model = Path(t.get("kokoro_model_path", "models/kokoro-v1.0.onnx"))
    voices = Path(t.get("kokoro_voices_path", "models/voices-v1.0.bin"))
    for f in (model, voices):
        if not f.exists():
            raise FileNotFoundError(
                f"No encontré {f}. Descarga el modelo con:\n"
                "  curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx\n"
                "  curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
            )

    device = str(t.get("kokoro_device", "auto")).lower()
    providers = ["CPUExecutionProvider"]
    if device in ("auto", "cuda"):
        try:
            ort.preload_dlls()  # carga cuBLAS/cuDNN desde los paquetes pip nvidia-*-cu12
        except Exception:  # noqa: BLE001 - versiones viejas de onnxruntime no lo tienen
            pass
        if "CUDAExecutionProvider" in ort.get_available_providers():
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        elif device == "cuda":
            raise RuntimeError("kokoro_device: cuda, pero onnxruntime no ve CUDAExecutionProvider "
                               "(instala onnxruntime-gpu y los paquetes nvidia-*-cu12)")
    opts = ort.SessionOptions()
    opts.log_severity_level = 3  # silenciar los warnings de Memcpy/ScatterND
    session = ort.InferenceSession(str(model), opts, providers=providers)
    used = session.get_providers()[0].replace("ExecutionProvider", "")
    print(f"[kokoro] modelo cargado en {used}")
    _KOKORO = Kokoro.from_session(session, str(voices))
    return _KOKORO


def synthesize_kokoro(text: str, out_path: Path, cfg: dict) -> None:
    """Kokoro-82M local (GPU si hay). Sale a 24 kHz y se normaliza como los demás."""
    import soundfile as sf

    t = cfg["tts"]
    kokoro = _load_kokoro(cfg)
    audio, sr = kokoro.create(
        text, voice=t.get("kokoro_voice", "em_alex"),
        speed=float(t.get("kokoro_speed", 1.0)), lang=t.get("kokoro_lang", "es"),
    )
    if len(audio) == 0:
        raise RuntimeError("kokoro devolvió audio vacío")
    raw = out_path.with_suffix(".kokoro.wav")
    sf.write(str(raw), audio, sr)
    normalize_wav(raw, out_path)
    raw.unlink(missing_ok=True)


def synthesize_elevenlabs(text: str, out_path: Path, cfg: dict) -> None:
    """
    TODO: implementar llamada a la API de ElevenLabs.
    - Leer API key desde la variable de entorno cfg["tts"]["elevenlabs_api_key_env"]
    - Leer voice_id desde cfg["tts"]["elevenlabs_voice_id"]
    - POST a https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
    - Guardar el mp3 y pasarlo por normalize_wav()
    """
    raise NotImplementedError(
        "Backend 'elevenlabs' todavía no implementado. Usa tts.engine: piper "
        "en config.yaml, o implementa esta función."
    )


ENGINES = {
    "kokoro": synthesize_kokoro,
    "edge": synthesize_edge,
    "piper": synthesize_piper,
    "elevenlabs": synthesize_elevenlabs,
}


def synthesize_cached(text: str, engine: str, cfg: dict, cache_dir: Path) -> tuple[Path, bool]:
    """Devuelve (ruta en caché, venía_de_caché). Sintetiza solo si no existe."""
    cached = cache_dir / f"{audio_key(text, engine, cfg)}.wav"
    if cached.exists():
        return cached, True
    tmp = cached.with_name(cached.stem + ".partial.wav")
    try:
        ENGINES[engine](text, tmp, cfg)
        tmp.replace(cached)   # solo queda en caché si la síntesis terminó bien
    finally:
        tmp.unlink(missing_ok=True)
    return cached, False


def main():
    if len(sys.argv) != 4:
        print("Uso: python generate_audio.py <bloques.json> <audio_dir> <config.yaml>")
        sys.exit(1)

    blocks_path = Path(sys.argv[1])
    audio_dir = Path(sys.argv[2])
    config_path = Path(sys.argv[3])

    audio_dir.mkdir(parents=True, exist_ok=True)
    blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    tts_cfg = cfg["tts"]
    engine_name = tts_cfg["engine"]
    # cadena de respaldo: tts.fallback_engines: [edge, piper] (o el viejo tts.fallback_engine)
    fallbacks = tts_cfg.get("fallback_engines")
    if fallbacks is None:
        fallbacks = [tts_cfg["fallback_engine"]] if tts_cfg.get("fallback_engine") else []
    fallbacks = [f for f in fallbacks if f and f != engine_name]
    for name in [engine_name, *fallbacks]:
        if name not in ENGINES:
            raise ValueError(f"Motor TTS desconocido: {name} (usa {', '.join(ENGINES)})")

    cache_dir = Path(tts_cfg.get("cache_dir", DEFAULT_CACHE_DIR))
    cache_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    failed = []
    n_cached = n_synth = 0
    t0 = time.time()

    primary_engine = engine_name

    for b in blocks:
        out_path = audio_dir / f"{b['index']:02d}_{b['slug']}.wav"
        cached, from_cache, used_engine, error = None, False, None, None

        # si ya estamos en el motor de respaldo pero este bloque existe en caché
        # con la voz principal (de una corrida anterior), preferimos esa
        if engine_name != primary_engine and \
                (cache_dir / f"{audio_key(b['text'], primary_engine, cfg)}.wav").exists():
            cached, from_cache = synthesize_cached(b["text"], primary_engine, cfg, cache_dir)
            used_engine = primary_engine

        while cached is None:
            try:
                cached, from_cache = synthesize_cached(b["text"], engine_name, cfg, cache_dir)
                used_engine = engine_name
            except Exception as e:  # noqa: BLE001
                error = f"{type(e).__name__}: {e}"
                if not fallbacks:
                    break  # no queda motor al que cambiar: el bloque queda sin audio
                print(f"[aviso] motor '{engine_name}' falló en {out_path.name} ({error}). "
                      f"Cambiando a '{fallbacks[0]}' para el resto del guion.")
                engine_name = fallbacks.pop(0)

        if cached is None:
            # ambos motores fallaron: silencio de duración estimada y seguimos
            est = max(1.0, b["word_count"] / WORDS_PER_SECOND)
            print(f"[ERROR] {out_path.name}: sin audio ({error}). Se deja un silencio de {est:.1f}s.")
            make_silence(out_path, est + float(b.get("pause_after", 0.0) or 0.0))
            failed.append({"index": b["index"], "slug": b["slug"], "error": error})
        else:
            src = "caché" if from_cache else used_engine
            n_cached += from_cache
            n_synth += not from_cache
            print(f"Audio: {out_path.name} ({src})")
            pause = float(b.get("pause_after", 0.0) or 0.0)
            if pause > 0:
                pad_silence(cached, out_path, pause)
            else:
                shutil.copyfile(cached, out_path)

        manifest.append(
            {
                "index": b["index"],
                "slug": b["slug"],
                "tag": b["tag"],
                "label": b.get("label"),
                "title": b.get("title"),
                "part": b.get("part", 1),
                "engine": used_engine,
                "audio_path": str(out_path),
                "duration_sec": get_wav_duration(out_path),
                "failed": cached is None,
            }
        )

    manifest_path = audio_dir.parent / "audio_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total = sum(m["duration_sec"] for m in manifest)
    print(f"\nListo en {time.time() - t0:.0f}s: {n_synth} bloques sintetizados, {n_cached} desde caché.")
    print(f"Duración total de narración: {total/60:.1f} min")
    print(f"Manifest guardado en {manifest_path}")
    if failed:
        print("\n" + "!" * 70)
        print(f"!! {len(failed)} bloque(s) SIN AUDIO (quedaron en silencio):")
        for f in failed:
            print(f"!!   [{f['index']:02d}] {f['slug']}: {f['error']}")
        print("!! Corrige el problema (internet, modelo de Piper) y vuelve a correr:")
        print("!! los bloques que sí salieron se reusan desde el caché.")
        print("!" * 70)


if __name__ == "__main__":
    main()

"""
Genera el audio de narración para cada bloque del guion.

Motores disponibles (config.yaml → tts.engine):
  - edge:  voces neuronales de Microsoft vía edge-tts (gratis, necesita internet).
           Tiene voces chilenas: es-CL-LorenzoNeural, es-CL-CatalinaNeural.
  - piper: TTS local y offline (calidad más robótica). Se usa también como
           respaldo automático si `edge` falla (sin internet, servicio caído).
  - elevenlabs: pendiente de implementar.

Uso:
    python generate_audio.py output/bloques.json output/audio/ config.yaml
"""

import asyncio
import json
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

import yaml

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"


def get_wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def find_piper_model(configured_path: str) -> Path:
    """
    Devuelve la ruta real del modelo de Piper. Si la ruta configurada no
    existe, busca el mismo nombre de archivo en las carpetas donde
    `python -m piper.download_voices` suele dejarlo:
      - el directorio configurado tal cual
      - la raíz del proyecto (cwd), que es donde cae si se corrió el
        comando de descarga sin --download-dir (el default de Piper)
      - ./models/ (la ubicación recomendada en este proyecto)
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
    """Llama al binario/módulo de Piper para generar un WAV a partir de texto."""
    model_path = find_piper_model(cfg["tts"]["piper_model_path"])

    # piper-tts expone un binario `piper` que lee texto por stdin y escribe WAV.
    cmd = [
        "piper",
        "--model", str(model_path),
        "--output_file", str(out_path),
        "--length_scale", str(1.0 / cfg["tts"].get("piper_speed", 1.0)),
        "--sentence-silence", str(cfg["tts"].get("piper_sentence_silence", 0.25)),
    ]
    subprocess.run(cmd, input=text.encode("utf-8"), check=True)


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

    subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-i", str(tmp_mp3),
         "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out_path)],
        check=True,
    )
    tmp_mp3.unlink(missing_ok=True)


def synthesize_elevenlabs(text: str, out_path: Path, cfg: dict) -> None:
    """
    TODO (para Claude Code): implementar llamada a la API de ElevenLabs.
    - Leer API key desde la variable de entorno cfg["tts"]["elevenlabs_api_key_env"]
    - Leer voice_id desde cfg["tts"]["elevenlabs_voice_id"]
    - POST a https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
    - Guardar el audio resultante (mp3) y convertir a wav con pydub si hace falta
    """
    raise NotImplementedError(
        "Backend 'elevenlabs' todavía no implementado. Usa tts.engine: piper "
        "en config.yaml, o implementa esta función."
    )


ENGINES = {
    "edge": synthesize_edge,
    "piper": synthesize_piper,
    "elevenlabs": synthesize_elevenlabs,
}


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

    engine_name = cfg["tts"]["engine"]
    fallback_name = cfg["tts"].get("fallback_engine")
    synth_fn = ENGINES.get(engine_name)
    if synth_fn is None:
        raise ValueError(f"Motor TTS desconocido: {engine_name}")

    manifest = []
    for b in blocks:
        out_path = audio_dir / f"{b['index']:02d}_{b['slug']}.wav"
        print(f"Generando audio: {out_path.name} ({engine_name})")
        try:
            synth_fn(b["text"], out_path, cfg)
        except Exception as e:  # noqa: BLE001
            if not fallback_name or fallback_name == engine_name:
                raise
            print(f"[aviso] motor '{engine_name}' falló ({type(e).__name__}: {e}). "
                  f"Cambiando a '{fallback_name}' para el resto del guion.")
            engine_name = fallback_name
            synth_fn = ENGINES[engine_name]
            synth_fn(b["text"], out_path, cfg)
        duration = get_wav_duration(out_path)
        manifest.append(
            {
                "index": b["index"],
                "slug": b["slug"],
                "tag": b["tag"],
                "audio_path": str(out_path),
                "duration_sec": duration,
            }
        )

    manifest_path = audio_dir.parent / "audio_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total = sum(m["duration_sec"] for m in manifest)
    print(f"\nListo. Duración total de narración: {total/60:.1f} min")
    print(f"Manifest guardado en {manifest_path}")


if __name__ == "__main__":
    main()

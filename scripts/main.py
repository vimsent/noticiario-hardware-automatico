"""
Orquesta el pipeline completo: guion → bloques → audio → visuales → video final.

Uso:
    python scripts/main.py --script input/guion.md --config config.yaml
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).parent


def clean_intermediates(output_dir: Path, keep: set[Path]) -> None:
    """Borra los archivos de trabajo (bloques, audios, imágenes, manifests) y deja
    solo el video final y lo que esté en `keep`."""
    intermediates = [
        output_dir / "bloques.json",
        output_dir / "audio_manifest.json",
        output_dir / "visuals_manifest.json",
        output_dir / "audio",
        output_dir / "visuals",
    ]
    for path in intermediates:
        if path.resolve() in keep or not path.exists():
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    print(f"[limpieza] archivos intermedios eliminados de {output_dir}/")


def run(cmd: list[str]):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\n[ERROR] Falló el paso: {' '.join(cmd)}")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Pipeline Noticiario de Hardware")
    parser.add_argument("--script", default="input/guion.md", help="Guion de entrada")
    parser.add_argument("--config", default="config.yaml", help="Archivo de configuración")
    parser.add_argument("--output-dir", default="output", help="Carpeta de trabajo/salida")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    blocks_json = output_dir / "bloques.json"
    audio_dir = output_dir / "audio"
    visuals_dir = output_dir / "visuals"

    run([
        sys.executable, str(SCRIPTS_DIR / "parse_script.py"),
        args.script, str(blocks_json), args.config,
    ])

    run([
        sys.executable, str(SCRIPTS_DIR / "generate_audio.py"),
        str(blocks_json), str(audio_dir), args.config,
    ])

    run([
        sys.executable, str(SCRIPTS_DIR / "generate_visuals.py"),
        str(blocks_json), str(visuals_dir), args.config,
    ])

    run([
        sys.executable, str(SCRIPTS_DIR / "assemble_video.py"),
        str(output_dir / "audio_manifest.json"),
        str(output_dir / "visuals_manifest.json"),
        args.config,
    ])

    video_path = Path(cfg["video"]["output_path"])
    if cfg.get("output", {}).get("clean_intermediates", True):
        clean_intermediates(output_dir, keep={video_path.resolve()})

    print("\n✅ Pipeline completo.")
    print(f"   Video:   {video_path}")
    sources = output_dir / "fuentes.md"
    if sources.exists():
        print(f"   Fuentes: {sources}  (para la descripción del video)")


if __name__ == "__main__":
    main()

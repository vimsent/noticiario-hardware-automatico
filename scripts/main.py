"""
Orquesta el pipeline completo: guion → bloques → audio → visuales → video final.

Uso:
    python scripts/main.py --script input/guion.md --config config.yaml

Para iterar sin esperar la voz de nuevo (el audio queda en cache/audio/ de todas
formas, pero estas banderas se saltan la etapa completa):
    --skip-audio      no toca output/audio ni el audio_manifest (usa los de la corrida anterior)
    --skip-visuals    no regenera las tarjetas
    --only-assemble   solo vuelve a armar el video con los manifests que ya existen
    --clean           borra los intermedios al terminar (ignora output.clean_intermediates)
    --no-lint         no revisar el guion antes de generar la voz
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).parent


def clean_intermediates(output_dir: Path, keep: set[Path]) -> None:
    """Borra los archivos de trabajo (bloques, audios, imágenes, manifests) y deja
    solo el video final y lo que esté en `keep`. El caché de audio (cache/) no se toca."""
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


def require(path: Path, flag: str) -> None:
    if not path.exists():
        sys.exit(f"[ERROR] {flag} necesita {path}, que no existe. Corre el pipeline completo primero.")


def main():
    parser = argparse.ArgumentParser(description="Pipeline Noticiario de Hardware")
    parser.add_argument("--script", default="input/guion.md", help="Guion de entrada")
    parser.add_argument("--config", default="config.yaml", help="Archivo de configuración")
    parser.add_argument("--output-dir", default="output", help="Carpeta de trabajo/salida")
    parser.add_argument("--skip-audio", action="store_true", help="Reusar output/audio y su manifest")
    parser.add_argument("--skip-visuals", action="store_true", help="Reusar output/visuals y su manifest")
    parser.add_argument("--only-assemble", action="store_true",
                        help="Solo armar el video con los manifests existentes (no parsea, no audio, no visuales)")
    parser.add_argument("--clean", action="store_true",
                        help="Borrar intermedios al terminar aunque config diga que no")
    parser.add_argument("--no-lint", action="store_true", help="Saltarse la revisión del guion")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    blocks_json = output_dir / "bloques.json"
    audio_dir = output_dir / "audio"
    visuals_dir = output_dir / "visuals"
    audio_manifest = output_dir / "audio_manifest.json"
    visuals_manifest = output_dir / "visuals_manifest.json"

    skip_audio = args.skip_audio or args.only_assemble
    skip_visuals = args.skip_visuals or args.only_assemble

    if not args.only_assemble:
        run([
            sys.executable, str(SCRIPTS_DIR / "parse_script.py"),
            args.script, str(blocks_json), args.config,
        ])
        if not args.no_lint:
            run([
                sys.executable, str(SCRIPTS_DIR / "lint_script.py"),
                args.script, str(blocks_json), args.config,
            ])

    if skip_audio:
        require(audio_manifest, "--skip-audio")
        print(f"\n[skip] audio: reusando {audio_manifest}")
    else:
        run([
            sys.executable, str(SCRIPTS_DIR / "generate_audio.py"),
            str(blocks_json), str(audio_dir), args.config,
        ])

    if skip_visuals:
        require(visuals_manifest, "--skip-visuals")
        print(f"[skip] visuales: reusando {visuals_manifest}")
    else:
        run([
            sys.executable, str(SCRIPTS_DIR / "generate_visuals.py"),
            str(blocks_json), str(visuals_dir), args.config,
        ])

    run([
        sys.executable, str(SCRIPTS_DIR / "assemble_video.py"),
        str(audio_manifest), str(visuals_manifest), args.config,
    ])

    failed = [m for m in json.loads(audio_manifest.read_text(encoding="utf-8")) if m.get("failed")]

    video_path = Path(cfg["video"]["output_path"])
    if args.clean or cfg.get("output", {}).get("clean_intermediates", False):
        if failed:
            print("[limpieza] hay bloques sin audio: se conservan los intermedios para reintentar")
        else:
            clean_intermediates(output_dir, keep={video_path.resolve()})

    print("\n✅ Pipeline completo.")
    print(f"   Video:   {video_path}")
    sources = output_dir / "fuentes.md"
    if sources.exists():
        print(f"   Fuentes: {sources}  (para la descripción del video)")
    pending = output_dir / "visuales_pendientes.md"
    if pending.exists():
        print(f"   Visuales pendientes: {pending}  (imágenes que pidió el guion y no existen)")
    if failed:
        print(f"\n⚠️  {len(failed)} bloque(s) quedaron en SILENCIO en el video:")
        for m in failed:
            print(f"     [{m['index']:02d}] {m['slug']}")
        print("   Revisa internet / Piper y vuelve a correr (el resto sale del caché).")


if __name__ == "__main__":
    main()

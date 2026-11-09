"""Orquesta el pipeline completo: ingesta -> ranking -> redaccion -> revision -> video. Uso:

    python start.py [--desde AAAA-MM-DD] [--hasta AAAA-MM-DD] [--episodio N]
                    [--etapas 1,2,3,4,5] [--sin-revision] [--commit] [--config config.yaml]

Cada etapa numerica (1, 2, 3, 5) es un subproceso independiente, igual que en scripts/main.py: si
uno falla, se detiene todo con un mensaje claro de que etapa fallo y donde esta su log. La etapa 4
(revision) no es un subproceso: pausa el propio start.py para que el humano lea el guion.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from ingest.comun import cargar_config  # noqa: E402
from ingest.ingesta import fechas_por_defecto  # noqa: E402
from redaccion import validar as val  # noqa: E402
from redaccion.run_claude import ultimo_episodio  # noqa: E402

log = logging.getLogger("start")

NOMBRES_ETAPA = {1: "ingesta", 2: "ranking", 3: "redaccion", 4: "revision", 5: "video"}


class ErrorEtapa(Exception):
    pass


def parsear_etapas(texto: str) -> list[int]:
    try:
        numeros = {int(n.strip()) for n in texto.split(",") if n.strip()}
    except ValueError:
        raise SystemExit(f"--etapas invalido: {texto!r} (debe ser una lista de numeros 1-5 separados por coma)")
    fuera_de_rango = sorted(numeros - set(NOMBRES_ETAPA))
    if fuera_de_rango:
        raise SystemExit(f"--etapas invalido: {fuera_de_rango} (las etapas validas son 1-5)")
    return sorted(numeros)  # siempre en orden, sin importar como las haya listado el usuario


def ejecutar_etapa(nombre: str, cmd: list[str], log_path: Path) -> int:
    """Corre un subproceso, mostrando su salida en vivo y dejandola tambien en log_path."""
    log.info("%s: %s", nombre, " ".join(cmd))
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"\n===== etapa {nombre}: {' '.join(cmd)}\n")
        f.flush()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                cwd=RAIZ, text=True, bufsize=1)
        assert proc.stdout is not None
        for linea in proc.stdout:
            print(linea, end="", flush=True)
            f.write(linea)
        codigo = proc.wait()
        f.write(f"\n[codigo de salida {codigo}]\n")
    return codigo


def requerir(ruta: Path, motivo: str) -> None:
    if not ruta.exists():
        raise ErrorEtapa(f"falta {ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta} ({motivo})")


# ---------------------------------------------------------------------------
# etapas 1, 2, 3, 5: subprocesos
# ---------------------------------------------------------------------------

def etapa_ingesta(desde: date, hasta: date, config: str, log_path: Path) -> None:
    cmd = [sys.executable, "-m", "ingest.ingesta", "--desde", desde.isoformat(), "--hasta", hasta.isoformat(),
           "--config", config]
    if ejecutar_etapa("1 (ingesta)", cmd, log_path) != 0:
        raise ErrorEtapa(f"la ingesta fallo; revisa {log_path.relative_to(RAIZ)}")


def etapa_ranking(desde: date, hasta: date, config: str, log_path: Path) -> None:
    cmd = [sys.executable, "-m", "rank.ranking", "--desde", desde.isoformat(), "--hasta", hasta.isoformat(),
           "--config", config]
    if ejecutar_etapa("2 (ranking)", cmd, log_path) != 0:
        raise ErrorEtapa(f"el ranking fallo; revisa {log_path.relative_to(RAIZ)}")


def etapa_redaccion(desde: date, hasta: date, episodio: int, config: str, log_path: Path, run_dir: Path) -> None:
    cmd = [sys.executable, "-m", "redaccion.run_claude", "--desde", desde.isoformat(), "--hasta", hasta.isoformat(),
           "--episodio", str(episodio), "--config", config]
    if ejecutar_etapa("3 (redaccion)", cmd, log_path) != 0:
        raise ErrorEtapa(
            f"la redaccion fallo o no paso la validacion; revisa {log_path.relative_to(RAIZ)} y "
            f"{(run_dir / 'redaccion.log').relative_to(RAIZ)}"
        )


def etapa_video(config: str, log_path: Path) -> None:
    cmd = [sys.executable, str(RAIZ / "scripts" / "main.py"), "--script", "input/guion.md", "--config", config]
    if ejecutar_etapa("5 (video)", cmd, log_path) != 0:
        raise ErrorEtapa(f"el armado del video fallo; revisa {log_path.relative_to(RAIZ)}")


# ---------------------------------------------------------------------------
# etapa 4: revision (no es subproceso, pausa el propio start.py)
# ---------------------------------------------------------------------------

def resumen_episodio(run_dir: Path) -> dict[str, Any]:
    """Titulares del guion, cantidad de candidatas y hallazgos del barrido, para el pantallazo de revision."""
    guion_path = RAIZ / "input" / "guion.md"
    candidatas_json = run_dir / "candidatas.json"
    barrido_json = run_dir / "barrido.json"

    titulares: list[str] = []
    if guion_path.exists():
        normalizado, _ = val.ps.normalize_markdown(guion_path.read_text(encoding="utf-8"))
        cuerpo, _ = val.ps.split_sources(normalizado)
        titulares = [m.group(1).strip() for m in val.TAG_RE.finditer(cuerpo)]

    n_candidatas = n_grupos = None
    if candidatas_json.exists():
        doc = json.loads(candidatas_json.read_text(encoding="utf-8"))
        n_candidatas, n_grupos = doc.get("grupos_exportados"), doc.get("total_grupos")

    n_barrido = 0
    if barrido_json.exists():
        hallazgos = json.loads(barrido_json.read_text(encoding="utf-8"))
        n_barrido = len(hallazgos) if isinstance(hallazgos, list) else 0

    return {"guion": guion_path, "candidatas_md": run_dir / "candidatas.md", "titulares": titulares,
            "n_candidatas": n_candidatas, "n_grupos": n_grupos, "n_barrido": n_barrido}


def etapa_revision(run_dir: Path, sin_revision: bool) -> bool:
    """Devuelve True para seguir a la etapa 5, False para abortar sin renderizar."""
    r = resumen_episodio(run_dir)
    print(f"\nGuion:      {r['guion']}")
    print(f"Candidatas: {r['candidatas_md']}")
    if r["titulares"]:
        print(f"\nTitulares ({len(r['titulares'])}):")
        for t in r["titulares"]:
            print(f"  [{t}]")
    else:
        print("\n(no se pudieron leer etiquetas del guion)")
    if r["n_candidatas"] is not None:
        print(f"\nCandidatas: {r['n_candidatas']} exportadas de {r['n_grupos']} grupos detectados")
    print(f"Barrido de seguridad: {r['n_barrido']} hallazgo(s) fuera de candidatas.json")

    if sin_revision:
        log.info("--sin-revision: se omite la pausa de la etapa 4")
        return True

    try:
        resp = input("\nEnter para seguir a la etapa 5 (video), 'q' para abortar sin renderizar: ").strip().lower()
    except EOFError:
        log.error("no hay entrada interactiva disponible para la revision; usa --sin-revision para saltarla")
        return False
    return resp != "q"


# ---------------------------------------------------------------------------
# --commit
# ---------------------------------------------------------------------------

def hacer_commit(run_dir: Path, episodio: int, desde: date, hasta: date) -> None:
    chequeo = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=RAIZ,
                             capture_output=True, text=True)
    if chequeo.returncode != 0:
        log.error("--commit: %s no es un repositorio git; corre 'git init' primero. No se hizo commit.", RAIZ)
        return
    archivos = ["data/historial.md", "data/leakers.md", str((run_dir / "candidatas.md").relative_to(RAIZ))]
    subprocess.run(["git", "add", *archivos], cwd=RAIZ, check=True)
    mensaje = f"episodio {episodio} ({desde.isoformat()} a {hasta.isoformat()})"
    resultado = subprocess.run(["git", "commit", "-m", mensaje], cwd=RAIZ, capture_output=True, text=True)
    if resultado.returncode != 0:
        log.warning("--commit: git commit no hizo nada (%s)", (resultado.stdout + resultado.stderr).strip()[:200])
    else:
        log.info("--commit: %s", mensaje)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="orquesta ingesta, ranking, redaccion, revision y video")
    ap.add_argument("--desde", type=date.fromisoformat)
    ap.add_argument("--hasta", type=date.fromisoformat)
    ap.add_argument("--episodio", type=int)
    ap.add_argument("--etapas", default="1,2,3,4,5")
    ap.add_argument("--sin-revision", action="store_true")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(argv)

    etapas = parsear_etapas(args.etapas)
    try:
        cfg = cargar_config(args.config)
    except OSError as e:
        raise SystemExit(f"no se pudo leer {args.config}: {e}")
    zona = cfg["ingesta"].get("zona_horaria", "America/Santiago")

    desde, hasta = args.desde, args.hasta
    if desde is None or hasta is None:
        d_def, h_def = fechas_por_defecto(zona)
        desde, hasta = desde or d_def, hasta or h_def

    episodio = args.episodio
    historial_path = RAIZ / "data" / "historial.md"
    if episodio is None:
        historial = historial_path.read_text(encoding="utf-8") if historial_path.exists() else ""
        episodio = ultimo_episodio(historial) + 1

    run_dir = RAIZ / cfg["ranking"].get("salida_dir", "runs") / hasta.isoformat()
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "start.log"

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    log.info("episodio %d: %s a %s | etapas %s | log en %s", episodio, desde, hasta, etapas,
             log_path.relative_to(RAIZ))

    try:
        if 1 in etapas:
            etapa_ingesta(desde, hasta, args.config, log_path)
        if 2 in etapas:
            etapa_ranking(desde, hasta, args.config, log_path)
        if 3 in etapas:
            etapa_redaccion(desde, hasta, episodio, args.config, log_path, run_dir)
        if 4 in etapas:
            if not etapa_revision(run_dir, args.sin_revision):
                log.info("abortado en la revision; no se corrio la etapa 5")
                return 130
        if 5 in etapas:
            requerir(RAIZ / "input" / "guion.md", "corre la etapa 3 primero, o pega un guion a mano")
            etapa_video(args.config, log_path)
    except ErrorEtapa as e:
        log.error("%s", e)
        return 1

    if args.commit:
        hacer_commit(run_dir, episodio, desde, hasta)

    log.info("listo. episodio %d (%s a %s).", episodio, desde, hasta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

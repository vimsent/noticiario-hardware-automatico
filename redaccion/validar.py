"""Validadores de las salidas de la etapa 3: guion.md, candidatas.md, historial.md,
leakers.md y barrido.json. Uso manual:

    python -m redaccion.validar --run 2026-09-14 [--guion input/guion.md]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))

import parse_script as ps  # noqa: E402
from rank.normalizar import sin_tildes, url_canonica  # noqa: E402

TAG_RE = re.compile(r"^[ \t]*\[([^\]\n]+)\][ \t]*$", re.MULTILINE)
MARCA_VISUAL_RE = re.compile(r"\[(?:PLACA|IMAGEN|DIAGRAMA|GR[ÁA]FICO|MANTENER|PAUSA)(?::[^\]\n]*)?\]", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>()\[\]\"']+")
FUENTES_RE = re.compile(r"^[ \t]*-{3,}[ \t]*\n(?:[ \t]*\n)*[ \t]*#{0,6}[ \t]*[*_]*FUENTES[*_]*[ \t]*:?[ \t]*$", re.MULTILINE)
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CAMPOS_BARRIDO = {"hecho": str, "fecha_hecho": str, "urls": list, "medios": list, "por_que_falto": str}


@dataclass
class Resultado:
    errores: list[str] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errores

    def error(self, msg: str) -> None:
        self.errores.append(msg)

    def advertencia(self, msg: str) -> None:
        self.advertencias.append(msg)

    def sumar(self, otro: "Resultado", prefijo: str = "") -> None:
        self.errores += [f"{prefijo}{e}" for e in otro.errores]
        self.advertencias += [f"{prefijo}{a}" for a in otro.advertencias]

    def texto(self) -> str:
        lineas = [f"ERROR: {e}" for e in self.errores] + [f"AVISO: {a}" for a in self.advertencias]
        return "\n".join(lineas) if lineas else "ok"


def _norm(texto: str) -> str:
    return sin_tildes(texto).lower()


def _palabras(texto: str) -> int:
    return len(texto.split())


def extraer_urls(texto: str) -> list[str]:
    urls = []
    for u in URL_RE.findall(texto):
        u = u.rstrip(".,;:!?)]>*\"'")
        if u:
            urls.append(u)
    return urls


def urls_permitidas(candidatas: dict[str, Any] | None, barrido: list[dict[str, Any]] | None) -> set[str]:
    urls: set[str] = set()
    for g in (candidatas or {}).get("grupos", []):
        urls.update(a["url"] for a in g.get("articulos", []) if a.get("url"))
        urls.update(t["url"] for t in g.get("textos", []) if t.get("url"))
    for h in barrido or []:
        urls.update(h.get("urls") or [])
    return {url_canonica(u) for u in urls}


# ---------------------------------------------------------------------------
# guion.md
# ---------------------------------------------------------------------------

def _revisar_etiquetas(guion: str, cfg: dict[str, Any], r: Resultado) -> None:
    tags = [m.group(1).strip() for m in TAG_RE.finditer(guion)]
    if not tags:
        r.error("guion sin etiquetas entre corchetes")
        return
    max_pal = int(cfg.get("titular_max_palabras", 10))
    sec_min = int(cfg.get("noticias_secundarias_min", 4))
    sec_max = int(cfg.get("noticias_secundarias_max", 6))

    etiquetas: list[tuple[str, str | None]] = []
    no_permitidas: list[str] = []
    for raw in tags:
        kind, titulo = ps.split_tag(raw)
        kind_n = ps.normalize_kind(kind)
        etiquetas.append((kind_n, titulo))
        if kind_n in ("INTRO", "CIERRE"):
            if titulo:
                r.error(f"[{raw}] no lleva titular")
            continue
        if kind_n == "CHILE" or re.fullmatch(r"NOTICIA \d+", kind_n):
            if not titulo:
                r.error(f"[{raw}] sin titular")
            else:
                if _palabras(titulo) > max_pal:
                    r.error(f"titular de mas de {max_pal} palabras: [{raw}]")
                if titulo.rstrip().endswith("."):
                    r.error(f"titular con punto final: [{raw}]")
                if re.search(r"[*#_`\"]", titulo):
                    r.error(f"titular con decoracion markdown o comillas: [{raw}]")
            continue
        no_permitidas.append(raw)
    if no_permitidas:
        ejemplos = ", ".join(f"[{t}]" for t in no_permitidas[:3])
        resto = f" y {len(no_permitidas) - 3} mas" if len(no_permitidas) > 3 else ""
        r.error(f"{len(no_permitidas)} etiquetas no permitidas: {ejemplos}{resto}")

    kinds = [k for k, _ in etiquetas]
    if kinds[0] != "INTRO":
        r.error(f"la primera etiqueta debe ser [INTRO], no [{tags[0]}]")
    if kinds[-1] != "CIERRE":
        r.error(f"la ultima etiqueta debe ser [CIERRE], no [{tags[-1]}]")
    if len(kinds) >= 2 and kinds[-2] != "CHILE":
        r.error("falta [CHILE: ...] justo antes de [CIERRE]")
    noticias = [k for k in kinds if k.startswith("NOTICIA ")]
    esperadas = [f"NOTICIA {i}" for i in range(1, len(noticias) + 1)]
    if noticias != esperadas:
        r.error(f"las noticias deben ir numeradas 1..{len(noticias)} en orden, se encontro {noticias}")
    if noticias and not (1 + sec_min <= len(noticias) <= 1 + sec_max):
        r.error(f"debe haber 1 principal y entre {sec_min} y {sec_max} secundarias; hay {len(noticias)} noticias")
    medio = kinds[1:-2] if len(kinds) >= 4 else []
    if any(not k.startswith("NOTICIA ") for k in medio):
        r.error("entre [INTRO] y [CHILE] solo van etiquetas [NOTICIA n: ...]")
    if kinds.count("INTRO") > 1 or kinds.count("CIERRE") > 1 or kinds.count("CHILE") > 1:
        r.error("[INTRO], [CHILE] y [CIERRE] van una sola vez")


def validar_guion(texto: str, cfg: dict[str, Any], permitidas: set[str] | None = None) -> Resultado:
    r = Resultado()
    normalizado, _ = ps.normalize_markdown(texto)
    guion, fuentes = ps.split_sources(normalizado)

    if not FUENTES_RE.search(normalizado):
        r.error("falta una linea --- seguida de FUENTES al final del guion")
    if not fuentes:
        r.error("falta la seccion FUENTES")
    urls = extraer_urls(fuentes)
    if fuentes and not urls:
        r.error("FUENTES no tiene ninguna vineta con url")

    _revisar_etiquetas(guion, cfg, r)
    for m in MARCA_VISUAL_RE.finditer(guion):
        r.error(f"marca de edicion no permitida en el texto: {m.group(0)}")
        break

    cuerpo = TAG_RE.sub("", guion)
    cuerpo_norm = _norm(cuerpo)
    for palabra in cfg.get("palabras_prohibidas") or []:
        if _norm(palabra) in cuerpo_norm:
            r.error(f"palabra prohibida: \"{palabra}\"")

    n = _palabras(cuerpo)
    pmin, pmax = int(cfg.get("palabras_min", 0)), int(cfg.get("palabras_max", 10 ** 9))
    if n < pmin:
        r.advertencia(f"guion corto: {n} palabras (minimo sugerido {pmin})")
    elif n > pmax:
        r.advertencia(f"guion largo: {n} palabras (maximo sugerido {pmax})")

    try:
        bloques = ps.parse_script(guion)
        if not bloques:
            r.error("parse_script no produjo bloques")
    except Exception as e:
        r.error(f"parse_script fallo: {e}")

    if permitidas is not None:
        fuera = sorted({u for u in urls if url_canonica(u) not in permitidas})
        for u in fuera:
            r.error(f"url de FUENTES que no esta en candidatas.json ni barrido.json: {u}")
    return r


# ---------------------------------------------------------------------------
# candidatas.md, historial.md, leakers.md, barrido.json
# ---------------------------------------------------------------------------

def validar_candidatas_md(texto: str, columnas: list[str]) -> Resultado:
    r = Resultado()
    lineas = [l.strip() for l in texto.splitlines()]
    encabezados = [i for i, l in enumerate(lineas) if l.startswith("|") and i + 1 < len(lineas)
                   and re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lineas[i + 1])]
    if not encabezados:
        r.error("candidatas.md no tiene una tabla markdown")
        return r
    i = encabezados[0]
    cab = _norm(lineas[i])
    faltan = [c for c in columnas if _norm(c) not in cab]
    if faltan:
        r.error(f"a la tabla de candidatas.md le faltan columnas: {faltan}")
    filas = [l for l in lineas[i + 2:] if l.startswith("|")]
    if not filas:
        r.error("la tabla de candidatas.md no tiene filas")
    return r


def validar_no_encoge(nuevo: str, respaldo: str, nombre: str) -> Resultado:
    """El archivo no puede ser mas corto que su respaldo, salvo que solo se hayan movido lineas."""
    r = Resultado()
    if len(nuevo) >= len(respaldo):
        return r
    lineas_nuevo = {l.strip() for l in nuevo.splitlines() if l.strip()}
    perdidas = [l for l in respaldo.splitlines() if l.strip() and l.strip() not in lineas_nuevo]
    if perdidas:
        r.error(f"{nombre} quedo mas corto que su respaldo y perdio {len(perdidas)} lineas, "
                f"por ejemplo: {perdidas[0][:80]!r}")
    return r


def validar_barrido(texto: str) -> tuple[Resultado, list[dict[str, Any]]]:
    r = Resultado()
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as e:
        r.error(f"barrido.json no es json valido: {e}")
        return r, []
    if not isinstance(datos, list):
        r.error("barrido.json debe ser una lista")
        return r, []
    for i, h in enumerate(datos):
        if not isinstance(h, dict):
            r.error(f"barrido.json[{i}] no es un objeto")
            continue
        for campo, tipo in CAMPOS_BARRIDO.items():
            if not isinstance(h.get(campo), tipo):
                r.error(f"barrido.json[{i}] campo {campo} falta o no es {tipo.__name__}")
        if isinstance(h.get("fecha_hecho"), str) and not FECHA_RE.fullmatch(h["fecha_hecho"]):
            r.error(f"barrido.json[{i}] fecha_hecho debe ser AAAA-MM-DD")
        if isinstance(h.get("urls"), list) and not all(isinstance(u, str) and u.startswith("http") for u in h["urls"]):
            r.error(f"barrido.json[{i}] urls debe ser una lista de urls http")
    return r, [h for h in datos if isinstance(h, dict)]


# ---------------------------------------------------------------------------
# todo junto
# ---------------------------------------------------------------------------

@dataclass
class Rutas:
    guion: Path
    candidatas_json: Path
    candidatas_md: Path
    barrido: Path
    historial: Path
    leakers: Path
    respaldo_historial: Path | None = None
    respaldo_leakers: Path | None = None


def validar_todo(rutas: Rutas, cfg: dict[str, Any]) -> Resultado:
    r = Resultado()
    candidatas = json.loads(rutas.candidatas_json.read_text(encoding="utf-8")) if rutas.candidatas_json.exists() else None
    if candidatas is None:
        r.error(f"no existe {rutas.candidatas_json}")

    hallazgos: list[dict[str, Any]] = []
    if rutas.barrido.exists():
        rb, hallazgos = validar_barrido(rutas.barrido.read_text(encoding="utf-8"))
        r.sumar(rb)
    else:
        r.error(f"no existe {rutas.barrido}")

    if rutas.guion.exists():
        permitidas = urls_permitidas(candidatas, hallazgos)
        r.sumar(validar_guion(rutas.guion.read_text(encoding="utf-8"), cfg, permitidas), "guion.md: ")
    else:
        r.error(f"no existe {rutas.guion}")

    if rutas.candidatas_md.exists():
        r.sumar(validar_candidatas_md(rutas.candidatas_md.read_text(encoding="utf-8"),
                                      cfg.get("columnas_candidatas") or []), "candidatas.md: ")
    else:
        r.error(f"no existe {rutas.candidatas_md}")

    for nombre, ruta, respaldo in (("historial.md", rutas.historial, rutas.respaldo_historial),
                                   ("leakers.md", rutas.leakers, rutas.respaldo_leakers)):
        if not ruta.exists():
            r.error(f"no existe {ruta}")
        elif respaldo and respaldo.exists():
            r.sumar(validar_no_encoge(ruta.read_text(encoding="utf-8"), respaldo.read_text(encoding="utf-8"), nombre))
    return r


def rutas_run(run: str, cfg: dict[str, Any], guion: str | None = None) -> Rutas:
    runs = RAIZ / cfg.get("ranking", {}).get("salida_dir", "runs") / run
    return Rutas(
        guion=Path(guion) if guion else RAIZ / "input" / "guion.md",
        candidatas_json=runs / "candidatas.json",
        candidatas_md=runs / "candidatas.md",
        barrido=runs / "barrido.json",
        historial=RAIZ / "data" / "historial.md",
        leakers=RAIZ / "data" / "leakers.md",
        respaldo_historial=runs / "antes" / "historial.md",
        respaldo_leakers=runs / "antes" / "leakers.md",
    )


def main(argv: list[str] | None = None) -> int:
    from ingest.comun import cargar_config

    ap = argparse.ArgumentParser(description="valida las salidas de la etapa 3")
    ap.add_argument("--run", help="fecha_fin del episodio (runs/<run>/)")
    ap.add_argument("--guion", help="validar solo este guion, sin cruzar urls")
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(argv)
    cfg = cargar_config(args.config)

    if args.guion and not args.run:
        r = validar_guion(Path(args.guion).read_text(encoding="utf-8"), cfg["redaccion"])
    elif args.run:
        r = validar_todo(rutas_run(args.run, cfg, args.guion), cfg["redaccion"])
    else:
        ap.error("indica --run o --guion")
    print(r.texto())
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())

"""Ingresa a la base lo que encontro el barrido de seguridad y lo acumula en runs/barrido_acumulado.md."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from ingest import db
from rank.normalizar import titulo_normalizado, url_canonica

FEED = "barrido"


def _medio(hallazgo: dict[str, Any], i: int, url: str) -> str:
    medios = hallazgo.get("medios") or []
    if i < len(medios) and medios[i]:
        return str(medios[i])
    if medios:
        return str(medios[0])
    return (urlsplit(url).hostname or "desconocido").removeprefix("www.")


def insertar_hallazgos(con: sqlite3.Connection, hallazgos: list[dict[str, Any]], obtenido_utc: str | None = None) -> int:
    """Cada url del barrido entra como articulo con fuente_tipo = 'barrido'. Devuelve cuantos son nuevos."""
    obtenido = obtenido_utc or db.ahora_utc()
    nuevos = 0
    for h in hallazgos:
        for i, url in enumerate(h.get("urls") or []):
            _, es_nuevo = db.upsert_articulo(con, {
                "url": url_canonica(url),
                "url_original": url,
                "feed": FEED,
                "fuente_tipo": FEED,
                "medio": _medio(h, i, url),
                "categoria_feed": "general",
                "titulo": h["hecho"],
                "titulo_norm": titulo_normalizado(h["hecho"]),
                "resumen": h.get("por_que_falto"),
                "publicado_utc": f"{h['fecha_hecho']}T00:00:00+00:00",
                "obtenido_utc": obtenido,
            })
            nuevos += int(es_nuevo)
    con.commit()
    return nuevos


def acumular(ruta: str | Path, run: str, hallazgos: list[dict[str, Any]]) -> None:
    """Una linea por hallazgo: es la lista de fuentes que hay que sumar a feeds.yaml."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not ruta.exists():
        ruta.write_text("# Hallazgos del barrido de seguridad\n\nFuentes que faltan en feeds.yaml. Una linea por hallazgo.\n\n"
                        "| run | fecha_hecho | hecho | por_que_falto | medios | urls |\n|---|---|---|---|---|---|\n",
                        encoding="utf-8")
    with ruta.open("a", encoding="utf-8") as f:
        for h in hallazgos:
            celdas = [run, h["fecha_hecho"], h["hecho"], h.get("por_que_falto", ""),
                      ", ".join(h.get("medios") or []), " ".join(h.get("urls") or [])]
            f.write("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in celdas) + " |\n")


def procesar(con: sqlite3.Connection, run: str, hallazgos: list[dict[str, Any]], ruta_acumulado: str | Path) -> int:
    nuevos = insertar_hallazgos(con, hallazgos)
    if hallazgos:
        acumular(ruta_acumulado, run, hallazgos)
    return nuevos

"""Descarga y extraccion del texto completo con trafilatura."""

from __future__ import annotations

import logging
import sqlite3
from typing import Any

import trafilatura

from ingest import db
from rank.normalizar import hash_texto

log = logging.getLogger("ingesta.texto")


def extraer(html: str | bytes, url: str | None = None) -> str | None:
    texto = trafilatura.extract(html, url=url, include_comments=False, include_tables=False,
                                favor_precision=True)
    texto = (texto or "").strip()
    return texto or None


def descargar_textos(con: sqlite3.Connection, cliente: Any, fuentes: list[dict[str, Any]],
                     desde_utc: str, hasta_utc: str, maximo: int = 300, min_chars: int = 300) -> dict[str, int]:
    """Baja el texto de los articulos sin texto de las fuentes con texto_completo: true."""
    feeds = [f["nombre"] for f in fuentes if f.get("texto_completo")]
    pendientes = db.articulos_sin_texto(con, feeds, desde_utc, hasta_utc)[:maximo]
    totales = {"pendientes": len(pendientes), "ok": 0, "fallidos": 0, "robots": 0}
    for fila in pendientes:
        url = fila["url_original"] or fila["url"]
        if not cliente.permitido_por_robots(url):
            totales["robots"] += 1
            continue
        try:
            resp = cliente.get(url)
            texto = extraer(resp.text, url)
        except Exception as e:
            log.info("[%s] sin texto: %s", fila["feed"], e)
            texto = None
        if texto and len(texto) >= min_chars:
            db.actualizar_texto(con, fila["id"], texto, hash_texto(texto), True)
            totales["ok"] += 1
        else:
            totales["fallidos"] += 1
        con.commit()
    return totales

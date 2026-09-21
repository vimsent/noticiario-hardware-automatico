"""Feeds rss y atom genericos."""

from __future__ import annotations

import calendar
import logging
from datetime import datetime, timezone
from typing import Any

import feedparser

from ingest.comun import limpiar_html
from rank.normalizar import titulo_normalizado, url_canonica

log = logging.getLogger("ingesta.rss")


def _fecha_entrada(entrada: Any, por_defecto: str) -> str:
    for campo in ("published_parsed", "updated_parsed", "created_parsed"):
        st = entrada.get(campo)
        if st:
            return datetime.fromtimestamp(calendar.timegm(st), tz=timezone.utc).isoformat()
    return por_defecto


def _resumen_entrada(entrada: Any) -> str:
    resumen = entrada.get("summary") or ""
    if not resumen and entrada.get("content"):
        resumen = entrada["content"][0].get("value") or ""
    return limpiar_html(resumen)


def parsear_feed(contenido: bytes | str, fuente: dict[str, Any], medios: list[str],
                 obtenido_utc: str) -> list[dict[str, Any]]:
    """Convierte el xml de un feed en articulos listos para upsert. Sin red."""
    parsed = feedparser.parse(contenido)

    articulos: list[dict[str, Any]] = []
    for entrada in parsed.entries:
        link = (entrada.get("link") or "").strip()
        titulo = " ".join((entrada.get("title") or "").split())
        if not link or not titulo:
            continue
        articulos.append({
            "url": url_canonica(link),
            "url_original": link,
            "feed": fuente["nombre"],
            "fuente_tipo": fuente.get("tipo", "rss"),
            "medio": fuente["medio"],
            "categoria_feed": fuente["categoria"],
            "idioma": fuente.get("idioma"),
            "titulo": titulo,
            "titulo_norm": titulo_normalizado(titulo, medios),
            "resumen": _resumen_entrada(entrada) or None,
            "publicado_utc": _fecha_entrada(entrada, obtenido_utc),
            "obtenido_utc": obtenido_utc,
        })
    if parsed.bozo and not articulos:
        raise ValueError(f"xml invalido: {parsed.bozo_exception}")
    return articulos


def filtrar_ventana(articulos: list[dict[str, Any]], desde_utc: str, hasta_utc: str) -> list[dict[str, Any]]:
    return [a for a in articulos if desde_utc <= a["publicado_utc"] <= hasta_utc]


def descargar_feed(cliente: Any, fuente: dict[str, Any]) -> bytes:
    resp = cliente.get(fuente["url"])
    return resp.content

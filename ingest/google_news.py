"""Busquedas fijas de google news como feed rss. Los links apuntan a news.google.com;
el medio real viene en el elemento source del item."""

from __future__ import annotations

import calendar
import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode

import feedparser

from ingest.comun import limpiar_html
from rank.normalizar import quitar_sufijo_medio, titulo_normalizado, url_canonica

log = logging.getLogger("ingesta.google_news")


def url_consulta(fuente: dict[str, Any], url_base: str, dias: int | None = None) -> str:
    consulta = fuente["consulta"]
    if dias:
        consulta = f"{consulta} when:{dias}d"
    params = {"q": consulta, "hl": fuente.get("hl", "es-419"), "gl": fuente.get("gl", "CL"),
              "ceid": fuente.get("ceid", "CL:es-419")}
    return f"{url_base}?{urlencode(params)}"


def parsear_google_news(contenido: bytes | str, fuente: dict[str, Any], medios: list[str],
                        obtenido_utc: str) -> list[dict[str, Any]]:
    parsed = feedparser.parse(contenido)
    articulos: list[dict[str, Any]] = []
    for entrada in parsed.entries:
        link = (entrada.get("link") or "").strip()
        titulo_bruto = " ".join((entrada.get("title") or "").split())
        if not link or not titulo_bruto:
            continue
        origen = entrada.get("source") or {}
        medio = (origen.get("title") or "").strip() or fuente.get("medio") or "Google News"
        titulo = quitar_sufijo_medio(titulo_bruto, [medio, *medios])
        st = entrada.get("published_parsed") or entrada.get("updated_parsed")
        publicado = datetime.fromtimestamp(calendar.timegm(st), tz=timezone.utc).isoformat() if st else obtenido_utc
        resumen = limpiar_html(entrada.get("summary") or "")
        if resumen.strip() == titulo_bruto.strip() or resumen.startswith(titulo):
            resumen = ""
        articulos.append({
            "url": url_canonica(link),
            "url_original": link,
            "feed": fuente["nombre"],
            "fuente_tipo": "google_news",
            "medio": medio,
            "categoria_feed": fuente.get("categoria", "general"),
            "idioma": fuente.get("idioma") or fuente.get("hl", "es-419")[:2],
            "titulo": titulo,
            "titulo_norm": titulo_normalizado(titulo, [medio, *medios]),
            "resumen": resumen or None,
            "publicado_utc": publicado,
            "obtenido_utc": obtenido_utc,
        })
    if parsed.bozo and not articulos:
        raise ValueError(f"xml invalido: {parsed.bozo_exception}")
    return articulos

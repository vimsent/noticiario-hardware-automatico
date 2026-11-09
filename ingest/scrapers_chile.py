"""Scrapers para paginas chilenas sin rss. Cada scraper recibe html y devuelve articulos.
Si el html cambio y no se encuentra nada, se registra una advertencia; no es un error."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any, Callable
from urllib.parse import urljoin

from selectolax.parser import HTMLParser

from rank.normalizar import titulo_normalizado, url_canonica

log = logging.getLogger("ingesta.scrapers")

Scraper = Callable[[str, str], list[dict[str, Any]]]
_FECHA_DMY = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{4})")


def _fecha_dmy(texto: str | None) -> str | None:
    m = _FECHA_DMY.search(texto or "")
    if not m:
        return None
    d, mes, a = (int(x) for x in m.groups())
    try:
        return datetime(a, mes, d, 12, 0, tzinfo=timezone.utc).isoformat()
    except ValueError:
        return None


def scrapear_usm_noticias(html: str, url_base: str) -> list[dict[str, Any]]:
    """informatica.usm.cl/noticias y usm.cl/noticias (wordpress + elementor): article > h3, a[href], time."""
    salida: list[dict[str, Any]] = []
    for art in HTMLParser(html).css("article"):
        titulo_nodo = art.css_first("h1, h2, h3, h4")
        link = next((a.attributes.get("href") for a in art.css("a[href]")
                     if (a.attributes.get("href") or "").startswith(("http", "/"))), None)
        if titulo_nodo is None or not link:
            continue
        titulo = " ".join(titulo_nodo.text(strip=True).split())
        tiempo = art.css_first("time")
        fecha = _fecha_dmy(tiempo.attributes.get("datetime") or tiempo.text() if tiempo else None)
        resumen_nodo = art.css_first("p")
        resumen = " ".join(resumen_nodo.text(strip=True).split()) if resumen_nodo else ""
        salida.append({
            "titulo": titulo,
            "url": urljoin(url_base, link),
            "publicado_utc": fecha,
            "resumen": resumen or None,
        })
    return salida


def scrapear_fcfm_uchile(html: str, url_base: str) -> list[dict[str, Any]]:
    """ingenieria.uchile.cl/noticias (liferay, cubre tambien al dcc): a.mod__list-item > h3 (titulo), p (resumen).
    La pagina no trae fecha por item; publicado_utc queda en None y cae a obtenido_utc en articulos_desde_scraper."""
    salida: list[dict[str, Any]] = []
    for item in HTMLParser(html).css("a.mod__list-item"):
        titulo_nodo = item.css_first("h3")
        link = item.attributes.get("href")
        if titulo_nodo is None or not link:
            continue
        titulo = " ".join(titulo_nodo.text(strip=True).split())
        if not titulo:
            continue
        resumen_nodo = item.css_first("p")
        resumen = " ".join(resumen_nodo.text(strip=True).split()) if resumen_nodo else ""
        salida.append({
            "titulo": titulo,
            "url": urljoin(url_base, link),
            "publicado_utc": None,
            "resumen": resumen or None,
        })
    return salida


SCRAPERS: dict[str, Scraper] = {
    "usm_noticias": scrapear_usm_noticias,
    "fcfm_uchile_noticias": scrapear_fcfm_uchile,
}


def articulos_desde_scraper(nombre_scraper: str, html: str, fuente: dict[str, Any], medios: list[str],
                            obtenido_utc: str) -> list[dict[str, Any]]:
    scraper = SCRAPERS.get(nombre_scraper)
    if scraper is None:
        raise ValueError(f"scraper desconocido: {nombre_scraper}")
    crudos = scraper(html, fuente["url"])
    if not crudos:
        log.warning("[%s] el scraper %s no encontro nada; puede que el html haya cambiado", fuente["nombre"], nombre_scraper)
    articulos = []
    for c in crudos:
        articulos.append({
            "url": url_canonica(c["url"]),
            "url_original": c["url"],
            "feed": fuente["nombre"],
            "fuente_tipo": "scraper",
            "medio": fuente["medio"],
            "categoria_feed": fuente.get("categoria", "chile"),
            "idioma": fuente.get("idioma", "es"),
            "titulo": c["titulo"],
            "titulo_norm": titulo_normalizado(c["titulo"], medios),
            "resumen": c.get("resumen"),
            "publicado_utc": c.get("publicado_utc") or obtenido_utc,
            "obtenido_utc": obtenido_utc,
        })
    return articulos

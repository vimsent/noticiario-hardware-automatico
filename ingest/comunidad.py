"""Reddit (rss anonimo u oauth) y hacker news (api de algolia)."""

from __future__ import annotations

import calendar
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode, urlsplit

import feedparser
import httpx

from ingest.comun import limpiar_html
from rank.normalizar import titulo_normalizado, url_canonica

log = logging.getLogger("ingesta.comunidad")

_HREF_RE = re.compile(r'href="([^"]+)"')


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat()


def _es_externo(url: str, dominios_propios: tuple[str, ...] = ("reddit.com", "redd.it")) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return bool(host) and not any(host == d or host.endswith("." + d) for d in dominios_propios)


def _base_reddit(fuente: dict[str, Any], titulo: str, permalink: str, publicado: str, obtenido: str,
                 medios: list[str]) -> dict[str, Any]:
    return {
        "url": url_canonica(permalink),
        "url_original": permalink,
        "feed": fuente["nombre"],
        "fuente_tipo": "reddit",
        "medio": fuente.get("medio") or f"r/{fuente['subreddit']}",
        "categoria_feed": fuente.get("categoria", "comunidad"),
        "idioma": fuente.get("idioma", "en"),
        "titulo": titulo,
        "titulo_norm": titulo_normalizado(titulo, medios),
        "publicado_utc": publicado,
        "obtenido_utc": obtenido,
    }


def url_reddit_rss(fuente: dict[str, Any], plantilla: str) -> str:
    return plantilla.format(subreddit=fuente["subreddit"], periodo=fuente.get("periodo", "week"),
                            limite=int(fuente.get("limite", 100)))


def parsear_reddit_rss(contenido: bytes | str, fuente: dict[str, Any], medios: list[str],
                       obtenido_utc: str) -> list[dict[str, Any]]:
    """El rss de reddit no trae puntaje: score_comunidad queda en null."""
    parsed = feedparser.parse(contenido)
    articulos: list[dict[str, Any]] = []
    for e in parsed.entries:
        permalink = (e.get("link") or "").strip()
        titulo = " ".join((e.get("title") or "").split())
        if not permalink or not titulo:
            continue
        html = (e.get("content") or [{}])[0].get("value") or e.get("summary") or ""
        enlazada = next((h for h in _HREF_RE.findall(html) if _es_externo(h)), None)
        st = e.get("published_parsed") or e.get("updated_parsed")
        publicado = _iso(calendar.timegm(st)) if st else obtenido_utc
        art = _base_reddit(fuente, titulo, permalink, publicado, obtenido_utc, medios)
        art["url_enlazada"] = url_canonica(enlazada) if enlazada else None
        art["resumen"] = None
        art["score_comunidad"] = None
        articulos.append(art)
    if parsed.bozo and not articulos:
        raise ValueError(f"xml invalido: {parsed.bozo_exception}")
    return articulos


def parsear_reddit_json(datos: dict[str, Any], fuente: dict[str, Any], medios: list[str],
                        obtenido_utc: str) -> list[dict[str, Any]]:
    """Respuesta de /r/{sub}/top (api oficial), con puntaje."""
    articulos: list[dict[str, Any]] = []
    min_puntos = int(fuente.get("min_puntos", 0))
    for hijo in datos.get("data", {}).get("children", []):
        d = hijo.get("data") or {}
        titulo = " ".join((d.get("title") or "").split())
        permalink = d.get("permalink")
        if not titulo or not permalink or int(d.get("score") or 0) < min_puntos:
            continue
        permalink = f"https://www.reddit.com{permalink}"
        art = _base_reddit(fuente, titulo, permalink, _iso(float(d.get("created_utc", 0))), obtenido_utc, medios)
        externo = d.get("url") if not d.get("is_self") and d.get("url") and _es_externo(d["url"]) else None
        art["url_enlazada"] = url_canonica(externo) if externo else None
        art["resumen"] = " ".join((d.get("selftext") or "").split())[:1000] or None
        art["score_comunidad"] = int(d.get("score") or 0)
        articulos.append(art)
    return articulos


def token_oauth_reddit(cliente: Any, cfg_reddit: dict[str, Any]) -> str:
    """Flujo client_credentials (app only). Credenciales por variables de entorno."""
    client_id = os.environ.get(cfg_reddit.get("client_id_env", "REDDIT_CLIENT_ID"), "")
    secreto = os.environ.get(cfg_reddit.get("client_secret_env", "REDDIT_CLIENT_SECRET"), "")
    if not client_id or not secreto:
        raise RuntimeError("faltan credenciales de reddit en el entorno")
    resp = httpx.post(cfg_reddit["oauth_token_url"], auth=(client_id, secreto),
                      data={"grant_type": "client_credentials"},
                      headers={"User-Agent": cliente.user_agent}, timeout=cliente.timeout_s)
    resp.raise_for_status()
    return resp.json()["access_token"]


def descargar_reddit(cliente: Any, fuente: dict[str, Any], cfg_reddit: dict[str, Any], medios: list[str],
                     obtenido_utc: str) -> list[dict[str, Any]]:
    metodo = cfg_reddit.get("metodo", "rss")
    if metodo == "oauth":
        token = token_oauth_reddit(cliente, cfg_reddit)
        url = url_reddit_rss(fuente, cfg_reddit["oauth_api_url"])
        resp = cliente.get(url, headers={"Authorization": f"bearer {token}"})
        return parsear_reddit_json(resp.json(), fuente, medios, obtenido_utc)
    resp = cliente.get(url_reddit_rss(fuente, cfg_reddit["rss_url"]))
    return parsear_reddit_rss(resp.content, fuente, medios, obtenido_utc)


def url_hn(fuente: dict[str, Any], url_base: str, desde_utc: str, hasta_utc: str) -> str:
    d = int(datetime.fromisoformat(desde_utc).timestamp())
    h = int(datetime.fromisoformat(hasta_utc).timestamp())
    params = {
        "query": fuente["consulta"],
        "tags": fuente.get("tags", "story"),
        "numericFilters": f"created_at_i>{d},created_at_i<{h}",
        "hitsPerPage": int(fuente.get("limite", 100)),
    }
    return f"{url_base}?{urlencode(params)}"


def parsear_hn(datos: dict[str, Any], fuente: dict[str, Any], medios: list[str], obtenido_utc: str,
               item_url: str) -> list[dict[str, Any]]:
    articulos: list[dict[str, Any]] = []
    min_puntos = int(fuente.get("min_puntos", 0))
    for h in datos.get("hits", []):
        titulo = " ".join((h.get("title") or "").split())
        objeto = h.get("objectID")
        if not titulo or not objeto or int(h.get("points") or 0) < min_puntos:
            continue
        permalink = item_url.format(id=objeto)
        externo = h.get("url") or None
        creado = h.get("created_at_i")
        publicado = _iso(int(creado)) if creado else (h.get("created_at") or obtenido_utc)
        articulos.append({
            "url": url_canonica(permalink),
            "url_original": permalink,
            "url_enlazada": url_canonica(externo) if externo else None,
            "feed": fuente["nombre"],
            "fuente_tipo": "hn",
            "medio": fuente.get("medio", "Hacker News"),
            "categoria_feed": fuente.get("categoria", "comunidad"),
            "idioma": fuente.get("idioma", "en"),
            "titulo": titulo,
            "titulo_norm": titulo_normalizado(titulo, medios),
            "resumen": limpiar_html(h.get("story_text") or "")[:1000] or None,
            "publicado_utc": publicado,
            "obtenido_utc": obtenido_utc,
            "score_comunidad": int(h.get("points") or 0),
        })
    return articulos

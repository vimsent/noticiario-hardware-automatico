"""Urls canonicas, titulos normalizados y hash de texto."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

CHARS_HASH = 2000
_PUNTUACION = re.compile(r"[^\w\s]", re.UNICODE)
_ESPACIOS = re.compile(r"\s+")
_SEPARADORES_SUFIJO = ("-", "|", "–", "—", ":", "·")


def sin_tildes(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")


def url_canonica(url: str) -> str:
    """Sin utm_*, sin fragmento, sin slash final y con host en minusculas."""
    url = url.strip()
    partes = urlsplit(url)
    esquema = (partes.scheme or "https").lower()
    host = (partes.hostname or "").lower()
    if partes.port and not ((esquema == "http" and partes.port == 80) or (esquema == "https" and partes.port == 443)):
        host = f"{host}:{partes.port}"
    ruta = partes.path or "/"
    if len(ruta) > 1:
        ruta = ruta.rstrip("/")
    query = [(k, v) for k, v in parse_qsl(partes.query, keep_blank_values=True)
             if not k.lower().startswith("utm_")]
    return urlunsplit((esquema, host, ruta, urlencode(query), ""))


def quitar_sufijo_medio(titulo: str, medios: list[str] | tuple[str, ...] = ()) -> str:
    """Quita ' - Tom's Hardware' y similares al final del titulo."""
    limpio = titulo.strip()
    for medio in sorted((m for m in medios if m), key=len, reverse=True):
        for sep in _SEPARADORES_SUFIJO:
            sufijo = f" {sep} {medio}"
            if limpio.lower().endswith(sufijo.lower()):
                return limpio[: -len(sufijo)].rstrip()
    return limpio


def titulo_normalizado(titulo: str, medios: list[str] | tuple[str, ...] = ()) -> str:
    """Minusculas, sin tildes, sin puntuacion, sin sufijo del medio."""
    texto = quitar_sufijo_medio(titulo, medios)
    texto = sin_tildes(texto).lower()
    texto = _PUNTUACION.sub(" ", texto)
    return _ESPACIOS.sub(" ", texto).strip()


def texto_normalizado(texto: str) -> str:
    texto = sin_tildes(texto).lower()
    texto = _PUNTUACION.sub(" ", texto)
    return _ESPACIOS.sub(" ", texto).strip()


def hash_texto(texto: str | None, n_chars: int = CHARS_HASH) -> str | None:
    """Sha1 sobre los primeros n_chars caracteres normalizados. None si no hay texto."""
    if not texto:
        return None
    base = texto_normalizado(texto)[:n_chars]
    if not base:
        return None
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def clave_grupo(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

"""Config, feeds.yaml y ventanas de fechas compartidas por las etapas."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def cargar_config(path: str | Path = "config.yaml") -> dict[str, Any]:
    ruta = Path(path)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta
    return yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}


def cargar_feeds(path: str | Path = "feeds.yaml", solo_activos: bool = True) -> list[dict[str, Any]]:
    ruta = Path(path)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta
    fuentes = yaml.safe_load(ruta.read_text(encoding="utf-8")) or []
    if solo_activos:
        fuentes = [f for f in fuentes if f.get("activo", True)]
    return fuentes


def medios_conocidos(fuentes: list[dict[str, Any]]) -> list[str]:
    return sorted({f["medio"] for f in fuentes if f.get("medio")})


def a_utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def ventana_utc(desde: date, hasta: date, zona: str, dias_extra: int = 0) -> tuple[str, str]:
    """Inicio del dia `desde - dias_extra` y fin del dia `hasta`, en hora local, como iso utc."""
    tz = ZoneInfo(zona)
    inicio = datetime.combine(desde - timedelta(days=dias_extra), time.min, tzinfo=tz)
    fin = datetime.combine(hasta, time.max, tzinfo=tz).replace(microsecond=0)
    return a_utc_iso(inicio), a_utc_iso(fin)


def parsear_fecha(texto: str) -> date:
    return date.fromisoformat(texto)


def limpiar_html(html: str | None) -> str:
    """Deja solo el texto de un fragmento html (resumenes de feeds)."""
    if not html:
        return ""
    from selectolax.parser import HTMLParser

    texto = HTMLParser(html).text(separator=" ", strip=True)
    return " ".join(texto.split())

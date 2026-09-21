"""Datos de contexto para el guion: dolar observado y, mas adelante, precios en tiendas chilenas."""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("ingesta.apoyo")


def _fecha_serie(item: dict[str, Any]) -> date:
    return datetime.fromisoformat(item["fecha"].replace("Z", "+00:00")).date()


def obtener_dolar(cliente: Any, fecha: date, url_base: str) -> dict[str, Any]:
    """Valor del dia pedido; si no hay (fin de semana), el ultimo anterior de la serie."""
    fuente = f"{url_base}/dolar"
    resp = cliente.get(f"{fuente}/{fecha.strftime('%d-%m-%Y')}")
    serie = resp.json().get("serie") or []
    if not serie:
        resp = cliente.get(fuente)
        serie = [s for s in resp.json().get("serie") or [] if _fecha_serie(s) <= fecha]
    if not serie:
        raise ValueError(f"sin dolar observado para {fecha}")
    mejor = max(serie, key=_fecha_serie)
    return {"valor": float(mejor["valor"]), "fecha": _fecha_serie(mejor).isoformat(), "fuente": fuente}


def obtener_precios(cliente: Any, cfg_precios: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Hook para precios de tiendas chilenas (solotodo). Fase posterior."""
    if not cfg_precios or not cfg_precios.get("activo"):
        return []
    log.warning("precios de tiendas: activo en config pero no implementado")
    return []


def escribir_apoyo(ruta: str | Path, dolar: dict[str, Any] | None, precios: list[dict[str, Any]],
                   errores: list[str]) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    doc = {"dolar": dolar, "precios": precios, "errores": errores}
    ruta.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ruta

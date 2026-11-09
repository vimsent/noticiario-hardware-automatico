"""Seleccion, orden y escritura de candidatas.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _fecha_desc(fecha: str) -> str:
    # invierte el orden lexicografico de una fecha iso para ordenar descendente
    return "".join(chr(0x10FFFF - ord(c)) for c in fecha)


def ordenar(grupos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """score desc, n_medios desc, fecha_hecho desc, clave asc."""
    return sorted(grupos, key=lambda g: (-g["score_prelim"], -g["n_medios"], _fecha_desc(g["fecha_hecho"]), g["clave"]))


def seleccionar(grupos: list[dict[str, Any]], max_grupos: int, max_grupos_chile: int,
                max_grupos_prioritarios: int = 0) -> list[dict[str, Any]]:
    """Todos los eventos mayores, hasta N de Chile, hasta N de temas prioritarios y los N mejores del resto."""
    ordenados = ordenar(grupos)
    elegidos: list[dict[str, Any]] = []
    claves: set[str] = set()

    def agregar(g: dict[str, Any]) -> None:
        if g["clave"] not in claves:
            claves.add(g["clave"])
            elegidos.append(g)

    for g in ordenados:
        if g["evento_mayor"]:
            agregar(g)
    n_chile = 0
    for g in ordenados:
        if g["es_chile"] and g["clave"] not in claves and n_chile < max_grupos_chile:
            agregar(g)
            n_chile += 1
    n_prio = 0
    for g in ordenados:
        if g.get("tema_prioritario") and g["clave"] not in claves and n_prio < max_grupos_prioritarios:
            agregar(g)
            n_prio += 1
    n_resto = 0
    for g in ordenados:
        if g["clave"] not in claves and n_resto < max_grupos:
            agregar(g)
            n_resto += 1
    return ordenar(elegidos)


def armar_documento(desde: str, hasta: str, generado_utc: str, n_articulos: int, n_grupos: int,
                    fuentes_fallidas: list[dict[str, Any]], grupos: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "desde": desde,
        "hasta": hasta,
        "generado_utc": generado_utc,
        "total_articulos": n_articulos,
        "total_grupos": n_grupos,
        "grupos_exportados": len(grupos),
        "fuentes_fallidas": fuentes_fallidas,
        "grupos": grupos,
    }


def a_json(doc: dict[str, Any]) -> str:
    return json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2) + "\n"


def escribir(doc: dict[str, Any], ruta: str | Path) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(a_json(doc), encoding="utf-8")
    return ruta

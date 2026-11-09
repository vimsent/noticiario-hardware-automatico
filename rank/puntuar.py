"""Puntaje preliminar determinista. Solo ordena y recorta; la rubrica final la aplica el modelo."""

from __future__ import annotations

import math
from typing import Any

PESOS_DEFECTO = {"medios": 3, "comunidad": 2, "evento_mayor": 4, "oficial": 1, "rumor": -1, "bloque_chile": 0, "tema_prioritario": 0}


def score_prelim(n_medios: int, score_comunidad: int, evento_mayor: bool, oficial: bool,
                 es_rumor: bool, pesos: dict[str, Any] | None = None, bloque_chile: bool = False,
                 tema_prioritario: bool = False) -> float:
    p = {**PESOS_DEFECTO, **(pesos or {})}
    valor = (
        p["medios"] * math.log2(1 + max(n_medios, 0))
        + p["comunidad"] * math.log10(1 + max(score_comunidad, 0))
        + p["evento_mayor"] * int(evento_mayor)
        + p["oficial"] * int(oficial)
        + p["rumor"] * int(es_rumor)
        + p["bloque_chile"] * int(bloque_chile)
        + p["tema_prioritario"] * int(tema_prioritario)
    )
    return round(valor, 4)

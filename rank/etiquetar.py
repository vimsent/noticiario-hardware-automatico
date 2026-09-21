"""Empresas, categoria, evento mayor, rumor y leakers, por keywords de config.yaml."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from rank.normalizar import texto_normalizado


def _patron(keyword: str) -> re.Pattern[str] | None:
    kw = texto_normalizado(keyword)
    if not kw:
        return None
    return re.compile(r"(?<!\w)" + re.escape(kw) + r"(?!\w)")


def _patrones(keywords: list[str]) -> list[re.Pattern[str]]:
    return [p for p in (_patron(k) for k in keywords) if p is not None]


def cargar_leakers(path: str | Path) -> dict[str, list[str]]:
    """Lee data/leakers.md: cada '### nombre' y su linea '- Alias: a, b'."""
    ruta = Path(path)
    if not ruta.exists():
        return {}
    leakers: dict[str, list[str]] = {}
    actual: str | None = None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith("### "):
            actual = linea[4:].strip()
            leakers[actual] = [actual]
        elif actual and linea.strip().lower().startswith("- alias:"):
            alias = linea.split(":", 1)[1]
            leakers[actual].extend(a.strip() for a in alias.split(",") if a.strip())
    return leakers


class Etiquetador:
    def __init__(self, cfg_ranking: dict[str, Any], leakers: dict[str, list[str]] | None = None) -> None:
        self.empresas = {n: _patrones(alias) for n, alias in (cfg_ranking.get("empresas") or {}).items()}
        self.categorias = [(c, _patrones(kws or [])) for c, kws in (cfg_ranking.get("categorias") or {}).items()]
        self.evento_mayor = _patrones(cfg_ranking.get("keywords_evento_mayor") or [])
        self.rumor = _patrones(cfg_ranking.get("keywords_rumor") or [])
        self.chile = _patrones(cfg_ranking.get("keywords_chile") or ["chile"])
        self.tema_chile = _patrones(cfg_ranking.get("keywords_tema_chile") or [])
        self.bloque_chile = _patrones(cfg_ranking.get("keywords_bloque_chile") or [])
        self.leakers = {n: _patrones(alias) for n, alias in (leakers or {}).items()}

    @staticmethod
    def texto(titulo: str, resumen: str | None = None) -> str:
        return texto_normalizado(f"{titulo} {resumen or ''}")

    def detectar_empresas(self, texto_norm: str) -> list[str]:
        return sorted(n for n, pats in self.empresas.items() if any(p.search(texto_norm) for p in pats))

    def detectar_categoria(self, titulos_norm: str, texto_norm: str | None = None, min_hits_texto: int = 2) -> str:
        """Por titulos, primera categoria en orden de prioridad que calce. Si ninguna calza,
        por el texto completo gana la de mas coincidencias (minimo min_hits_texto)."""
        for categoria, pats in self.categorias:
            if any(p.search(titulos_norm) for p in pats):
                return categoria
        if texto_norm:
            mejor, mejor_hits = "industria", min_hits_texto - 1
            for categoria, pats in self.categorias:
                hits = sum(len(p.findall(texto_norm)) for p in pats)
                if hits > mejor_hits:
                    mejor, mejor_hits = categoria, hits
            return mejor
        return "industria"

    def es_evento_mayor(self, texto_norm: str, empresas: list[str]) -> bool:
        return bool(empresas) and any(p.search(texto_norm) for p in self.evento_mayor)

    def detectar_leakers(self, texto_norm: str) -> list[str]:
        return sorted(n for n, pats in self.leakers.items() if any(p.search(texto_norm) for p in pats))

    def es_rumor(self, texto_norm: str, leakers: list[str]) -> bool:
        return bool(leakers) or any(p.search(texto_norm) for p in self.rumor)

    def menciona_chile(self, texto_norm: str) -> bool:
        return any(p.search(texto_norm) for p in self.chile)

    def tema_bloque_chile(self, texto_norm: str) -> bool:
        return any(p.search(texto_norm) for p in self.bloque_chile)

    def tema_tecnologico(self, texto_norm: str, empresas: list[str]) -> bool:
        """Para medios chilenos generales: solo cuenta como es_chile si habla de tecnologia."""
        if empresas or not self.tema_chile:
            return True
        return any(p.search(texto_norm) for p in self.tema_chile)

    def etiquetar(self, texto_norm: str, titulos_norm: str | None = None) -> dict[str, Any]:
        empresas = self.detectar_empresas(texto_norm)
        leakers = self.detectar_leakers(texto_norm)
        return {
            "empresas": empresas,
            "categoria": self.detectar_categoria(titulos_norm or texto_norm, texto_norm),
            "evento_mayor": int(self.es_evento_mayor(texto_norm, empresas)),
            "leakers": leakers,
            "es_rumor": int(self.es_rumor(texto_norm, leakers)),
            "menciona_chile": self.menciona_chile(texto_norm),
        }

"""Agrupa articulos del mismo hecho con union-find y similitud de titulos."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from rapidfuzz import fuzz


@dataclass
class Articulo:
    id: int
    url: str
    medio: str
    categoria_feed: str
    titulo: str
    titulo_norm: str
    publicado_utc: str
    fecha: date
    resumen: str | None = None
    texto: str | None = None
    texto_ok: int = 0
    hash_texto: str | None = None
    url_enlazada: str | None = None
    score_comunidad: int | None = None
    empresas: list[str] = field(default_factory=list)
    feed: str = ""
    titulo_cmp: str = ""  # titulo_norm sin stopwords, para comparar

    def __post_init__(self) -> None:
        if not self.titulo_cmp:
            self.titulo_cmp = self.titulo_norm

    @property
    def es_comunidad(self) -> bool:
        return self.categoria_feed == "comunidad"

    @property
    def orden(self) -> tuple[str, int]:
        return (self.publicado_utc, self.id)


@dataclass
class Grupo:
    articulos: list[Articulo]
    adjuntos: list[Articulo] = field(default_factory=list)  # comunidad sin enlace, solo aporta score


class UnionFind:
    def __init__(self, n: int) -> None:
        self.padre = list(range(n))

    def raiz(self, i: int) -> int:
        while self.padre[i] != i:
            self.padre[i] = self.padre[self.padre[i]]
            i = self.padre[i]
        return i

    def unir(self, a: int, b: int) -> None:
        ra, rb = self.raiz(a), self.raiz(b)
        if ra != rb:
            self.padre[max(ra, rb)] = min(ra, rb)


def _comparten_empresa(a: Articulo, b: Articulo) -> bool:
    if not a.empresas and not b.empresas:
        return True
    return bool(set(a.empresas) & set(b.empresas))


MIN_TOKENS_SET = 3


def sin_stopwords(titulo_norm: str, stopwords: frozenset[str]) -> str:
    return " ".join(t for t in titulo_norm.split() if t not in stopwords)


def similitud(a: str, b: str) -> float:
    """token_set_ratio, salvo que alguno sea muy corto: ahi el set ratio da 100 por
    cualquier subconjunto y se usa el ratio ordenado, mas estricto."""
    if min(len(a.split()), len(b.split())) < MIN_TOKENS_SET:
        return fuzz.token_sort_ratio(a, b)
    return fuzz.token_set_ratio(a, b)


def agrupar(articulos: list[Articulo], umbral: float, ventana_dias: int) -> list[Grupo]:
    """Devuelve grupos en orden estable (articulo mas antiguo primero). Un par se une si
    ambos titulos se parecen entre si y ademas el nuevo se parece al representante
    (el mas antiguo) del grupo del otro, para no encadenar hechos distintos."""
    orden = sorted(articulos, key=lambda a: a.orden)
    sueltos = [a for a in orden if a.es_comunidad and not a.url_enlazada]
    base = [a for a in orden if not (a.es_comunidad and not a.url_enlazada)]
    uf = UnionFind(len(base))

    por_hash: dict[str, int] = {}
    por_url: dict[str, int] = {}
    for i, a in enumerate(base):
        if a.hash_texto and not a.es_comunidad:
            if a.hash_texto in por_hash:
                uf.unir(por_hash[a.hash_texto], i)
            else:
                por_hash[a.hash_texto] = i
        por_url.setdefault(a.url, i)
    for i, a in enumerate(base):
        if a.es_comunidad and a.url_enlazada and a.url_enlazada in por_url:
            uf.unir(por_url[a.url_enlazada], i)

    for i, a in enumerate(base):
        for j in range(i + 1, len(base)):
            b = base[j]
            if (b.fecha - a.fecha).days > ventana_dias:
                break
            ri, rj = uf.raiz(i), uf.raiz(j)
            if ri == rj or not _comparten_empresa(a, b):
                continue
            if similitud(a.titulo_cmp, b.titulo_cmp) < umbral:
                continue
            rep_i, rep_j = base[ri], base[rj]
            if similitud(rep_i.titulo_cmp, b.titulo_cmp) >= umbral and similitud(rep_j.titulo_cmp, a.titulo_cmp) >= umbral:
                uf.unir(i, j)

    miembros: dict[int, list[Articulo]] = {}
    for i, a in enumerate(base):
        miembros.setdefault(uf.raiz(i), []).append(a)
    grupos = [Grupo(articulos=sorted(m, key=lambda a: a.orden)) for m in miembros.values()]
    grupos.sort(key=lambda g: g.articulos[0].orden)

    for post in sueltos:
        mejor, mejor_sim = None, 0.0
        for g in grupos:
            sim = max(similitud(post.titulo_cmp, a.titulo_cmp) for a in g.articulos)
            if sim > mejor_sim:
                mejor, mejor_sim = g, sim
        if mejor is not None and mejor_sim >= umbral:
            mejor.adjuntos.append(post)
    return grupos

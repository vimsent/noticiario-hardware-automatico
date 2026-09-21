"""Etapa 2: agrupa, etiqueta, puntua y exporta candidatas.json. Uso:

    python -m rank.ranking --desde 2026-09-08 --hasta 2026-09-14
"""

from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingest import db  # noqa: E402
from ingest.comun import RAIZ, cargar_config, cargar_feeds, medios_conocidos, ventana_utc  # noqa: E402
from rank import exportar  # noqa: E402
from rank.agrupar import Articulo, Grupo, agrupar, sin_stopwords  # noqa: E402
from rank.etiquetar import Etiquetador, cargar_leakers  # noqa: E402
from rank.normalizar import clave_grupo, quitar_sufijo_medio  # noqa: E402
from rank.puntuar import score_prelim  # noqa: E402

log = logging.getLogger("ranking")


def _fecha_local(publicado_utc: str, zona: str) -> date:
    return datetime.fromisoformat(publicado_utc).astimezone(ZoneInfo(zona)).date()


def cargar_articulos(con: sqlite3.Connection, desde_utc: str, hasta_utc: str, zona: str,
                     etiquetador: Etiquetador, stopwords: frozenset[str] = frozenset()) -> list[Articulo]:
    articulos = []
    for fila in db.articulos_en_rango(con, desde_utc, hasta_utc):
        texto_norm = etiquetador.texto(fila["titulo"], fila["resumen"])
        articulos.append(Articulo(
            id=fila["id"], url=fila["url"], medio=fila["medio"], categoria_feed=fila["categoria_feed"],
            titulo=fila["titulo"], titulo_norm=fila["titulo_norm"], publicado_utc=fila["publicado_utc"],
            fecha=_fecha_local(fila["publicado_utc"], zona), resumen=fila["resumen"], texto=fila["texto"],
            texto_ok=fila["texto_ok"], hash_texto=fila["hash_texto"], url_enlazada=fila["url_enlazada"],
            score_comunidad=fila["score_comunidad"], empresas=etiquetador.detectar_empresas(texto_norm),
            feed=fila["feed"], titulo_cmp=sin_stopwords(fila["titulo_norm"], stopwords),
        ))
    return articulos


def _medios_tras_sindicacion(articulos: list[Articulo]) -> list[str]:
    """Copias con el mismo hash_texto cuentan como el medio de la mas antigua."""
    medio_por_hash: dict[str, str] = {}
    medios: set[str] = set()
    for a in articulos:
        if a.es_comunidad:
            continue
        if a.hash_texto:
            medios.add(medio_por_hash.setdefault(a.hash_texto, a.medio))
        else:
            medios.add(a.medio)
    return sorted(medios)


def _textos_para_exportar(articulos: list[Articulo], maximo: int, max_chars: int) -> list[dict[str, Any]]:
    con_texto = [a for a in articulos if a.texto]
    con_texto.sort(key=lambda a: (a.categoria_feed != "oficial", -len(a.texto or ""), a.orden))
    return [{"medio": a.medio, "url": a.url, "texto": (a.texto or "")[:max_chars]} for a in con_texto[:maximo]]


def construir_grupo(grupo: Grupo, etiquetador: Etiquetador, cfg: dict[str, Any], desde: date,
                    medios_conocidos: list[str], feeds_filtro_tema: frozenset[str] = frozenset()) -> dict[str, Any]:
    arts = grupo.articulos
    principales = [a for a in arts if not a.es_comunidad] or arts
    prioridad = {c: i for i, c in enumerate(cfg.get("prioridad_medios") or [])}
    repr_ = min(principales, key=lambda a: (prioridad.get(a.categoria_feed, len(prioridad)), a.orden))
    mas_antiguo = principales[0]

    texto_norm = " ".join(etiquetador.texto(a.titulo, a.resumen) for a in arts)
    titulos_norm = " ".join(a.titulo_norm for a in arts)
    etiquetas = etiquetador.etiquetar(texto_norm, titulos_norm)
    empresas = sorted({e for a in arts for e in a.empresas} | set(etiquetas["empresas"]))
    medios = _medios_tras_sindicacion(arts)
    score_comunidad = sum(int(a.score_comunidad or 0) for a in arts + grupo.adjuntos if a.es_comunidad)
    oficial = any(a.categoria_feed == "oficial" for a in arts)
    chile_por_feed = [a for a in arts if a.categoria_feed == "chile"]
    es_chile = bool(chile_por_feed) or etiquetas["menciona_chile"]
    if es_chile and (not chile_por_feed or all(a.feed in feeds_filtro_tema for a in chile_por_feed)):
        # solo medios generales (o mencion suelta de chile): exigir tema tecnologico
        es_chile = etiquetador.tema_tecnologico(texto_norm, empresas)
    categoria = etiquetas["categoria"]
    fecha_hecho = mas_antiguo.fecha
    evento_mayor = bool(etiquetas["evento_mayor"] and empresas)
    tema_chile = bool(es_chile and etiquetador.tema_bloque_chile(texto_norm))

    return {
        "clave": clave_grupo(mas_antiguo.url),
        "titulo_repr": quitar_sufijo_medio(repr_.titulo, medios_conocidos),
        "fecha_hecho": fecha_hecho.isoformat(),
        "n_medios": len(medios),
        "medios": medios,
        "score_comunidad": score_comunidad,
        "categoria": categoria,
        "empresas": empresas,
        "evento_mayor": int(evento_mayor),
        "es_rumor": int(etiquetas["es_rumor"]),
        "leakers": etiquetas["leakers"],
        "es_chile": int(es_chile),
        "tema_chile": int(tema_chile),
        "rezagada": int(fecha_hecho < desde),
        "score_prelim": score_prelim(len(medios), score_comunidad, evento_mayor, oficial,
                                     bool(etiquetas["es_rumor"]), cfg.get("pesos"), tema_chile),
        "articulos": [
            {"medio": a.medio, "titulo": a.titulo, "url": a.url, "fecha": a.publicado_utc,
             "texto_ok": int(a.texto_ok), "comunidad": int(a.es_comunidad),
             "score_comunidad": a.score_comunidad}
            for a in arts + grupo.adjuntos
        ],
        "textos": _textos_para_exportar(arts, int(cfg.get("max_articulos_con_texto", 3)),
                                        int(cfg.get("max_chars_texto", 6000))),
        "_ids": [a.id for a in arts + grupo.adjuntos],
    }


def generar_candidatas(con: sqlite3.Connection, cfg: dict[str, Any], desde: date, hasta: date,
                       leakers: dict[str, list[str]], medios_conocidos: list[str],
                       generado_utc: str | None = None,
                       feeds_filtro_tema: frozenset[str] = frozenset()) -> dict[str, Any]:
    ing, rk = cfg["ingesta"], cfg["ranking"]
    zona = ing.get("zona_horaria", "America/Santiago")
    desde_utc, hasta_utc = ventana_utc(desde, hasta, zona, dias_extra=int(ing.get("dias_rezagadas", 7)))
    run = hasta.isoformat()

    etiquetador = Etiquetador(rk, leakers)
    stopwords = frozenset(rk.get("stopwords") or [])
    articulos = cargar_articulos(con, desde_utc, hasta_utc, zona, etiquetador, stopwords)
    grupos = agrupar(articulos, float(rk.get("umbral_titulo", 70)), int(rk.get("ventana_agrupacion_dias", 4)))
    docs = [construir_grupo(g, etiquetador, rk, desde, medios_conocidos, feeds_filtro_tema) for g in grupos]
    log.info("%d articulos en %d grupos", len(articulos), len(docs))

    db.borrar_grupos_run(con, run)
    for d in docs:
        db.insertar_grupo(con, run, d, d["_ids"])
    con.commit()

    elegidos = exportar.seleccionar(docs, int(rk.get("max_grupos", 50)), int(rk.get("max_grupos_chile", 25)))
    for d in elegidos:
        d.pop("_ids", None)
    return exportar.armar_documento(
        desde.isoformat(), hasta.isoformat(), generado_utc or db.ahora_utc(), len(articulos), len(docs),
        db.fuentes_fallidas(con, run), elegidos,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="etapa 2: ranking")
    ap.add_argument("--desde", type=date.fromisoformat, required=True)
    ap.add_argument("--hasta", type=date.fromisoformat, required=True)
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    cfg = cargar_config(args.config)
    feeds = cargar_feeds(cfg["ingesta"].get("feeds_path", "feeds.yaml"), solo_activos=False)
    leakers = cargar_leakers(RAIZ / cfg["ranking"].get("leakers_path", "data/leakers.md"))
    con = db.conectar(RAIZ / cfg["ingesta"].get("db_path", "data/noticias.db"))
    filtro = frozenset(f["nombre"] for f in feeds if f.get("filtro_tema"))
    doc = generar_candidatas(con, cfg, args.desde, args.hasta, leakers, medios_conocidos(feeds), feeds_filtro_tema=filtro)
    con.close()

    salida = RAIZ / cfg["ranking"].get("salida_dir", "runs") / args.hasta.isoformat() / "candidatas.json"
    exportar.escribir(doc, salida)
    log.info("%d grupos exportados a %s", doc["grupos_exportados"], salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

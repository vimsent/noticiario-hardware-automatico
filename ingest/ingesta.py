"""Etapa 1: recorre feeds.yaml, llena la base, baja texto completo y datos de apoyo. Uso:

    python -m ingest.ingesta --desde 2026-09-08 --hasta 2026-09-14 [--solo phoronix,r_hardware] [--sin-texto]
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingest import apoyo, comunidad, db, google_news, rss, scrapers_chile, texto_completo  # noqa: E402
from ingest.comun import RAIZ, cargar_config, cargar_feeds, medios_conocidos, ventana_utc  # noqa: E402
from ingest.red import ClienteHttp  # noqa: E402

log = logging.getLogger("ingesta")


@dataclass
class Contexto:
    cliente: Any
    cfg: dict[str, Any]
    medios: list[str]
    desde_utc: str
    hasta_utc: str

    @property
    def dias_ventana(self) -> int:
        d = datetime.fromisoformat(self.desde_utc)
        h = datetime.fromisoformat(self.hasta_utc)
        return (h - d).days + 1


Ingestor = Callable[[Contexto, dict[str, Any]], list[dict[str, Any]]]


def _ingerir_rss(ctx: Contexto, fuente: dict[str, Any]) -> list[dict[str, Any]]:
    contenido = rss.descargar_feed(ctx.cliente, fuente)
    return rss.parsear_feed(contenido, fuente, ctx.medios, db.ahora_utc())


def _ingerir_google_news(ctx: Contexto, fuente: dict[str, Any]) -> list[dict[str, Any]]:
    url = google_news.url_consulta(fuente, ctx.cfg["google_news_url"], ctx.dias_ventana)
    resp = ctx.cliente.get(url)
    return google_news.parsear_google_news(resp.content, fuente, ctx.medios, db.ahora_utc())


def _ingerir_reddit(ctx: Contexto, fuente: dict[str, Any]) -> list[dict[str, Any]]:
    return comunidad.descargar_reddit(ctx.cliente, fuente, ctx.cfg["reddit"], ctx.medios, db.ahora_utc())


def _ingerir_hn(ctx: Contexto, fuente: dict[str, Any]) -> list[dict[str, Any]]:
    cfg_hn = ctx.cfg["hn"]
    resp = ctx.cliente.get(comunidad.url_hn(fuente, cfg_hn["url"], ctx.desde_utc, ctx.hasta_utc))
    return comunidad.parsear_hn(resp.json(), fuente, ctx.medios, db.ahora_utc(), cfg_hn["item_url"])


def _ingerir_scraper(ctx: Contexto, fuente: dict[str, Any]) -> list[dict[str, Any]]:
    if not ctx.cliente.permitido_por_robots(fuente["url"]):
        raise PermissionError(f"robots.txt no permite {fuente['url']}")
    resp = ctx.cliente.get(fuente["url"])
    return scrapers_chile.articulos_desde_scraper(fuente["scraper"], resp.text, fuente, ctx.medios, db.ahora_utc())


INGESTORES: dict[str, Ingestor] = {
    "rss": _ingerir_rss,
    "scraper": _ingerir_scraper,
    "google_news": _ingerir_google_news,
    "reddit": _ingerir_reddit,
    "hn": _ingerir_hn,
}


def ingerir_todo(con: Any, ctx: Contexto, fuentes: list[dict[str, Any]], run: str) -> dict[str, int]:
    """Recorre las fuentes. Una que falla se registra y no detiene el resto."""
    totales = {"fuentes_ok": 0, "fuentes_error": 0, "nuevos": 0, "vistos": 0}
    for fuente in fuentes:
        nombre = fuente["nombre"]
        ingestor = INGESTORES.get(fuente.get("tipo", "rss"))
        if ingestor is None:
            log.warning("[%s] tipo %s no implementado, se salta", nombre, fuente.get("tipo"))
            continue
        try:
            articulos = rss.filtrar_ventana(ingestor(ctx, fuente), ctx.desde_utc, ctx.hasta_utc)
        except Exception as e:  # una fuente caida no detiene la etapa
            log.error("[%s] fallo: %s", nombre, e)
            db.registrar_fuente_estado(con, run, nombre, False, 0, f"{type(e).__name__}: {e}")
            con.commit()
            totales["fuentes_error"] += 1
            continue
        nuevos = 0
        for articulo in articulos:
            _, es_nuevo = db.upsert_articulo(con, articulo)
            nuevos += int(es_nuevo)
        db.registrar_fuente_estado(con, run, nombre, True, len(articulos))
        con.commit()
        log.info("[%s] %d en ventana, %d nuevos", nombre, len(articulos), nuevos)
        totales["fuentes_ok"] += 1
        totales["nuevos"] += nuevos
        totales["vistos"] += len(articulos)
    return totales


def generar_apoyo(cliente: Any, cfg_apoyo: dict[str, Any], hasta: date, ruta: Path) -> Path:
    errores: list[str] = []
    dolar = None
    try:
        dolar = apoyo.obtener_dolar(cliente, hasta, cfg_apoyo["dolar_url"])
        log.info("dolar observado %s: %s", dolar["fecha"], dolar["valor"])
    except Exception as e:
        errores.append(f"dolar: {type(e).__name__}: {e}")
        log.error("dolar: %s", e)
    precios = apoyo.obtener_precios(cliente, cfg_apoyo.get("precios"))
    return apoyo.escribir_apoyo(ruta, dolar, precios, errores)


def fechas_por_defecto(zona: str) -> tuple[date, date]:
    hoy = datetime.now(ZoneInfo(zona)).date()
    hasta = hoy - timedelta(days=1)
    return hasta - timedelta(days=6), hasta


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="etapa 1: ingesta de fuentes")
    ap.add_argument("--desde", type=date.fromisoformat)
    ap.add_argument("--hasta", type=date.fromisoformat)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--solo", help="nombres de fuentes separados por coma (para probar)")
    ap.add_argument("--sin-texto", action="store_true", help="no descargar texto completo")
    ap.add_argument("--sin-apoyo", action="store_true", help="no generar apoyo.json")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    cfg = cargar_config(args.config)
    ing = cfg["ingesta"]
    zona = ing.get("zona_horaria", "America/Santiago")
    desde, hasta = args.desde, args.hasta
    if desde is None or hasta is None:
        d_def, h_def = fechas_por_defecto(zona)
        desde, hasta = desde or d_def, hasta or h_def

    desde_utc, hasta_utc = ventana_utc(desde, hasta, zona, dias_extra=int(ing.get("dias_rezagadas", 7)))
    run = hasta.isoformat()
    fuentes = cargar_feeds(ing.get("feeds_path", "feeds.yaml"))
    medios = medios_conocidos(fuentes)
    if args.solo:
        pedidas = set(args.solo.split(","))
        fuentes = [f for f in fuentes if f["nombre"] in pedidas]
    log.info("run %s: ventana %s a %s, %d fuentes", run, desde_utc, hasta_utc, len(fuentes))

    con = db.conectar(RAIZ / ing.get("db_path", "data/noticias.db"))
    with ClienteHttp(
        user_agent=ing["user_agent"],
        timeout_s=float(ing.get("timeout_s", 20)),
        reintentos=int(ing.get("reintentos", 2)),
        req_por_seg_por_host=float(ing.get("req_por_seg_por_host", 1)),
        intervalo_por_host=ing.get("intervalo_por_host") or {},
    ) as cliente:
        ctx = Contexto(cliente, ing, medios, desde_utc, hasta_utc)
        totales = ingerir_todo(con, ctx, fuentes, run)
        log.info("fuentes: %s", totales)
        if not args.sin_texto:
            tc = ing.get("texto_completo") or {}
            res = texto_completo.descargar_textos(
                con, cliente, fuentes, desde_utc, hasta_utc,
                maximo=int(tc.get("max_por_run", 300)), min_chars=int(tc.get("min_chars", 300)))
            log.info("texto completo: %s", res)
        if not args.sin_apoyo:
            ruta = RAIZ / cfg["ranking"].get("salida_dir", "runs") / run / "apoyo.json"
            generar_apoyo(cliente, cfg["apoyo"], hasta, ruta)
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

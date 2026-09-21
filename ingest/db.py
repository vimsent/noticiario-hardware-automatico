"""Esquema, conexion y operaciones basicas sobre data/noticias.db."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ESQUEMA = """
create table if not exists articulos (
  id integer primary key,
  url text not null unique,
  url_original text,
  url_enlazada text,
  feed text not null,
  fuente_tipo text not null,
  medio text not null,
  categoria_feed text not null,
  idioma text,
  titulo text not null,
  titulo_norm text not null,
  resumen text,
  texto text,
  texto_ok integer not null default 0,
  hash_texto text,
  publicado_utc text not null,
  obtenido_utc text not null,
  score_comunidad integer
);

create index if not exists idx_articulos_publicado on articulos(publicado_utc);
create index if not exists idx_articulos_hash on articulos(hash_texto);

create table if not exists grupos (
  id integer primary key,
  run text not null,
  clave text not null,
  titulo_repr text not null,
  fecha_hecho text not null,
  n_medios integer not null,
  medios text not null,
  score_comunidad integer not null default 0,
  categoria text not null,
  empresas text not null,
  evento_mayor integer not null default 0,
  es_rumor integer not null default 0,
  leakers text not null default '[]',
  es_chile integer not null default 0,
  rezagada integer not null default 0,
  score_prelim real not null,
  unique (run, clave)
);

create table if not exists grupo_articulos (
  grupo_id integer not null references grupos(id),
  articulo_id integer not null references articulos(id),
  primary key (grupo_id, articulo_id)
);

create table if not exists fuentes_estado (
  run text not null,
  feed text not null,
  ok integer not null,
  n_items integer not null,
  error text,
  ts_utc text not null
);
"""

CAMPOS_ARTICULO = (
    "url", "url_original", "url_enlazada", "feed", "fuente_tipo", "medio",
    "categoria_feed", "idioma", "titulo", "titulo_norm", "resumen", "texto",
    "texto_ok", "hash_texto", "publicado_utc", "obtenido_utc", "score_comunidad",
)


def ahora_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def conectar(db_path: str | Path) -> sqlite3.Connection:
    """Abre la base (creandola si no existe) con el esquema aplicado."""
    path = Path(db_path)
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    con.execute("pragma foreign_keys = on")
    con.executescript(ESQUEMA)
    return con


def upsert_articulo(con: sqlite3.Connection, articulo: dict[str, Any]) -> tuple[int, bool]:
    """Inserta por url canonica. Si ya existe, completa lo que falte sin pisar
    el texto ya descargado. Devuelve (id, es_nuevo)."""
    fila = {campo: articulo.get(campo) for campo in CAMPOS_ARTICULO}
    fila.setdefault("texto_ok", 0)
    fila["texto_ok"] = int(fila["texto_ok"] or 0)
    fila["obtenido_utc"] = fila["obtenido_utc"] or ahora_utc()
    faltantes = [c for c in ("url", "feed", "fuente_tipo", "medio", "categoria_feed",
                              "titulo", "titulo_norm", "publicado_utc") if not fila.get(c)]
    if faltantes:
        raise ValueError(f"articulo sin campos obligatorios: {faltantes}")

    existente = con.execute("select id from articulos where url = ?", (fila["url"],)).fetchone()
    columnas = ", ".join(CAMPOS_ARTICULO)
    marcas = ", ".join(f":{c}" for c in CAMPOS_ARTICULO)
    con.execute(
        f"""
        insert into articulos ({columnas}) values ({marcas})
        on conflict(url) do update set
          url_enlazada = coalesce(articulos.url_enlazada, excluded.url_enlazada),
          resumen = coalesce(articulos.resumen, excluded.resumen),
          texto = case when articulos.texto_ok = 1 then articulos.texto
                       else coalesce(excluded.texto, articulos.texto) end,
          texto_ok = max(articulos.texto_ok, excluded.texto_ok),
          hash_texto = case when articulos.texto_ok = 1 then articulos.hash_texto
                            else coalesce(excluded.hash_texto, articulos.hash_texto) end,
          score_comunidad = max(coalesce(articulos.score_comunidad, 0),
                                coalesce(excluded.score_comunidad, 0))
        """,
        fila,
    )
    fila_id = con.execute("select id from articulos where url = ?", (fila["url"],)).fetchone()["id"]
    return int(fila_id), existente is None


def actualizar_texto(con: sqlite3.Connection, articulo_id: int, texto: str | None,
                     hash_texto: str | None, texto_ok: bool) -> None:
    con.execute(
        "update articulos set texto = ?, hash_texto = ?, texto_ok = ? where id = ?",
        (texto, hash_texto, int(texto_ok), articulo_id),
    )


def articulos_sin_texto(con: sqlite3.Connection, feeds: Iterable[str],
                        desde_utc: str, hasta_utc: str) -> list[sqlite3.Row]:
    nombres = list(feeds)
    if not nombres:
        return []
    marcas = ", ".join("?" for _ in nombres)
    return con.execute(
        f"""
        select * from articulos
        where texto_ok = 0 and feed in ({marcas})
          and publicado_utc >= ? and publicado_utc <= ?
        order by publicado_utc, id
        """,
        (*nombres, desde_utc, hasta_utc),
    ).fetchall()


def articulos_en_rango(con: sqlite3.Connection, desde_utc: str, hasta_utc: str) -> list[sqlite3.Row]:
    return con.execute(
        "select * from articulos where publicado_utc >= ? and publicado_utc <= ? order by publicado_utc, id",
        (desde_utc, hasta_utc),
    ).fetchall()


def registrar_fuente_estado(con: sqlite3.Connection, run: str, feed: str, ok: bool,
                            n_items: int, error: str | None = None) -> None:
    con.execute(
        "insert into fuentes_estado (run, feed, ok, n_items, error, ts_utc) values (?, ?, ?, ?, ?, ?)",
        (run, feed, int(ok), n_items, error, ahora_utc()),
    )


def fuentes_fallidas(con: sqlite3.Connection, run: str) -> list[dict[str, Any]]:
    """Ultimo estado de cada feed en el run, solo las que fallaron."""
    filas = con.execute(
        """
        select feed, error from fuentes_estado
        where run = ? and rowid in (
          select max(rowid) from fuentes_estado where run = ? group by feed
        ) and ok = 0
        order by feed
        """,
        (run, run),
    ).fetchall()
    return [{"feed": f["feed"], "error": f["error"]} for f in filas]


def borrar_grupos_run(con: sqlite3.Connection, run: str) -> None:
    con.execute(
        "delete from grupo_articulos where grupo_id in (select id from grupos where run = ?)", (run,)
    )
    con.execute("delete from grupos where run = ?", (run,))


def insertar_grupo(con: sqlite3.Connection, run: str, grupo: dict[str, Any],
                   articulo_ids: Iterable[int]) -> int:
    cur = con.execute(
        """
        insert into grupos (run, clave, titulo_repr, fecha_hecho, n_medios, medios, score_comunidad,
                            categoria, empresas, evento_mayor, es_rumor, leakers, es_chile, rezagada, score_prelim)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run, grupo["clave"], grupo["titulo_repr"], grupo["fecha_hecho"], grupo["n_medios"],
            json.dumps(grupo["medios"], ensure_ascii=False), grupo.get("score_comunidad", 0),
            grupo["categoria"], json.dumps(grupo["empresas"], ensure_ascii=False),
            int(grupo.get("evento_mayor", 0)), int(grupo.get("es_rumor", 0)),
            json.dumps(grupo.get("leakers", []), ensure_ascii=False),
            int(grupo.get("es_chile", 0)), int(grupo.get("rezagada", 0)), float(grupo["score_prelim"]),
        ),
    )
    grupo_id = int(cur.lastrowid)
    con.executemany(
        "insert into grupo_articulos (grupo_id, articulo_id) values (?, ?)",
        [(grupo_id, int(a)) for a in sorted(set(articulo_ids))],
    )
    return grupo_id

import pytest

from ingest import db


def articulo(**extra):
    base = {
        "url": "https://www.phoronix.com/news/x",
        "url_original": "https://www.phoronix.com/news/x?utm_source=rss",
        "feed": "phoronix",
        "fuente_tipo": "rss",
        "medio": "Phoronix",
        "categoria_feed": "hardware",
        "idioma": "en",
        "titulo": "Intel X",
        "titulo_norm": "intel x",
        "resumen": "resumen",
        "publicado_utc": "2026-09-10T12:00:00+00:00",
    }
    base.update(extra)
    return base


@pytest.fixture
def con(tmp_path):
    c = db.conectar(tmp_path / "t.db")
    yield c
    c.close()


def test_conectar_crea_esquema(con):
    tablas = {r["name"] for r in con.execute("select name from sqlite_master where type='table'")}
    assert {"articulos", "grupos", "grupo_articulos", "fuentes_estado"} <= tablas


def test_upsert_es_idempotente(con):
    id1, nuevo1 = db.upsert_articulo(con, articulo())
    id2, nuevo2 = db.upsert_articulo(con, articulo())
    assert id1 == id2
    assert nuevo1 is True and nuevo2 is False
    assert con.execute("select count(*) from articulos").fetchone()[0] == 1


def test_upsert_no_pisa_texto_descargado(con):
    aid, _ = db.upsert_articulo(con, articulo())
    db.actualizar_texto(con, aid, "texto largo", "hash1", True)
    db.upsert_articulo(con, articulo(texto="resumen corto", texto_ok=0, hash_texto="hash2"))
    fila = con.execute("select texto, texto_ok, hash_texto from articulos where id = ?", (aid,)).fetchone()
    assert fila["texto"] == "texto largo"
    assert fila["texto_ok"] == 1
    assert fila["hash_texto"] == "hash1"


def test_upsert_completa_campos_faltantes_y_score(con):
    db.upsert_articulo(con, articulo(resumen=None, score_comunidad=10))
    db.upsert_articulo(con, articulo(resumen="ahora si", score_comunidad=50, url_enlazada="https://x.com/a"))
    fila = con.execute("select resumen, score_comunidad, url_enlazada from articulos").fetchone()
    assert fila["resumen"] == "ahora si"
    assert fila["score_comunidad"] == 50
    assert fila["url_enlazada"] == "https://x.com/a"


def test_upsert_exige_campos_obligatorios(con):
    with pytest.raises(ValueError):
        db.upsert_articulo(con, articulo(titulo=None))


def test_articulos_sin_texto_y_en_rango(con):
    db.upsert_articulo(con, articulo(url="https://a.com/1", publicado_utc="2026-09-01T00:00:00+00:00"))
    aid, _ = db.upsert_articulo(con, articulo(url="https://a.com/2", publicado_utc="2026-09-10T00:00:00+00:00"))
    db.upsert_articulo(con, articulo(url="https://a.com/3", publicado_utc="2026-09-10T01:00:00+00:00", feed="otro"))
    db.actualizar_texto(con, aid, "t", "h", True)
    pendientes = db.articulos_sin_texto(con, ["phoronix", "otro"], "2026-09-05", "2026-09-11")
    assert [p["url"] for p in pendientes] == ["https://a.com/3"]
    rango = db.articulos_en_rango(con, "2026-09-05", "2026-09-11")
    assert [r["url"] for r in rango] == ["https://a.com/2", "https://a.com/3"]


def test_fuentes_estado_solo_ultimo_estado(con):
    db.registrar_fuente_estado(con, "2026-09-14", "phoronix", False, 0, "timeout")
    db.registrar_fuente_estado(con, "2026-09-14", "tomshardware", True, 20)
    db.registrar_fuente_estado(con, "2026-09-14", "videocardz", False, 0, "403")
    assert db.fuentes_fallidas(con, "2026-09-14") == [
        {"feed": "phoronix", "error": "timeout"},
        {"feed": "videocardz", "error": "403"},
    ]
    assert db.fuentes_fallidas(con, "2026-09-07") == []


def test_grupos_insertar_y_borrar_run(con):
    aid, _ = db.upsert_articulo(con, articulo())
    grupo = {
        "clave": "abc", "titulo_repr": "Intel X", "fecha_hecho": "2026-09-10", "n_medios": 1,
        "medios": ["Phoronix"], "categoria": "cpu", "empresas": ["Intel"], "score_prelim": 3.0,
    }
    gid = db.insertar_grupo(con, "2026-09-14", grupo, [aid])
    assert con.execute("select count(*) from grupo_articulos where grupo_id = ?", (gid,)).fetchone()[0] == 1
    db.borrar_grupos_run(con, "2026-09-14")
    assert con.execute("select count(*) from grupos").fetchone()[0] == 0
    assert con.execute("select count(*) from grupo_articulos").fetchone()[0] == 0

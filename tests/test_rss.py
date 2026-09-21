from pathlib import Path

import pytest

from ingest import db, rss
from ingest.comun import ventana_utc
from ingest.ingesta import Contexto, ingerir_todo

FIXTURES = Path(__file__).parent / "fixtures"
FUENTE = {"nombre": "ejemplo", "medio": "Ejemplo", "tipo": "rss", "url": "https://ejemplo.com/rss",
          "categoria": "hardware", "idioma": "es", "texto_completo": True}
OBTENIDO = "2026-09-14T00:00:00+00:00"


def test_parsear_feed_basico():
    arts = rss.parsear_feed((FIXTURES / "feed_basico.xml").read_bytes(), FUENTE, ["Tom's Hardware"], OBTENIDO)
    assert [a["titulo"] for a in arts] == ["Intel lanza Panther Lake - Tom's Hardware",
                                            "Noticia vieja fuera de la ventana", "Sin fecha"]
    a = arts[0]
    assert a["url"] == "https://www.ejemplo.com/noticias/intel-panther-lake"
    assert a["url_original"].startswith("https://www.Ejemplo.com/")
    assert a["titulo_norm"] == "intel lanza panther lake"
    assert a["resumen"] == "Intel anuncia Panther Lake con Xe3."
    assert a["publicado_utc"] == "2026-09-10T15:00:00+00:00"
    assert a["feed"] == "ejemplo" and a["medio"] == "Ejemplo" and a["categoria_feed"] == "hardware"
    assert arts[2]["publicado_utc"] == OBTENIDO


def test_parsear_feed_atom():
    arts = rss.parsear_feed((FIXTURES / "feed_atom.xml").read_bytes(), FUENTE, [], OBTENIDO)
    assert len(arts) == 1
    assert arts[0]["url"] == "https://ejemplo.org/amd-zen-6"
    assert arts[0]["publicado_utc"] == "2026-09-12T12:30:00+00:00"
    assert arts[0]["resumen"] == "Zen 6 llega en 2027."


def test_parsear_feed_roto_lanza():
    with pytest.raises(ValueError):
        rss.parsear_feed((FIXTURES / "feed_roto.xml").read_bytes(), FUENTE, [], OBTENIDO)


def test_parsear_feed_real_phoronix():
    fuente = dict(FUENTE, nombre="phoronix", medio="Phoronix")
    arts = rss.parsear_feed((FIXTURES / "feed_phoronix.xml").read_bytes(), fuente, ["Phoronix"], OBTENIDO)
    assert len(arts) > 10
    assert all(a["url"].startswith("https://www.phoronix.com/") for a in arts)
    assert all(a["publicado_utc"] != OBTENIDO for a in arts)


def test_filtrar_ventana():
    arts = rss.parsear_feed((FIXTURES / "feed_basico.xml").read_bytes(), FUENTE, [], OBTENIDO)
    desde, hasta = ventana_utc(__import__("datetime").date(2026, 9, 8), __import__("datetime").date(2026, 9, 14),
                               "America/Santiago", dias_extra=7)
    dentro = rss.filtrar_ventana(arts, desde, hasta)
    assert [a["url"] for a in dentro] == ["https://www.ejemplo.com/noticias/intel-panther-lake",
                                          "https://ejemplo.com/sin-fecha"]


class ClienteFalso:
    """Devuelve fixtures por url; lanza en las urls marcadas."""

    def __init__(self, respuestas: dict[str, bytes | Exception]):
        self.respuestas = respuestas
        self.llamadas: list[str] = []

    def get(self, url, **kw):
        self.llamadas.append(url)
        r = self.respuestas[url]
        if isinstance(r, Exception):
            raise r

        class Resp:
            content = r
        return Resp()


def test_ingerir_todo_aisla_fallas_y_es_idempotente(tmp_path):
    con = db.conectar(tmp_path / "t.db")
    fuentes = [
        dict(FUENTE, nombre="ok", url="https://ok/rss"),
        dict(FUENTE, nombre="caida", url="https://caida/rss"),
        dict(FUENTE, nombre="rota", url="https://rota/rss"),
    ]
    cliente = ClienteFalso({
        "https://ok/rss": (FIXTURES / "feed_basico.xml").read_bytes(),
        "https://caida/rss": TimeoutError("timeout"),
        "https://rota/rss": (FIXTURES / "feed_roto.xml").read_bytes(),
    })
    desde, hasta = "2026-09-01T00:00:00+00:00", "2099-01-01T00:00:00+00:00"
    ctx = Contexto(cliente, {}, ["Ejemplo"], desde, hasta)
    t1 = ingerir_todo(con, ctx, fuentes, "2026-09-14")
    assert t1 == {"fuentes_ok": 1, "fuentes_error": 2, "nuevos": 2, "vistos": 2}
    t2 = ingerir_todo(con, ctx, fuentes, "2026-09-14")
    assert t2["nuevos"] == 0 and t2["vistos"] == 2
    assert con.execute("select count(*) from articulos").fetchone()[0] == 2
    fallidas = db.fuentes_fallidas(con, "2026-09-14")
    assert [f["feed"] for f in fallidas] == ["caida", "rota"]
    assert "timeout" in fallidas[0]["error"]

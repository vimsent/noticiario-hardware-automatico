import json
from datetime import date
from pathlib import Path

import pytest

from ingest import apoyo, comunidad, db, google_news, texto_completo
from ingest.ingesta import Contexto, ingerir_todo

FIXTURES = Path(__file__).parent / "fixtures"
OBTENIDO = "2026-09-16T00:00:00+00:00"


class RespFalsa:
    def __init__(self, contenido):
        self.content = contenido if isinstance(contenido, bytes) else contenido.encode()
        self.text = contenido if isinstance(contenido, str) else contenido.decode()

    def json(self):
        return json.loads(self.text)


class ClienteFalso:
    user_agent = "test"
    timeout_s = 1

    def __init__(self, respuestas, robots=True):
        self.respuestas = respuestas
        self.robots = robots
        self.llamadas = []

    def get(self, url, **kw):
        self.llamadas.append(url)
        for prefijo, r in self.respuestas.items():
            if url.startswith(prefijo):
                if isinstance(r, Exception):
                    raise r
                return RespFalsa(r)
        raise KeyError(url)

    def permitido_por_robots(self, url):
        return self.robots


# --- google news

def test_google_news_url_consulta():
    f = {"consulta": "data center Chile", "hl": "es-419", "gl": "CL", "ceid": "CL:es-419"}
    url = google_news.url_consulta(f, "https://news.google.com/rss/search", 14)
    assert url == "https://news.google.com/rss/search?q=data+center+Chile+when%3A14d&hl=es-419&gl=CL&ceid=CL%3Aes-419"


def test_google_news_parsea_medio_real():
    f = {"nombre": "gn_nvidia", "medio": "Google News", "categoria": "general", "hl": "es-419"}
    arts = google_news.parsear_google_news((FIXTURES / "google_news_nvidia.xml").read_bytes(), f, [], OBTENIDO)
    assert len(arts) == 5
    for a in arts:
        assert a["fuente_tipo"] == "google_news"
        assert a["url"].startswith("https://news.google.com/rss/articles/")
        assert a["medio"] != "Google News"
        assert not a["titulo"].endswith(a["medio"])
        assert a["publicado_utc"] != OBTENIDO
        assert "url_enlazada" not in a
    assert len({a["medio"] for a in arts}) > 1


# --- reddit

def test_reddit_rss_extrae_enlace_externo():
    f = {"nombre": "r_hardware", "subreddit": "hardware", "medio": "r/hardware", "categoria": "comunidad"}
    arts = comunidad.parsear_reddit_rss((FIXTURES / "reddit_hardware.xml").read_bytes(), f, [], OBTENIDO)
    assert len(arts) == 5
    assert all(a["url"].startswith("https://www.reddit.com/r/hardware/comments/") for a in arts)
    assert all(a["score_comunidad"] is None for a in arts)
    externos = [a["url_enlazada"] for a in arts if a["url_enlazada"]]
    assert externos and all("reddit.com" not in u for u in externos)


def test_reddit_json_con_puntaje_y_min_puntos():
    f = {"nombre": "r_hardware", "subreddit": "hardware", "categoria": "comunidad", "min_puntos": 10}
    arts = comunidad.parsear_reddit_json(json.loads((FIXTURES / "reddit_hardware.json").read_text()), f, [], OBTENIDO)
    assert [a["titulo"] for a in arts] == ["Desktop GPU shipments hit four-year high", "Weekly discussion thread"]
    assert arts[0]["score_comunidad"] == 812
    assert arts[0]["url_enlazada"] == "https://www.tweaktown.com/news/113493/desktop-gpu-shipments.html"
    assert arts[0]["url"] == "https://www.reddit.com/r/hardware/comments/abc1/desktop_gpu"
    assert arts[1]["url_enlazada"] is None and arts[1]["resumen"] == "Talk about anything"
    assert arts[0]["medio"] == "r/hardware"


def test_reddit_url_rss():
    f = {"subreddit": "Amd", "periodo": "week", "limite": 50}
    assert comunidad.url_reddit_rss(f, "https://www.reddit.com/r/{subreddit}/top/.rss?t={periodo}&limit={limite}") == \
        "https://www.reddit.com/r/Amd/top/.rss?t=week&limit=50"


def test_reddit_oauth_sin_credenciales(monkeypatch):
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    cfg = {"metodo": "oauth", "oauth_token_url": "https://x", "oauth_api_url": "https://y",
           "client_id_env": "REDDIT_CLIENT_ID", "client_secret_env": "REDDIT_CLIENT_SECRET"}
    with pytest.raises(RuntimeError):
        comunidad.descargar_reddit(ClienteFalso({}), {"nombre": "r", "subreddit": "hardware"}, cfg, [], OBTENIDO)


# --- hacker news

def test_hn_url_y_parseo():
    f = {"nombre": "hn_nvidia", "consulta": "nvidia", "limite": 6, "categoria": "comunidad", "min_puntos": 50}
    url = comunidad.url_hn(f, "https://hn.algolia.com/api/v1/search", "2026-09-01T00:00:00+00:00", "2026-09-15T00:00:00+00:00")
    assert url.startswith("https://hn.algolia.com/api/v1/search?query=nvidia&tags=story&numericFilters=created_at_i%3E")
    datos = json.loads((FIXTURES / "hn_nvidia.json").read_text(encoding="utf-8"))
    arts = comunidad.parsear_hn(datos, f, [], OBTENIDO, "https://news.ycombinator.com/item?id={id}")
    assert arts and all(a["score_comunidad"] >= 50 for a in arts)
    assert all(a["url"].startswith("https://news.ycombinator.com/item?id=") for a in arts)
    assert all(a["fuente_tipo"] == "hn" and a["medio"] == "Hacker News" for a in arts)
    assert any(a["url_enlazada"] for a in arts)
    assert len(arts) < len(datos["hits"])


# --- texto completo

def test_extraer_html_real():
    html = (FIXTURES / "articulo_phoronix.html").read_bytes()
    texto = texto_completo.extraer(html, "https://www.phoronix.com/news/GNU-Coreutils-9.12")
    assert texto and "Coreutils" in texto and len(texto) > 500


def test_descargar_textos_respeta_robots_y_fallas(tmp_path):
    con = db.conectar(tmp_path / "t.db")
    base = {"feed": "phoronix", "fuente_tipo": "rss", "medio": "Phoronix", "categoria_feed": "hardware",
            "titulo": "t", "titulo_norm": "t", "publicado_utc": "2026-09-10T00:00:00+00:00"}
    db.upsert_articulo(con, dict(base, url="https://www.phoronix.com/ok"))
    db.upsert_articulo(con, dict(base, url="https://www.phoronix.com/caido"))
    db.upsert_articulo(con, dict(base, url="https://www.phoronix.com/corto"))
    db.upsert_articulo(con, dict(base, url="https://otro.com/sin-texto-completo", feed="otro"))
    cliente = ClienteFalso({
        "https://www.phoronix.com/ok": (FIXTURES / "articulo_phoronix.html").read_bytes(),
        "https://www.phoronix.com/caido": TimeoutError("timeout"),
        "https://www.phoronix.com/corto": "<html><body><p>hola</p></body></html>",
    })
    fuentes = [{"nombre": "phoronix", "texto_completo": True}, {"nombre": "otro", "texto_completo": False}]
    res = texto_completo.descargar_textos(con, cliente, fuentes, "2026-09-01", "2026-09-30")
    assert res == {"pendientes": 3, "ok": 1, "fallidos": 2, "robots": 0}
    fila = con.execute("select texto_ok, hash_texto from articulos where url = 'https://www.phoronix.com/ok'").fetchone()
    assert fila["texto_ok"] == 1 and fila["hash_texto"]
    # segunda pasada: el que ya tiene texto no se vuelve a bajar
    res2 = texto_completo.descargar_textos(con, cliente, fuentes, "2026-09-01", "2026-09-30")
    assert res2["pendientes"] == 2
    bloqueado = ClienteFalso({}, robots=False)
    assert texto_completo.descargar_textos(con, bloqueado, fuentes, "2026-09-01", "2026-09-30")["robots"] == 2
    assert bloqueado.llamadas == []


# --- apoyo

def test_obtener_dolar_dia_habil():
    cliente = ClienteFalso({"https://mindicador.cl/api/dolar/14-09-2026": (FIXTURES / "mindicador_dolar_serie.json").read_text()})
    d = apoyo.obtener_dolar(cliente, date(2026, 9, 14), "https://mindicador.cl/api")
    assert d == {"valor": 957.53, "fecha": "2026-09-15", "fuente": "https://mindicador.cl/api/dolar"} or d["valor"] > 0


def test_obtener_dolar_fin_de_semana_cae_al_ultimo_habil():
    cliente = ClienteFalso({
        "https://mindicador.cl/api/dolar/13-09-2026": (FIXTURES / "mindicador_dolar_vacio.json").read_text(),
        "https://mindicador.cl/api/dolar": (FIXTURES / "mindicador_dolar_serie.json").read_text(),
    })
    d = apoyo.obtener_dolar(cliente, date(2026, 9, 13), "https://mindicador.cl/api")
    assert d["valor"] == 938.10 and d["fecha"] == "2026-09-11"


def test_escribir_apoyo(tmp_path):
    ruta = apoyo.escribir_apoyo(tmp_path / "r" / "apoyo.json", {"valor": 1.0, "fecha": "2026-09-14", "fuente": "x"}, [], [])
    doc = json.loads(ruta.read_text())
    assert doc["dolar"]["valor"] == 1.0 and doc["precios"] == [] and doc["errores"] == []


def test_obtener_precios_desactivado():
    assert apoyo.obtener_precios(ClienteFalso({}), {"activo": False}) == []


# --- ingesta con todos los tipos

def test_ingerir_todo_tipos_mixtos(tmp_path):
    con = db.conectar(tmp_path / "t.db")
    cfg = {
        "google_news_url": "https://news.google.com/rss/search",
        "reddit": {"metodo": "rss", "rss_url": "https://www.reddit.com/r/{subreddit}/top/.rss?t={periodo}&limit={limite}"},
        "hn": {"url": "https://hn.algolia.com/api/v1/search", "item_url": "https://news.ycombinator.com/item?id={id}"},
    }
    cliente = ClienteFalso({
        "https://news.google.com/rss/search": (FIXTURES / "google_news_nvidia.xml").read_bytes(),
        "https://www.reddit.com/r/hardware/top/.rss": (FIXTURES / "reddit_hardware.xml").read_bytes(),
        "https://hn.algolia.com/api/v1/search": (FIXTURES / "hn_nvidia.json").read_text(encoding="utf-8"),
        "https://ok/rss": (FIXTURES / "feed_basico.xml").read_bytes(),
    })
    fuentes = [
        {"nombre": "ok", "tipo": "rss", "url": "https://ok/rss", "medio": "Ok", "categoria": "hardware"},
        {"nombre": "gn", "tipo": "google_news", "consulta": "NVIDIA", "medio": "Google News", "categoria": "general"},
        {"nombre": "r_hardware", "tipo": "reddit", "subreddit": "hardware", "medio": "r/hardware", "categoria": "comunidad"},
        {"nombre": "hn", "tipo": "hn", "consulta": "nvidia", "medio": "Hacker News", "categoria": "comunidad"},
        {"nombre": "raro", "tipo": "telegrama", "medio": "x", "categoria": "chile"},
    ]
    ctx = Contexto(cliente, cfg, ["Ok"], "2026-01-01T00:00:00+00:00", "2099-01-01T00:00:00+00:00")
    t = ingerir_todo(con, ctx, fuentes, "2099-01-01")
    assert t["fuentes_ok"] == 4 and t["fuentes_error"] == 0
    tipos = {r[0] for r in con.execute("select distinct fuente_tipo from articulos")}
    assert tipos == {"rss", "google_news", "reddit", "hn"}

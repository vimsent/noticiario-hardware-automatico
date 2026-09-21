from pathlib import Path

from ingest import scrapers_chile as sc

FIXTURES = Path(__file__).parent / "fixtures"


def test_scraper_usm_noticias_fixture_real():
    html = (FIXTURES / "usm_informatica_noticias.html").read_text(encoding="utf-8")
    items = sc.scrapear_usm_noticias(html, "https://informatica.usm.cl/noticias/")
    assert len(items) >= 10
    assert all(i["url"].startswith("https://informatica.usm.cl/noticias/") for i in items)
    assert all(i["titulo"] and i["publicado_utc"] for i in items)
    assert items[0]["publicado_utc"].startswith("2026-09-16")


def test_scraper_html_cambiado_devuelve_vacio(caplog):
    fuente = {"nombre": "usm", "medio": "USM", "url": "https://x", "categoria": "chile"}
    arts = sc.articulos_desde_scraper("usm_noticias", "<html><body><p>nada</p></body></html>", fuente, [], "2026-09-20T00:00:00+00:00")
    assert arts == []
    assert any("no encontro nada" in r.message for r in caplog.records)


def test_articulos_desde_scraper_completa_campos():
    html = '<article><h3>Titulo X</h3><a href="/noticias/x/">Ver</a><time>05/09/2026</time><p>Resumen.</p></article>'
    fuente = {"nombre": "usm", "medio": "Informatica USM", "url": "https://informatica.usm.cl/noticias/", "categoria": "chile"}
    arts = sc.articulos_desde_scraper("usm_noticias", html, fuente, [], "2026-09-20T00:00:00+00:00")
    a = arts[0]
    assert a["url"] == "https://informatica.usm.cl/noticias/x"
    assert a["fuente_tipo"] == "scraper" and a["categoria_feed"] == "chile"
    assert a["publicado_utc"] == "2026-09-05T12:00:00+00:00" and a["resumen"] == "Resumen."
    assert a["titulo_norm"] == "titulo x"

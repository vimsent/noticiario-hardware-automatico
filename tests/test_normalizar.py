from rank import normalizar as nz


def test_url_canonica_quita_utm_fragmento_y_slash():
    url = "HTTPS://WWW.Phoronix.com/news/Intel-Xe3/?utm_source=rss&utm_medium=feed#comments"
    assert nz.url_canonica(url) == "https://www.phoronix.com/news/Intel-Xe3"


def test_url_canonica_conserva_query_util_y_orden():
    url = "https://example.com/a?id=5&utm_campaign=x&page=2"
    assert nz.url_canonica(url) == "https://example.com/a?id=5&page=2"


def test_url_canonica_raiz_y_puerto_por_defecto():
    assert nz.url_canonica("https://example.com:443/") == "https://example.com/"
    assert nz.url_canonica("http://example.com:8080/x/") == "http://example.com:8080/x"


def test_url_canonica_idempotente():
    url = "https://www.techpowerup.com/330000/nvidia-rtx?utm_source=rss"
    una = nz.url_canonica(url)
    assert nz.url_canonica(una) == una


def test_titulo_normalizado_quita_sufijo_medio():
    t = "Intel's Panther Lake hits 5 GHz - Tom's Hardware"
    assert nz.titulo_normalizado(t, ["Tom's Hardware"]) == "intel s panther lake hits 5 ghz"


def test_titulo_normalizado_sufijo_con_pipe_y_case():
    t = "AMD anuncia Zen 6 | VIDEOCARDZ"
    assert nz.titulo_normalizado(t, ["VideoCardz"]) == "amd anuncia zen 6"


def test_titulo_normalizado_sin_medio_conocido_no_corta():
    t = "Ryzen 9 - a review"
    assert nz.titulo_normalizado(t, ["Phoronix"]) == "ryzen 9 a review"


def test_titulo_normalizado_tildes_y_puntuacion():
    assert nz.titulo_normalizado("¡Filtración! Qualcomm compró a Alphawave, según Reuters.") == \
        "filtracion qualcomm compro a alphawave segun reuters"


def test_hash_texto_ignora_espacios_y_mayusculas():
    a = nz.hash_texto("Hola   Mundo.\nSegunda linea")
    b = nz.hash_texto("hola mundo segunda LINEA")
    assert a == b


def test_hash_texto_solo_primeros_2000():
    base = "x " * 1500
    assert nz.hash_texto(base + "cola distinta") == nz.hash_texto(base + "otra cola")


def test_hash_texto_vacio():
    assert nz.hash_texto(None) is None
    assert nz.hash_texto("   ") is None


def test_clave_grupo_estable():
    assert nz.clave_grupo("https://a.com/x") == nz.clave_grupo("https://a.com/x")
    assert len(nz.clave_grupo("https://a.com/x")) == 40

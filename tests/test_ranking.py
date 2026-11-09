import json
import re
from datetime import date
from pathlib import Path

import pytest

from ingest import db
from ingest.comun import cargar_config
from rank import exportar
from rank.agrupar import Articulo, Grupo, agrupar
from rank.etiquetar import Etiquetador, cargar_leakers
from rank.normalizar import hash_texto, titulo_normalizado
from rank.puntuar import score_prelim
from rank.ranking import construir_grupo, generar_candidatas

FIXTURES = Path(__file__).parent / "fixtures"
MEDIOS = ["Tom's Hardware", "TechPowerUp", "Phoronix", "VideoCardz", "La Tercera", "Emol"]
DESDE, HASTA = date(2026, 9, 8), date(2026, 9, 14)


@pytest.fixture(scope="module")
def cfg():
    return cargar_config()


@pytest.fixture(scope="module")
def leakers():
    return cargar_leakers(FIXTURES.parent.parent / "data" / "leakers.md")


def base_con_fixtures(tmp_path):
    con = db.conectar(tmp_path / "rank.db")
    for a in json.loads((FIXTURES / "articulos_ranking.json").read_text(encoding="utf-8")):
        a["titulo_norm"] = titulo_normalizado(a["titulo"], MEDIOS)
        a["hash_texto"] = hash_texto(a.get("texto"))
        a.setdefault("obtenido_utc", "2026-09-14T00:00:00+00:00")
        db.upsert_articulo(con, a)
    db.registrar_fuente_estado(con, "2026-09-14", "caida", False, 0, "timeout")
    con.commit()
    return con


def art(i, titulo, fecha="2026-09-10", empresas=(), **extra):
    base = dict(id=i, url=f"https://x.com/{i}", medio=f"M{i}", categoria_feed="hardware", titulo=titulo,
                titulo_norm=titulo_normalizado(titulo), publicado_utc=f"{fecha}T10:00:00+00:00",
                fecha=date.fromisoformat(fecha), empresas=list(empresas))
    base.update(extra)
    return Articulo(**base)


def test_agrupar_por_titulo_y_empresa():
    a = art(1, "Nvidia acquires Acme Photonics for $2 billion", empresas=["NVIDIA"])
    b = art(2, "NVIDIA to acquire Acme Photonics in $2B deal", empresas=["NVIDIA"])
    c = art(3, "AMD acquires Acme Photonics for $2 billion", empresas=["AMD"])
    d = art(4, "Nvidia acquires Acme Photonics for $2 billion", fecha="2026-09-20", empresas=["NVIDIA"])
    grupos = agrupar([d, c, b, a], umbral=70, ventana_dias=4)
    miembros = [[x.id for x in g.articulos] for g in grupos]
    assert miembros == [[1, 2], [3], [4]]


def test_agrupar_sindicacion_y_comunidad():
    a = art(1, "Nvidia acquires Acme", empresas=["NVIDIA"], hash_texto="h1")
    copia = art(2, "Totally different headline here", empresas=[], hash_texto="h1")
    post = art(3, "Nvidia acquires Acme", categoria_feed="comunidad", url_enlazada="https://x.com/1", score_comunidad=50)
    suelto = art(4, "Nvidia acquires Acme discussion", categoria_feed="comunidad", score_comunidad=7)
    otro = art(5, "Asus NAS review", empresas=[])
    grupos = agrupar([a, copia, post, suelto, otro], umbral=70, ventana_dias=4)
    assert [x.id for x in grupos[0].articulos] == [1, 2, 3]
    assert [x.id for x in grupos[0].adjuntos] == [4]
    assert [x.id for x in grupos[1].articulos] == [5]
    assert grupos[1].adjuntos == []


def test_etiquetador(cfg, leakers):
    et = Etiquetador(cfg["ranking"], leakers)
    t = et.texto("GeForce RTX 6090 reportedly features 512-bit bus, says kopite7kimi", "Leaker claims")
    e = et.etiquetar(t, titulo_normalizado("GeForce RTX 6090 reportedly features 512-bit bus"))
    assert e["empresas"] == ["NVIDIA"]
    assert e["categoria"] == "gpu"
    assert e["es_rumor"] == 1 and e["leakers"] == ["kopite7kimi"]
    assert e["evento_mayor"] == 0

    t2 = et.texto("Intel names new CEO after board vote", "")
    e2 = et.etiquetar(t2, t2)
    assert e2["evento_mayor"] == 1 and e2["empresas"] == ["Intel"]

    t3 = et.texto("Startup names new CEO", "")
    assert et.etiquetar(t3, t3)["evento_mayor"] == 0

    assert et.detectar_categoria(titulo_normalizado("Rustls fixes bug"), "memory safety") == "industria"
    assert et.detectar_categoria(titulo_normalizado("Rustls fixes bug"), "memory dram hbm") == "memoria"
    assert et.menciona_chile(et.texto("Data center en Chile", ""))


def test_cargar_leakers(leakers):
    assert "kopite7kimi" in leakers
    assert "9550pro" in leakers["HXL"]


def test_score_prelim():
    assert score_prelim(1, 0, False, False, False) == 3.0
    assert score_prelim(3, 99, True, True, True) == pytest.approx(3 * 2 + 2 * 2 + 4 + 1 - 1)


def test_seleccionar_y_ordenar():
    def g(clave, score, n=1, em=0, ch=0, fecha="2026-09-10"):
        return {"clave": clave, "score_prelim": score, "n_medios": n, "evento_mayor": em, "es_chile": ch, "fecha_hecho": fecha}
    grupos = [g("a", 1.0), g("b", 9.0), g("c", 2.0, em=1), g("d", 0.5, ch=1), g("e", 0.4, ch=1), g("f", 5.0, n=2),
              g("g", 5.0, n=2, fecha="2026-09-12"), g("h", 5.0, n=3)]
    sel = exportar.seleccionar(grupos, max_grupos=3, max_grupos_chile=1)
    assert [x["clave"] for x in sel] == ["b", "h", "g", "c", "d"]
    sel = exportar.seleccionar(grupos, max_grupos=2, max_grupos_chile=1)
    assert [x["clave"] for x in sel] == ["b", "h", "c", "d"]


def test_generar_candidatas_campos(tmp_path, cfg, leakers):
    con = base_con_fixtures(tmp_path)
    doc = generar_candidatas(con, cfg, DESDE, HASTA, leakers, MEDIOS, generado_utc="2026-09-14T00:00:00+00:00")
    assert doc["total_articulos"] == 10
    assert doc["fuentes_fallidas"] == [{"feed": "caida", "error": "timeout"}]
    por_titulo = {g["titulo_repr"]: g for g in doc["grupos"]}

    nv = por_titulo["Nvidia acquires Acme Photonics for $2 billion"]
    # la copia sindicada no suma medio; emol (titulo en espanol) calza por los nombres propios
    assert nv["n_medios"] == 3 and nv["medios"] == ["Emol", "TechPowerUp", "Tom's Hardware"]
    assert nv["evento_mayor"] == 1 and nv["empresas"] == ["NVIDIA"]
    assert nv["score_comunidad"] == 999
    assert nv["es_chile"] == 1 and nv["categoria"] == "industria"
    assert nv["fecha_hecho"] == "2026-09-10" and nv["rezagada"] == 0
    assert len(nv["articulos"]) == 6 and len(nv["textos"]) == 3
    assert nv["textos"][0]["url"] == "https://www.tomshardware.com/nvidia-acquires-acme"
    assert nv["articulos"][-1]["comunidad"] == 1 and nv["articulos"][-1]["score_comunidad"] == 99

    rumor = por_titulo["GeForce RTX 6090 reportedly features 512-bit bus, says kopite7kimi"]
    assert rumor["es_rumor"] == 1 and rumor["leakers"] == ["kopite7kimi"] and rumor["categoria"] == "gpu"

    chile = por_titulo["Google reactiva el data center de Cerrillos tras fallo ambiental"]
    assert chile["es_chile"] == 1 and chile["categoria"] == "datacenter"

    vieja = por_titulo["Intel Panther Lake Linux driver lands in kernel 7.3"]
    assert vieja["rezagada"] == 1

    assert "Old news outside the window" not in por_titulo
    assert doc["grupos"][0] is nv
    assert con.execute("select count(*) from grupos where run = '2026-09-14'").fetchone()[0] == doc["total_grupos"]


def test_determinismo(tmp_path, cfg, leakers):
    con = base_con_fixtures(tmp_path)
    salidas = []
    for i in range(2):
        doc = generar_candidatas(con, cfg, DESDE, HASTA, leakers, MEDIOS)
        texto = exportar.a_json(doc)
        salidas.append(re.sub(r'"generado_utc": "[^"]*"', '"generado_utc": ""', texto))
    assert salidas[0] == salidas[1]
    assert con.execute("select count(*) from grupos").fetchone()[0] == doc["total_grupos"]


def test_filtro_tema_chile(cfg, leakers):
    et = Etiquetador(cfg["ranking"], leakers)
    a = art(1, "Exseleccionado de ciclismo vende bicicletas en Vitacura", categoria_feed="chile", feed="gn_df")
    b = art(2, "Google reactiva el data center de Cerrillos", categoria_feed="chile", feed="gn_df")
    c = art(3, "Subtel anuncia licitacion 5G", categoria_feed="chile", feed="subtel")
    d = art(4, "Chile pierde con Bolivia en futbol", empresas=[])
    filtro = frozenset({"gn_df"})
    for x, esperado in ((a, 0), (b, 1), (c, 1), (d, 0)):
        g = construir_grupo(Grupo(articulos=[x]), et, cfg["ranking"], DESDE, MEDIOS, filtro)
        assert g["es_chile"] == esperado, x.titulo
    # un medio sin filtro_tema entra siempre aunque no calce ningun tema
    e = art(5, "Exseleccionado de ciclismo vende bicicletas", categoria_feed="chile", feed="ciper_sin_filtro")
    assert construir_grupo(Grupo(articulos=[e]), et, cfg["ranking"], DESDE, MEDIOS, filtro)["es_chile"] == 1


def test_agrupar_no_encadena_hechos_distintos():
    sw = frozenset({"de", "el", "en", "la", "y", "a", "the", "is", "an"})
    def mk(i, t, fecha="2026-09-10"):
        a = art(i, t, fecha=fecha, empresas=["NVIDIA"])
        a.titulo_cmp = __import__("rank.agrupar", fromlist=["sin_stopwords"]).sin_stopwords(a.titulo_norm, sw)
        return a
    a = mk(1, "Nvidia is giving away an RTX 5090")
    b = mk(2, "NVIDIA is Giving Away RTX 5090s Through an NBA 2K27 Screenshot Contest")
    c = mk(3, "NBA 2K27 screenshot contest rules and dates explained")
    d = mk(4, "Nvidia")
    grupos = agrupar([a, b, c, d], umbral=70, ventana_dias=4)
    miembros = [[x.id for x in g.articulos] for g in grupos]
    assert [1, 2] in miembros and [3] in miembros and [4] in miembros


def test_similitud_stopwords_no_juntan():
    from rank.agrupar import similitud, sin_stopwords
    sw = frozenset({"de", "el", "en", "la", "y", "a", "pone", "sus"})
    x = sin_stopwords(titulo_normalizado("Calor extremo de El Nino pone a Chile en alerta"), sw)
    y = sin_stopwords(titulo_normalizado("FMI pone sus fichas en el cobre y las reformas para que Chile vuelva a crecer"), sw)
    assert similitud(x, y) < 70
    assert similitud("nvidia", "nvidia earth 2 forecast air pollution") < 70


def test_bono_bloque_chile(cfg, leakers):
    et = Etiquetador(cfg["ranking"], leakers)
    rk = dict(cfg["ranking"], pesos={**cfg["ranking"]["pesos"], "bloque_chile": 2})
    gadget = art(1, "El iPhone 18 Pro se luce en el test de camaras", categoria_feed="chile", feed="pisapapeles")
    dc = art(2, "Google busca reactivar su data center en Cerrillos", categoria_feed="chile", feed="pisapapeles")
    g1 = construir_grupo(Grupo(articulos=[gadget]), et, rk, DESDE, MEDIOS)
    g2 = construir_grupo(Grupo(articulos=[dc]), et, rk, DESDE, MEDIOS)
    assert g1["tema_chile"] == 0 and g2["tema_chile"] == 1
    assert g2["score_prelim"] == g1["score_prelim"] + 2
    assert score_prelim(1, 0, False, False, False, {"bloque_chile": 0}, True) == 3.0


def test_tema_prioritario_marca_y_bono(cfg, leakers):
    et = Etiquetador(cfg["ranking"], leakers)
    rk = dict(cfg["ranking"], pesos={**cfg["ranking"]["pesos"], "tema_prioritario": 3})
    normal = art(1, "Nuevo mouse gamer con sensor de 30000 dpi")
    euv = art(2, "Samsung usara High-NA EUV para DRAM desde 2028")
    alternativa = art(3, "Startup demuestra litografia con laser de electrones libres")
    china = art(4, "SMEE muestra prototipo de escaner para chips avanzados")
    g = [construir_grupo(Grupo(articulos=[a]), et, rk, DESDE, MEDIOS) for a in (normal, euv, alternativa, china)]
    assert [x["tema_prioritario"] for x in g] == [0, 1, 1, 1]
    assert g[1]["score_prelim"] == g[0]["score_prelim"] + 3
    assert score_prelim(1, 0, False, False, False, {"tema_prioritario": 3}, False, True) == 6.0


def test_seleccionar_cupo_prioritarios():
    def g(clave, score, prio=0):
        return {"clave": clave, "score_prelim": score, "n_medios": 1, "evento_mayor": 0, "es_chile": 0,
                "tema_prioritario": prio, "fecha_hecho": "2026-09-10"}
    grupos = [g("a", 9.0), g("b", 8.0), g("c", 7.0), g("p1", 0.5, prio=1), g("p2", 0.4, prio=1), g("p3", 0.3, prio=1)]
    sel = exportar.seleccionar(grupos, max_grupos=2, max_grupos_chile=0, max_grupos_prioritarios=2)
    assert [x["clave"] for x in sel] == ["a", "b", "p1", "p2"]
    # sin cupo, los prioritarios de bajo puntaje quedan fuera como antes
    sel = exportar.seleccionar(grupos, max_grupos=2, max_grupos_chile=0)
    assert [x["clave"] for x in sel] == ["a", "b"]

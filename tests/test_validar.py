import json
from pathlib import Path

import pytest

from ingest.comun import cargar_config
from redaccion import validar as v

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def cfg():
    return cargar_config()["redaccion"]


def leer(nombre):
    return (FIXTURES / nombre).read_text(encoding="utf-8")


GUION_OK = """\
[INTRO]
Hola a todos, semana del 8 al 14 de septiembre.

[NOTICIA 1: NVIDIA se compra Hugging Face]
Primer parrafo con opinion.

Segundo parrafo.

[NOTICIA 2: AMD lanza el Ryzen 5 5500F]
Texto.

[NOTICIA 3: Steam Frame cuesta lo que cuesta]
Texto.

[NOTICIA 4: Intel y el socket nuevo]
Texto.

[NOTICIA 5: Linux se pone al dia]
Texto.

[CHILE: Data centers con sed]
Texto del bloque Chile.

[CIERRE]
Chao, suscribanse.

---

FUENTES

- NVIDIA compra Hugging Face, Tom's Hardware, 10 de septiembre. https://www.tomshardware.com/nvidia-hf
- Ryzen 5 5500F, TechPowerUp, 12 de septiembre. https://www.techpowerup.com/5500f?utm_source=rss
"""

PERMITIDAS = {"https://www.tomshardware.com/nvidia-hf", "https://www.techpowerup.com/5500f"}


def test_guion_minimo_ok(cfg):
    r = v.validar_guion(GUION_OK, cfg, PERMITIDAS)
    assert r.errores == []
    assert any("corto" in a for a in r.advertencias)


def test_guion_url_fuera_de_candidatas(cfg):
    r = v.validar_guion(GUION_OK, cfg, {"https://www.tomshardware.com/nvidia-hf"})
    assert len(r.errores) == 1
    assert "https://www.techpowerup.com/5500f" in r.errores[0]


def test_guion_sin_permitidas_no_cruza(cfg):
    assert v.validar_guion(GUION_OK, cfg).errores == []


def test_guion_tono_informe_palabra_prohibida(cfg):
    r = v.validar_guion(leer("guion_informe.md"), cfg)
    assert any("el presente analisis" in e for e in r.errores)
    assert any("largo" in a for a in r.advertencias)


def test_guion_con_placas_e_imagenes(cfg):
    r = v.validar_guion(leer("guion_placas.md"), cfg)
    texto = "\n".join(r.errores)
    assert "etiquetas no permitidas" in texto and "[PLACA" in texto
    assert "primera etiqueta debe ser [INTRO]" in texto
    assert "marca de edicion" in texto
    assert "FUENTES" in texto


def test_guion_bueno_real_solo_falla_por_titulares(cfg):
    r = v.validar_guion(leer("guion_bueno.md"), dict(cfg, titular_max_palabras=10))
    assert r.errores and all("titular de mas de" in e for e in r.errores)
    assert v.validar_guion(leer("guion_bueno.md"), dict(cfg, titular_max_palabras=14)).errores == []


@pytest.mark.parametrize("cambio,esperado", [
    ("[NOTICIA 2: AMD lanza el Ryzen 5 5500F]", "[NOTICIA 2: AMD lanza el Ryzen 5 5500F.]"),
    ("[NOTICIA 2: AMD lanza el Ryzen 5 5500F]", "[NOTICIA 2: **AMD lanza el Ryzen**]"),
    ("[NOTICIA 2: AMD lanza el Ryzen 5 5500F]", "[NOTICIA 2]"),
    ("[NOTICIA 3: Steam Frame cuesta lo que cuesta]", "[NOTICIA 7: Steam Frame cuesta lo que cuesta]"),
    ("[CHILE: Data centers con sed]", "[ANALISIS: Data centers con sed]"),
    ("[INTRO]", "[INTRO: hola]"),
    ("---\n\nFUENTES", "FUENTES"),
    ("Texto del bloque Chile.", "Texto del bloque Chile. Esto es revolucionario."),
    ("Texto del bloque Chile.", "Texto [MANTENER] del bloque Chile."),
])
def test_guion_errores_puntuales(cfg, cambio, esperado):
    texto = GUION_OK.replace(cambio, esperado, 1)
    assert not v.validar_guion(texto, cfg, PERMITIDAS).ok


def test_guion_cantidad_de_noticias(cfg):
    pocas = GUION_OK.replace("[NOTICIA 5: Linux se pone al dia]\nTexto.\n\n", "")
    assert any("secundarias" in e for e in v.validar_guion(pocas, cfg, PERMITIDAS).errores)
    extra = "".join(f"[NOTICIA {i}: Noticia {i}]\nTexto.\n\n" for i in range(6, 9))
    muchas = GUION_OK.replace("[CHILE:", extra + "[CHILE:")
    assert any("secundarias" in e for e in v.validar_guion(muchas, cfg, PERMITIDAS).errores)
    justo = GUION_OK.replace("[CHILE:", "[NOTICIA 6: Seis]\nTexto.\n\n[NOTICIA 7: Siete]\nTexto.\n\n[CHILE:")
    assert v.validar_guion(justo, cfg, PERMITIDAS).errores == []


def test_guion_acepta_etiquetas_decoradas(cfg):
    texto = GUION_OK.replace("[NOTICIA 2: AMD lanza el Ryzen 5 5500F]", "## **\\[NOTICIA 2: AMD lanza el Ryzen 5 5500F\\]**")
    assert v.validar_guion(texto, cfg, PERMITIDAS).errores == []


def test_urls_permitidas_canonicas():
    cand = {"grupos": [{"articulos": [{"url": "https://A.com/x/"}], "textos": [{"url": "https://b.com/y?utm_source=z"}]}]}
    barrido = [{"urls": ["https://c.com/z#frag"]}]
    assert v.urls_permitidas(cand, barrido) == {"https://a.com/x", "https://b.com/y", "https://c.com/z"}


def test_extraer_urls_limpia_puntuacion():
    assert v.extraer_urls("ver [x](https://a.com/b). y https://c.com/d, fin") == ["https://a.com/b", "https://c.com/d"]


CANDIDATAS_MD = """\
# Candidatas ep 3

| Hecho | Fecha del hecho | Cobertura | Estatus | Hilo | Clasificación | Puntaje | Decisión | Motivo |
|---|---|---|---|---|---|---|---|---|
| NVIDIA compra HF | 2026-09-10 | 3 medios | confirmado | nvidia-compras | NUEVA | 9 | NOTICIA 1 | evento mayor |
| Steam Frame | 2026-09-14 | 2 medios | confirmado | - | NUEVA | 5 | DESCARTADA | poco hardware |

Fuentes que fallaron: ninguna.
"""


def test_candidatas_md(cfg):
    cols = cfg["columnas_candidatas"]
    assert v.validar_candidatas_md(CANDIDATAS_MD, cols).ok
    sin_col = CANDIDATAS_MD.replace("| Puntaje ", "| Nota ")
    assert any("puntaje" in e for e in v.validar_candidatas_md(sin_col, cols).errores)
    assert not v.validar_candidatas_md("sin tabla", cols).ok
    sin_filas = "\n".join(CANDIDATAS_MD.splitlines()[:4])
    assert any("filas" in e for e in v.validar_candidatas_md(sin_filas, cols).errores)


HISTORIAL = """\
# Historial

## HILO: ram-cara
- Descripcion: precios de memoria
- Estado actual: sigue subiendo

## HILO: viejo
- Descripcion: algo antiguo
- Estado actual: nada nuevo

## Noticias puntuales
- ep 1: algo
"""


def test_no_encoge():
    assert v.validar_no_encoge(HISTORIAL + "\n## HILO: nuevo\n- Descripcion: x\n", HISTORIAL, "historial.md").ok
    movido = HISTORIAL.replace("## HILO: viejo\n- Descripcion: algo antiguo\n- Estado actual: nada nuevo\n\n", "") \
        + "\n## Hilos inactivos\n\n## HILO: viejo\n- Descripcion: algo antiguo\n- Estado actual: nada nuevo\n"
    assert v.validar_no_encoge(movido, HISTORIAL, "historial.md").ok
    resumido = HISTORIAL.replace("- Descripcion: algo antiguo\n- Estado actual: nada nuevo\n", "- resumen\n")
    r = v.validar_no_encoge(resumido, HISTORIAL, "historial.md")
    assert r.errores and "perdio" in r.errores[0]


def test_barrido():
    ok = json.dumps([{"hecho": "x", "fecha_hecho": "2026-09-03", "urls": ["https://a.com"], "medios": ["A"], "por_que_falto": "sin feed"}])
    r, hallazgos = v.validar_barrido(ok)
    assert r.ok and len(hallazgos) == 1
    assert v.validar_barrido("[]")[0].ok
    assert not v.validar_barrido("{no json")[0].ok
    assert not v.validar_barrido('{"hecho": "x"}')[0].ok
    malo = json.dumps([{"hecho": "x", "fecha_hecho": "3 sep", "urls": "https://a.com", "medios": [], "por_que_falto": ""}])
    r, _ = v.validar_barrido(malo)
    assert len(r.errores) == 2


def test_validar_todo(tmp_path, cfg):
    run = tmp_path / "runs" / "2026-09-14"
    (run / "antes").mkdir(parents=True)
    data = tmp_path / "data"
    data.mkdir()
    (tmp_path / "input").mkdir()
    cand = {"grupos": [{"articulos": [{"url": u}], "textos": []} for u in PERMITIDAS]}
    (run / "candidatas.json").write_text(json.dumps(cand))
    (run / "candidatas.md").write_text(CANDIDATAS_MD)
    (run / "barrido.json").write_text("[]")
    (run / "antes" / "historial.md").write_text(HISTORIAL)
    (run / "antes" / "leakers.md").write_text("# leakers\n")
    (data / "historial.md").write_text(HISTORIAL + "\n- ep 2: otra\n")
    (data / "leakers.md").write_text("# leakers\n\n### nuevo\n")
    (tmp_path / "input" / "guion.md").write_text(GUION_OK)
    rutas = v.Rutas(
        guion=tmp_path / "input" / "guion.md", candidatas_json=run / "candidatas.json",
        candidatas_md=run / "candidatas.md", barrido=run / "barrido.json",
        historial=data / "historial.md", leakers=data / "leakers.md",
        respaldo_historial=run / "antes" / "historial.md", respaldo_leakers=run / "antes" / "leakers.md",
    )
    assert v.validar_todo(rutas, cfg).errores == []

    (data / "historial.md").write_text("# Historial\n")
    (run / "barrido.json").unlink()
    r = v.validar_todo(rutas, cfg)
    assert any("historial.md" in e for e in r.errores)
    assert any("barrido.json" in e for e in r.errores)

import json
import os
import shutil
import stat
from datetime import date
from pathlib import Path

import pytest

from ingest import db
from ingest.comun import cargar_config
from redaccion import barrido, run_claude, validar
from tests.test_validar import CANDIDATAS_MD, GUION_OK, PERMITIDAS

RAIZ_REAL = Path(__file__).resolve().parents[1]


def test_ultimo_episodio():
    assert run_claude.ultimo_episodio("nada") == 0
    assert run_claude.ultimo_episodio("- Cubierto en: ep 1 (2026-09-07) como NOTICIA 1; ep 3 (2026-09-21)\nepisodio 2") == 3


def test_renderizar_prompt_exige_todos_los_valores():
    assert run_claude.renderizar_prompt("a {{X}} b {{Y}}", {"X": 1, "Y": "dos"}) == "a 1 b dos"
    with pytest.raises(run_claude.ErrorRedaccion):
        run_claude.renderizar_prompt("a {{X}} {{Z}}", {"X": 1})


def test_prompt_real_renderiza_completo():
    cfg = cargar_config()
    rutas = validar.rutas_run("2026-09-14", cfg)
    valores = run_claude.valores_prompt(cfg, rutas, {"dolar": {"valor": 940.9, "fecha": "2026-09-14", "fuente": "x"}},
                                        date(2026, 9, 8), date(2026, 9, 14), 3)
    texto = run_claude.renderizar_prompt((RAIZ_REAL / "prompts" / "redaccion.md").read_text(encoding="utf-8"), valores)
    assert "{{" not in texto
    assert "runs/2026-09-14/candidatas.json" in texto and "NVIDIA, AMD" in texto and "940.9" in texto
    assert "## REGLAS DURAS" in texto and "## FILTRACIONES" in texto


def test_ejecutar_guion_alternativo_no_toca_input(tmp_path, monkeypatch):
    """--guion permite escribir en otra ruta, para comparar sin pisar input/guion.md."""
    cfg = cargar_config()
    cfg["redaccion"]["prompt_path"] = str(RAIZ_REAL / "prompts" / "redaccion.md")  # absoluta: sobrevive el RAIZ falso
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs" / "2026-09-14").mkdir(parents=True)
    (tmp_path / "runs" / "2026-09-14" / "candidatas.json").write_text("{}", encoding="utf-8")
    (tmp_path / "runs" / "2026-09-14" / "apoyo.json").write_text('{"dolar": {}}', encoding="utf-8")
    monkeypatch.setattr(run_claude, "RAIZ", tmp_path)

    alterno = "comparaciones/2026-09-14/manual/guion.md"
    resultado = run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), 3, solo_prompt=True, guion=alterno)
    assert resultado.ok  # solo_prompt: no valida nada, solo confirma que no revento
    assert not (tmp_path / "input" / "guion.md").exists()
    prompt = (tmp_path / "runs" / "2026-09-14" / "prompt.md").read_text(encoding="utf-8")
    assert alterno in prompt


def test_barrido_procesar(tmp_path):
    con = db.conectar(tmp_path / "t.db")
    hallazgos = [
        {"hecho": "Intel despide a 5000", "fecha_hecho": "2026-09-03", "urls": ["https://Reuters.com/a/", "https://www.bloomberg.com/b"],
         "medios": ["Reuters"], "por_que_falto": "medio de negocios sin feed"},
    ]
    acum = tmp_path / "runs" / "barrido_acumulado.md"
    assert barrido.procesar(con, "2026-09-14", hallazgos, acum) == 2
    filas = con.execute("select url, medio, fuente_tipo, titulo, publicado_utc from articulos order by url").fetchall()
    assert [f["url"] for f in filas] == ["https://reuters.com/a", "https://www.bloomberg.com/b"]
    assert [f["medio"] for f in filas] == ["Reuters", "Reuters"]
    assert filas[0]["fuente_tipo"] == "barrido" and filas[0]["publicado_utc"] == "2026-09-03T00:00:00+00:00"
    assert barrido.procesar(con, "2026-09-21", hallazgos, acum) == 0
    lineas = acum.read_text().splitlines()
    assert lineas[0].startswith("# ") and sum(l.startswith("| 2026-09-") for l in lineas) == 2
    assert "medio de negocios sin feed" in lineas[-1]


# --- flujo completo con un claude falso

FALSO = '''#!/usr/bin/env python3
import sys, json
from pathlib import Path
raiz = Path({raiz!r})
prompt = sys.stdin.read()
run = raiz / "runs" / "2026-09-14"
contador = run / "intentos.txt"
n = int(contador.read_text()) + 1 if contador.exists() else 1
contador.write_text(str(n))
modo = {modo!r}
guion = Path({guion!r}).read_text()
if modo == "arregla_al_segundo" and n == 1:
    guion = guion.replace("https://www.techpowerup.com/5500f?utm_source=rss", "https://inventada.com/x")
if modo == "siempre_malo":
    guion = guion.replace("[INTRO]", "[PLACA: hola]")
(raiz / "input" / "guion.md").write_text(guion)
(run / "candidatas.md").write_text({candidatas_md!r})
(run / "barrido.json").write_text(json.dumps([{{"hecho": "algo", "fecha_hecho": "2026-09-03", "urls": ["https://reuters.com/x"], "medios": ["Reuters"], "por_que_falto": "sin feed"}}]))
h = raiz / "data" / "historial.md"
h.write_text(h.read_text() + "\\n## HILO: nuevo\\n- Cubierto en: ep 1 (2026-09-14)\\n")
if modo == "borra_historial":
    h.write_text("# nada\\n")
l = raiz / "data" / "leakers.md"
l.write_text(l.read_text() + "\\n### otro\\n- Nivel: C\\n")
print(json.dumps({{"result": "", "is_error": False}}))
'''


def preparar(tmp_path, monkeypatch, modo):
    raiz = tmp_path / "repo"
    (raiz / "runs" / "2026-09-14").mkdir(parents=True)
    (raiz / "data").mkdir()
    (raiz / "input").mkdir()
    (raiz / "prompts").mkdir()
    shutil.copy(RAIZ_REAL / "prompts" / "redaccion.md", raiz / "prompts" / "redaccion.md")
    cand = {"grupos": [{"articulos": [{"url": u}], "textos": []} for u in PERMITIDAS]}
    (raiz / "runs" / "2026-09-14" / "candidatas.json").write_text(json.dumps(cand))
    (raiz / "runs" / "2026-09-14" / "apoyo.json").write_text(json.dumps({"dolar": {"valor": 940.9, "fecha": "2026-09-14", "fuente": "x"}}))
    guion_ok = tmp_path / "guion_ok.md"
    guion_ok.write_text(GUION_OK)
    falso = tmp_path / "claude_falso.py"
    falso.write_text(FALSO.format(raiz=str(raiz), modo=modo, guion=str(guion_ok), candidatas_md=CANDIDATAS_MD))
    falso.chmod(falso.stat().st_mode | stat.S_IEXEC)

    cfg = cargar_config()
    cfg["redaccion"]["claude_bin"] = str(falso)
    cfg["redaccion"]["claude_args"] = []
    cfg["ingesta"]["db_path"] = "data/noticias.db"
    monkeypatch.setattr(run_claude, "RAIZ", raiz)
    monkeypatch.setattr(validar, "RAIZ", raiz)
    return raiz, cfg


def test_flujo_ok_al_primer_intento(tmp_path, monkeypatch):
    raiz, cfg = preparar(tmp_path, monkeypatch, "bueno")
    r = run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), None)
    assert r.ok
    run = raiz / "runs" / "2026-09-14"
    assert run.joinpath("intentos.txt").read_text() == "1"
    assert (run / "antes" / "historial.md").exists() and (run / "redaccion.log").exists()
    assert "Sin episodios anteriores" in (raiz / "data" / "historial.md").read_text()
    assert "HILO: nuevo" in (raiz / "data" / "historial.md").read_text()
    assert (raiz / "runs" / "barrido_acumulado.md").exists()
    con = db.conectar(raiz / "data" / "noticias.db")
    assert con.execute("select count(*) from articulos where fuente_tipo = 'barrido'").fetchone()[0] == 1
    assert "EPISODIO: 1" in (run / "prompt.md").read_text()


def test_flujo_reintento_corrige(tmp_path, monkeypatch):
    raiz, cfg = preparar(tmp_path, monkeypatch, "arregla_al_segundo")
    r = run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), 5)
    assert r.ok
    assert (raiz / "runs" / "2026-09-14" / "intentos.txt").read_text() == "2"
    log = (raiz / "runs" / "2026-09-14" / "redaccion.log").read_text()
    assert "intento 1" in log and "intento 2" in log


def test_flujo_falla_dos_veces_y_restaura(tmp_path, monkeypatch):
    raiz, cfg = preparar(tmp_path, monkeypatch, "siempre_malo")
    r = run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), None)
    assert not r.ok
    assert (raiz / "runs" / "2026-09-14" / "intentos.txt").read_text() == "2"
    assert "HILO: nuevo" not in (raiz / "data" / "historial.md").read_text()
    assert "### otro" not in (raiz / "data" / "leakers.md").read_text()
    assert not (raiz / "runs" / "barrido_acumulado.md").exists()


def test_flujo_detecta_historial_borrado(tmp_path, monkeypatch):
    raiz, cfg = preparar(tmp_path, monkeypatch, "borra_historial")
    r = run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), None)
    assert not r.ok and any("historial.md" in e for e in r.errores)
    assert "Sin episodios anteriores" in (raiz / "data" / "historial.md").read_text()


def test_faltan_entradas(tmp_path, monkeypatch):
    raiz, cfg = preparar(tmp_path, monkeypatch, "bueno")
    (raiz / "runs" / "2026-09-14" / "apoyo.json").unlink()
    with pytest.raises(run_claude.ErrorRedaccion):
        run_claude.ejecutar(cfg, date(2026, 9, 8), date(2026, 9, 14), None)

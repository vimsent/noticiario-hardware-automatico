import json
import subprocess
import sys
from pathlib import Path

import pytest

import start
from tests.test_validar import GUION_OK


def test_parsear_etapas_ordena_y_dedupe():
    assert start.parsear_etapas("5,1,3,1") == [1, 3, 5]
    assert start.parsear_etapas(" 2 , 4 ") == [2, 4]


def test_parsear_etapas_invalido():
    with pytest.raises(SystemExit, match="1-5"):
        start.parsear_etapas("1,9")
    with pytest.raises(SystemExit, match="invalido"):
        start.parsear_etapas("abc")


def test_requerir(tmp_path):
    existe = tmp_path / "x.txt"
    existe.write_text("hola", encoding="utf-8")
    start.requerir(existe, "prueba")  # no lanza
    with pytest.raises(start.ErrorEtapa, match="no_existe.md"):
        start.requerir(tmp_path / "no_existe.md", "corre la etapa 1 primero")


def test_ejecutar_etapa_ok_y_tee(tmp_path):
    log_path = tmp_path / "start.log"
    cmd = [sys.executable, "-c", "print('linea de prueba')"]
    codigo = start.ejecutar_etapa("1 (prueba)", cmd, log_path)
    assert codigo == 0
    contenido = log_path.read_text(encoding="utf-8")
    assert "etapa 1 (prueba)" in contenido
    assert "linea de prueba" in contenido
    assert "[codigo de salida 0]" in contenido


def test_ejecutar_etapa_propaga_codigo_de_error(tmp_path):
    log_path = tmp_path / "start.log"
    cmd = [sys.executable, "-c", "import sys; sys.exit(3)"]
    codigo = start.ejecutar_etapa("2 (prueba)", cmd, log_path)
    assert codigo == 3
    assert "[codigo de salida 3]" in log_path.read_text(encoding="utf-8")


def test_resumen_episodio(tmp_path, monkeypatch):
    (tmp_path / "input").mkdir()
    (tmp_path / "input" / "guion.md").write_text(GUION_OK, encoding="utf-8")
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    (run_dir / "candidatas.json").write_text(
        json.dumps({"grupos_exportados": 12, "total_grupos": 340}), encoding="utf-8")
    (run_dir / "barrido.json").write_text(
        json.dumps([{"hecho": "x", "fecha_hecho": "2026-09-10", "urls": ["https://a.cl"],
                    "medios": ["A"], "por_que_falto": "sin feed"}]), encoding="utf-8")

    monkeypatch.setattr(start, "RAIZ", tmp_path)
    r = start.resumen_episodio(run_dir)

    tags = r["titulares"]
    assert tags[0] == "INTRO" and tags[-1] == "CIERRE"
    assert any(t.startswith("NOTICIA 1:") for t in tags)
    assert r["n_candidatas"] == 12 and r["n_grupos"] == 340
    assert r["n_barrido"] == 1


def test_resumen_episodio_sin_archivos(tmp_path, monkeypatch):
    monkeypatch.setattr(start, "RAIZ", tmp_path)
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    r = start.resumen_episodio(run_dir)
    assert r["titulares"] == [] and r["n_candidatas"] is None and r["n_barrido"] == 0


def test_etapa_revision_sin_revision_no_pregunta(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(start, "RAIZ", tmp_path)
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    assert start.etapa_revision(run_dir, sin_revision=True) is True
    assert "Barrido de seguridad" in capsys.readouterr().out


def test_etapa_revision_q_aborta(tmp_path, monkeypatch):
    monkeypatch.setattr(start, "RAIZ", tmp_path)
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert start.etapa_revision(run_dir, sin_revision=False) is False


def test_etapa_revision_enter_continua(tmp_path, monkeypatch):
    monkeypatch.setattr(start, "RAIZ", tmp_path)
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert start.etapa_revision(run_dir, sin_revision=False) is True


def test_hacer_commit_sin_repo_git(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(start, "RAIZ", tmp_path)
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    (run_dir / "candidatas.md").write_text("x", encoding="utf-8")
    with caplog.at_level("ERROR"):
        start.hacer_commit(run_dir, 3, __import__("datetime").date(2026, 9, 8), __import__("datetime").date(2026, 9, 14))
    assert any("no es un repositorio git" in r.message for r in caplog.records)


def test_hacer_commit_con_repo_git(tmp_path, monkeypatch):
    from datetime import date

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.cl"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "historial.md").write_text("h", encoding="utf-8")
    (tmp_path / "data" / "leakers.md").write_text("l", encoding="utf-8")
    run_dir = tmp_path / "runs" / "2026-09-14"
    run_dir.mkdir(parents=True)
    (run_dir / "candidatas.md").write_text("c", encoding="utf-8")

    monkeypatch.setattr(start, "RAIZ", tmp_path)
    start.hacer_commit(run_dir, 3, date(2026, 9, 8), date(2026, 9, 14))

    log = subprocess.run(["git", "log", "--oneline", "-1"], cwd=tmp_path, capture_output=True, text=True, check=True)
    assert "episodio 3 (2026-09-08 a 2026-09-14)" in log.stdout

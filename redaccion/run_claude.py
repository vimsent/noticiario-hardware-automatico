"""Etapa 3: invoca claude code en modo no interactivo y valida sus salidas. Uso:

    python -m redaccion.run_claude --desde 2026-09-08 --hasta 2026-09-14 [--episodio N] [--solo-prompt]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from ingest import db  # noqa: E402
from ingest.comun import cargar_config  # noqa: E402
from redaccion import barrido, validar  # noqa: E402

log = logging.getLogger("redaccion")

PLANTILLA_HISTORIAL = """# Historial del noticiario

Sin episodios anteriores: este es el primero.

## Noticias puntuales

## Hilos inactivos
"""

PLANTILLA_LEAKERS = """# Registro de leakers

Punto de partida editorial. Lo corrige el modelo semana a semana; nunca se borran rumores.

## REGISTRO DE LEAKERS

### kopite7kimi
- Nivel: A
- Base del nivel: punto de partida editorial (NVIDIA)
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Kepler_L2
- Nivel: A
- Base del nivel: punto de partida editorial (AMD)
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Jaykihn
- Nivel: A
- Base del nivel: punto de partida editorial (Intel)
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### HXL
- Alias: 9550pro, @9550pro
- Nivel: B
- Base del nivel: punto de partida editorial
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### momomo_us
- Nivel: B
- Base del nivel: punto de partida editorial
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Moore's Law Is Dead
- Alias: MLID
- Nivel: C
- Base del nivel: punto de partida editorial
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0

### RedGamingTech
- Nivel: C
- Base del nivel: punto de partida editorial
- Rumores registrados:
- Balance: cumplidos 0, fallidos 0, pendientes 0
"""

TEXTO_BARRIDO_CHILE = (
    " Además, como parte del barrido de seguridad, ejecuta una búsqueda con WebSearch por cada uno de estos temas, "
    "acotada a la ventana: data centers en Chile (inversión, agua, energía, permisos); Subtel, fibra, cables submarinos "
    "y satelital; Ley 21.719 de datos personales y Ley 21.663 con la ANCI; convocatorias de ANID, Corfo y Startup Chile; "
    "ALMA, Vera Rubin, ELT y NLHPC; noticias de la USM y su Departamento de Informática. Lo que no esté en "
    "`candidatas.json` va a `barrido.json` con el mismo esquema, y si lo usas en el guion se marca `BARRIDO` en "
    "`candidatas.md`."
)
TEXTO_SIN_BARRIDO_CHILE = " No busques más noticias chilenas por fuera."

EPISODIO_RE = re.compile(r"\bep(?:isodio)?\.?\s*(\d+)\b", re.IGNORECASE)


class ErrorRedaccion(Exception):
    pass


def ultimo_episodio(historial: str) -> int:
    numeros = [int(n) for n in EPISODIO_RE.findall(historial)]
    return max(numeros) if numeros else 0


def asegurar_plantillas(historial: Path, leakers: Path) -> None:
    for ruta, plantilla in ((historial, PLANTILLA_HISTORIAL), (leakers, PLANTILLA_LEAKERS)):
        if not ruta.exists():
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text(plantilla, encoding="utf-8")
            log.info("creado %s con la plantilla vacia (primer episodio)", ruta)


def respaldar(historial: Path, leakers: Path, destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    shutil.copy2(historial, destino / historial.name)
    shutil.copy2(leakers, destino / leakers.name)


def restaurar(historial: Path, leakers: Path, origen: Path) -> None:
    shutil.copy2(origen / historial.name, historial)
    shutil.copy2(origen / leakers.name, leakers)


def _rel(ruta: Path) -> str:
    try:
        return ruta.relative_to(RAIZ).as_posix()
    except ValueError:
        return ruta.as_posix()


def renderizar_prompt(plantilla: str, valores: dict[str, Any]) -> str:
    texto = plantilla
    for clave, valor in valores.items():
        texto = texto.replace("{{" + clave + "}}", str(valor))
    sobrantes = sorted(set(re.findall(r"\{\{(\w+)\}\}", texto)))
    if sobrantes:
        raise ErrorRedaccion(f"placeholders sin valor en el prompt: {sobrantes}")
    return texto


def valores_prompt(cfg: dict[str, Any], rutas: validar.Rutas, apoyo: dict[str, Any], desde: date, hasta: date,
                   episodio: int) -> dict[str, Any]:
    red = cfg["redaccion"]
    dolar = apoyo.get("dolar") or {}
    return {
        "FECHA_INICIO": desde.isoformat(),
        "FECHA_FIN": hasta.isoformat(),
        "EPISODIO": episodio,
        "PALABRAS_MIN": red.get("palabras_min", 1800),
        "PALABRAS_MAX": red.get("palabras_max", 3000),
        "TITULAR_MAX": red.get("titular_max_palabras", 10),
        "DOLAR_VALOR": dolar.get("valor", "no disponible"),
        "DOLAR_FECHA": dolar.get("fecha", "sin fecha"),
        "DOLAR_FUENTE": dolar.get("fuente", "sin fuente"),
        "EMPRESAS": ", ".join(cfg["ranking"].get("empresas") or {}),
        "BARRIDO_CHILE": TEXTO_BARRIDO_CHILE if red.get("barrido_chile") else TEXTO_SIN_BARRIDO_CHILE,
        "RUTA_CANDIDATAS": _rel(rutas.candidatas_json),
        "RUTA_CANDIDATAS_MD": _rel(rutas.candidatas_md),
        "RUTA_GUION": _rel(rutas.guion),
        "RUTA_HISTORIAL": _rel(rutas.historial),
        "RUTA_LEAKERS": _rel(rutas.leakers),
        "RUTA_BARRIDO": _rel(rutas.barrido),
    }


def prompt_reintento(prompt: str, errores: list[str]) -> str:
    lista = "\n".join(f"- {e}" for e in errores)
    return (prompt + "\n\n---\n\n## CORRECCIÓN\n\n"
            "Los cinco archivos de salida ya existen de un intento anterior, pero la validación falló con estos errores:\n\n"
            f"{lista}\n\n"
            "Corrige los archivos existentes con Edit para resolver exactamente esos errores. No reescribas todo desde cero, "
            "no cambies lo que ya estaba bien, y no agregues URLs que no estén en candidatas.json o barrido.json. "
            "Termina sin escribir ningún texto de respuesta.\n")


def _resumen_evento(evento: dict[str, Any]) -> str | None:
    """Una linea corta por evento de stream-json, para la consola."""
    tipo = evento.get("type")
    if tipo == "assistant":
        partes = []
        for bloque in evento.get("message", {}).get("content") or []:
            if bloque.get("type") == "tool_use":
                entrada = bloque.get("input") or {}
                detalle = entrada.get("file_path") or entrada.get("query") or entrada.get("url") or entrada.get("pattern") or ""
                partes.append(f"{bloque.get('name')} {detalle}".strip())
            elif bloque.get("type") == "text" and bloque.get("text", "").strip():
                partes.append("texto: " + " ".join(bloque["text"].split())[:100])
        return "; ".join(partes) or None
    if tipo == "result":
        return (f"fin: {evento.get('subtype')} | turnos {evento.get('num_turns')} | "
                f"costo usd {evento.get('total_cost_usd', 0):.2f} | error {evento.get('is_error')}")
    if tipo == "system" and evento.get("subtype") == "init":
        return f"sesion iniciada, modelo {evento.get('model')}, herramientas {evento.get('tools')}"
    return None


def invocar_claude(prompt: str, cfg_red: dict[str, Any], log_path: Path, intento: int) -> int:
    """Corre claude -p con el prompt por stdin, escribiendo el log en vivo. Devuelve el codigo de salida
    (124 si hubo timeout, 127 si no se encontro el binario)."""
    comando = [cfg_red.get("claude_bin", "claude"), *(cfg_red.get("claude_args") or [])]
    timeout = float(cfg_red.get("timeout_min", 30)) * 60
    log.info("intento %d: %s (timeout %.0f min); log en vivo: tail -f %s", intento, " ".join(comando), timeout / 60, log_path)
    inicio = time.monotonic()
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"\n===== intento {intento}: {' '.join(comando)}\n")
        f.flush()
        try:
            proc = subprocess.Popen(comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    cwd=RAIZ, text=True, bufsize=1)
        except FileNotFoundError as e:
            f.write(f"\n[no se pudo ejecutar: {e}]\n")
            return 127
        assert proc.stdin is not None and proc.stdout is not None
        try:
            proc.stdin.write(prompt)
            proc.stdin.close()
            for linea in proc.stdout:
                f.write(linea)
                f.flush()
                try:
                    resumen = _resumen_evento(json.loads(linea))
                except (json.JSONDecodeError, TypeError):
                    resumen = None
                if resumen:
                    log.info("[%dm%02ds] %s", *divmod(int(time.monotonic() - inicio), 60), resumen)
                if time.monotonic() - inicio > timeout:
                    proc.kill()
                    f.write(f"\n[timeout tras {timeout / 60:.0f} min]\n")
                    return 124
            codigo = proc.wait()
        except KeyboardInterrupt:
            proc.kill()
            proc.wait()
            f.write("\n[interrumpido por el usuario]\n")
            raise
        f.write(f"\n[codigo de salida {codigo}]\n")
    return codigo


def ejecutar(cfg: dict[str, Any], desde: date, hasta: date, episodio: int | None, solo_prompt: bool = False) -> validar.Resultado:
    red = cfg["redaccion"]
    run = hasta.isoformat()
    run_dir = RAIZ / cfg["ranking"].get("salida_dir", "runs") / run
    rutas = validar.rutas_run(run, cfg)
    prompt_path = RAIZ / red.get("prompt_path", "prompts/redaccion.md")
    apoyo_path = run_dir / "apoyo.json"

    for ruta in (rutas.candidatas_json, apoyo_path, prompt_path):
        if not ruta.exists():
            raise ErrorRedaccion(f"falta {ruta}; corre las etapas 1 y 2 primero")
    asegurar_plantillas(rutas.historial, rutas.leakers)
    if episodio is None:
        episodio = ultimo_episodio(rutas.historial.read_text(encoding="utf-8")) + 1

    apoyo = json.loads(apoyo_path.read_text(encoding="utf-8"))
    prompt = renderizar_prompt(prompt_path.read_text(encoding="utf-8"),
                               valores_prompt(cfg, rutas, apoyo, desde, hasta, episodio))
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    if solo_prompt:
        log.info("prompt renderizado en %s", run_dir / "prompt.md")
        return validar.Resultado()

    antes = run_dir / "antes"
    respaldar(rutas.historial, rutas.leakers, antes)
    rutas.respaldo_historial, rutas.respaldo_leakers = antes / "historial.md", antes / "leakers.md"
    log_path = run_dir / "redaccion.log"

    resultado = validar.Resultado()
    for intento in (1, 2):
        texto = prompt if intento == 1 else prompt_reintento(prompt, resultado.errores)
        try:
            codigo = invocar_claude(texto, red, log_path, intento)
        except KeyboardInterrupt:
            restaurar(rutas.historial, rutas.leakers, antes)
            log.error("interrumpido; historial.md y leakers.md restaurados desde %s", antes)
            raise
        if codigo != 0:
            log.error("claude termino con codigo %d (ver %s)", codigo, log_path)
        resultado = validar.validar_todo(rutas, red)
        for a in resultado.advertencias:
            log.warning("aviso: %s", a)
        if resultado.ok:
            break
        log.error("validacion fallida en el intento %d:\n%s", intento, "\n".join(f"  - {e}" for e in resultado.errores))

    if not resultado.ok:
        restaurar(rutas.historial, rutas.leakers, antes)
        log.error("se restauraron historial.md y leakers.md desde %s", antes)
        return resultado

    _, hallazgos = validar.validar_barrido(rutas.barrido.read_text(encoding="utf-8"))
    con = db.conectar(RAIZ / cfg["ingesta"].get("db_path", "data/noticias.db"))
    nuevos = barrido.procesar(con, run, hallazgos, RAIZ / cfg["ranking"].get("salida_dir", "runs") / "barrido_acumulado.md")
    con.close()
    log.info("episodio %d listo: %d hallazgos del barrido, %d urls nuevas en la base", episodio, len(hallazgos), nuevos)
    return resultado


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="etapa 3: redaccion con claude code")
    ap.add_argument("--desde", type=date.fromisoformat, required=True)
    ap.add_argument("--hasta", type=date.fromisoformat, required=True)
    ap.add_argument("--episodio", type=int)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--solo-prompt", action="store_true", help="renderiza el prompt y termina, sin invocar claude")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        resultado = ejecutar(cargar_config(args.config), args.desde, args.hasta, args.episodio, args.solo_prompt)
    except ErrorRedaccion as e:
        log.error("%s", e)
        return 2
    except KeyboardInterrupt:
        return 130
    return 0 if resultado.ok else 1


if __name__ == "__main__":
    sys.exit(main())

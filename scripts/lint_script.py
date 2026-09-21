"""
Revisa el guion y los bloques parseados ANTES de gastar minutos en voz y render.
Corre en un par de segundos. Los errores abortan el pipeline; los avisos solo se
imprimen.

Revisa:
  - etiquetas mal formadas (**[INTRO]**, `# [NOTICIA 1]`, corchete sin cerrar,
    texto en la misma línea de la etiqueta), etiquetas desconocidas (typos),
    numeración de NOTICIA con saltos, falta de [INTRO]/[CIERRE].
  - que no hayan quedado URLs, markdown ni marcas [..] en el texto que va al TTS.
  - que el corte de FUENTES exista y se haya llevado un porcentaje razonable.
  - que ningún bloque sea absurdamente largo o corto, y que el total de palabras
    esté en el rango de un episodio.

Uso:
    python lint_script.py input/guion.md output/bloques.json config.yaml
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import parse_script as ps  # noqa: E402

KNOWN_KINDS = {"INTRO", "CIERRE", "CHILE", "ANALISIS", "OPINION", "PLACA", "IMAGEN",
               "DIAGRAMA", "GRAFICO", "MANTENER", "PAUSA"}
KNOWN_PREFIXES = ("NOTICIA ", "SEGMENTO ")

DECORATED_TAG_RE = re.compile(r"^\s*(?:[*_#>`]+\s*)+\[[^\]\n]+\]|^\s*\[[^\]\n]+\]\s*[*_`]+\s*$", re.MULTILINE)
UNCLOSED_TAG_RE = re.compile(r"^\s*\[[^\]\n]{0,80}$", re.MULTILINE)
TAG_WITH_TEXT_RE = re.compile(r"^\s*\[(INTRO|NOTICIA \d+|CHILE|CIERRE|PLACA|IMAGEN|DIAGRAMA|GR[ÁA]FICO)(?::[^\]\n]*)?\][ \t]*\S", re.IGNORECASE | re.MULTILINE)
LEFTOVER_MARK_RE = re.compile(r"\[[^\]\n]{1,60}\]")
MD_RE = re.compile(r"\*\*|^#{1,6}\s|^\s*[-*•]\s", re.MULTILINE)
CHATTY_RE = re.compile(r"^\s*(aquí tienes|aquí está|claro|por supuesto|here is|here's)", re.IGNORECASE)

MIN_TOTAL_WORDS, MAX_TOTAL_WORDS = 600, 5000
MIN_SOURCES_PCT, MAX_SOURCES_PCT = 2.0, 40.0


def lint(raw_text: str, blocks: list[dict], max_block_words: int) -> tuple[list[str], list[str]]:
    errors, warnings = [], []

    # --- texto crudo: etiquetas ---
    raw_text, n_norm = ps.normalize_markdown(raw_text)
    if n_norm:
        warnings.append(f"{n_norm} etiqueta(s) venían con markdown encima (## **\\[..\\]**); se normalizaron")
    for m in DECORATED_TAG_RE.finditer(raw_text):
        errors.append(f"etiqueta con formato encima (no se detecta): {m.group(0).strip()!r}")
    for m in TAG_WITH_TEXT_RE.finditer(raw_text):
        errors.append(f"texto en la misma línea que la etiqueta (la etiqueta debe ir sola): {m.group(0).strip()[:70]!r}")
    for m in UNCLOSED_TAG_RE.finditer(raw_text):
        line = m.group(0).strip()
        if line.upper().startswith(("[INTRO", "[NOTICIA", "[CHILE", "[CIERRE", "[PLACA", "[IMAGEN", "[DIAGRAMA", "[GR")):
            errors.append(f"corchete sin cerrar: {line[:70]!r}")

    script_text, sources_text = ps.split_sources(raw_text)
    tts_text = ps.select_tts_version(script_text) if ps.TTS_HEADER_RE.search(script_text) else script_text
    kinds = []
    for m in ps.TAG_RE.finditer(tts_text):
        kind, _ = ps.split_tag(m.group(1))
        kinds.append(ps.normalize_kind(kind))
    for k in kinds:
        if k not in KNOWN_KINDS and not k.startswith(KNOWN_PREFIXES):
            warnings.append(f"etiqueta desconocida [{k}] (¿typo?): se trata como tarjeta normal")
    news = [int(k.split()[1]) for k in kinds if k.startswith("NOTICIA ") and k.split()[1].isdigit()]
    if news and news != list(range(1, len(news) + 1)):
        warnings.append(f"numeración de NOTICIA con saltos o repetida: {news}")
    if kinds and "INTRO" not in kinds and "PLACA" not in kinds:
        warnings.append("no hay [INTRO] (ni [PLACA]): el primer bloque no tendrá titular")
    if kinds and "INTRO" in kinds and "CIERRE" not in kinds:
        warnings.append("hay [INTRO] pero no [CIERRE]")
    if not kinds:
        warnings.append("guion sin etiquetas: se usa el modo de segmentos automáticos")

    # --- fuentes ---
    total_raw = len(raw_text.split())
    if not sources_text:
        warnings.append("no se encontró la línea FUENTES: no se cortó nada (¿el guion viene sin fuentes?)")
    else:
        pct = 100.0 * len(sources_text.split()) / max(1, total_raw)
        if pct > MAX_SOURCES_PCT:
            errors.append(f"el corte de FUENTES se llevó el {pct:.0f}% del archivo: "
                          "probablemente hay una línea FUENTES en medio del guion")
        elif pct < MIN_SOURCES_PCT:
            warnings.append(f"la sección FUENTES es muy corta ({pct:.1f}% del archivo)")

    # --- bloques ---
    if len(blocks) < 2:
        errors.append(f"solo {len(blocks)} bloque(s): el guion no se segmentó bien")
    total = sum(b["word_count"] for b in blocks)
    if total < MIN_TOTAL_WORDS:
        warnings.append(f"episodio muy corto: {total} palabras (~{total/150:.0f} min)")
    elif total > MAX_TOTAL_WORDS:
        warnings.append(f"episodio muy largo: {total} palabras (~{total/150:.0f} min)")
    for b in blocks:
        tag = f"[{b['index']:02d}] {b['slug']}"
        text = b["text"]
        if ps.URL_RE.search(text):
            errors.append(f"{tag}: quedó una URL en el texto a narrar")
        if MD_RE.search(text):
            errors.append(f"{tag}: quedó markdown (**, #, viñetas) en el texto a narrar")
        for m in LEFTOVER_MARK_RE.finditer(text):
            errors.append(f"{tag}: quedó una marca entre corchetes en el texto: {m.group(0)!r}")
        if b["word_count"] > max_block_words * 1.5:
            errors.append(f"{tag}: bloque de {b['word_count']} palabras (máximo {max_block_words})")
        if b["word_count"] < 8:
            warnings.append(f"{tag}: bloque muy corto ({b['word_count']} palabras): {text[:50]!r}")
    if blocks and CHATTY_RE.search(blocks[0]["text"]):
        warnings.append(f"el primer bloque parece un saludo del modelo, no narración: {blocks[0]['text'][:60]!r}")

    return errors, warnings


def main():
    if len(sys.argv) not in (3, 4):
        print("Uso: python lint_script.py <guion.md> <bloques.json> [config.yaml]")
        sys.exit(2)
    raw_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    blocks = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    _, max_block_words, _ = ps._load_parsing_cfg(sys.argv[3] if len(sys.argv) == 4 else None)

    errors, warnings = lint(raw_text, blocks, max_block_words)
    for w in warnings:
        print(f"[lint] aviso: {w}")
    for e in errors:
        print(f"[lint] ERROR: {e}")
    total = sum(b["word_count"] for b in blocks)
    if errors:
        print(f"[lint] {len(errors)} error(es). Corrige el guion antes de generar la voz "
              "(o corre main.py con --no-lint si estás seguro).")
        sys.exit(1)
    print(f"[lint] OK: {len(blocks)} bloques, {total} palabras (~{total/150:.0f} min), "
          f"{len(warnings)} aviso(s)")


if __name__ == "__main__":
    main()

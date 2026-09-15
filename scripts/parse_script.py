"""
Parsea un guion de texto en una lista de bloques estructurados, para que
generate_audio.py y generate_visuals.py generen un audio + una imagen por bloque.

Soporta DOS formatos de guion:

1) Con etiquetas explícitas tipo [INTRO], [NOTICIA 1], [ANÁLISIS]:

    [INTRO]
    texto del bloque...

    [NOTICIA 1: TITULO LARGO]
    más texto...

2) Monólogo corrido SIN ningún marcador (el estilo "cero markdown, cero
   encabezados" de guiones más naturales/hablados). En ese caso no hay forma
   de saber dónde "debería" cortar semánticamente, así que el script agrupa
   párrafos consecutivos hasta juntar ~AUTO_SEGMENT_TARGET_WORDS palabras y
   arma bloques genéricos ("SEGMENTO 1", "SEGMENTO 2", ...). Esto es solo
   para tener puntos de corte razonables donde cambiar de imagen y generar
   el audio en piezas manejables; no representa una estructura editorial.

Uso:
    python parse_script.py input/guion.md output/bloques.json [config.yaml]

Si se pasa config.yaml y tiene la clave parsing.auto_segment_target_words,
se usa ese valor en vez del default (130 palabras) para el modo sin etiquetas.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

TAG_RE = re.compile(r"^\[([^\]]+)\]\s*$", re.MULTILINE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¡¿])")

# Dónde termina el guion y empieza la lista de fuentes (que NO se narra):
# una línea de solo guiones, o una línea que diga FUENTES / REFERENCIAS.
SOURCES_SPLIT_RE = re.compile(
    r"^\s*(?:-{3,}|_{3,}|\*{3,}|#*\s*(?:FUENTES|REFERENCIAS|BIBLIOGRAF[ÍI]A)\b.*)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MD_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
MD_BULLET_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+", re.MULTILINE)

DEFAULT_AUTO_SEGMENT_TARGET_WORDS = 130
DEFAULT_MAX_BLOCK_WORDS = 220


def split_sources(text: str) -> tuple[str, str]:
    """Separa el guion de la sección de fuentes/referencias del final.

    Devuelve (guion, fuentes). Si no hay separador, fuentes es "".
    Solo se considera un separador que esté en la segunda mitad del texto,
    para no confundirlo con un guion largo que use '---' al principio.
    """
    for m in SOURCES_SPLIT_RE.finditer(text):
        if m.start() > len(text) * 0.4:
            return text[: m.start()].rstrip(), text[m.start():].strip()
    return text, ""


def clean_for_speech(text: str) -> str:
    """Quita formato markdown y URLs para que el TTS no lea asteriscos ni 'https://'."""
    text = URL_RE.sub("", text)
    text = MD_HEADING_RE.sub("", text)
    text = MD_BULLET_RE.sub("", text)
    text = re.sub(r"\*{1,3}|_{2,}|`+", "", text)          # **negrita**, __x__, `code`
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)  # > citas
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_tag(raw_tag: str) -> tuple[str, str | None]:
    """'NOTICIA 1: La RAM se disparó' -> ('NOTICIA 1', 'La RAM se disparó')."""
    if ":" in raw_tag:
        label, title = raw_tag.split(":", 1)
        return label.strip(), (title.strip() or None)
    return raw_tag.strip(), None


def slugify(tag: str) -> str:
    """[NOTICIA 1: LA BOMBA] -> noticia_1_la_bomba"""
    tag = tag.split(":")[0].strip()  # nos quedamos con la parte antes de ':' para el slug corto
    tag = unicodedata.normalize("NFKD", tag).encode("ascii", "ignore").decode("ascii")
    tag = tag.lower().strip()
    tag = re.sub(r"[^a-z0-9]+", "_", tag).strip("_")
    return tag or "bloque"


def _dedupe_slugs(blocks: list[dict]) -> None:
    """Si hay slugs repetidos (ej. dos [ANÁLISIS]), les agrega un sufijo numérico, in-place."""
    seen = {}
    for b in blocks:
        base = b["slug"]
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            b["slug"] = f"{base}_{seen[base]}"


def parse_tagged_script(text: str) -> list[dict]:
    """Modo 1: guion con etiquetas [TAG] explícitas."""
    matches = list(TAG_RE.finditer(text))

    blocks = []
    for i, m in enumerate(matches):
        raw_tag = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        if not body:
            continue  # etiqueta sin contenido, la saltamos

        label, title = split_tag(raw_tag)
        blocks.append(
            {
                "index": len(blocks),
                "tag": raw_tag,
                "label": label,
                "title": title,
                "slug": slugify(raw_tag),
                "text": body,
                "word_count": len(body.split()),
            }
        )

    _dedupe_slugs(blocks)
    return blocks


def split_long_blocks(blocks: list[dict], max_words: int) -> list[dict]:
    """Parte los bloques que superen max_words en sub-bloques (misma etiqueta y título,
    slug con sufijo _p1, _p2...). Así una noticia principal de 800 palabras cambia
    de imagen cada ~1,5 min en vez de quedarse 5 min con la misma."""
    out = []
    for b in blocks:
        if b["word_count"] <= max_words:
            out.append(b)
            continue
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", b["text"]) if p.strip()]
        pieces = []
        for p in paragraphs:
            pieces.extend(_split_long_paragraph(p, max_words, tolerance=1.0))
        chunks, current, current_words = [], [], 0
        for piece in pieces:
            w = len(piece.split())
            if current and current_words + w > max_words:
                chunks.append("\n\n".join(current))
                current, current_words = [], 0
            current.append(piece)
            current_words += w
        if current:
            chunks.append("\n\n".join(current))
        for k, chunk in enumerate(chunks, start=1):
            out.append({
                **b,
                "slug": f"{b['slug']}_p{k}",
                "part": k,
                "parts": len(chunks),
                "text": chunk,
                "word_count": len(chunk.split()),
            })
    for i, b in enumerate(out):
        b["index"] = i
    return out


def _split_long_paragraph(paragraph: str, target_words: int, tolerance: float = 1.8) -> list[str]:
    """Si un párrafo es más largo que target_words * tolerance, lo corta por oraciones."""
    if len(paragraph.split()) <= target_words * tolerance:
        return [paragraph]

    sentences = SENTENCE_RE.split(paragraph)
    chunks, current, current_words = [], [], 0
    for sentence in sentences:
        w = len(sentence.split())
        if current and current_words + w > target_words:
            chunks.append(" ".join(current))
            current, current_words = [], 0
        current.append(sentence)
        current_words += w
    if current:
        chunks.append(" ".join(current))
    return chunks


def parse_freeform_script(text: str, target_words: int) -> list[dict]:
    """Modo 2: monólogo corrido sin etiquetas. Agrupa párrafos en segmentos."""
    raw_paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    # Si el guion viene con un párrafo por línea (sin líneas en blanco entre
    # medio, típico de la "transcripción" con párrafos de una sola línea),
    # re.split por doble salto de línea puede devolver un solo bloque gigante.
    # En ese caso, partimos por línea simple en vez de por línea en blanco.
    if len(raw_paragraphs) <= 1:
        raw_paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    # Corta párrafos anormalmente largos (por si el guion sí trae bloques
    # grandes tipo la "noticia principal" del prompt chileno, de 600-900 palabras).
    paragraphs = []
    for p in raw_paragraphs:
        paragraphs.extend(_split_long_paragraph(p, target_words))

    blocks = []
    current, current_words = [], 0

    def flush():
        nonlocal current, current_words
        if not current:
            return
        body = " ".join(current)
        n = len(blocks) + 1
        blocks.append(
            {
                "index": len(blocks),
                "tag": f"SEGMENTO {n}",
                "label": f"SEGMENTO {n}",
                "title": None,
                "slug": f"segmento_{n:02d}",
                "text": body,
                "word_count": len(body.split()),
            }
        )
        current, current_words = [], 0

    for p in paragraphs:
        w = len(p.split())
        if current and current_words + w > target_words:
            flush()
        current.append(p)
        current_words += w
    flush()

    return blocks


def parse_script(text: str, target_words: int = DEFAULT_AUTO_SEGMENT_TARGET_WORDS,
                 max_block_words: int = DEFAULT_MAX_BLOCK_WORDS) -> list[dict]:
    tagged = parse_tagged_script(text)
    if tagged:
        return split_long_blocks(tagged, max_block_words)

    print(
        "[aviso] No se encontraron etiquetas tipo [INTRO] en el guion. "
        f"Usando modo sin etiquetas: agrupando párrafos en bloques de ~{target_words} palabras."
    )
    blocks = parse_freeform_script(text, target_words)
    if not blocks:
        raise ValueError("El guion está vacío o no se pudo segmentar. Revisa el archivo de entrada.")
    return blocks


def _load_parsing_cfg(config_path: str | None) -> tuple[int, int]:
    """Devuelve (auto_segment_target_words, max_block_words) desde config.yaml."""
    defaults = (DEFAULT_AUTO_SEGMENT_TARGET_WORDS, DEFAULT_MAX_BLOCK_WORDS)
    if not config_path:
        return defaults
    try:
        import yaml
        cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
        parsing = cfg.get("parsing", {}) or {}
        return (
            int(parsing.get("auto_segment_target_words", defaults[0])),
            int(parsing.get("max_block_words", defaults[1])),
        )
    except FileNotFoundError:
        return defaults


def main():
    if len(sys.argv) not in (3, 4):
        print("Uso: python parse_script.py <guion.md> <bloques.json> [config.yaml]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    config_path = sys.argv[3] if len(sys.argv) == 4 else None
    output_path.parent.mkdir(parents=True, exist_ok=True)

    target_words, max_block_words = _load_parsing_cfg(config_path)
    raw_text = input_path.read_text(encoding="utf-8")

    # La sección FUENTES del final no se narra: se guarda aparte (sirve para la
    # descripción del video en YouTube).
    script_text, sources_text = split_sources(raw_text)
    sources_path = output_path.parent / "fuentes.md"
    if sources_text:
        sources_path.write_text(sources_text + "\n", encoding="utf-8")
        print(f"[fuentes] sección de fuentes separada del guion → {sources_path}")
    elif sources_path.exists():
        sources_path.unlink()

    text = clean_for_speech(script_text)
    blocks = parse_script(text, target_words, max_block_words)

    output_path.write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_words = sum(b["word_count"] for b in blocks)
    print(f"{len(blocks)} bloques detectados ({total_words} palabras) → {output_path}")
    for b in blocks:
        print(f"  [{b['index']:02d}] {b['slug']:<25} ({b['word_count']} palabras)")


if __name__ == "__main__":
    main()

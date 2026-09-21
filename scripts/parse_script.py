"""
Parsea un guion de texto en una lista de bloques estructurados, para que
generate_audio.py y generate_visuals.py generen un audio + un visual por bloque.

Soporta DOS formatos de guion:

1) Con marcas explícitas entre corchetes, solas en su línea. Hay dos familias
   y se pueden mezclar:

   a) Marcas visuales (las que emite el prompt en su sección GUION PARA TTS):

        [PLACA: titular corto]            nueva tarjeta de titular; el titular
                                          queda "vigente" para las marcas siguientes
        [IMAGEN: qué imagen buscar]       nuevo bloque que hereda el titular vigente
        [DIAGRAMA: qué dibujar]           ídem; puede traer debajo un bloque
                                          ```mermaid ... ``` que se renderiza
        [GRÁFICO: qué datos graficar]     ídem
        [MANTENER]                        el texto sigue con el visual anterior
                                          (se pega al bloque previo)
        [PAUSA]                           pausa larga después del bloque previo

   b) Etiquetas editoriales (formato antiguo): [INTRO], [NOTICIA 1: Titular],
      [CHILE: Titular], [CIERRE], [ANÁLISIS]... Cada una es una tarjeta con
      rótulo (NOTICIA 1) y titular.

   Si el archivo trae una línea `GUION PARA TTS`, solo se usa lo que viene
   después de ella (lo anterior es la versión de lectura, sin marcas).

2) Monólogo corrido SIN ningún marcador. El script agrupa párrafos consecutivos
   hasta juntar ~AUTO_SEGMENT_TARGET_WORDS palabras y arma bloques genéricos
   ("SEGMENTO 1", "SEGMENTO 2", ...).

En ambos casos, lo que venga después de la línea FUENTES (o REFERENCIAS) del
final se separa del guion y no se narra.

Uso:
    python parse_script.py input/guion.md output/bloques.json [config.yaml]
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

TAG_RE = re.compile(r"^[ \t]*\[([^\]\n]+)\][ \t]*$", re.MULTILINE)
# Etiqueta con decoración markdown encima, como la deja un export de Google Docs /
# Gemini: `## **\[NOTICIA 1: Titular\]**`. Se normaliza a `[NOTICIA 1: Titular]`.
DECORATED_TAG_RE = re.compile(
    r"^[ \t]*#{0,6}[ \t]*[*_`]*[ \t]*\\?\[([^\]\\\n]+?)\\?\][ \t]*[*_`]*[ \t]*$",
    re.MULTILINE,
)
MD_ESCAPE_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!>|~])")   # 2026\. -> 2026.   \- -> -
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\](?:\([^)]*\)|\[[^\]]*\])")   # ![alt](url) o ![][image1]
MD_REF_DEF_RE = re.compile(r"^[ \t]*\[[^\]]+\]:[ \t]*\S.*$", re.MULTILINE)   # [image1]: <data:...>
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((?:[^)(]|\([^)]*\))*\)")   # [texto](url) -> texto
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¡¿])")
TTS_HEADER_RE = re.compile(r"^[ \t]*[#*_ ]*GUION PARA TTS[ \t:*_]*$", re.MULTILINE | re.IGNORECASE)
MERMAID_FENCE_RE = re.compile(r"^\s*```\s*mermaid[^\n]*\n(.*?)^\s*```[ \t]*$", re.DOTALL | re.MULTILINE)

# Dónde termina el guion y empieza la lista de fuentes (que NO se narra): una
# línea que diga solo FUENTES / REFERENCIAS / BIBLIOGRAFÍA (con o sin decoración
# markdown). Una línea de solo guiones NO basta por sí sola: solo cuenta si va
# justo antes del encabezado de fuentes.
SOURCES_HEADING_RE = re.compile(
    r"^[ \t]*#{0,6}[ \t]*[*_]*[ \t]*(?:FUENTES|REFERENCIAS|BIBLIOGRAF[ÍI]A|WORKS CITED|SOURCES|REFERENCES)"
    r"[ \t]*[*_]*[ \t]*:?[ \t]*$",
    re.MULTILINE | re.IGNORECASE,
)
RULE_LINE_RE = re.compile(r"^[ \t]*(?:-{3,}|_{3,}|\*{3,})[ \t]*$", re.MULTILINE)

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MD_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
MD_BULLET_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+", re.MULTILINE)
# Marca que quedó en medio de una línea (el modelo a veces no la deja sola):
# se elimina para que la voz no la lea.
INLINE_MARK_RE = re.compile(
    r"\[(?:PLACA|IMAGEN|DIAGRAMA|GR[ÁA]FICO|MANTENER|PAUSA)(?::[^\]\n]*)?\]",
    re.IGNORECASE,
)

VISUAL_KINDS = {"PLACA": "tarjeta", "IMAGEN": "imagen", "DIAGRAMA": "diagrama", "GRAFICO": "grafico"}
CONTROL_KINDS = {"MANTENER", "PAUSA"}

DEFAULT_AUTO_SEGMENT_TARGET_WORDS = 130
DEFAULT_MAX_BLOCK_WORDS = 220
DEFAULT_PAUSE_SEC = 0.8
SLUG_MAX_LEN = 48


def _strip_accents(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def _words(s: str) -> int:
    return len(s.split())


# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------

def split_sources(text: str) -> tuple[str, str]:
    """Separa el guion de la sección de fuentes/referencias del final.

    Devuelve (guion, fuentes). Si no hay encabezado FUENTES, fuentes es "".
    Se usa el ÚLTIMO encabezado del archivo (no el primero), y si justo antes
    hay una línea `---`, el corte se hace ahí para que no quede colgando.
    """
    headings = list(SOURCES_HEADING_RE.finditer(text))
    if not headings:
        return text, ""
    m = headings[-1]
    cut = m.start()

    before = text[:cut]
    rule = None
    for r in RULE_LINE_RE.finditer(before):
        rule = r  # nos quedamos con la última línea de guiones antes del encabezado
    if rule is not None and not before[rule.end():].strip():
        cut = rule.start()

    return text[:cut].rstrip(), text[m.start():].strip()


def report_sources_cut(full_text: str, script_text: str, sources_text: str) -> None:
    total = _words(full_text)
    cut = _words(sources_text)
    pct = 100.0 * cut / total if total else 0.0
    if not sources_text:
        print("[fuentes] no se encontró una línea FUENTES: no se corta nada del guion")
        return
    print(f"[fuentes] se cortaron {cut} palabras del guion ({pct:.0f}% del total)")
    if pct > 50:
        print("[ALERTA] la sección de fuentes es más de la mitad del archivo. "
              "Revisa que el encabezado FUENTES esté solo al final del guion.")


# ---------------------------------------------------------------------------
# Limpieza para TTS
# ---------------------------------------------------------------------------

def select_tts_version(text: str) -> str:
    """Si el guion trae la línea GUION PARA TTS, devuelve solo lo que sigue."""
    m = TTS_HEADER_RE.search(text)
    if not m:
        return text
    skipped = _words(text[:m.start()])
    print(f"[guion] usando la versión GUION PARA TTS (se ignoran {skipped} palabras de la versión de lectura)")
    return text[m.end():]


def normalize_markdown(text: str) -> tuple[str, int]:
    """Deja las etiquetas decoradas (`## **\\[INTRO\\]**`) como `[INTRO]`, quita
    imágenes embebidas y definiciones de referencia, y des-escapa `\\.` `\\-` `\\[`.
    Devuelve (texto, cantidad de etiquetas normalizadas)."""
    text, n_tags = DECORATED_TAG_RE.subn(lambda m: f"[{m.group(1).strip()}]", text)
    text = MD_REF_DEF_RE.sub("", text)
    text = MD_IMAGE_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = MD_ESCAPE_RE.sub(r"\1", text)
    return text, n_tags


def clean_for_speech(text: str) -> str:
    """Quita formato markdown, URLs y marcas sueltas para que el TTS no las lea."""
    text = MD_IMAGE_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = URL_RE.sub("", text)
    text = INLINE_MARK_RE.sub("", text)
    text = MD_HEADING_RE.sub("", text)
    text = MD_BULLET_RE.sub("", text)
    text = re.sub(r"\*{1,3}|_{2,}|`+", "", text)          # **negrita**, __x__, `code`
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)  # > citas
    text = re.sub(r"\(\s*\)", "", text)                  # paréntesis vacíos (quedan al sacar imágenes)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" +([,.;:])", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Etiquetas
# ---------------------------------------------------------------------------

def split_tag(raw_tag: str) -> tuple[str, str | None]:
    """'NOTICIA 1: La RAM se disparó' -> ('NOTICIA 1', 'La RAM se disparó')."""
    if ":" in raw_tag:
        label, title = raw_tag.split(":", 1)
        return label.strip(), (title.strip() or None)
    return raw_tag.strip(), None


def normalize_kind(label: str) -> str:
    """'Gráfico' -> 'GRAFICO', 'noticia 1' -> 'NOTICIA 1'."""
    return re.sub(r"\s+", " ", _strip_accents(label)).strip().upper()


def slugify(text: str, max_len: int = SLUG_MAX_LEN) -> str:
    """'NOTICIA 1' -> 'noticia_1'; 'Obleas de silicio de Samsung' -> 'obleas_de_silicio_de_samsung'."""
    s = _strip_accents(text).lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if len(s) > max_len:
        s = s[:max_len]
        s = s[: s.rfind("_")] if "_" in s else s  # cortar en límite de palabra
    return s.strip("_") or "bloque"


def _dedupe_slugs(blocks: list[dict]) -> None:
    """Si hay slugs repetidos, les agrega un sufijo numérico, in-place."""
    seen = {}
    for b in blocks:
        base = b["slug"]
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            b["slug"] = f"{base}_{seen[base]}"


def _extract_mermaid(body: str) -> tuple[str, str | None]:
    """Saca un bloque ```mermaid``` del texto (no se narra). Devuelve (texto, mermaid|None)."""
    m = MERMAID_FENCE_RE.search(body)
    if not m:
        return body, None
    code = m.group(1).strip()
    body = (body[:m.start()] + "\n\n" + body[m.end():]).strip()
    return body, code or None


def _new_block(*, tag, label, title, slug, text, visual, pause_after=0.0) -> dict:
    return {
        "index": 0,
        "tag": tag,
        "label": label,
        "title": title,
        "slug": slug,
        "text": text,
        "word_count": _words(text),
        "visual": visual,
        "pause_after": pause_after,
    }


def parse_tagged_script(text: str, pause_sec: float = DEFAULT_PAUSE_SEC) -> list[dict]:
    """Modo 1: guion con marcas [TAG] explícitas (visuales y/o editoriales)."""
    matches = list(TAG_RE.finditer(text))
    if not matches:
        return []

    preamble = text[: matches[0].start()].strip()
    if preamble:
        print(f"[aviso] {_words(preamble)} palabras antes de la primera etiqueta: se ignoran "
              "(si era narración, ponle una etiqueta [INTRO] o [PLACA: ...] arriba).")

    blocks: list[dict] = []
    current_title: str | None = None
    ignored_marks = 0

    def append_to_previous(body: str) -> None:
        if not body:
            return
        if not blocks:
            blocks.append(_new_block(tag="INTRO", label=None, title=current_title,
                                     slug="intro", text=body,
                                     visual={"type": "tarjeta", "desc": None, "mermaid": None}))
            return
        prev = blocks[-1]
        prev["text"] = (prev["text"] + "\n\n" + body).strip()
        prev["word_count"] = _words(prev["text"])

    for i, m in enumerate(matches):
        raw_tag = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        kind, rest = split_tag(raw_tag)
        kind_n = normalize_kind(kind)

        if kind_n == "PAUSA":
            if blocks:
                blocks[-1]["pause_after"] = pause_sec
            append_to_previous(clean_for_speech(body))
            continue

        if kind_n == "MANTENER":
            append_to_previous(clean_for_speech(body))
            continue

        mermaid = None
        if kind_n in VISUAL_KINDS:
            vtype = VISUAL_KINDS[kind_n]
            if vtype == "tarjeta":
                current_title = rest
                label, title, desc = None, rest, None
                slug = slugify(rest or "placa")
            else:
                label, title, desc = None, current_title, rest
                slug = slugify(rest or vtype)
                if vtype == "diagrama":
                    body, mermaid = _extract_mermaid(body)
        else:
            # etiqueta editorial (formato antiguo): [INTRO], [NOTICIA 1: ...], [CHILE: ...]
            vtype = "tarjeta"
            current_title = rest
            label, title, desc = kind, rest, None
            slug = slugify(kind)

        body = clean_for_speech(body)
        if not body:
            ignored_marks += 1  # marca seguida de otra marca, sin texto: no hay nada que narrar
            continue

        blocks.append(_new_block(
            tag=raw_tag, label=label, title=title, slug=slug, text=body,
            visual={"type": vtype, "desc": desc, "mermaid": mermaid},
        ))

    if ignored_marks:
        print(f"[aviso] {ignored_marks} marca(s) sin texto debajo se ignoraron")

    _dedupe_slugs(blocks)
    for i, b in enumerate(blocks):
        b["index"] = i
    return blocks


# ---------------------------------------------------------------------------
# Bloques largos (red de seguridad)
# ---------------------------------------------------------------------------

def split_long_blocks(blocks: list[dict], max_words: int) -> list[dict]:
    """Parte los bloques que superen max_words en sub-bloques (misma etiqueta, título
    y visual; slug con sufijo _p1, _p2...). Con guiones que traen marcas visuales
    cada 25-45 palabras esto casi nunca actúa: es la red de seguridad para
    guiones sin marcas."""
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
            w = _words(piece)
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
                "word_count": _words(chunk),
                # la pausa larga va solo después del último trozo
                "pause_after": b.get("pause_after", 0.0) if k == len(chunks) else 0.0,
            })
    for i, b in enumerate(out):
        b["index"] = i
    return out


def _split_long_paragraph(paragraph: str, target_words: int, tolerance: float = 1.8) -> list[str]:
    """Si un párrafo es más largo que target_words * tolerance, lo corta por oraciones."""
    if _words(paragraph) <= target_words * tolerance:
        return [paragraph]

    sentences = SENTENCE_RE.split(paragraph)
    chunks, current, current_words = [], [], 0
    for sentence in sentences:
        w = _words(sentence)
        if current and current_words + w > target_words:
            chunks.append(" ".join(current))
            current, current_words = [], 0
        current.append(sentence)
        current_words += w
    if current:
        chunks.append(" ".join(current))
    return chunks


# ---------------------------------------------------------------------------
# Sin etiquetas
# ---------------------------------------------------------------------------

def parse_freeform_script(text: str, target_words: int) -> list[dict]:
    """Modo 2: monólogo corrido sin etiquetas. Agrupa párrafos en segmentos."""
    raw_paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    # Si el guion viene con un párrafo por línea (sin líneas en blanco entre medio),
    # re.split por doble salto puede devolver un solo bloque gigante.
    if len(raw_paragraphs) <= 1:
        raw_paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

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
        blocks.append(_new_block(
            tag=f"SEGMENTO {n}", label=f"SEGMENTO {n}", title=None,
            slug=f"segmento_{n:02d}", text=body,
            visual={"type": "tarjeta", "desc": None, "mermaid": None},
        ))
        blocks[-1]["index"] = len(blocks) - 1
        current, current_words = [], 0

    for p in paragraphs:
        w = _words(p)
        if current and current_words + w > target_words:
            flush()
        current.append(p)
        current_words += w
    flush()

    return blocks


# ---------------------------------------------------------------------------
# Entrada principal
# ---------------------------------------------------------------------------

def parse_script(text: str, target_words: int = DEFAULT_AUTO_SEGMENT_TARGET_WORDS,
                 max_block_words: int = DEFAULT_MAX_BLOCK_WORDS,
                 pause_sec: float = DEFAULT_PAUSE_SEC) -> list[dict]:
    """Texto del guion (ya sin la sección de fuentes) -> lista de bloques."""
    text = select_tts_version(text)
    tagged = parse_tagged_script(text, pause_sec=pause_sec)
    if tagged:
        return split_long_blocks(tagged, max_block_words)

    print(
        "[aviso] No se encontraron etiquetas tipo [INTRO] o [PLACA: ...] en el guion. "
        f"Usando modo sin etiquetas: agrupando párrafos en bloques de ~{target_words} palabras."
    )
    blocks = parse_freeform_script(clean_for_speech(text), target_words)
    if not blocks:
        raise ValueError("El guion está vacío o no se pudo segmentar. Revisa el archivo de entrada.")
    return blocks


def _load_parsing_cfg(config_path: str | None) -> tuple[int, int, float]:
    """Devuelve (auto_segment_target_words, max_block_words, pause_sec) desde config.yaml."""
    defaults = (DEFAULT_AUTO_SEGMENT_TARGET_WORDS, DEFAULT_MAX_BLOCK_WORDS, DEFAULT_PAUSE_SEC)
    if not config_path:
        return defaults
    try:
        import yaml
        cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
        parsing = cfg.get("parsing", {}) or {}
        return (
            int(parsing.get("auto_segment_target_words", defaults[0])),
            int(parsing.get("max_block_words", defaults[1])),
            float(parsing.get("pause_sec", defaults[2])),
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

    target_words, max_block_words, pause_sec = _load_parsing_cfg(config_path)
    raw_text, n_norm = normalize_markdown(input_path.read_text(encoding="utf-8"))
    if n_norm:
        print(f"[guion] {n_norm} etiqueta(s) venían con markdown encima (## **\\[..\\]**): normalizadas")

    # La sección FUENTES del final no se narra: se guarda aparte (sirve para la
    # descripción del video en YouTube).
    script_text, sources_text = split_sources(raw_text)
    report_sources_cut(raw_text, script_text, sources_text)
    sources_path = output_path.parent / "fuentes.md"
    if sources_text:
        sources_path.write_text(sources_text + "\n", encoding="utf-8")
        print(f"[fuentes] sección de fuentes separada del guion → {sources_path}")
    elif sources_path.exists():
        sources_path.unlink()

    blocks = parse_script(script_text, target_words, max_block_words, pause_sec)

    output_path.write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_words = sum(b["word_count"] for b in blocks)
    print(f"{len(blocks)} bloques detectados ({total_words} palabras, ~{total_words/150:.1f} min) → {output_path}")
    for b in blocks:
        v = b["visual"]["type"]
        extra = f"  ← {b['visual']['desc']}" if b["visual"].get("desc") else ""
        pause = "  [pausa]" if b.get("pause_after") else ""
        print(f"  [{b['index']:02d}] {v:<8} {b['slug']:<40} ({b['word_count']:>3} palabras){pause}{extra}")


if __name__ == "__main__":
    main()

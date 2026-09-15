"""
Resuelve la imagen de apoyo para cada bloque del guion:
  1. Si existe assets/images/<slug>.png (o .jpg/.webp), la usa tal cual.
     (para bloques partidos, también sirve la imagen del slug base: noticia_1.png
      vale para noticia_1_p1, noticia_1_p2, ...)
  2. Si no existe, genera una tarjeta de titular con Pillow: nombre del canal,
     fecha del episodio, etiqueta del bloque (NOTICIA 1, INTRO...), el titular
     (el texto tras ':' en la etiqueta, o la primera oración del bloque si el
     guion vino sin etiquetas) y un extracto del texto.

TODO: buscar imágenes reales por API (Pexels/Unsplash) o generarlas con un
modelo de imágenes cuando no haya imagen propia.

Uso:
    python generate_visuals.py output/bloques.json output/visuals/ config.yaml
"""

import datetime as dt
import json
import re
import sys
import textwrap
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s")


def _font_path(bold: bool) -> Path:
    """DejaVu Sans viene empaquetada con matplotlib, así no dependemos de fuentes del sistema."""
    import matplotlib
    ttf_dir = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
    return ttf_dir / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(_font_path(bold)), size)


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def find_existing_image(images_dir: Path, slug: str) -> Path | None:
    candidates = [slug]
    base = re.sub(r"_p\d+$", "", slug)  # noticia_1_p2 -> noticia_1
    if base != slug:
        candidates.append(base)
    for name in candidates:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            candidate = images_dir / f"{name}{ext}"
            if candidate.exists():
                return candidate
    return None


def headline_for(block: dict, max_chars: int = 110) -> str:
    """Titular: el de la etiqueta si existe, si no la primera oración del texto."""
    title = block.get("title")
    if title:
        return title
    first = SENTENCE_END_RE.split(block["text"].replace("\n", " ").strip(), maxsplit=1)[0]
    return textwrap.shorten(first, width=max_chars, placeholder="…")


def excerpt_for(block: dict, max_chars: int = 220) -> str:
    text = block["text"].replace("\n", " ")
    # si el titular salió de la primera oración, el extracto arranca en la segunda
    if not block.get("title"):
        parts = SENTENCE_END_RE.split(text.strip(), maxsplit=1)
        text = parts[1] if len(parts) > 1 else ""
    return textwrap.shorten(text, width=max_chars, placeholder="…")


def wrap_to_width(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for w in words:
        trial = f"{current} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, text, max_width, max_lines, bold=True, start=84, minimum=48):
    """Baja el tamaño de fuente hasta que el titular quepa en max_lines líneas."""
    size = start
    while True:
        fnt = font(size, bold)
        lines = wrap_to_width(draw, text, fnt, max_width)
        if len(lines) <= max_lines or size <= minimum:
            return fnt, lines[:max_lines]
        size -= 4


def episode_label(cfg_visuals: dict) -> str:
    label = cfg_visuals.get("episode_label")
    if label:
        return str(label)
    today = dt.date.today()
    return f"{today.day} de {MESES[today.month - 1]} de {today.year}"


def make_card(block: dict, out_path: Path, cfg: dict, resolution) -> None:
    vis = cfg["visuals"]
    w, h = resolution
    bg = hex_to_rgb(vis.get("placeholder_bg_color", "#111319"))
    fg = hex_to_rgb(vis.get("placeholder_text_color", "#F5F5F5"))
    accent = hex_to_rgb(vis.get("accent_color", "#4F8CFF"))
    muted = tuple(int(c * 0.62) for c in fg)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # Degradado vertical sutil (más claro arriba a la izquierda)
    top = tuple(min(255, c + 14) for c in bg)
    for y in range(h):
        t = y / h
        row = tuple(int(top[i] * (1 - t) + bg[i] * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=row)

    margin = int(w * 0.07)
    content_w = w - 2 * margin

    # Cabecera: canal (izq) y fecha (der)
    head_y = int(h * 0.08)
    draw.text((margin, head_y), vis.get("channel_name", "Noticiario de Hardware").upper(),
              font=font(30, bold=True), fill=muted)
    date_txt = episode_label(vis)
    draw.text((w - margin - draw.textlength(date_txt, font=font(30)), head_y),
              date_txt, font=font(30), fill=muted)
    draw.line([(margin, head_y + 52), (w - margin, head_y + 52)], fill=muted, width=1)

    # Medir el bloque central (etiqueta + titular + extracto) para centrarlo verticalmente
    label = block.get("label") or block.get("tag", "")
    if block.get("parts", 1) > 1:
        label = f"{label}  ·  parte {block['part']}/{block['parts']}"
    f_label = font(34, bold=True)

    f_title, title_lines = fit_headline(draw, headline_for(block), content_w, max_lines=3)
    title_line_h = int(f_title.size * 1.18)

    f_body = font(34)
    body_line_h = int(f_body.size * 1.35)
    body_lines = wrap_to_width(draw, excerpt_for(block), f_body, content_w)[:3]

    label_h = f_label.size + 24
    title_h = title_line_h * len(title_lines)
    body_h = (30 + body_line_h * len(body_lines)) if body_lines else 0
    total_h = label_h + title_h + body_h
    y = max(head_y + 100, (h - total_h) // 2 + 20)

    # Etiqueta del bloque (NOTICIA 1 · parte 2/3)
    draw.text((margin, y), label.upper(), font=f_label, fill=accent)
    y += label_h

    # Barra de acento a la izquierda del titular
    draw.rectangle([margin - 28, y + 6, margin - 14, y + title_h - 6], fill=accent)

    # Titular
    for line in title_lines:
        draw.text((margin, y), line, font=f_title, fill=fg)
        y += title_line_h

    # Extracto
    if body_lines:
        y += 30
        for line in body_lines:
            draw.text((margin, y), line, font=f_body, fill=muted)
            y += body_line_h

    img.save(out_path, "PNG")


def main():
    if len(sys.argv) != 4:
        print("Uso: python generate_visuals.py <bloques.json> <visuals_dir> <config.yaml>")
        sys.exit(1)

    blocks_path = Path(sys.argv[1])
    visuals_dir = Path(sys.argv[2])
    config_path = Path(sys.argv[3])

    visuals_dir.mkdir(parents=True, exist_ok=True)
    blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    images_dir = Path(cfg["visuals"]["images_dir"])
    resolution = cfg["video"]["resolution"]

    manifest = []
    for b in blocks:
        existing = find_existing_image(images_dir, b["slug"])
        if existing:
            print(f"[{b['slug']}] usando imagen propia: {existing.name}")
            manifest.append({"index": b["index"], "slug": b["slug"], "image_path": str(existing)})
            continue

        out_path = visuals_dir / f"{b['index']:02d}_{b['slug']}.png"
        print(f"[{b['slug']}] sin imagen propia → tarjeta de titular")
        make_card(b, out_path, cfg, resolution)
        manifest.append({"index": b["index"], "slug": b["slug"], "image_path": str(out_path)})

    manifest_path = visuals_dir.parent / "visuals_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nManifest guardado en {manifest_path}")


if __name__ == "__main__":
    main()

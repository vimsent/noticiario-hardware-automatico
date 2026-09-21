"""
Resuelve el visual de cada bloque del guion según lo que decidió el guion
(bloques.json → campo "visual", que viene de las marcas [PLACA], [IMAGEN],
[DIAGRAMA], [GRÁFICO] del prompt):

  tarjeta   → tarjeta de titular con Pillow (titular grande + extracto).
  imagen    → si existe assets/images/<slug>.(png|jpg|webp), se usa tal cual.
              Si no, tarjeta "cita" (titular chico + extracto grande) y el
              bloque queda anotado en output/visuales_pendientes.md con el
              nombre de archivo que espera, para que lo consigas y lo dejes ahí.
  diagrama  → si el bloque trae código Mermaid y hay `mmdc` instalado, se
              renderiza a PNG sobre la tarjeta. Si no, igual que "imagen".
  grafico   → igual que "imagen".

Con visuals.strict_assets: true, cualquier imagen/diagrama/gráfico sin archivo
aborta el pipeline en vez de caer a tarjeta.

Para el formato antiguo ([NOTICIA 1: ...] partida en _p1, _p2...), también
sirve assets/images/noticia_1.png para todas las partes; y las partes 2+ usan
el layout "cita" para que no se vean seis tarjetas idénticas seguidas.

Uso:
    python generate_visuals.py output/bloques.json output/visuals/ config.yaml
"""

import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


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


# ---------------------------------------------------------------------------
# Assets propios
# ---------------------------------------------------------------------------

def asset_candidates(slug: str) -> list[str]:
    """Nombres de archivo (sin extensión) que sirven para este bloque."""
    names = [slug]
    base = re.sub(r"_p\d+$", "", slug)      # noticia_1_p2 -> noticia_1
    if base != slug:
        names.append(base)
    base2 = re.sub(r"_\d+$", "", base)      # slug_2 (deduplicado) -> slug
    if base2 != base:
        names.append(base2)
    return names


def find_existing_image(images_dir: Path, slug: str) -> Path | None:
    for name in asset_candidates(slug):
        for ext in IMAGE_EXTS:
            candidate = images_dir / f"{name}{ext}"
            if candidate.exists():
                return candidate
    return None


# ---------------------------------------------------------------------------
# Texto de las tarjetas
# ---------------------------------------------------------------------------

# El GUION PARA TTS trae las siglas deletreadas ("hache be eme") para que la voz
# las lea bien. En pantalla se ven mal, así que se revierten las más comunes.
SPELLED_ACRONYMS = {
    "hache be eme": "HBM", "de de erre cinco": "DDR5", "de de erre cuatro": "DDR4",
    "ge de de erre siete": "GDDR7", "ge de de erre seis": "GDDR6", "ge pe u": "GPU",
    "ce pe u": "CPU", "ene pe u": "NPU", "ese ese de": "SSD", "te ese eme ce": "TSMC",
    "e u ve": "EUV", "pe ce i e": "PCIe", "hache de eme i": "HDMI", "u ese be": "USB",
    "a pe i": "API", "i a": "IA", "ce ve e": "CVE", "a eme de": "AMD", "ese de ka": "SDK",
    "ele ele eme": "LLM", "a ene i de": "ANID", "u ese eme": "USM", "e u": "EU",
}
_SPELLED_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in sorted(SPELLED_ACRONYMS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def display_text(text: str) -> str:
    """Texto para mostrar en pantalla: siglas deletreadas de vuelta a su forma escrita."""
    return _SPELLED_RE.sub(lambda m: SPELLED_ACRONYMS[m.group(1).lower()], text)


def headline_for(block: dict, max_chars: int = 110) -> str:
    """Titular: el de la etiqueta si existe, si no la primera oración del texto."""
    title = block.get("title")
    if title:
        return display_text(title)
    first = SENTENCE_END_RE.split(block["text"].replace("\n", " ").strip(), maxsplit=1)[0]
    return textwrap.shorten(display_text(first), width=max_chars, placeholder="…")


def excerpt_for(block: dict, max_chars: int = 220) -> str:
    text = display_text(block["text"].replace("\n", " "))
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


def fit_text(draw, text, max_width, max_lines, bold=True, start=84, minimum=48):
    """Baja el tamaño de fuente hasta que el texto quepa en max_lines líneas."""
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


# ---------------------------------------------------------------------------
# Tarjetas
# ---------------------------------------------------------------------------

class Canvas:
    """Lienzo base: fondo con degradado, cabecera con canal y fecha."""

    def __init__(self, cfg: dict, resolution):
        vis = cfg["visuals"]
        self.w, self.h = resolution
        self.bg = hex_to_rgb(vis.get("placeholder_bg_color", "#111319"))
        self.fg = hex_to_rgb(vis.get("placeholder_text_color", "#F5F5F5"))
        self.accent = hex_to_rgb(vis.get("accent_color", "#4F8CFF"))
        self.muted = tuple(int(c * 0.62) for c in self.fg)
        self.margin = int(self.w * 0.07)
        self.content_w = self.w - 2 * self.margin
        self.head_y = int(self.h * 0.08)
        self.body_top = self.head_y + 100

        self.img = Image.new("RGB", (self.w, self.h), self.bg)
        self.draw = ImageDraw.Draw(self.img)

        top = tuple(min(255, c + 14) for c in self.bg)
        for y in range(self.h):
            t = y / self.h
            row = tuple(int(top[i] * (1 - t) + self.bg[i] * t) for i in range(3))
            self.draw.line([(0, y), (self.w, y)], fill=row)

        d, m, hy = self.draw, self.margin, self.head_y
        d.text((m, hy), vis.get("channel_name", "Noticiario de Hardware").upper(),
               font=font(30, bold=True), fill=self.muted)
        date_txt = episode_label(vis)
        d.text((self.w - m - d.textlength(date_txt, font=font(30)), hy),
               date_txt, font=font(30), fill=self.muted)
        d.line([(m, hy + 52), (self.w - m, hy + 52)], fill=self.muted, width=1)

    def save(self, out_path: Path) -> None:
        self.img.save(out_path, "PNG")


def _label_text(block: dict) -> str | None:
    label = block.get("label")
    if not label:
        return None
    if block.get("parts", 1) > 1:
        label = f"{label}  ·  parte {block['part']}/{block['parts']}"
    return label.upper()


def make_headline_card(block: dict, out_path: Path, cfg: dict, resolution) -> None:
    """Layout 'placa': rótulo (opcional), titular grande con barra de acento, extracto chico."""
    c = Canvas(cfg, resolution)
    d, m = c.draw, c.margin

    label = _label_text(block)
    f_label = font(34, bold=True)
    f_title, title_lines = fit_text(d, headline_for(block), c.content_w, max_lines=3)
    title_line_h = int(f_title.size * 1.18)
    f_body = font(34)
    body_line_h = int(f_body.size * 1.35)
    body_lines = wrap_to_width(d, excerpt_for(block), f_body, c.content_w)[:3]

    label_h = (f_label.size + 24) if label else 0
    title_h = title_line_h * len(title_lines)
    body_h = (30 + body_line_h * len(body_lines)) if body_lines else 0
    total_h = label_h + title_h + body_h
    y = max(c.body_top, (c.h - total_h) // 2 + 20)

    if label:
        d.text((m, y), label, font=f_label, fill=c.accent)
        y += label_h

    d.rectangle([m - 28, y + 6, m - 14, y + title_h - 6], fill=c.accent)
    for line in title_lines:
        d.text((m, y), line, font=f_title, fill=c.fg)
        y += title_line_h

    if body_lines:
        y += 30
        for line in body_lines:
            d.text((m, y), line, font=f_body, fill=c.muted)
            y += body_line_h

    c.save(out_path)


def make_quote_card(block: dict, out_path: Path, cfg: dict, resolution) -> None:
    """Layout 'cita': titular chico arriba (contexto) y el extracto grande como
    protagonista. Se usa para los tramos que siguen a una placa, para que el
    ojo note el cambio aunque el titular sea el mismo."""
    c = Canvas(cfg, resolution)
    d, m = c.draw, c.margin

    f_title = font(36, bold=True)
    title_lines = wrap_to_width(d, headline_for(block), f_title, c.content_w)[:2]
    f_quote, quote_lines = fit_text(d, excerpt_for(block, max_chars=260), c.content_w - 60,
                                    max_lines=5, bold=False, start=64, minimum=40)
    quote_line_h = int(f_quote.size * 1.3)

    y = c.body_top
    for line in title_lines:
        d.text((m, y), line, font=f_title, fill=c.accent)
        y += int(f_title.size * 1.25)

    quote_h = quote_line_h * len(quote_lines)
    y = max(y + 40, (c.h - quote_h) // 2)
    d.text((m - 10, y - 30), "“", font=font(140, bold=True), fill=c.accent)
    for line in quote_lines:
        d.text((m + 60, y), line, font=f_quote, fill=c.fg)
        y += quote_line_h

    c.save(out_path)


# ---------------------------------------------------------------------------
# Mermaid
# ---------------------------------------------------------------------------

def mermaid_cmd(cfg: dict) -> str | None:
    """Ruta al CLI de Mermaid (mmdc) si está instalado; None si no."""
    configured = cfg["visuals"].get("mermaid_cmd") or "mmdc"
    return shutil.which(configured)


def make_diagram_card(block: dict, out_path: Path, cfg: dict, resolution, mmdc: str) -> None:
    """Renderiza el Mermaid del bloque con mmdc y lo monta sobre el lienzo con el titular."""
    c = Canvas(cfg, resolution)
    d, m = c.draw, c.margin

    f_title = font(36, bold=True)
    title_lines = wrap_to_width(d, headline_for(block), f_title, c.content_w)[:2]
    y = c.body_top
    for line in title_lines:
        d.text((m, y), line, font=f_title, fill=c.accent)
        y += int(f_title.size * 1.25)
    y += 30

    box_w, box_h = c.content_w, c.h - y - int(c.h * 0.08)
    bg_hex = "#%02x%02x%02x" % c.bg
    with tempfile.TemporaryDirectory(prefix="mermaid_") as tmp:
        src = Path(tmp) / "diagram.mmd"
        png = Path(tmp) / "diagram.png"
        src.write_text(block["visual"]["mermaid"], encoding="utf-8")
        subprocess.run(
            [mmdc, "-q", "-i", str(src), "-o", str(png), "-b", bg_hex,
             "-t", cfg["visuals"].get("mermaid_theme", "dark"),
             "-w", str(box_w * 2), "-H", str(box_h * 2), "-s", "2"],
            check=True, capture_output=True, text=True,
        )
        diagram = Image.open(png).convert("RGB")

    scale = min(box_w / diagram.width, box_h / diagram.height, 1.0)
    diagram = diagram.resize((max(1, int(diagram.width * scale)), max(1, int(diagram.height * scale))),
                             Image.LANCZOS)
    x = m + (box_w - diagram.width) // 2
    c.img.paste(diagram, (x, y + (box_h - diagram.height) // 2))
    c.save(out_path)


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------

def resolve_visual(block: dict, visuals_dir: Path, images_dir: Path, cfg: dict,
                   resolution, mmdc: str | None, pending: list[dict]) -> str:
    """Devuelve la ruta de la imagen de este bloque, generándola si hace falta."""
    visual = block.get("visual") or {"type": "tarjeta", "desc": None, "mermaid": None}
    vtype = visual.get("type", "tarjeta")
    slug = block["slug"]
    out_path = visuals_dir / f"{block['index']:02d}_{slug}.png"

    existing = find_existing_image(images_dir, slug)
    if existing:
        print(f"[{slug}] imagen propia: {existing.name}")
        return str(existing)

    if vtype == "diagrama" and visual.get("mermaid"):
        if mmdc:
            try:
                make_diagram_card(block, out_path, cfg, resolution, mmdc)
                print(f"[{slug}] diagrama Mermaid renderizado")
                return str(out_path)
            except subprocess.CalledProcessError as e:
                print(f"[{slug}] mmdc falló ({e.stderr.strip().splitlines()[-1] if e.stderr else e}); "
                      "cayendo a tarjeta")
        else:
            print(f"[{slug}] el bloque trae Mermaid pero no hay `mmdc` instalado "
                  "(npm i -g @mermaid-js/mermaid-cli); cayendo a tarjeta")

    if vtype in ("imagen", "diagrama", "grafico"):
        expected = images_dir / f"{asset_candidates(slug)[-1]}.png"
        pending.append({"index": block["index"], "type": vtype, "desc": visual.get("desc"),
                        "expected": str(expected), "title": block.get("title")})
        print(f"[{slug}] {vtype} sin archivo ({expected.name}) → tarjeta cita")
        make_quote_card(block, out_path, cfg, resolution)
        return str(out_path)

    # tarjeta: la primera parte con titular grande; las siguientes, como cita
    if block.get("part", 1) > 1:
        print(f"[{slug}] tarjeta cita (parte {block['part']}/{block['parts']})")
        make_quote_card(block, out_path, cfg, resolution)
    else:
        print(f"[{slug}] tarjeta de titular")
        make_headline_card(block, out_path, cfg, resolution)
    return str(out_path)


def write_pending(pending: list[dict], path: Path) -> None:
    lines = [
        "# Visuales pendientes",
        "",
        "Bloques que el guion pidió con imagen/diagrama/gráfico y no tienen archivo.",
        "Mientras no exista el archivo se usa una tarjeta de texto. Para reemplazarla,",
        "guarda la imagen con el nombre indicado (png, jpg o webp) y vuelve a correr",
        "`python scripts/main.py --skip-audio`.",
        "",
    ]
    for p in pending:
        lines.append(f"- [{p['index']:02d}] **{p['type']}** — {p['desc']}")
        if p.get("title"):
            lines.append(f"  - contexto: {p['title']}")
        lines.append(f"  - archivo esperado: `{p['expected']}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    resolution = tuple(cfg["video"]["resolution"])
    strict = bool(cfg["visuals"].get("strict_assets", False))
    mmdc = mermaid_cmd(cfg)

    manifest = []
    pending: list[dict] = []
    for b in blocks:
        image_path = resolve_visual(b, visuals_dir, images_dir, cfg, resolution, mmdc, pending)
        manifest.append({"index": b["index"], "slug": b["slug"], "image_path": image_path})

    manifest_path = visuals_dir.parent / "visuals_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nManifest guardado en {manifest_path}")

    pending_path = visuals_dir.parent / "visuales_pendientes.md"
    if pending:
        write_pending(pending, pending_path)
        print(f"[aviso] {len(pending)} visual(es) pedidos por el guion no tienen archivo; "
              f"se usaron tarjetas. Lista con nombres esperados: {pending_path}")
        if strict:
            raise SystemExit("[ERROR] visuals.strict_assets está activado: faltan imágenes (ver lista).")
    elif pending_path.exists():
        pending_path.unlink()


if __name__ == "__main__":
    main()

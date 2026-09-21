"""Tests del parser. Correr con:  python -m unittest discover -s tests -v"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import parse_script as ps  # noqa: E402

MARK_RE = re.compile(r"\[(PLACA|IMAGEN|DIAGRAMA|GR[ÁA]FICO|MANTENER|PAUSA|INTRO|NOTICIA|CIERRE)", re.I)

GUION_V2 = """\
Versión de lectura, texto corrido que no se debe narrar dos veces.

GUION PARA TTS

[PLACA: RAM por las nubes]
Partamos por el fondo técnico, porque si no, no se entiende.

[IMAGEN: Obleas de silicio de Samsung]
Salen de las mismas fábricas de obleas. Es la misma torta.

[MANTENER]
Y cuando los tres grandes cortan la torta, le dan la tajada gorda a la HBM.

[DIAGRAMA: Oblea repartida entre HBM y DDR5]
```mermaid
graph LR
  O[Oblea] --> H[HBM]
  O --> D[DDR5]
```
Fabricar HBM se come tres veces la oblea.

[PAUSA]

[PLACA: Intel logra hito con High-NA]
Y ya que estamos con fábricas [MANTENER] pasemos a Intel.

[GRÁFICO: Acciones de Intel]
Subieron harto el ocho de septiembre.

FUENTES

- Precio spot de DDR4 — Capital & Compute, 11 de septiembre. https://ejemplo.com/a
- Intel High-NA — Intel, 8 de septiembre. https://ejemplo.com/b
"""

GUION_LEGACY = """\
[INTRO]
Buenas a todos, bienvenidos.

[NOTICIA 1: La RAM se disparó]
Primer párrafo.

Segundo párrafo.

[CHILE: Datacenters y cable Humboldt]
Ahora el bloque de la casa.

[CIERRE]
Eso fue todo.

---

FUENTES

- algo. https://x.y
"""


class SplitSourcesTests(unittest.TestCase):
    def test_uses_last_heading_and_swallows_rule(self):
        script, sources = ps.split_sources(GUION_LEGACY)
        self.assertTrue(sources.startswith("FUENTES"))
        self.assertNotIn("---", script)
        self.assertIn("Eso fue todo.", script)

    def test_lone_rule_does_not_cut(self):
        text = "[INTRO]\nHola.\n\n---\n\n[NOTICIA 1: X]\nMás texto.\n\n---\n\nFUENTES\n- a\n"
        script, sources = ps.split_sources(text)
        self.assertIn("Más texto.", script)
        self.assertTrue(sources.startswith("FUENTES"))

    def test_fuentes_word_inside_narration_is_not_a_heading(self):
        text = "[INTRO]\nFuentes del sector dicen que sí.\nSigue.\n\nFUENTES\n- a\n"
        script, sources = ps.split_sources(text)
        self.assertIn("Fuentes del sector", script)
        self.assertEqual(sources.splitlines()[0].strip(), "FUENTES")

    def test_no_heading_keeps_everything(self):
        text = "[INTRO]\nHola.\n\n---\n\nChao.\n"
        script, sources = ps.split_sources(text)
        self.assertEqual(sources, "")
        self.assertIn("Chao.", script)


class VisualMarkersTests(unittest.TestCase):
    def setUp(self):
        script, _ = ps.split_sources(GUION_V2)
        self.blocks = ps.parse_script(script)

    def test_no_marker_reaches_tts_text(self):
        for b in self.blocks:
            self.assertIsNone(MARK_RE.search(b["text"]), f"marca en el texto de {b['slug']}: {b['text']!r}")
            self.assertNotIn("```", b["text"])
            self.assertNotIn("graph LR", b["text"])

    def test_reading_version_is_ignored(self):
        joined = " ".join(b["text"] for b in self.blocks)
        self.assertNotIn("Versión de lectura", joined)

    def test_blocks_and_types(self):
        types = [b["visual"]["type"] for b in self.blocks]
        self.assertEqual(types, ["tarjeta", "imagen", "diagrama", "tarjeta", "grafico"])

    def test_mantener_merges_into_previous(self):
        img = self.blocks[1]
        self.assertIn("Es la misma torta.", img["text"])
        self.assertIn("tajada gorda", img["text"])

    def test_image_inherits_current_title(self):
        self.assertEqual(self.blocks[1]["title"], "RAM por las nubes")
        self.assertEqual(self.blocks[1]["visual"]["desc"], "Obleas de silicio de Samsung")
        self.assertEqual(self.blocks[4]["title"], "Intel logra hito con High-NA")

    def test_mermaid_extracted(self):
        diag = self.blocks[2]
        self.assertIn("graph LR", diag["visual"]["mermaid"])
        self.assertEqual(diag["text"], "Fabricar HBM se come tres veces la oblea.")

    def test_pausa_sets_pause_after(self):
        self.assertGreater(self.blocks[2]["pause_after"], 0)
        self.assertEqual(self.blocks[1]["pause_after"], 0)

    def test_inline_marker_is_stripped(self):
        self.assertEqual(self.blocks[3]["text"], "Y ya que estamos con fábricas pasemos a Intel.")


GUION_GDOCS = """\
# **Reporte de Análisis Técnico**

## **\\[INTRO\\]**

Texto de la intro del 7 al 14 de septiembre de 2026\\. Sigue.

## **\\[NOTICIA 1: La RTX 5090 desaparece\\]**

El calentamiento por efecto Joule (![][image1]) es agnóstico\\-al diseño, ver [Tom's](https://tomshardware.com/x).

## **\\[CIERRE\\]**

Chao.

#### **Works cited**

> 1. Algo, [https://a.b/c](https://a.b/c)

[image1]: <data:image/png;base64,iVBORw0KGgo>
"""


class MarkdownExportTests(unittest.TestCase):
    def test_decorated_tags_and_escapes(self):
        text, n = ps.normalize_markdown(GUION_GDOCS)
        self.assertEqual(n, 3)
        script, sources = ps.split_sources(text)
        self.assertIn("Works cited", sources)
        blocks = ps.parse_script(script)
        self.assertEqual([b["slug"] for b in blocks], ["intro", "noticia_1", "cierre"])
        self.assertEqual(blocks[1]["title"], "La RTX 5090 desaparece")
        self.assertIn("de 2026. Sigue.", blocks[0]["text"])
        self.assertEqual(blocks[1]["text"], "El calentamiento por efecto Joule es agnóstico-al diseño, ver Tom's.")
        for b in blocks:
            self.assertNotIn("[", b["text"])
            self.assertNotIn("\\", b["text"])


class LegacyFormatTests(unittest.TestCase):
    def test_legacy_tags(self):
        script, _ = ps.split_sources(GUION_LEGACY)
        blocks = ps.parse_script(script)
        self.assertEqual([b["slug"] for b in blocks], ["intro", "noticia_1", "chile", "cierre"])
        self.assertEqual(blocks[1]["label"], "NOTICIA 1")
        self.assertEqual(blocks[1]["title"], "La RAM se disparó")
        self.assertTrue(all(b["visual"]["type"] == "tarjeta" for b in blocks))

    def test_long_block_is_split_as_safety_net(self):
        body = "\n\n".join("Oración número %d con varias palabras adentro." % i for i in range(60))
        text = f"[NOTICIA 1: Larga]\n{body}\n"
        blocks = ps.parse_script(text, max_block_words=100)
        self.assertGreater(len(blocks), 1)
        self.assertTrue(all(b["slug"].startswith("noticia_1_p") for b in blocks))
        self.assertTrue(all(b["word_count"] <= 100 for b in blocks))


if __name__ == "__main__":
    unittest.main()

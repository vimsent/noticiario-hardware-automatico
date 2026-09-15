# Noticiario de Hardware — Pipeline de generación de video

Convierte un guion de texto (la respuesta de Claude al prompt de
`prompt_noticiario_hardware.md`, pegada en `input/guion.md`) en un video con
narración por voz neuronal, música de fondo y tarjetas de titular por bloque.

## Flujo del pipeline

```
guion.md  →  parse_script.py  →  bloques.json  (+ fuentes.md, la sección FUENTES separada)
bloques.json  →  generate_audio.py   →  audio/*.wav  + audio_manifest.json (duraciones)
bloques.json  →  generate_visuals.py → visuals/*.png (una tarjeta de titular por bloque)
audio_manifest.json + visuals/ + música →  assemble_video.py → output/video_final.mp4
```

`scripts/main.py` corre las 4 etapas en orden y al final borra los archivos
intermedios (`output.clean_intermediates` en `config.yaml`). En `output/` quedan
solo `video_final.mp4` y `fuentes.md` (la lista de fuentes, para la descripción
del video en YouTube).

## Requisitos del sistema (Fedora/Debian)

```bash
sudo dnf install ffmpeg          # Fedora (de RPM Fusion, con soporte NVENC)
# o
sudo apt install ffmpeg          # Debian

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Voz (TTS)

- **`edge`** (por defecto): voces neuronales de Microsoft vía `edge-tts`. Gratis,
  necesita internet. Voces chilenas: `es-CL-LorenzoNeural` (hombre) y
  `es-CL-CatalinaNeural` (mujer). Lista completa: `edge-tts --list-voices | grep es-`.
- **`piper`**: local y offline, calidad más robótica. Se usa automáticamente como
  respaldo si `edge` falla (sin internet, servicio caído). Necesita el modelo en
  `models/`:

  ```bash
  python -m piper.download_voices --download-dir models es_ES-davefx-medium
  ```

Se elige en `config.yaml` → `tts.engine` / `tts.fallback_engine`.

### GPU

`assemble_video.py` usa ffmpeg directo. Con `video.encoder: auto` detecta la GPU
NVIDIA (`h264_nvenc`) y si no hay cae a `libx264` por CPU. Un episodio de ~16 min
tarda ~4 min en total (la mayor parte es descargar la voz).

## Uso

1. Genera el guion en claude.ai con `prompt_noticiario_hardware.md` (con búsqueda
   web activada) y pega la respuesta completa en `input/guion.md`.
2. Pon una o varias pistas mp3 en `assets/music/` (pueden ser playlists largas de ~1h).
   En cada corrida se elige un mp3 al azar y, si es más largo que el video, arranca
   en un punto aleatorio. Para repetir un render fija `music.seed` en `config.yaml`.
3. (Opcional) Imágenes propias en `assets/images/`, nombradas `<slug>.png` donde
   `<slug>` es la etiqueta del bloque en minúsculas sin espacios ni acentos
   (`intro.png`, `noticia_1.png`, `cierre.png`). `noticia_1.png` sirve también para
   las partes `noticia_1_p1`, `noticia_1_p2`, ... de una noticia larga. Si no hay
   imagen, se genera una tarjeta de titular.
4. Ajusta `config.yaml` (nombre del canal, voz, colores, etc.).
5. Corre todo:

```bash
python scripts/main.py --script input/guion.md
```

## Formato del guion

Dos formatos, detectados automáticamente:

**Con etiquetas (recomendado):** cada bloque empieza con una línea `[ETIQUETA]` o
`[ETIQUETA: Titular]`. El titular se muestra en la tarjeta; la etiqueta no se narra.

```
[INTRO]
Buenas a todos, bienvenidos...

[NOTICIA 1: La RAM se disparó y te va a doler el bolsillo]
Partamos por el fondo técnico...

[NOTICIA 2: Intel y ASML pasan el millón de obleas High-NA]
...

[CHILE: Datacenters, el cable Humboldt y la ley de datos]
...

[CIERRE]
Eso fue todo por esta semana...
```

Bloques más largos que `parsing.max_block_words` (220) se parten en sub-bloques con
el mismo titular y distinto extracto, para que la imagen cambie cada ~1,5 min.

**Sin etiquetas:** texto corrido; se agrupa en segmentos de ~130 palabras y el
titular de cada tarjeta es la primera oración del segmento.

En ambos casos:
- Todo lo que venga después de una línea `---` o de una línea `FUENTES` se saca del
  guion (no se narra) y se guarda en `output/fuentes.md`.
- Se eliminan URLs, `**negritas**`, `#` y viñetas antes de narrar.

## Estructura

```
noticiario-hardware/
├── README.md
├── prompt_noticiario_hardware.md   # prompt para generar el guion en claude.ai
├── requirements.txt
├── config.yaml
├── scripts/
│   ├── parse_script.py       # texto → bloques.json (+ fuentes.md)
│   ├── generate_audio.py     # bloques.json → audio/*.wav + manifest (edge-tts / piper)
│   ├── generate_visuals.py   # bloques.json → visuals/*.png (tarjetas de titular)
│   ├── assemble_video.py     # todo → output/video_final.mp4 (ffmpeg + NVENC)
│   └── main.py               # orquesta las 4 etapas y limpia intermedios
├── input/
│   └── guion.md
├── models/                   # voz de Piper (respaldo offline)
├── assets/
│   ├── images/               # imágenes propias opcionales
│   └── music/                # pistas de música de fondo
└── output/                   # video_final.mp4 + fuentes.md
```

## TODOs

- [ ] `generate_visuals.py`: imágenes reales (Pexels/Unsplash API) o generadas
      (Stable Diffusion) cuando no haya imagen propia.
- [ ] `generate_audio.py`: backend ElevenLabs/OpenAI TTS.
- [ ] `assemble_video.py`: subtítulos automáticos con Whisper.

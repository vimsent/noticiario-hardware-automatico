# Comparar el pipeline automático vs. pegar el prompt en claude.ai

Tutorial para hacer, de forma repetible, la comparación entre:

- **Método A — pipeline** (`start.py` / `redaccion.run_claude`): la ventana la arma código
  determinista (ingesta + ranking) y Claude Code solo selecciona, verifica y escribe.
- **Método B — manual**: pegas `prompt_noticiario_hardware_final.md` en claude.ai con búsqueda
  web activada, como se hacía antes de que existiera `start.py`.

## Qué pasó la vez anterior, para que no se repita

El 20 de septiembre la etapa de redacción del pipeline chocó con el límite de sesión a mitad de
camino. Para no perder la semana, se volvió al método manual — pero el resultado se pegó en
`input/guion.md`, que es el **mismo archivo** que usa `scripts/main.py` para armar el video y que
la etapa 3 del pipeline también escribe ahí. Unos días después, `scripts/main.py` renderizó ese
guion pegado a mano, y el video que salió no correspondía a ninguna corrida de `runs/<fecha>/`:
sus fuentes no estaban en `candidatas.json` ni en `barrido.json`, y sus noticias no coincidían con
las que el ranking había elegido. Nada se rompió — el validador de hecho detecta exactamente este
caso — pero quedó imposible saber después cuál método había producido ese video en particular.

**La causa de fondo:** dos métodos escribiendo en la misma ruta, sin ningún rastro de cuál escribió
qué. La regla de este documento es simple — **`input/guion.md` es solo del pipeline automático**;
el método manual nunca escribe ahí.

## Convención de carpetas

Todo lo que generes para comparar va en `comparaciones/<fecha_hasta>/`, una subcarpeta por
método:

```
comparaciones/
└── 2026-09-25/
    ├── pipeline/
    │   ├── guion.md              ← lo escribe la etapa 3, con --guion
    │   ├── output/video_final.mp4
    │   └── output/fuentes.md
    ├── manual/
    │   ├── guion.md              ← lo pegas tú desde claude.ai
    │   ├── output/video_final.mp4
    │   └── output/fuentes.md
    └── bitacora.md               ← tu comparación (plantilla más abajo)
```

`comparaciones/*/*/output/` está en `.gitignore` (son videos pesados); los `guion.md` y
`bitacora.md` sí quedan versionados, para poder revisar episodios de comparación antiguos.

## Paso a paso

Todo esto asume el venv activado: `source .venv/bin/activate`.

### 0. Define la ventana una sola vez

```bash
DESDE=2026-09-19
HASTA=2026-09-25
mkdir -p comparaciones/$HASTA/pipeline comparaciones/$HASTA/manual
```

### 1. Método A — pipeline

Corre ingesta y ranking normal (si ya los corriste hoy para esta ventana, sáltate estos dos):

```bash
python -m ingest.ingesta --desde $DESDE --hasta $HASTA
python -m rank.ranking   --desde $DESDE --hasta $HASTA
```

La etapa 3 es la única con un flag pensado justo para esto: `--guion` le cambia la ruta de salida
sin tocar `input/guion.md`.

```bash
python -m redaccion.run_claude --desde $DESDE --hasta $HASTA \
    --guion comparaciones/$HASTA/pipeline/guion.md
```

Esto también valida el guion contra `candidatas.json`/`barrido.json` y reintenta una vez si falla,
igual que siempre — la única diferencia es dónde queda escrito el resultado. Revisa el costo real
de esta corrida (ver la sección de costos más abajo).

Renderiza el video con `--output-dir` apuntando a la misma carpeta, para que tampoco compita con
`output/` ni con el otro método:

```bash
python scripts/main.py --script comparaciones/$HASTA/pipeline/guion.md \
    --output-dir comparaciones/$HASTA/pipeline/output
```

(`--output-dir` gobierna dónde cae el video final, no solo los intermedios — así que dos corridas
con `--output-dir` distinto nunca se pisan el video una a la otra.)

### 2. Método B — manual

1. Abre claude.ai, activa búsqueda web, pega `~/Descargas/prompt_noticiario_hardware_final.md`
   completo. Si no lo corres el mismo día que el Método A, ajusta el parámetro `VENTANA` del
   prompt para que apunte a la misma semana (`$DESDE` a `$HASTA`), si no la comparación no es justa.
2. Copia la respuesta completa — texto corrido y luego `GUION PARA TTS` si el prompt lo pide —
   directo a `comparaciones/$HASTA/manual/guion.md`. **Nunca a `input/guion.md`.**
3. Renderiza igual que el otro lado:

```bash
python scripts/main.py --script comparaciones/$HASTA/manual/guion.md \
    --output-dir comparaciones/$HASTA/manual/output
```

Si el guion pegado a mano no trae etiquetas `[NOTICIA n: ...]` bien formadas, el lint de
`scripts/main.py` te lo va a decir altiro (para eso está: revisa el guion antes de gastar minutos
en voz, sea de donde sea que vino el texto).

#### Ojo con qué prompt usas y qué pegas

**Si usas `prompt_noticiario_hardware_v2.md` (o el de redacción del pipeline) en claude.ai**, la
respuesta no es un guion solo: son varios archivos en un mismo mensaje, separados por líneas como
`=== ARCHIVO: guion.md ===`, `=== ARCHIVO: candidatas.md ===`, `=== ARCHIVO: historial.md ===`.
Si pegas la respuesta entera en `guion.md`, todo lo que viene después del guion (la tabla de
candidatas, los hilos del historial, el registro de leakers) queda pegado al `[CIERRE]` y se
narraría como parte del cierre. Pasó en la comparación del 2026-09-25: el cierre quedó en 12
bloques y 3.000 palabras.

Parte la respuesta por esos marcadores antes de guardar. Desde la raíz del repo:

```bash
python -c "
import re, pathlib
base = pathlib.Path('comparaciones/$HASTA/manual')
raw = (base / 'respuesta_completa.md').read_text(encoding='utf-8')
partes = re.split(r'^=== ARCHIVO: (.+?) ===\s*$', raw, flags=re.MULTILINE)
for nombre, contenido in zip(partes[1::2], partes[2::2]):
    (base / nombre.strip()).write_text(contenido.strip() + '\n', encoding='utf-8')
    print('escrito', base / nombre.strip())
"
```

O sea: pega la respuesta completa en `comparaciones/$HASTA/manual/respuesta_completa.md`, corre
eso, y te quedan `guion.md`, `candidatas.md` e `historial.md` por separado. Los dos últimos no se
usan para el video, pero sirven para comparar la selección de noticias contra la del pipeline.

**Marcadores de cita.** Con búsqueda web, claude.ai deja referencias numeradas pegadas al texto:
`...desde 2030.\[1\]\[2\]`. El lint las marca como error (una vez sin el `\` quedan como `[1]`,
igual que una etiqueta mal puesta, y la voz las leería). Quítalas antes de renderizar:

```bash
python -c "
import re, pathlib
p = pathlib.Path('comparaciones/$HASTA/manual/guion.md')
t = p.read_text(encoding='utf-8')
t = re.sub(r'(?:\\\\?\[\d+\\\\?\])+', '', t)
p.write_text(t, encoding='utf-8')
"
```

(Borra tanto `\[1\]` como `[1]`; no toca las etiquetas `[NOTICIA 1: ...]` porque esas tienen
texto además del número.)

### 3. Comparar

**Costo.** Del Método A sale de `runs/<fecha>/redaccion.log`, en la última línea (`"type":"result"`):

```bash
python -c "
import json
for l in open('runs/$HASTA/redaccion.log'):
    d = json.loads(l)
    if d.get('type') == 'result':
        print('costo (precio de lista):', d['total_cost_usd'])
        print('turnos:', d['num_turns'], '| websearch:', sum(
            m.get('webSearchRequests', 0) for m in d['modelUsage'].values()))
"
```

Del Método B no hay una cifra en dólares por mensaje — lo más parecido es el medidor de uso de tu
plan en claude.ai (si tu plan lo muestra). Compáralos como orden de magnitud, no como cifra exacta:
el `total_cost_usd` del pipeline es precio de lista de esos tokens, no necesariamente lo que se te
descuenta si estás en un plan de suscripción en vez de pago por uso.

**Calidad.** Mira los dos `guion.md` lado a lado y los dos videos. Usa la bitácora de abajo.

## Plantilla de bitácora (`comparaciones/<fecha>/bitacora.md`)

```markdown
# Comparación episodio N — <desde> a <hasta>

| | Pipeline | Manual |
|---|---|---|
| Costo / uso | | |
| Duración del guion (min) | | |
| Noticia principal elegida | | |
| ¿Coinciden las noticias secundarias? | | |
| Alucinaciones o datos no verificables | | |
| Tono / naturalidad | | |
| Bloque Chile | | |
| Notas |  |  |

**Veredicto:** ...
```

## Checklist para no volver a descuadrarse

- [ ] `input/guion.md` solo lo toca `start.py` / `redaccion.run_claude` sin `--guion`.
- [ ] Cualquier guion pegado a mano va directo a `comparaciones/<fecha>/manual/guion.md`.
- [ ] Cada render usa su propio `--output-dir` (nunca el `output/` por defecto para una comparación).
- [ ] Si la respuesta de claude.ai trae `=== ARCHIVO: ... ===`, se partió antes de guardar `guion.md`.
- [ ] Sin marcadores de cita `[1]`, `\[1\]` en el guion antes de renderizar.
- [ ] Ambos métodos con el mismo prompt base (v2 y `prompts/redaccion.md` comparten los temas
      prioritarios); si uno usa `prompt_noticiario_hardware_final.md`, anótalo en la bitácora
      porque no es una comparación pareja.
- [ ] Si algún día un video no coincide con ninguna corrida en `runs/`, es señal de que salió de un
      guion pegado a mano — no es un bug del pipeline, solo falta la bitácora de esa vez.

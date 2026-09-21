# CLAUDE.md — noticiario-hardware-automatico

> **Si fuiste invocado por `start.py` como etapa 3 (redacción):** este archivo no es tu tarea. Tu tarea completa está en `prompts/redaccion.md`. No modifiques código.
>
> Todo lo que sigue es la especificación de desarrollo, para las sesiones donde se trabaja en el código del repo.

## Qué es este repo

Pipeline que produce un noticiario semanal de hardware en video, con mirada chilena. Hoy el repo solo cubre la mitad final:

```
input/guion.md → parse_script.py → generate_audio.py → generate_visuals.py → assemble_video.py → output/video_final.mp4
```

El guion todavía se genera a mano en claude.ai. El objetivo de este trabajo es agregar tres etapas previas para que todo corra con un solo comando, sin depender de claude.ai:

```
python start.py --desde 2026-09-15 --hasta 2026-09-21

  1. ingesta    feeds RSS, Google News, comunidad y scrapers → texto completo → SQLite
  2. ranking    dedupe, agrupar artículos del mismo hecho, contar medios, etiquetar y ordenar → candidatas.json
  3. redacción  Claude Code en modo no interactivo lee candidatas.json, historial y leakers,
                hace un barrido de seguridad y escribe guion.md, candidatas.md, historial.md y leakers.md
  4. revisión   pausa para que el humano lea el guion (se salta con --sin-revision)
  5. video      scripts/main.py, el pipeline que ya existe
```

**Principio central.** La búsqueda de noticias la hace código determinista, no el modelo.

- Con la misma base de datos y las mismas fechas, las etapas 1 y 2 deben producir exactamente el mismo `candidatas.json`.
- El modelo solo selecciona, verifica y escribe.
- La única búsqueda web del modelo es el barrido de seguridad de eventos mayores.

## Reglas para trabajar en este repo

- **No romper el pipeline de video existente.** `scripts/main.py` y sus etapas deben seguir funcionando igual con un `input/guion.md` pegado a mano.
- **Estilo de código nuevo:**
  - Sin emojis.
  - Sin tildes ni eñes en identificadores, comentarios ni strings de log.
  - Comentarios mínimos.
  - Mayúsculas solo al inicio de oración, o para énfasis puntual.
  - Nombres en español, como el resto del repo.
  - No reescribas el código existente solo para cumplir este estilo.
- **Python 3.11+**, con type hints. Base de datos en `sqlite3` de la librería estándar, sin ORM.
- **Dependencias nuevas** van en `requirements.txt`:
  - `feedparser`
  - `trafilatura`
  - `httpx`
  - `rapidfuzz`
  - `selectolax` (para scrapers)
  - `pytest`
  - Cualquier otra, justificarla antes de agregarla.
- **Configuración** en `config.yaml` (secciones nuevas abajo) y la lista de fuentes en `feeds.yaml`. Nada de URLs ni umbrales hardcodeados en el código.
- **Tests sin red.** Usa fixtures con XML y HTML guardados en `tests/fixtures/`.
- **Cambios de a una etapa**, con sus tests, antes de pasar a la siguiente.
- **APIs externas no documentadas en este archivo** (formato de URL, parámetros, límites): verifícalas contra la documentación actual antes de implementarlas, y deja la fuente en el mensaje del commit.

## Estructura objetivo

```
start.py                     orquestador de las 5 etapas
config.yaml                  se agregan secciones ingesta, ranking, redaccion
feeds.yaml                   lista de fuentes
ingest/
  __init__.py
  rss.py                     feeds RSS y Atom genericos
  google_news.py             busquedas fijas como feed
  comunidad.py               reddit y hacker news
  scrapers_chile.py          paginas sin rss (usm, anid, etc)
  texto_completo.py          descarga y extraccion con trafilatura
  apoyo.py                   dolar observado y otros datos de contexto
  db.py                      esquema, conexion, upserts
rank/
  normalizar.py              urls canonicas, titulos normalizados, hash de texto
  agrupar.py                 clustering de articulos por hecho
  etiquetar.py               empresas, categoria, evento mayor, rumor y leaker
  puntuar.py                 puntaje preliminar determinista
  exportar.py                candidatas.json
redaccion/
  run_claude.py              invoca claude code y valida salidas
  validar.py                 validadores de guion.md y demas archivos
  barrido.py                 ingresa a la db lo que encontro el barrido
prompts/
  redaccion.md               prompt de la etapa 3
data/
  noticias.db                (gitignored)
  historial.md               versionado en git
  leakers.md                 versionado en git
runs/
  <fecha_fin>/               un directorio por episodio (gitignored salvo candidatas.md)
tests/
  fixtures/
```

## Etapa 1: ingesta

### feeds.yaml

Cada fuente tiene estos campos:

```yaml
- nombre: phoronix
  medio: Phoronix            # para contar medios independientes
  tipo: rss                  # rss | google_news | reddit | hn | scraper
  url: https://www.phoronix.com/rss.php
  categoria: hardware        # hardware | general | oficial | chile | comunidad
  idioma: en
  texto_completo: true
  activo: true
```

**Cobertura mínima inicial.** Verifica cada URL de feed antes de agregarla; si un sitio no tiene RSS, márcalo como scraper pendiente.

- **Hardware:** Phoronix, TechPowerUp, Tom's Hardware, VideoCardz, The Register, ServeTheHome, Ars Technica, Notebookcheck, Igor's Lab.
- **Oficiales:** salas de prensa de NVIDIA, AMD, Intel, Qualcomm, ARM, TSMC, Samsung, Micron y SK Hynix, las que tengan feed.
- **General y negocios:** al menos tres medios generales de tecnología o negocios con RSS público. Motivo: los eventos corporativos grandes suelen salir primero ahí.
- **Chile:** La Tercera, Diario Financiero, El Mostrador, BioBioChile, Emol, Pisapapeles, Subtel.
- **Google News:** una consulta por cada empresa de la lista de eventos mayores (ver etapa 2), más consultas temáticas de Chile ("data center Chile", "ley 21.719", "ANCI ciberseguridad", "ANID concurso", "Subtel").
  - Cada consulta es una entrada `tipo: google_news` con los campos `consulta`, `hl`, `gl` y `ceid`.
- **Comunidad:** r/hardware, r/Amd, r/nvidia, r/intel (top de la semana) y Hacker News vía la API de búsqueda de Algolia, filtrada por la ventana.

### Comportamiento

- **Rango de ingesta:** `desde - 7 días` hasta `hasta`. Los 7 días extra sirven para las noticias rezagadas.
- **Ingesta idempotente.** La clave única es la URL canónica: sin `utm_*`, sin fragmento, sin slash final y con el host en minúsculas. Correr dos veces no duplica nada. Si el artículo ya tiene texto, no se vuelve a descargar.
- **Fallas aisladas.** Una fuente que falla (timeout, 403, XML roto) nunca detiene la etapa. Se registra en `fuentes_estado` y se sigue con la siguiente.
- **Red:**
  - User-Agent propio y configurable.
  - Timeout de 20 segundos.
  - Dos reintentos con backoff.
  - Máximo 1 request por segundo por host.
  - Respetar robots.txt en los scrapers y en la descarga de texto completo.
- **Texto completo:** con `trafilatura`, solo para fuentes con `texto_completo: true`.
  - Si falla (paywall, bloqueo), queda el resumen del feed y el artículo se marca `texto_ok = 0`. Igual cuenta como cobertura.
- **Google News:**
  - Los links apuntan a news.google.com, no al medio.
  - Guarda el medio real que viene en el elemento `source` del item y úsalo en `medio`.
  - No intentes resolver la URL final en la v1: el artículo queda sin texto completo, pero suma al conteo de medios.
- **Comunidad:** guarda el puntaje (upvotes, points) en `score_comunidad`, y si el post enlaza a un artículo externo, en `url_enlazada`.
  - Reddit puede exigir autenticación o limitar el acceso anónimo. Verifica el método vigente y deja la alternativa en `config.yaml`.
- **Scrapers de Chile:** empieza con las noticias de Informática USM y los concursos de ANID. Cada scraper es una función que recibe HTML y devuelve una lista de artículos, testeada con fixtures.
  - Si el HTML cambió y el scraper no encuentra nada, registra una advertencia; no es un error.
- **apoyo.py:** obtiene el dólar observado del día (por ejemplo desde mindicador.cl) y lo guarda en `runs/<fecha_fin>/apoyo.json` con valor, fecha y fuente.
  - Los precios de tiendas chilenas (SoloTodo) quedan para una fase posterior. Deja el hook preparado.

### Esquema SQLite

```sql
create table articulos (
  id integer primary key,
  url text not null unique,          -- url canonica
  url_original text,
  url_enlazada text,                 -- solo comunidad
  feed text not null,                -- nombre en feeds.yaml
  fuente_tipo text not null,         -- rss | google_news | reddit | hn | scraper | barrido
  medio text not null,
  categoria_feed text not null,
  idioma text,
  titulo text not null,
  titulo_norm text not null,
  resumen text,
  texto text,
  texto_ok integer not null default 0,
  hash_texto text,                   -- para detectar sindicacion
  publicado_utc text not null,       -- iso 8601
  obtenido_utc text not null,
  score_comunidad integer
);

create table grupos (
  id integer primary key,
  run text not null,                 -- fecha_fin del episodio
  clave text not null,               -- id estable derivado de los articulos (ver etapa 2)
  titulo_repr text not null,
  fecha_hecho text not null,
  n_medios integer not null,
  medios text not null,              -- json, ordenado
  score_comunidad integer not null default 0,
  categoria text not null,
  empresas text not null,            -- json, ordenado
  evento_mayor integer not null default 0,
  es_rumor integer not null default 0,
  leakers text not null default '[]',
  es_chile integer not null default 0,
  rezagada integer not null default 0,
  score_prelim real not null,
  unique (run, clave)
);

create table grupo_articulos (
  grupo_id integer not null references grupos(id),
  articulo_id integer not null references articulos(id),
  primary key (grupo_id, articulo_id)
);

create table fuentes_estado (
  run text not null,
  feed text not null,
  ok integer not null,
  n_items integer not null,
  error text,
  ts_utc text not null
);
```

## Etapa 2: ranking

**Entrada:** la base de datos y las fechas.
**Salida:** las tablas `grupos` y `grupo_articulos` para ese run, y el archivo `runs/<fecha_fin>/candidatas.json`.

Todo es determinista. No se usan modelos de lenguaje en esta etapa.

### Pasos

1. **Selección.** Artículos con `publicado_utc` entre `desde - 7 días` y `hasta` (fin del día, hora de Chile, configurable).
   - Las entradas de comunidad sin enlace externo no forman grupo propio. Solo aportan `score_comunidad` si su título calza con un grupo existente.
2. **Normalización.** `titulo_norm` en minúsculas, sin tildes, sin puntuación y sin sufijos del medio (" - Tom's Hardware").
   - `hash_texto` sobre los primeros 2.000 caracteres normalizados del texto.
3. **Sindicación.** Artículos con el mismo `hash_texto` en medios distintos cuentan como un solo medio. Se usa el más antiguo.
4. **Agrupación.** Dos artículos van al mismo grupo si se cumplen tres condiciones:
   - comparten al menos una empresa detectada, o ambos no tienen empresa;
   - sus fechas están a 4 días o menos (configurable);
   - `rapidfuzz.fuzz.token_set_ratio` entre títulos es mayor o igual que el umbral (configurable, partir en 70).

   Detalles del algoritmo:
   - Usa union-find y procesa los pares en orden estable: fecha, luego id.
   - Los títulos en inglés y en español no van a calzar entre sí en la v1. Se acepta; queda como mejora futura con embeddings multilingües detrás de un flag `ranking.embeddings`, apagado por defecto.
5. **Campos del grupo:**
   - `titulo_repr`: el título del artículo del medio con más prioridad (configurable: oficiales primero), y si hay empate, el más antiguo.
   - `fecha_hecho`: la fecha del artículo más antiguo del grupo. Es una estimación; el modelo la verifica.
   - `n_medios`: la cantidad de valores distintos de `medio`, después de resolver la sindicación.
   - `clave`: sha1 de la URL del artículo más antiguo. Es estable entre corridas mientras ese artículo siga en el grupo.
   - `rezagada = 1` si la `fecha_hecho` es anterior a `desde`.
6. **Etiquetado** con diccionarios en `config.yaml`:
   - **Empresas:** NVIDIA, AMD, Intel, TSMC, Qualcomm, ARM, Apple, Samsung, SK Hynix, Micron, ASML, más alias.
   - **Categoría:** una sola por grupo: cpu, gpu, fabricacion, memoria, datacenter, software, industria, rumores, chile. Se asigna por coincidencia de keywords con prioridad fija; si no calza nada, va a `industria`.
   - **Evento mayor:** empresa de la lista más keyword de compra, fusión, quiebra, cambio de CEO, despidos masivos, control de exportación, demanda o resultados trimestrales, en inglés y español.
   - **Rumor:** keywords (leak, rumor, reportedly, filtración, supuestamente) o mención de un nombre presente en `data/leakers.md`. Los nombres de leakers detectados van a `leakers`.
   - **es_chile:** `categoria_feed = chile`, o menciones de Chile en título o resumen.
7. **Puntaje preliminar.** Solo sirve para ordenar y recortar; la rúbrica final la aplica el modelo.
   ```
   score_prelim = 3*log2(1 + n_medios)
                + 2*log10(1 + score_comunidad)
                + 4*evento_mayor
                + 1*(categoria_feed incluye oficial)
                - 1*es_rumor
   ```
   Los pesos van en `config.yaml`.
8. **Exportación a `candidatas.json`.** Se incluyen:
   - todos los grupos con `evento_mayor = 1`;
   - todos los grupos con `es_chile = 1` (máximo configurable, partir en 25);
   - los N grupos restantes de mayor `score_prelim` (configurable, partir en 50).

   **Orden** estable: `score_prelim` descendente, `n_medios` descendente, `fecha_hecho` descendente, `clave`.

   **Contenido de cada grupo:**
   - todos sus campos;
   - la lista de artículos (medio, título, URL, fecha, `texto_ok`);
   - el texto de hasta 3 artículos del grupo (priorizando oficiales y luego los más largos), truncado a 6.000 caracteres cada uno (configurable).

   **Encabezado del archivo:**
   - `desde` y `hasta`;
   - la fecha de generación;
   - el conteo total de artículos y grupos;
   - la lista de fuentes que fallaron, tomada de `fuentes_estado`.

   **Formato:** JSON con `sort_keys=True`, `ensure_ascii=False` e indentación de 2.

### Test obligatorio de determinismo

Con una base de fixtures, correr la etapa 2 dos veces debe producir un `candidatas.json` idéntico byte a byte, ignorando el campo de fecha de generación.

## Etapa 3: redacción

### prompts/redaccion.md

Se construye a partir de `prompt_noticiario_hardware_v2.md` (el humano lo deja en la raíz del repo). Mantén sin cambios las secciones de rol, rúbrica, reglas de selección, filtraciones y leakers, formato, estructura, estilo, localización, bloque Chile y reglas duras.

Cambia lo siguiente:

- **Parámetros.** Los inyecta `run_claude.py`: FECHA_INICIO, FECHA_FIN, EPISODIO, las rutas de entrada y salida y el dólar del día desde `apoyo.json`.
- **Fase 1 (barrido).** Se reemplaza por esta instrucción: "lee `runs/<fecha_fin>/candidatas.json`; esa es tu fuente de noticias". Se mantiene solo la parte de eventos mayores, convertida en el barrido de seguridad descrito más abajo.
- **Reglas de herramientas:**
  - **WebSearch:** solo para el barrido de seguridad.
  - **WebFetch:** permitido para URLs que estén en `candidatas.json` (verificar detalles de un artículo sin texto completo) y para precios en tiendas chilenas.
  - **Prohibido** buscar noticias nuevas por fuera del barrido.
- **Registro de leakers.** Vive en `data/leakers.md`, no dentro del historial. Mismo formato que la sección "Registro de leakers" del prompt v2.
- **Salidas en rutas fijas:**
  - `input/guion.md`
  - `runs/<fecha_fin>/candidatas.md`
  - `data/historial.md`
  - `data/leakers.md`
  - `runs/<fecha_fin>/barrido.json`
- **Sin respuesta final.** El modelo no escribe ningún texto de respuesta aparte de los archivos.

### Barrido de seguridad

El modelo busca en la web eventos mayores de las empresas de la lista en la ventana y en los 7 días previos. Compara cada hallazgo contra `candidatas.json` y escribe en `barrido.json` solo lo que no está:

```json
[
  {
    "hecho": "una linea",
    "fecha_hecho": "2026-09-03",
    "urls": ["https://..."],
    "medios": ["..."],
    "por_que_falto": "hipotesis breve: que tipo de fuente lo cubrio"
  }
]
```

Si un hallazgo del barrido cumple las reglas de selección, puede entrar al guion. En `candidatas.md` se marca como `BARRIDO`.

### run_claude.py

1. **Verificaciones previas:** que existan `candidatas.json`, `apoyo.json`, `prompts/redaccion.md`, `data/historial.md` y `data/leakers.md`.
   - Si no existen `historial.md` o `leakers.md`, créalos con la plantilla vacía. Es el primer episodio.
2. **Respaldo.** Copia `data/historial.md` y `data/leakers.md` a `runs/<fecha_fin>/antes/`.
3. **Invocación de Claude Code** en modo no interactivo (`claude -p`), desde la raíz del repo, con el prompt ya renderizado.
   - Revisa `claude --help` y la documentación vigente para los flags de:
     - restricción de herramientas: solo lectura y escritura de archivos, WebSearch y WebFetch, sin bash;
     - modo de permisos;
     - formato de salida.
   - Deja los flags en `config.yaml` (`redaccion.claude_args`), no en el código.
   - Timeout configurable (partir en 30 minutos).
   - Todo el stdout y el stderr van a `runs/<fecha_fin>/redaccion.log`.
4. **Validación de salidas** con `redaccion/validar.py`:
   - **guion.md:**
     - Primera etiqueta `[INTRO]`, luego `[NOTICIA 1: ...]`, luego de 4 a 6 `[NOTICIA n: ...]` consecutivas, luego `[CHILE: ...]` y al final `[CIERRE]`.
     - Titulares de 10 palabras o menos, sin punto final.
     - Ninguna otra etiqueta entre corchetes.
     - Una línea `---` seguida de `FUENTES` y al menos una viñeta con URL.
     - `parse_script.py` debe poder parsearlo sin error.
     - El conteo de palabras debe estar dentro del rango de `config.yaml`; si queda fuera, es advertencia, no error, porque una semana floja justifica un episodio corto.
     - **Lista de palabras prohibidas** (configurable): "revolucionario", "cambia las reglas del juego", "un antes y un después", "el presente análisis". Si aparecen, es error.
   - **Todas las URLs de FUENTES** deben estar en `candidatas.json` o en `barrido.json`. Si alguna no está, es error, porque indica una fuente inventada o una búsqueda fuera de las reglas.
   - **candidatas.md:** contiene una tabla con las columnas definidas en el prompt.
   - **historial.md y leakers.md:** no son más cortos que su respaldo, salvo que el diff solo mueva hilos a "Hilos inactivos". Así se detecta si el modelo resumió o borró historia.
   - **barrido.json:** es JSON válido con el esquema de arriba.
5. **Si la validación falla,** un solo reintento. El prompt del reintento agrega la lista exacta de errores y pide corregir los archivos existentes, no reescribir todo.
   - Si el reintento también falla, restaura el historial y los leakers desde el respaldo y termina con código de error.
6. **Si pasa,** `redaccion/barrido.py` inserta cada hallazgo de `barrido.json` en `articulos` con `fuente_tipo = 'barrido'`.
   - Además agrega una línea a `runs/barrido_acumulado.md` con la fecha y el `por_que_falto`.
   - Ese archivo es la lista de fuentes que hay que sumar a `feeds.yaml`.

## start.py

```
python start.py [--desde AAAA-MM-DD] [--hasta AAAA-MM-DD] [--episodio N]
                [--etapas 1,2,3,4,5] [--sin-revision] [--commit]
```

- **Fechas por defecto:** `hasta` = ayer y `desde` = `hasta - 6 días`, en hora de Chile.
- **Episodio por defecto:** el último episodio registrado en `data/historial.md` más 1.
- **Etapas:** corre las pedidas en orden. Cada etapa es un subproceso, igual que en `scripts/main.py`, y un error detiene todo con un mensaje claro de qué etapa falló y dónde está su log.
- **Etapa 4 (revisión):**
  - Imprime las rutas de `guion.md` y `candidatas.md`, más un resumen: titulares elegidos, cantidad de candidatas y hallazgos del barrido.
  - Espera Enter para continuar, o `q` para abortar sin renderizar.
- **Etapa 5:** llama `scripts/main.py --script input/guion.md`.
- **`--commit`:** al final hace `git add data/historial.md data/leakers.md runs/<fecha_fin>/candidatas.md` y un commit con el mensaje `episodio N (desde a hasta)`.
- **Log general** en `runs/<fecha_fin>/start.log`.

## Secciones nuevas de config.yaml

```yaml
ingesta:
  feeds_path: feeds.yaml
  db_path: data/noticias.db
  user_agent: "noticiario-hardware/0.1 (+https://github.com/vimsent/noticiario-hardware-automatico)"
  timeout_s: 20
  reintentos: 2
  req_por_seg_por_host: 1
  dias_rezagadas: 7
  zona_horaria: America/Santiago

ranking:
  umbral_titulo: 70
  ventana_agrupacion_dias: 4
  embeddings: false
  max_grupos: 50
  max_grupos_chile: 25
  max_articulos_con_texto: 3
  max_chars_texto: 6000
  pesos: {medios: 3, comunidad: 2, evento_mayor: 4, oficial: 1, rumor: -1}
  prioridad_medios: [oficial, hardware, general, chile, comunidad]
  empresas: {}          # nombre: [alias]
  categorias: {}        # categoria: [keywords], en orden de prioridad
  keywords_evento_mayor: []
  keywords_rumor: []

redaccion:
  prompt_path: prompts/redaccion.md
  claude_args: []       # completar tras revisar claude --help
  timeout_min: 30
  palabras_min: 1800
  palabras_max: 3000
  palabras_prohibidas: [revolucionario, "cambia las reglas del juego", "un antes y un despues", "el presente analisis"]
```

## Orden de implementación

1. `ingest/db.py` y el esquema, más `rank/normalizar.py`, con tests.
2. `ingest/rss.py` con 3 feeds reales y `feeds.yaml` mínimo. Probar a mano que llena la base.
3. `rank/` completo, con el test de determinismo.
4. Google News, comunidad, texto completo y `apoyo.py`.
5. `redaccion/validar.py` con tests. Usa como casos los guiones malos de ejemplo: uno con tono de informe y uno con etiquetas `[PLACA]` / `[IMAGEN]`.
6. `prompts/redaccion.md`, `run_claude.py` y `barrido.py`.
7. `start.py`.
8. Scrapers de Chile.
9. Completar `feeds.yaml` hasta la cobertura mínima.

## Criterios de aceptación

- `python start.py --etapas 1,2` corre sin intervención y deja un `candidatas.json` no vacío.
- Correr las etapas 1 y 2 dos veces seguidas no duplica artículos, y el `candidatas.json` resultante es idéntico salvo la fecha de generación.
- Una fuente caída no detiene la ingesta y aparece listada en `candidatas.json` y en `candidatas.md`.
- `python start.py --sin-revision` produce `output/video_final.mp4` y deja `data/historial.md` y `data/leakers.md` actualizados.
- Un guion con una URL que no está en `candidatas.json` ni en `barrido.json` es rechazado por el validador.
- `scripts/main.py` sigue funcionando solo con un guion pegado a mano.

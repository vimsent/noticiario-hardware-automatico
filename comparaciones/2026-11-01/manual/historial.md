# historial.md

Nota: este historial se creó desde cero en el episodio 2 (2026-10-02) porque el historial.md previo no vino adjunto. Si existía un historial del episodio 1, hay que fusionarlo con este a mano. Actualizado en el episodio 3 (2026-10-26). Actualizado en el episodio 4 (2026-11-01).

## HILO: escasez-memoria-ia
- Descripción: escasez y alza de precios de DRAM, HBM y NAND causada por la demanda de IA, con su impacto en productos de consumo.
- Estado actual: Micron (Q4 fiscal 2026, 30 de septiembre de 2026) reportó US$54.230 M de ingresos, un margen bruto de 86,8% y una guía de US$61.500 M ± 1.500 M para el Q1 fiscal 2027. Su CEO dice que la oferta estará mucho más apretada en 2027-2028 y que no se ve el equilibrio; más del 75% de la producción de 2027 ya está comprometida. Las fuentes no coinciden en si hablaba de años fiscales o calendario. Raspberry Pi subió US$12,50 sus modelos de 2 GB el 1 de octubre. La planta ID2 de Micron sacaría obleas a fines de 2028. Al 26 de octubre de 2026: TrendForce (30 de septiembre) proyectaba alzas de 10-15% en contratos de DRAM convencional y 15-20% en NAND para el 4T26; TrendForce News, citando al Commercial Times (20 de octubre), habla de cerca de 20% en DRAM tras ~80% en el Q2 y ~40% en el Q3 (las cifras no cuadran entre sí). ASML informó el 14 de octubre que el 46% de sus ventas de sistemas del Q3 fue a memoria y que ve clientes nuevos de EUV en DRAM. SK Hynix publica resultados Q3 el 28 de octubre y Samsung el 29 de octubre. Al 1 de noviembre de 2026: Intel (29 de octubre) reportó Q3 por US$16.500 M (+21% interanual), pero guió el Q4 en US$15.000-16.000 M contra ~US$17.000 M esperados; su acción cerró con -28,58% el 30 de octubre. El CFO prevé una caída de unidades de PC de ~12% en 2026 (más de 20% en el 2S26) y ~10% en 2027 por precio y disponibilidad de memoria (cifras de la transcripción de la llamada, Motley Fool, no de la SEC). CCPG: US$8.100 M (-5% interanual, -9% trimestral; volumen de CPUs de cliente -14%); DCAI: ~US$7.300 M (+78%), con alza de 54% en el precio promedio de servidores. SK Hynix (28 de octubre): ingresos de 104,62 billones de wones, margen operacional de 80%, LTAs con 14 clientes que cubren más de 50% de la capacidad de 2027 y 2028; según Chosun Biz, DRAM y HBM vendidas hasta 2029; escasez esperada hasta 2030. Samsung (29 de octubre): ingresos de 195,3 billones de wones, utilidad operacional de 107,4 billones; pérdida de 0,8 billones en la división DX; según BigGo, HBM de 2027 vendida y estrechez hasta 2028. TrendForce (28 de octubre): spot de NAND TLC 512 Gb -9,19% (spot, no contrato). AMD reporta el 3 de noviembre y NVIDIA el 17 de noviembre.
- Cubierto en: ep 2 (2026-10-02) como NOTICIA 1 — resultados récord de Micron, la HBM se come más oblea por bit, la EUV en el nodo 1-gamma, el alza de Raspberry Pi; opinión: no esperar que la RAM baje. ep 3 (2026-10-26) como REPETIDA, una frase dentro de NOTICIA 1 — la cifra de ~20% del Commercial Times contra el 10-15% de TrendForce; ninguna es baja. ep 4 (2026-11-01) como NOTICIA 1 (DESARROLLO): Intel se desploma por la caída del mercado de PC causada por la memoria; opinión: la escasez pasó a ser dato macro y vienen PCs con configuraciones más flacas (especulación). ep 4 (2026-11-01) como NOTICIA 2 (DESARROLLO): récords de SK Hynix y Samsung, memoria vendida hasta 2029 según prensa coreana, matiz del spot de NAND a la baja; opinión: no esperar DDR5 barata.
- Reabrir solo si: TrendForce u otro analista reporta una caída trimestral de precios contractuales de DRAM o NAND; un fabricante (Micron, Samsung o SK Hynix) recorta o adelanta su guía de oferta 2027-2030; se anuncia una fábrica nueva que adelante capacidad; AMD (3 de noviembre), NVIDIA (17 de noviembre) o Micron (Q1 fiscal 2027) reportan un quiebre en demanda de PC o en precios de memoria; Intel cambia su proyección de mercado de PC; la caída del spot de NAND se traslada a contratos; o hay un alza o baja de precios verificable en el retail chileno.

## HILO: control-exportacion-gpus-china
- Descripción: controles de exportación de EE.UU. sobre GPUs de IA hacia China y los casos de contrabando o triangulación.
- Estado actual: el 1 de octubre de 2026 arrestaron a Greg Lui (Earthmade Computer), acusado de enviar a China más de US$300 M en servidores con GPUs NVIDIA vía Malasia y Singapur; la acusación del gran jurado es del 29 de septiembre. Tiene tres cargos, con un máximo combinado de 50 años según las cifras del DOJ. Antecedentes: Wally Liaw (Super Micro), arrestado el 19 de marzo de 2026, se declaró no culpable y su juicio está fijado para el 2 de noviembre; en Taiwán, la fiscalía de Keelung acusó el 24 de agosto de 2026 a nueve personas por 130 servidores B300 (74 llegaron a China). Novedad al 26 de octubre: el 22 de octubre The Information reveló que Lava detectó 32 GPUs B300 en sistemas ligados a la red de China Telecom vía DCGM Exporter expuesto; según SDxCentral, Lava identificó 4.724 GPUs NVIDIA en total y advierte que la geolocalización por IP no es definitiva. NVIDIA no lo negó y dijo a Tom's Hardware que el desvío es menor a medio por ciento en casos judiciales recientes. IDC (13-14 de octubre) estima la participación de NVIDIA en IA de China en 34% en el 1S26. Al 1 de noviembre de 2026: corrección, el juicio de Liaw se postergó a marzo de 2027 (Fortune, 20 de agosto de 2026); su coacusado Willy Sun se declaró culpable el 8 de octubre en un acuerdo con la fiscalía (Bloomberg, 9 de octubre). El 29 de octubre el New York Times reportó que inteligencia de EE.UU. cree que Alice Huang, ejecutiva de Megaspeed (Singapur), pasaba información a Beijing y tenía relación cercana con Jensen Huang; NVIDIA dijo que el trato fue normal y que las acusaciones de desvío contra Megaspeed se investigaron y descartaron el año pasado; la cancillería china lo calificó de especulación (30 de octubre); la senadora Warren pidió respuestas. Sin acusación formal.
- Cubierto en: ep 2 (2026-10-02) como SECUNDARIA (NOTICIA 3) — acusación contra Greg Lui y la triangulación por el sudeste asiático; opinión: es jugar al topo. ep 3 (2026-10-26) como DESARROLLO (NOTICIA 4) — B300 detectadas en red de China Telecom por telemetría mal configurada; opinión: el argumento del porcentaje de NVIDIA es tramposo; debería mostrar verificación de ubicación. ep 4 (2026-11-01) como DESARROLLO (NOTICIA 4): reportaje del NYT sobre Megaspeed y Jensen Huang, respuestas oficiales, corrección de la fecha del juicio de Liaw y culpabilidad de Willy Sun; opinión: NVIDIA debería publicar una auditoría externa de ubicación de sus GPUs.
- Reabrir solo si: hay una condena, una declaración de culpabilidad o un sobreseimiento en los casos de Lui o Liaw (juicio de Liaw en marzo de 2027); hay acusación formal, sanción o investigación oficial contra Megaspeed o sus ejecutivos; NVIDIA o su directorio responden formalmente a la senadora Warren; EE.UU. cambia las reglas de exportación (nuevas licencias, nuevos países con requisitos, ley de Warren u otra); NVIDIA anuncia mecanismos de verificación de ubicación del hardware; o China Telecom, el gobierno chino o el de EE.UU. responden oficialmente al hallazgo de Lava.

## HILO: anci-ley-21663
- Descripción: implementación de la Ley 21.663 marco de ciberseguridad y la actividad regulatoria de la ANCI.
- Estado actual: el 1 de octubre de 2026 la ANCI anunció un portal ciudadano, una consulta pública durante octubre sobre autenticación multifactor (previa a un estándar obligatorio) y el primer CTF nacional en octubre. Más de 320 incidentes reportados en el primer semestre de 2026 (según DF). Summit UE-ANCI el 6 de octubre. Al 26 de octubre: inscripciones del primer Ejercicio Nacional de Ciberseguridad abiertas desde el 7 de octubre hasta el 27 de octubre; el ejercicio es en línea el 29 de octubre con 12 desafíos, nivel intermedio o superior, individual o por equipos. No se encontró publicado el texto de la consulta MFA. Al 1 de noviembre de 2026: el ejercicio se realizó el 29 de octubre; según la ANCI (vía Veredictum, 30 de octubre) hubo 1.047 inscritos válidos, 636 participantes, unos 400 equipos, 321 equipos con al menos un desafío resuelto y 21 con los 12; implementado por Hackrocks con apoyo del BID; se repetirá cada año. La ANCI ha calificado 1.154 instituciones como operadores de importancia vital (Tour Innovación). Sigue sin encontrarse el texto de la consulta MFA.
- Cubierto en: ep 2 (2026-10-02) como CHILE — los tres anuncios del Mes de la Ciberseguridad y el seminario PDI-USM con CTF. ep 3 (2026-10-26) como mención en CHILE — cierre de inscripciones del CTF nacional el 27 de octubre. ep 4 (2026-11-01) como CHILE (DESARROLLO): resultados del primer Ejercicio Nacional; opinión: casi 4 de cada 10 inscritos no se presentaron y falta el desglose por tipo de participante.
- Reabrir solo si: se publica el texto de la consulta MFA o el estándar obligatorio final; la ANCI publica resultados desglosados del ejercicio o el Boletín de Amenazas; se aplica la primera sanción bajo la ley; cambia la calificación de Operadores de Importancia Vital; o se anuncia la fecha del ejercicio de 2027.

## HILO: datacenters-chile
- Descripción: inversión, capacidad y polémicas (agua, energía, permisos ambientales) de los datacenters en Chile.
- Estado actual: Colliers (30 de septiembre de 2026) cuenta 36 data centers operando con 255 MW y 34 desarrollos futuros; ResearchAndMarkets habla de unos 39 operando. Alto Jahuel (Terranova) sería el primero eximido del SEIA. Al 1 de noviembre de 2026: según El Mercurio (26 de octubre, vía CPI), el Ministerio de Energía proyecta que la demanda eléctrica de data centers se cuadruplica hacia 2030, con compromisos de hiperescaladores sobre US$7.500 M y US$1.600 M en proyectos identificados hacia 2031; es proyección, sin proyecto nuevo aprobado.
- Cubierto en: ep 2 (2026-10-02) como CHILE — informe de Colliers y la exención ambiental de Alto Jahuel. ep 4 (2026-11-01) como REPETIDA, una frase en CHILE: proyección del Ministerio de Energía.
- Reabrir solo si: un proyecto concreto recibe aprobación o rechazo ambiental, se judicializa o recibe una nueva inversión anunciada con monto; cambian las reglas del SEIA para datacenters; se presenta la Ley de Redes Eléctricas con efecto directo sobre data centers; o hay un conflicto fechado por agua o energía.

## HILO: litio-baterias-chile
- Descripción: intentos de Chile de subir en la cadena del litio (cátodos, celdas, packs, BESS) más allá de la extracción y refinación
- Estado actual: NovaAndino Litio (Codelco + SQM) operativa desde fines de 2025 con contrato hasta 2060; Corfo revocó a BYD su condición de Productor Especializado el 26 de enero de 2026; el proyecto de Tsingshan/Yongqing fue declarado abandonado; sin planta de cátodos ni de celdas comprometida; Chile importa sus sistemas BESS. Al 26 de octubre de 2026: el litio marcó US$16.050/t el 20 de octubre (datos del Banco Central vía La Tercera), mínimo desde el 20 de enero (US$15.950); promedio de octubre ~US$17.513/t; máximo mensual en mayo (US$21.674). DF (14 de octubre): spot de Asian Metal en US$16.800/t, -42% desde máximos de mayo. GEM proyecta US$15.000-21.000/t para 2027. Según The Rio Times citando a La Tercera, el Informe de Finanzas Públicas estima US$1.289 M para Corfo en 2026 (no verificado en la fuente original). Salar Futuro ingresó su EIA el 10 de julio de 2026 (US$3.000 M); sin novedades del 12 al 26 de octubre. pv magazine (9 de octubre): desde agosto se aprobaron 17 proyectos solares con al menos 15.370,65 MWh de almacenamiento.
- Cubierto en: ep 3 (2026-10-26) como CHILE (DESARROLLO) — caída del precio del litio al mínimo desde enero; voces de GEM y KPMG; opinión: litio barato es el momento de negociar eslabones hacia abajo, pero no hubo ningún anuncio de planta.
- Reabrir solo si: anuncio oficial de planta de cátodos, celdas, packs o BESS con socio y fecha; adjudicación de la licitación de Albemarle con compromisos downstream; aprobación o rechazo ambiental de Salar Futuro; nueva política de precios preferentes o de concesibilidad del litio; o el precio del litio rompe de nuevo la tendencia (nuevo mínimo anual bajo US$15.950/t o recuperación sobre US$20.000/t).

## HILO: euv-high-na
- Descripción: adopción de la litografía EUV y High-NA EUV (ASML, TSMC, Samsung, Intel, memoria) y los intentos de China por desarrollar litografía EUV propia.
- Estado actual: ASML (14 de octubre de 2026) reportó ventas récord de 11.700 M EUR, utilidad de 5.000 M EUR y margen bruto de 57,5%; 4.100 M EUR en EUV con una High-NA vendida; 46% de las ventas de sistemas a memoria; guía 2026 de 44.000-45.000 M EUR. Intel expuso más de un millón de obleas con High-NA; Samsung la usará en producción masiva en 2028 (DRAM, según Quartz) y TSMC en 2030; iniciativa ASML-TSMC de máscaras de 12 pulgadas con línea piloto hacia 2031; clientes piden órdenes para 2029-2030; ASML estudia ampliar capacidad 2028 por sobre el 30%. Contradicción: Quartz/CNBC dicen que las ventas quedaron levemente bajo consenso en euros e Investing dice que lo superaron en dólares. China: Langdao Silex mostró (~15 de octubre) un prototipo de fuente de luz EUV de más de 15 W con 90% de componentes locales; producción masiva a 3-5 años según el personal del stand. Al 1 de noviembre de 2026: Micron (21 de octubre) sacó la DRAM 4F² de su roadmap, sigue con 6F², wafer bonding y luego DRAM 3D, y explora High-NA para generaciones futuras; SK Hynix (28 de octubre, según DigiTimes) extenderá la 6F² con EUV y mantiene 4F² y DRAM 3D en carpeta; CXMT empuja la 4F². Intel liberó el PDK 0.9 de Intel 14A en octubre (8-K del Q3).
- Cubierto en: ep 3 (2026-10-26) como NOTICIA 1 (rezagada) — resultados de ASML, qué es High-NA y el patrón múltiple, el peso de la memoria en sus ventas, máscaras de 12 pulgadas y el prototipo chino como contexto; opinión: la inversión en litografía no baja la RAM antes de 2028. ep 4 (2026-11-01) como mención dentro de NOTICIA 2: SK Hynix extiende 6F² con EUV, Micron abandona 4F² (contexto del 21 de octubre); explicación de 6F² contra 4F².
- Reabrir solo si: ASML publica resultados del Q4 2026 o cambia su guía; un fabricante (Samsung, SK Hynix, Micron, TSMC, Intel) anuncia fecha nueva de High-NA en producción; se anuncia un costo por máquina verificable; un fabricante anuncia producción de DRAM 4F² o 3D con fecha; China muestra una máquina EUV completa o un chip fabricado con EUV propia con evidencia independiente; o cambian los controles de exportación de equipos de litografía.

## Noticias puntuales
- ep 2 (2026-10-02) — NVIDIA DGX Spark de 64 GB desde US$4.999 (23 de octubre, solo vía OEMs); las fuentes no coinciden sobre si la versión de 128 GB cuesta US$4.699 o US$6.950.
- ep 2 (2026-10-02) — Beta de Ubuntu 26.10 (1 de octubre) con Linux 7.3 aún en RC; versión final el 15 de octubre y Linux 7.3 estable esperado el 18 de octubre. Mención breve: mejora del driver Xe para Battlemage en Linux 7.4.
- ep 2 (2026-10-02) — Seminario Internacional de Ciberseguridad PDI-USM (7 y 8 de octubre) con su primer CTF.
- ep 2 (2026-10-02) — USM: investigación en tecnología WAAM (Depto. de Ingeniería de Minas, Metalurgia y Materiales).
- ep 3 (2026-10-26) — AMD Adrenalin 26.10.1 (20 de octubre) lleva FSR 4.1 a toda la serie RX 6000 (modelo INT8 en shaders, solo escalado), Ryzen AI 9/AI Max 300 y 400 y Ryzen Z2; Xbox sin fecha.
- ep 3 (2026-10-26) — TSMC Q3 2026 (15 de octubre, rezagada): 46.720 M USD, margen bruto 66,4%, 2 nm el 8% de ingresos por obleas, guía Q4 52.300-54.300 M USD; mención de la advertencia de suministro de Lam Research (21 de octubre) y el avance de las fábricas de Intel en Arizona y Ohio (21 de octubre).
- ep 3 (2026-10-26) — Ventana de fusión de Linux 7.4: aceleración de la compilación (serie completa 36%/70%), workqueues 10-100x en colas ociosas, drivers EDAC huérfanos por parches de IA; estable a fines de diciembre.
- ep 3 (2026-10-26) — Entrevista a Travis Kirsch (AMD, vía MyNavi Tech+): Lisa Su propuso revivir el 5800X3D; AMD dice que no fue por la DDR5; solo cuatro Ryzen 3 nuevos a la venta.
- ep 4 (2026-11-01): Intel firma (26 de octubre) acuerdo definitivo para comprar Classiq, software cuántico; monto US$2.300 M según Calcalist o ~US$1.900 M según documento citado por Newsquawk (contradicción sin resolver); cierre esperado en el 1S27; Lip-Bu Tan era inversionista personal de Classiq según Calcalist y Ynet.
- ep 4 (2026-11-01): Linux 7.4-rc1 (fecha inferida 1 de noviembre): ventana de fusión récord de ~20 mil commits, árbol de ~41,6 M de líneas, HDMI 2.1 por defecto en AMDGPU, base para Zen 6, AMD PerfOpt para iGPUs Radeon, IPU8 para Nova Lake, soporte inicial de Apple M4 y Tensor G5; probable LTS con estable cerca del 20 de diciembre.

## Hilos inactivos
(Ninguno todavía.)

## REGISTRO DE LEAKERS

### kopite7kimi
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno usado en el guion del ep 2; su rumor del 21 de septiembre de 2026 sobre RTX 60 en 2028 quedó fuera de ventana y no se usó)
  - (ninguno usado en el guion del ep 3)
  - (ninguno usado en el guion del ep 4)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Kepler_L2
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno usado en el guion del ep 2)
  - (ninguno usado en el guion del ep 3)
  - (ninguno usado en el guion del ep 4; su rumor del 20 de octubre de 2026 sobre la RTX 6060 atrasada hasta 2029 quedó fuera de ventana y no se usó)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Jaykihn
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### HXL (@9550pro)
- Nivel: B
- Base del nivel: punto de partida editorial. Evidencia agregada en ep 3: su filtración de abril de 2026 sobre el regreso del Ryzen 7 5800X3D como edición aniversario de AM4 se cumplió (Tom's Hardware, 2 de junio de 2026). Un solo acierto documentado no basta para subirlo a A.
- Rumores registrados:
  - ep 3 (2026-10-26): (filtración de abril de 2026, mencionada de pasada) AMD relanzaría el Ryzen 7 5800X3D como edición del décimo aniversario de AM4; Tom's Hardware (17 de abril) lo reportó para la segunda mitad de 2026 y Wccftech para el Q2 2026 — resultado: CUMPLIDO (reanunciado en Computex 2026, Tom's Hardware, 2 de junio de 2026)
- Balance: cumplidos 1, fallidos 0, pendientes 0

### momomo_us
- Nivel: B
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Moore's Law Is Dead
- Nivel: C
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno usado en el guion del ep 2; sus afirmaciones de septiembre de 2026 sobre la RTX 6090 en 2027 y Zen 6 "Powderhorn" B0 quedaron fuera de ventana)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### RedGamingTech
- Nivel: C
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### MEGAsizeGPU
- Nivel: C
- Base del nivel: leaker que no está en la lista editorial; no se buscó su historial en esta sesión, así que queda en C.
- Rumores registrados:
  - (ninguno usado en el guion; un agregador lo cita diciendo que RTX 60 no llegaría antes de 2028, con fecha del 15 de septiembre de 2026, fuera de ventana)
- Balance: cumplidos 0, fallidos 0, pendientes 0

## Fuentes (ep 2)
Lista numerada de 35 URLs del episodio 2 (Micron/TechPowerUp, SEC press release Micron Q4 2026, 24/7 Wall St, tech-insider, Yahoo Finance Micron CFO, OMG Ubuntu Raspberry Pi, Hardware Busters Raspberry Pi 5, KuCoin/ThePCEnthusiast/VideoCardz/WindowsForum/Futunn sobre DGX Spark 64GB, Aduana.cl sobre impuestos y courier, The Register / Yahoo / AIWeekly sobre Greg Lui, Phoronix y OMG Ubuntu sobre Ubuntu 26.10 y Linux 7.3, preyproject / trendtic.cl / pdichile.cl / df.cl sobre ANCI y ciberseguridad, construnoticias / GlobeNewswire sobre datacenters Chile, portalinnova.cl sobre WAAM USM, SCMP sobre China EUV, CNBC sobre High NA EUV TSMC Samsung). Conservar esta sección tal cual en el historial actualizado y agregar las fuentes nuevas.

## Fuentes (ep 3)
1. https://investor.asml.com/static-files/44d4bee1-b2f9-41b7-b3f8-1bf28f993fe6
2. https://www.fool.com/earnings/call-transcripts/2026/10/14/asml-asml-q3-2026-earnings-call-transcript/
3. https://qz.com/asml-quarterly-earnings-profit-customers-orders-2030-101426
4. https://www.investing.com/news/transcripts/earnings-call-transcript-asml-tops-q3-2026-estimates-but-shares-fall-93CH-4948118
5. https://finance.yahoo.com/markets/stocks/articles/asml-holding-nv-asml-q3-090027829.html
6. https://www.tomshardware.com/tech-industry/semiconductors/china-startup-demoes-prototype-euv-light-source-15w-of-output-power-and-90-percent-domestic-components-still-years-away-from-viability
7. https://www.scmp.com/tech/big-tech/article/3370966/start-unveils-prototype-heart-euv-lithography-amid-china-chipmaking-push
8. https://www.trendforce.com/news/2026/10/20/news-dram-prices-seen-rising-20-qoq-in-4q26-despite-slower-gains-ai-demand-tight-supply-support-outlook/
9. https://www.trendforce.com/presscenter/news/20260930-13258.html
10. https://www.infobae.com/noticias/2026/10/26/dolar-hoy-en-chile-cotizacion-de-apertura-del-26-de-octubre/
11. https://www.infobae.com/noticias/2026/10/23/precio-del-dolar-hoy-en-chile-cotizacion-de-cierre-del-23-de-octubre/
12. https://www.tweaktown.com/news/114186/amd-confirms-fsr-4-1-expands-to-rx-6000-gpus-ryzen-laptops-handhelds-and-xbox-consoles/index.html
13. https://www.dlcompare.com/gaming-news/amd-confirms-fsr-4-1-is-coming-to-rx-6000-gpus-and-ryzen-powered-handhelds-86242
14. https://www.ntcompatible.com/story/amd-adrenalin-26101-driver-fsr-41-now-supports-rx-6000-cards
15. https://gamerheadlines.com/amd-fsr-4-1-radeon-rx-6000-xbox/
16. https://tech-insider.org/amd-fsr-4-1-six-year-old-rx-6000-gpus-2026/
17. https://www.cnn.com/2026/09/03/tech/nvidia-hugging-face-ai-acquisition
18. https://pr.tsmc.com/english/news/3346
19. https://www.sec.gov/Archives/edgar/data/1046179/000104617926000726/a3q26e_withguidancexfinal.htm
20. https://247wallst.com/investing/2026/10/22/chip-stocks-fall-as-supply-warning-deepens-ai-selloff-marvell-and-amd-sink-8-intel-drops-7/
21. https://www.bloomberg.com/news/articles/2026-10-21/intel-touts-factory-expansion-progress-in-sign-of-growing-demand
22. https://www.tomshardware.com/tech-industry/data-centers/illegal-nvidia-blackwell-ultra-b300-gpus-found-inside-state-owned-china-telecoms-network-nvidia-says-chip-smuggling-a-drop-in-the-bucket-insists-smuggling-remains-a-nonfactor
23. https://www.theinformation.com/briefings/nvidias-powerful-b300-chips-spotted-chinese-state-owned-network
24. https://www.sdxcentral.com/news/banned-nvidia-gpus-spotted-powering-telecom-cloud-workloads-in-china-report/
25. https://www.lebigdata.fr/nvidia-32-puces-b300-interdites-reperees-sur-un-reseau-lie-a-letat-chinois
26. https://www.phoronix.com/news/Linux-7.4-Kbuild
27. https://www.phoronix.com/news/Linux-7.4-Workqueue
28. https://www.phoronix.com/news/Linux-7.4-EDAC
29. https://www.phoronix.com/news/ASUS-UX3407NA-Linux-7.4
30. https://www.tomshardware.com/pc-components/cpus/amd-ceo-lisa-su-proposed-bringing-back-the-ryzen-7-5800x3d-set-plan-in-motion-before-ddr5-shortages-am4-cpu-considered-a-final-gift-to-loyal-fans-of-the-decade-old-socket
31. https://www.tomshardware.com/pc-components/cpus/amd-had-to-re-engineer-the-ryzen-7-5800x3d-for-a-re-release-10th-anniversary-edition-chip-had-a-whole-body-of-engineering-work-put-into-it
32. https://www.tomshardware.com/pc-components/cpus/amd-to-resurrect-ryzen-7-5800x3d-am4-with-10th-anniversary-edition-leaker-claims-return-of-legendary-cpu-a-sign-of-bleak-pc-building-landscape
33. https://wccftech.com/amd-ryzen-7-5800x3d-reportedly-making-a-comeback-in-q2-2026-as-am4-turns-10/
34. https://www.latercera.com/pulso/noticia/el-precio-del-litio-retrocede-en-octubre-a-su-nivel-mas-bajo-desde-enero/
35. https://www.df.cl/mercados/commodities/los-precios-del-litio-acaban-de-borrar-todas-sus-alzas-de-2026-por-las
36. https://www.riotimesonline.com/chile-lithium-price-october-2026/
37. https://larazon.bo/economia-y-empresa/2026/10/23/el-precio-del-litio-cae-a-us-17-513-la-tonelada-en-octubre/
38. http://www.pv-magazine-latam.com/2026/10/09/chile-aprueba-desde-agosto-17-proyectos-con-1-35812-mw-solares-y-al-menos-15-37065-mwh-de-almacenamiento/
39. https://www.trendtic.cl/2026/10/anci-abre-inscripciones-para-el-primer-ejercicio-nacional-de-ciberseguridad/
40. https://anci.gob.cl/eventos/
41. https://www.sec.gov/Archives/edgar/data/0002120882/000119312526430985/d132707d6k.htm

## Fuentes

1. [ASML Q3 2026: record €11.7 billion sales, margin beat, supply gap](https://vestedfinance.com/blog/us-stocks/asml-q3-earnings-2026/)
2. [ASML 2026 third-quarter results Veldhoven, the Netherlands October 14, 2026](https://investor.asml.com/static-files/44d4bee1-b2f9-41b7-b3f8-1bf28f993fe6)
3. [ASML Q3 2026 earnings: net income climbs to €5B](https://www.stocktitan.net/sec-filings/ASML/6-k-asml-holding-nv-current-report-foreign-issuer-d706c81f3750.html)
4. [Dólar hoy en Chile: cotización de apertura del 26 de octubre - Infobae](https://www.infobae.com/noticias/2026/10/26/dolar-hoy-en-chile-cotizacion-de-apertura-del-26-de-octubre/)
5. [Earnings call transcript: ASML tops Q3 2026 estimates but shares fall By Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-asml-tops-q3-2026-estimates-but-shares-fall-93CH-4948118)
6. [ASML Q3 2026 earnings: profit beats, customers eye 2030 orders](https://qz.com/asml-quarterly-earnings-profit-customers-orders-2030-101426)
7. [AI Server Demand Sustains Memory Contract Price Increases in 4Q26, While Consumer-Side Pressure Persists, Says TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html)
8. [[News] DRAM Prices Seen Rising 20% QoQ in 4Q26 Despite Slower Gains; AI Demand, Tight Supply Support Outlook](https://www.trendforce.com/news/2026/10/20/news-dram-prices-seen-rising-20-qoq-in-4q26-despite-slower-gains-ai-demand-tight-supply-support-outlook/)
9. [China startup demoes prototype EUV light source — 15W of output power and 90% domestic components, still years away from viability](https://www.tomshardware.com/tech-industry/semiconductors/china-startup-demoes-prototype-euv-light-source-15w-of-output-power-and-90-percent-domestic-components-still-years-away-from-viability)
10. [Start-up unveils prototype 'heart' of EUV lithography amid China chipmaking push](https://www.scmp.com/tech/big-tech/article/3370966/start-unveils-prototype-heart-euv-lithography-amid-china-chipmaking-push)
11. [Chinese Startup Unveils First EUV Light Source Prototype To Challenge ASML's Monopoly, But Dutch Firm Won't Be Losing Any Sleep Over This Progress](https://wccftech.com/chinese-startup-euv-light-source-prototype-asml/)
12. [News Archive](https://www.tomshardware.com/news/archive)
13. [AMD Software Adrenalin 26.10.1 WHQL Driver Brings FSR 4.1 Support to Radeon RX 6000 GPUs - eTeknix](https://www.eteknix.com/amd-software-adrenalin-26-10-1-whql-driver-brings-fsr-4-1-support-to-radeon-rx-6000-gpus/)
14. [AMD FSR 4.1 Comes To Radeon RX 6000 GPUs, Xbox Support Coming Soon](https://gamerheadlines.com/amd-fsr-4-1-radeon-rx-6000-xbox/)
15. [AMD confirms FSR 4.1 expands to RX 6000 GPUs, Ryzen laptops, handhelds, and Xbox consoles](https://www.tweaktown.com/news/114186/amd-confirms-fsr-4-1-expands-to-rx-6000-gpus-ryzen-laptops-handhelds-and-xbox-consoles/index.html)
16. [AMD confirms FSR 4.1 is coming to RX 6000 GPUs and Ryzen-powered handhelds](https://www.dlcompare.com/gaming-news/amd-confirms-fsr-4-1-is-coming-to-rx-6000-gpus-and-ryzen-powered-handhelds-86242)
17. [AMD FSR 4.1 Hits RX 6000 GPUs: Real Cost Explained](https://tech-insider.org/amd-fsr-4-1-six-year-old-rx-6000-gpus-2026/)
18. [AMD Adrenalin 26.10.1 Driver: FSR 4.1 Now Supports RX 6000 Cards](https://www.ntcompatible.com/story/amd-adrenalin-26101-driver-fsr-41-now-supports-rx-6000-cards)
19. [Nvidia inks $13 billion deal to buy the AI startup that was hacked by OpenAI](https://www.cnn.com/2026/09/03/tech/nvidia-hugging-face-ai-acquisition)
20. [NVIDIA to Acquire Hugging Face](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/)
21. [TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD - Form 6-K - FY2026](https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000726/a3q26e_withguidancexfinal.htm)
22. [Document](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000726/a3q26e_withguidancexfinal.htm)
23. [Chip Stocks Fall as Supply Warning Deepens AI Selloff: Marvell and AMD Sink 8%, Intel Drops 7% - 24/7 Wall St.](https://247wallst.com/investing/2026/10/22/chip-stocks-fall-as-supply-warning-deepens-ai-selloff-marvell-and-amd-sink-8-intel-drops-7/)
24. [Intel Touts Factory Expansion Progress in Sign of Growing Demand - Bloomberg](https://www.bloomberg.com/news/articles/2026-10-21/intel-touts-factory-expansion-progress-in-sign-of-growing-demand)
25. [Man Charged With Illegally Shipping Nvidia Chips to China - Bloomberg](https://www.bloomberg.com/news/articles/2026-10-02/man-charged-by-us-with-illegally-shipping-nvidia-chips-to-china)
26. [Banned Nvidia GPUs spotted powering telecom, cloud workloads in China: report - SDxCentral](https://www.sdxcentral.com/news/banned-nvidia-gpus-spotted-powering-telecom-cloud-workloads-in-china-report/)
27. [Nvidia's Powerful B300 Chips Spotted on Chinese State-Owned Network — The Information](https://www.theinformation.com/briefings/nvidias-powerful-b300-chips-spotted-chinese-state-owned-network)
28. [Nvidia : 32 puces B300 interdites repérées sur un réseau lié à l'État chinois ?](https://www.lebigdata.fr/nvidia-32-puces-b300-interdites-reperees-sur-un-reseau-lie-a-letat-chinois)
29. [32 export-controlled Nvidia Blackwell Ultra B300 GPUs detected on China Telecom network](https://mezha.net/eng/news/mezha-081c71eded7893de6d627b5e_32_export-controlled_nvidia)
30. [Nvidia B300 restringidas halladas en red de China Telecom](https://foro3d.com/2026/octubre/nvidia-b300-restringidas-halladas-en-red-de-china-telecom.html)
31. [Linux 7.4 Begins Landing Patches To Speed Up The Kernel Build Process - Phoronix](https://www.phoronix.com/news/Linux-7.4-Kbuild)
32. [Linux 7.4 Workqueue Changes Bring A "10 To 100 Times Faster" Optimization - Phoronix](https://www.phoronix.com/news/Linux-7.4-Workqueue)
33. [Linux 7.4 Sunsetting Old EDAC Drivers Due To "AI Generated Fixes Frenzy" - Phoronix](https://www.phoronix.com/news/Linux-7.4-EDAC)
34. [Linux 7.4 To Upstream Support For Three Snapdragon X2 Elite Laptops - Phoronix](https://www.phoronix.com/news/ASUS-UX3407NA-Linux-7.4)
35. [AMD Ryzen 7 5800X3D Returns as AM4's Anniversary Upgrade: BIOS Compatibility and AM5 Support](https://windowsforum.com/news/amd-ryzen-7-5800x3d-returns-as-am4s-anniversary-upgrade-bios-compatibility-and-am5-support.449921/)
36. [AMD CEO Lisa Su proposed bringing back the Ryzen 7 5800X3D, set plan in motion before DDR5 shortages — AM4 CPU considered a 'final gift' to loyal fans of the decade-old socket](https://www.tomshardware.com/pc-components/cpus/amd-ceo-lisa-su-proposed-bringing-back-the-ryzen-7-5800x3d-set-plan-in-motion-before-ddr5-shortages-am4-cpu-considered-a-final-gift-to-loyal-fans-of-the-decade-old-socket)
37. [All content Archive](https://www.tomshardware.com/archive)
38. [AMD Ryzen 7 5800X3D Is Making A Comeback In Q2 2026 As AM4 Turns 10](https://wccftech.com/amd-ryzen-7-5800x3d-reportedly-making-a-comeback-in-q2-2026-as-am4-turns-10/)
39. [AMD Revives Ryzen 7 5800X3D as Final Gift for AM4 Users - Memesita](https://www.memesita.com/amd-revives-ryzen-7-5800x3d-as-final-gift-for-am4-users/)
40. [AMD to resurrect Ryzen 7 5800X3D AM4 with 10th anniversary edition, leaker claims — return of legendary CPU a sign of bleak PC building landscape](https://www.tomshardware.com/pc-components/cpus/amd-to-resurrect-ryzen-7-5800x3d-am4-with-10th-anniversary-edition-leaker-claims-return-of-legendary-cpu-a-sign-of-bleak-pc-building-landscape)
41. [AMD 'had to re-engineer' the Ryzen 7 5800X3D for a re-release — 10th Anniversary Edition chip had 'a whole body of engineering work' put into it](https://www.tomshardware.com/pc-components/cpus/amd-had-to-re-engineer-the-ryzen-7-5800x3d-for-a-re-release-10th-anniversary-edition-chip-had-a-whole-body-of-engineering-work-put-into-it)
42. [El precio del litio retrocede en octubre a su nivel más bajo desde enero - La Tercera](https://www.latercera.com/pulso/noticia/el-precio-del-litio-retrocede-en-octubre-a-su-nivel-mas-bajo-desde-enero/)
43. [El precio del litio cae a $us 17.513 la tonelada en octubre - La Razón](https://larazon.bo/economia-y-empresa/2026/10/23/el-precio-del-litio-cae-a-us-17-513-la-tonelada-en-octubre/)
44. [Chile Lithium Price Falls to US$16,050, Lowest Since Jan](https://www.riotimesonline.com/chile-lithium-price-october-2026/)
45. [Litio: el precio cae 42% y borra sus alzas de 2026](https://ecosistemastartup.com/litio-el-precio-cae-42-y-borra-sus-alzas-de-2026/)
46. [Los precios del litio acaban de borrar todas sus alzas de 2026 por las expectativas de una sobreoferta el próximo año](https://www.df.cl/mercados/commodities/los-precios-del-litio-acaban-de-borrar-todas-sus-alzas-de-2026-por-las)
47. [Chile aprueba desde agosto 17 proyectos con 1.358,12 MW solares y al menos 15.370,65 MWh de almacenamiento - pv magazine Latinoamérica](http://www.pv-magazine-latam.com/2026/10/09/chile-aprueba-desde-agosto-17-proyectos-con-1-35812-mw-solares-y-al-menos-15-37065-mwh-de-almacenamiento/)
48. [Agencia Nacional de Ciberseguridad](https://anci.gob.cl/)
49. [ANCI abre inscripciones para el primer Ejercicio Nacional de Ciberseguridad](https://www.trendtic.cl/2026/10/anci-abre-inscripciones-para-el-primer-ejercicio-nacional-de-ciberseguridad/)

## Fuentes (ep 4)
1. https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000188/q326earningsrelease.htm
2. https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm
3. https://www.fool.com/earnings/call-transcripts/2026/10/30/intel-intc-q3-2026-earnings-call-transcript/
4. https://techcrunch.com/2026/10/30/intels-stock-crashes-knocking-12b-from-governments-stake/
5. https://247wallst.com/investing/2026/10/30/intel-plunges-25-as-weak-outlook-and-pc-slump-overshadow-earnings-beat-dell-tumbles-13-amd-sinks-10-nvidia-falls-3/
6. https://www.marketbeat.com/earnings/reports/2026-10-29-intel-co-stock/
7. https://en.sedaily.com/international/2026/10/30/intel-shares-plunge-as-memory-crunch-hits-pc-chip-demand
8. https://si3.bcentral.cl/Bdemovil/BDE/Series/MOV_SC_TC1
9. https://www.latercera.com/pulso/noticia/el-valor-del-dolar-en-chile-el-30-de-octubre-de-2026/
10. https://news.skhynix.com/en/q3-2026-business-results/
11. https://www.trendforce.com/news/2026/10/28/news-sk-hynix-3q26-opm-hits-record-80-says-dram-hbm-effectively-sold-out-to-2029-14-lta-customers-signed/
12. https://finance.yahoo.com/markets/stocks/articles/etfs-focus-sk-hynix-reports-145800137.html
13. https://news.samsung.com/global/samsung-electronics-announces-third-quarter-2026-results
14. https://www.sammobile.com/news/samsung-record-breaking-profit-usd-80-5-billion-q3-2026
15. https://finance.biggo.com/news/KR_005930.KS_2026-10-29
16. https://www.digitimes.com/news/a20261028VL220/sk-hynix-dram-cxmt-euv-technology.html
17. https://www.tomshardware.com/pc-components/dram/micron-pulls-the-plug-on-future-4f2-dram-after-two-decades-of-research-in-dramatic-shift-company-says-architecture-offers-no-meaningful-density-advantages-increases-manufacturing-complexity-and-costs-and-has-fundamental-scaling-limitations
18. https://www.trendforce.com/news/2026/10/28/insights-memory-spot-price-update-nand-spot-price-cuts-accelerate-amid-china-phone-discounts-512gb-tlc-sink-9-19/
19. https://www.intc.com/news-events/press-releases/detail/1784/intel-to-acquire-classiq-to-create-a-full-stack-quantum
20. https://www.calcalistech.com/ctechnews/article/psr5mmhcl
21. https://www.ynetnews.com/business/article/rkd8qnanme
22. https://www.newsquawk.com/headlines/intel-intc-says-it-entered-into-a-definitive-agreement-in-october-2026-to-acquire-100-of-classiq-technologies-for-approximately-usd-19bln-according-to-a-filing
23. https://thequantuminsider.com/2026/10/26/intel-to-acquire-classiq-to-create-a-full-stack-quantum-computing-platform/
24. https://www.cnbc.com/2026/10/29/nvidia-jensen-huang-chinese-intelligence-asset.html
25. https://www.bloomberg.com/news/articles/2026-10-29/nvidia-ceo-says-ties-to-company-under-spying-probe-were-normal
26. https://www.euronews.com/2026/10/30/china-rejects-report-of-spy-plot-targeting-nvidias-jensen-huang
27. https://finance.yahoo.com/markets/stocks/articles/nvidia-ceo-jensen-huang-may-193307067.html
28. https://thehill.com/policy/technology/6181938-nvidia-huang-china-intelligence-report/
29. https://fortune.com/2026/08/20/supermicro-investigation-ceo-nvidia-smuggling/
30. https://www.bloomberg.com/news/articles/2026-10-09/super-micro-case-fixer-pleads-guilty-to-diverting-ai-servers
31. https://www.phoronix.com/news/Linux-7.4-rc1
32. https://www.phoronix.com/news/Linux-7.4-Massive-Window
33. https://www.phoronix.com/news/Linux-7.4-Merge-Window
34. https://veredictum.cl/ciberseguridad-636-compitieron-en-primer-ejercicio-nacional/
35. https://www.tourinnovacion.cl/actualidad/primer-ejercicio-nacional-de-ciberseguridad-con-324-incidentes-significativos-en-seis-meses-las-empresas-tambien-deberian-ensayar-su-respuesta/
36. https://cpichile.org/proyecciones-y-desafios-ministerio-de-energia-proyecta-que-demanda-electrica-de-data-centers-se-cuadruplicara-hacia-2030/

## Fuentes

1. [INTEL CORP - Form 8-K - FY2026](https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000188/q326earningsrelease.htm)
2. [Intel (INTC) Q3 2026 Earnings Results & Call Transcript](https://www.marketbeat.com/earnings/reports/2026-10-29-intel-co-stock/)
3. [Intel shares plunge 23% after weak forecast as chip supply shortages threaten growth](https://americanbazaaronline.com/2026/10/30/intel-shares-plunge-23-after-weak-forecast-as-chip-supply-shortages-threaten-growth/)
4. [Intel Shares Plunge as Memory Crunch Hits PC Chip Demand - Seoul Economic Daily](https://en.sedaily.com/international/2026/10/30/intel-shares-plunge-as-memory-crunch-hits-pc-chip-demand)
5. [Intel Stock Plunge: 25% Premarket Drop \[2026\]](https://shattered.io/intel-falls-25-percent-premarket-guidance-gap-chip-rout-2026/)
6. [Intel (INTC) Q3 2026 Earnings Call Transcript | The Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/10/30/intel-intc-q3-2026-earnings-call-transcript/)
7. [Intel's stock crashes, knocking \$12B from government's stake](https://techcrunch.com/2026/10/30/intels-stock-crashes-knocking-12b-from-governments-stake/)
8. [Intel Corp Earnings - Analysis & Highlights for Q3 2026](https://www.alpha-sense.com/earnings/intc/)
9. [INTEL CORP - Form 10-Q - FY2026](https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm)
10. [Intel Corp (INTC) Q3 2026 Earnings Call Highlights: Data Center Surge and Foundry Progress ...](https://finance.yahoo.com/markets/stocks/articles/intel-corp-intc-q3-2026-051348065.html)
11. [Intel Q3 2026 Earnings Data Center Soars While PC Faces Memory Pressure - ServeTheHome](https://www.servethehome.com/intel-q3-2026-earnings-data-center-foundry-client/)
12. [Intel Plunges 25% as Weak Outlook and PC Slump Overshadow Earnings Beat; Dell Tumbles 13%, AMD Sinks 10%, NVIDIA Falls 3% - 24/7 Wall St.](https://247wallst.com/investing/2026/10/30/intel-plunges-25-as-weak-outlook-and-pc-slump-overshadow-earnings-beat-dell-tumbles-13-amd-sinks-10-nvidia-falls-3/)
13. [AMD to Report Fiscal Third Quarter 2026 Financial Results - AMD Newsroom](https://newsroom.amd.com/news/earnings-date-3q-2026/)
14. [El dólar sube en el balance de octubre y el tipo de cambio registra su quinto mes consecutivo al alza - La Tercera](https://www.latercera.com/pulso/noticia/el-valor-del-dolar-en-chile-el-30-de-octubre-de-2026/)
15. [Banco Central - Base de datos Estadísticos](https://si3.bcentral.cl/Bdemovil/BDE/Series/MOV_SC_TC1)
16. [Samsung Electronics Announces Third Quarter 2026 Results](https://news.samsung.com/global/samsung-electronics-announces-third-quarter-2026-results)
17. [Samsung earns record-breaking profit of \$80.5 billion, thanks to memory chips - SamMobile](https://www.sammobile.com/news/samsung-record-breaking-profit-usd-80-5-billion-q3-2026)
18. [\[News\] SK hynix 3Q26 OPM Hits Record 80%; Says DRAM, HBM Effectively Sold Out to 2029, 14 LTA Customers Signed](https://www.trendforce.com/news/2026/10/28/news-sk-hynix-3q26-opm-hits-record-80-says-dram-hbm-effectively-sold-out-to-2029-14-lta-customers-signed/)
19. [SK hynix Announces 3Q26 Financial Results](https://news.skhynix.com/en/q3-2026-business-results/)
20. [\[삼성전자 Q3 2026 Earnings Call\] Samsung Posts First-Ever KRW 100 Trillion Quarterly Operating Profit as AI Memory Demand Sells Out 2027 HBM Supply — BigGo Finance](https://finance.biggo.com/news/KR_005930.KS_2026-10-29)
21. [SK Hynix bets on EUV to extend 6F² DRAM as CXMT pushes 4F²](https://www.digitimes.com/news/a20261028VL220/sk-hynix-dram-cxmt-euv-technology.html)
22. [CXMT Completes Validation of 4F² DRAM Prototype, Kicking Off Commercialization Ahead of Samsung and SK Hynix — BigGo Finance](https://finance.biggo.com/news/a68f4d67-0e12-4def-b2f4-449160328760)
23. [Micron skips 4F² DRAM in strategic pivot against Samsung, SK Hynix and CXMT - Sammy Fans](https://www.sammyfans.com/2026/10/21/micron-skips-4f2-dram-scaling/)
24. [Intel to Acquire Classiq to Create a Full-stack Quantum Computing Platform](https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-classiq-accelerate-scalable-quantum-computing.html)
25. [Intel to Acquire Classiq to Create a Full-stack Quantum Computing Platform :: Intel Corporation (INTC)](https://www.intc.com/news-events/press-releases/detail/1784/intel-to-acquire-classiq-to-create-a-full-stack-quantum)
26. [Intel to Acquire Classiq: Strategic Move Creates Full-Stack Quantum Computing Platform - Quantum Computing Report](https://quantumcomputingreport.com/intel-to-acquire-classiq/)
27. [Intel to Acquire Classiq to Create a Full-stack Quantum Computing Platform](https://thequantuminsider.com/2026/10/26/intel-to-acquire-classiq-to-create-a-full-stack-quantum-computing-platform/)
28. [“Intel will be among the first names people think of in quantum computing,” says Classiq CEO](https://www.calcalistech.com/ctechnews/article/psr5mmhcl)
29. [Intel to acquire Israeli quantum startup Classiq for \$2.3 billion in record deal](https://www.ynetnews.com/business/article/rkd8qnanme)
30. [Nvidia responds to report Jensen Huang was target of Chinese asset, says diversion allegations were 'investigated and debunked'](https://www.cnbc.com/2026/10/29/nvidia-jensen-huang-chinese-intelligence-asset.html)
31. [Nvidia dismisses reports of alleged espionage targeting CEO Jensen Huang](https://thehill.com/policy/technology/6181938-nvidia-huang-china-intelligence-report/)
32. [Jensen Huang China Spy Report: 4 Facts Verified \[2026\]](https://tech-insider.org/jensen-huang-chinese-spy-report-alice-huang-megaspeed-2026/)
33. [Nvidia defends billionaire Jensen Huang in China spy report](https://www.billionaires.africa/2026/10/31/american-chip-billionaire-jensen-huangs-nvidia-defends-his-meetings-with-suspected-chinese-spy/)
34. [China rejects report of spy plot targeting Nvidia's Jensen Huang](https://www.euronews.com/2026/10/30/china-rejects-report-of-spy-plot-targeting-nvidias-jensen-huang)
35. [Nvidia's Huang Defends Megaspeed Ties as US Probes China Spying Allegations - Bloomberg](https://www.bloomberg.com/news/articles/2026-10-29/nvidia-ceo-says-ties-to-company-under-spying-probe-were-normal)
36. [Nvidia CEO Jensen Huang May Have Been Targeted by Chinese Spy Plot. What It Means for NVDA Stock.](https://finance.yahoo.com/markets/stocks/articles/nvidia-ceo-jensen-huang-may-193307067.html)
37. [Supermicro investigation clears CEO in \$2.5 billion alleged smuggling scheme](https://fortune.com/2026/08/20/supermicro-investigation-ceo-nvidia-smuggling/)
38. [Super Micro Case ‘Fixer’ Pleads Guilty to Diverting AI Servers - Bloomberg](https://www.bloomberg.com/news/articles/2026-10-09/super-micro-case-fixer-pleads-guilty-to-diverting-ai-servers)
39. [Linux 7.4-rc1 Released With Nice Performance Improvements, AMD Ryzen Zen 6 Preparations & AMDGPU HDMI 2.1 Default - Phoronix](https://www.phoronix.com/news/Linux-7.4-rc1)
40. [Linux 7.4-rc1 Released With Nice Performance Improvements, AMD Ryzen Zen 6 Preparations & AMDGPU HDMI 2.1 Default](https://daily.dev/posts/linux-7-4-rc1-released-with-nice-performance-improvements-amd-ryzen-zen-6-preparations-amdgpu-hdm-hqsvacthn)
41. [Ciberseguridad: 636 compitieron en primer Ejercicio Nacional](https://veredictum.cl/ciberseguridad-636-compitieron-en-primer-ejercicio-nacional/)
42. [ANCI realizará primer Ejercicio Nacional de Ciberseguridad](https://veredictum.cl/anci-realizara-primer-ejercicio-nacional-de-ciberseguridad/)
43. [PROYECCIONES Y DESAFÍOS: Ministerio de Energía proyecta que demanda eléctrica de data centers se cuadruplicará hacia 2030 - CPI](https://cpichile.org/proyecciones-y-desafios-ministerio-de-energia-proyecta-que-demanda-electrica-de-data-centers-se-cuadruplicara-hacia-2030/)

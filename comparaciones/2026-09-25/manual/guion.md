[INTRO]
Hola, hola, ¿cómo están? Bienvenidos a un nuevo episodio del noticiario de hardware, el número dos.

Hoy repasamos lo que pasó entre el martes 15 y el lunes 21 de septiembre de 2026, una semana con Fiestas Patrias de por medio, así que espero que hayan sobrevivido a las empanadas.

Y aunque medio país estaba de asado, la industria no paró: la litografía más cara del mundo por fin tiene fecha para la RAM, faltan CPUs y las RTX 60 se alejan otra vez.

Así que vamos al tiro.

[NOTICIA 1: High-NA llega a la RAM, pero no este año]
Parto con una que se nos pasó la semana anterior. Ocurrió el 8 de septiembre, un par de días antes de nuestra ventana, pero es demasiado importante para dejarla fuera, sobre todo en un canal que vive quejándose del precio de la memoria.

Lo confirmado es esto: Samsung y TSMC se comprometieron a usar las máquinas High-NA EUV de ASML en producción masiva. Samsung, para fabricar DRAM hacia 2028. TSMC, recién desde 2030. Lo anunciaron las propias empresas en comunicados oficiales, en el marco de la conferencia de SPIE sobre fotomáscaras y EUV en Monterey, California, y lo reportaron Bloomberg y CNBC.

Samsung, en su sala de prensa del 8 de septiembre, dice que planea meter High-NA en la producción masiva de DRAM hacia 2028 y que sería la primera de la industria en hacerlo. Ojo con esa palabra: primera en DRAM, no en todo.

Porque la que ya está usando High-NA en producción es Intel. Según el comunicado conjunto de Intel Foundry y ASML, llevan más de un millón de obleas procesadas con estas máquinas, sumando pruebas, investigación y producción real en algunas capas de una parte de los Core Ultra Series 3, o sea, Panther Lake.

Y acá viene la parte que a mí me da risa. Intel llegó tarde a la fiesta del EUV normal, y ahora resulta que es la única que está imprimiendo chips de verdad con la generación siguiente.

Ya, vamos a lo técnico, porque sin esto no se entiende por qué importa.

La litografía es básicamente proyectar un dibujo con luz sobre una oblea de silicio. El EUV usa luz de 13,5 nanómetros de longitud de onda. Lo más chico que puedes imprimir depende de esa longitud de onda dividida por algo que se llama apertura numérica, o NA, que en simple es cuánto ángulo de luz alcanza a juntar el lente.

Piénsenlo como una cámara: mientras más ángulos de luz capture el lente, más fino es el detalle que puedes resolver. El EUV normal trabaja con 0,33 de NA. El High-NA sube a 0,55. Eso permite imprimir líneas más finas de una sola pasada, en vez de hacer dos o tres exposiciones encima de la misma capa, que es lo que se hace hoy y que encarece todo.

Pero nada es gratis. Con este diseño, el área que la máquina expone de una vez queda en la mitad. Por eso ASML e Intel presentaron trabajos sobre lo que llaman "stitching", que es coser dos medios campos para armar un chip grande usando las máscaras de 6 pulgadas de siempre.

La analogía es pintar un mural con un esténcil que ahora mide la mitad: tienes que hacer dos pasadas y rezar para que calcen perfecto.

La otra salida es agrandar el esténcil. El 7 de septiembre, ASML y TSMC armaron una iniciativa de industria para pasar a fotomáscaras de 12 pulgadas, con una línea piloto hacia 2031 y máquinas High-NA de 12 pulgadas en producción recién hacia 2033. Samsung también se sumó a esa iniciativa. Eso es harto tiempo.

¿Y la plata? Bloomberg y CNBC hablan de unos 400 millones de dólares por máquina. Al dólar observado del 21 de septiembre, 958,42 pesos, eso son como 383 mil millones de pesos por cada equipo. Una máquina.

Ahora, ¿a quién le conviene esto? A ASML, obvio. En julio, en el comunicado de resultados del segundo trimestre que presentó ante la SEC, su CEO, Christophe Fouquet, ya había dicho que su capacidad de EUV normal ronda las 65 máquinas en 2026, que le quiere sumar un 30% para 2027 y que está estudiando otro 30% para 2028. Barclays, en una nota que citó CNBC el 8 de septiembre, dijo que ASML tiene por delante una decisión importante: si agranda la capacidad de EUV más allá de las metas que ya subió, porque la demanda está claramente fuerte.

A Samsung también le conviene, porque la DRAM ya usa EUV y cada generación necesita más capas críticas. Si puede reemplazar varias exposiciones por una sola, baja pasos, baja tiempo y, en teoría, baja el costo por bit.

TrendForce, por su parte, tituló que Samsung y SK hynix ya pusieron calendario para High-NA en DRAM y que Micron se mantiene callada. Lo de SK hynix no lo alcancé a verificar con cifra, así que no les voy a inventar una fecha.

¿A quién le duele? Primero, a nosotros. Que nadie se confunda: esto no baja el precio de la RAM ni este año ni el próximo. Hablamos de 2028 para Samsung, y entre que la máquina llega, se calibra y la producción sale con buen rendimiento, pasa harto tiempo.

Segundo, le duele a China. El 2 de septiembre, TrendForce recogió un análisis de UBS citado por Bloomberg que dice que China podría producir en volumen sus propias máquinas DUV de inmersión en dos a cinco años, pero que es poco probable que tenga EUV propio dentro de esta década.

Como contexto: en julio, The Diplomat contaba que las fuentes de luz EUV chinas andan entre 100 y 150 watts, contra los 600 que ya maneja ASML. Y mientras la industria occidental conversa sobre High-NA, China sigue peleando con el EUV de la generación anterior.

Y sí, existen startups que quieren saltarse a ASML: Substrate, con litografía de rayos X usando un acelerador de partículas, y xLight, con láseres de electrones libres como fuente de luz. Pero hoy son promesas, no máquinas en una fábrica.

Mi opinión: TSMC, con 2030, está siendo la más racional de todas. No se va a meter a pagar 400 millones por máquina mientras le rinda el EUV normal con varias pasadas. Samsung, en cambio, necesita una historia para recuperar terreno y la está comprando con la chequera.

Y mi consejo no pedido para Samsung: si quieren que alguien les crea lo de ser primeros en DRAM con High-NA, publiquen datos de rendimiento, no solo fechas. Porque fechas en esta industria hemos visto varias, y las cumplidas son harto menos.

Mi especulación, y lo marco como especulación: si Samsung llega de verdad en 2028, la pelea por HBM en 2029 se pone mucho más interesante, porque la memoria para IA es justo donde cada capa de más cuesta caro.

[NOTICIA 2: SK Hynix quiere fabricar memoria en la casa de Intel]
Y hablando de memoria y de fábricas, pasemos a lo del 16 de septiembre.

Reuters publicó en exclusiva, citando a tres personas al tanto de las conversaciones, que SK Hynix está conversando con Intel para fabricar chips de memoria en Estados Unidos, algo que nunca ha hecho.

El estatus de esto importa: es un reporte periodístico con fuentes anónimas, no un anuncio. SK Hynix le dijo a TechCrunch que está evaluando opciones para reforzar su competitividad, pero que no hay nada cerrado. Intel no comentó las conversaciones y solo dijo que sigue preparando su sitio de Ohio.

Según Reuters, se barajan dos caminos: que SK Hynix arriende parte del complejo que Intel tiene en Ohio, o que armen una empresa conjunta con Intel y con grandes proveedores de nube que quieren asegurarse memoria. Nadie sabe todavía qué tipo de memoria se fabricaría.

Ohio es la herida abierta de Intel. En 2022 anunció hasta 100 mil millones de dólares, casi 96 billones de pesos, para producir desde 2025. Hoy sus dos plantas están atrasadas hasta 2030 y 2031.

Por eso el mercado se entusiasmó: Intel cerró ese día con un alza de 4% y SK Hynix subió 4,1% en Seúl.

Pero hay un problema político. Corea considera la DRAM y la HBM tecnologías sensibles, y el ministerio coreano dijo que un acuerdo así se revisaría bajo su ley de protección de tecnología industrial.

Ojo con un detalle de cifras: SK Hynix ya construye una planta de empaquetado de HBM en West Lafayette, Indiana. En 2024 la propia empresa la anunció en unos 3.870 millones de dólares, y según TechSpot, cuando partió la obra en agosto de 2026 la cifra ya pasaba los 4.000 millones, con producción masiva para la segunda mitad de 2029. O sea, más de 3,8 billones de pesos.

Yo creo que para Intel esto sería oro: un cliente grande que llene fábricas vacías. Para nosotros, más fábricas de memoria es lo único que de verdad baja precios, pero con plantas para 2030 esto es una solución para la próxima década, no para su próximo PC.

[NOTICIA 3: Faltan CPUs y la cuenta la pagamos nosotros]
Y ya que estamos con Intel, el lunes 21 sus acciones subieron 12%, según CNBC. Pero lo interesante no es la bolsa, es la razón.

Subieron sobre todo las empresas que venden procesadores centrales. Arm subió 13%, a 312,46 dólares, según 24/7 Wall St. a mitad de la sesión, mientras CNBC habla de más de 15%, así que ahí tienen una diferencia entre fuentes, probablemente por la hora en que midió cada uno. AMD subió cerca de 9% y quedó rozando el billón de dólares de valor. NVIDIA, apenas 2%.

Según CNBC, Stacy Rasgon, analista de Bernstein, dijo que si los agentes de IA, como la app Muse de Meta, se masifican entre los consumidores, la oferta de CPUs, que ya está apretada, se apretaría todavía más, y eso le conviene directo a Intel y AMD en servidores x86. Un chatbot responde y listo. Un agente planifica, ejecuta código y consulta herramientas y bases de datos todo el día, y eso carga mucho a la CPU, no solo a la GPU.

Encima, Lip-Bu Tan, el CEO de Intel, dijo en la conferencia.conf26 de Splunk, en Denver, que Intel solo está cubriendo cerca del 50% de la demanda de CPUs que le piden, y que otros CEO lo han llamado directamente para pedirle más chips. Esto lo sabemos de segunda mano, a través de The Motley Fool, y no dio ni producto, ni segmento, ni cómo calculó ese 50%. Así que es una frase fuerte de un CEO, no una estadística.

¿Por qué les tiene que importar? Porque cuando falta oferta, el precio sube. El 8 de septiembre, DigiTimes reportó con fuentes de la cadena de suministro que Intel subiría cerca de 10% sus CPUs de PC el 5 de octubre. Intel no lo ha confirmado, aunque algún agregador lo contó como anuncio oficial. No lo es.

Lo que sí está confirmado es que en julio Intel subió el precio sugerido del Core Ultra 7 270K Plus de 299 a 349 dólares. Eso son unos 334 mil pesos, y con el 19% de IVA pasa los 398 mil, antes del margen del retail y de la espera. No alcancé a verificar esta semana cuánto está en Solotodo o PC Factory, así que compárenlo ustedes.

Si importan por courier: bajo 500 dólares pagan solo IVA y sobre 500 se suma un arancel de 6%, según la Aduana.

Y de pasada: sobre AMD circula que avisó a sus socios de un alza de 10% para el cuarto trimestre. Viene de ChannelGate, un medio de canal sin historial que yo pueda verificar, así que para mí es nivel C y no es noticia. Lo menciono solo porque su acción subió ese día.

Mi consejo para el que va a armar PC: si ya tiene elegido el procesador, no espere a octubre.

[NOTICIA 4: Las RTX 60 se van para el 2028]
En fin, pasemos a los rumores, y este duele.

Parto por el leaker. kopite7kimi es, para este canal, nivel A con NVIDIA: suele adelantar especificaciones con meses de ventaja. Pero ojo, en enero él mismo decía que las RTX 60 llegaban en la segunda mitad de 2027, o sea, ahora se está corrigiendo.

El 21 de septiembre escribió que GR20x, que sería la familia de chips gamer basada en Rubin detrás de las RTX 60, es un producto de 2028 y que NVIDIA lo volvió a postergar. Además dijo que va a publicar menos hasta que haya algo definitivo.

Y no está solo. Días antes, Kepler_L2, también nivel A, pero más fuerte con AMD, dijo que las RTX 60 no vienen el próximo año y que AMD sacaría un solo chip RDNA 5, el AT2, en 2027. Son dos leakers A diciendo lo mismo por su cuenta. Sigue siendo rumor, pero de los serios.

NVIDIA, como siempre, le dijo a Tom's Hardware que no comenta rumores ni productos no anunciados.

¿Por qué pasaría esto? Lo que se reporta, y que no está confirmado, es que la capacidad de TSMC y de empaquetado se va primero a los Rubin para datacenter, y que la memoria GDDR7 compite con la HBM para IA.

Para mí esto es lo más penca de la semana. Si se cumple, el gamer queda como tercera prioridad, después de la IA y de la IA.

Mi consejo: si necesita tarjeta de video ahora, no espere la generación siguiente, porque esa espera podría ser de más de un año.

Y mi consejo para NVIDIA: si no va a haber generación nueva, por lo menos bajen el precio de lo que ya venden. Aunque ya sabemos que eso no va a pasar.

[CHILE: La ley de datos podría correrse un año]
Y aterricemos en Chile.

Lo que sí tiene fecha en la semana es la Ley 21.719 de protección de datos personales. El gobierno ingresó el 31 de agosto un proyecto para postergar su entrada en vigencia un año completo: del 1 de diciembre de 2026 al 1 de diciembre de 2027, con suma urgencia. Lo contó La Tercera el 1 de septiembre.

La novedad dentro de la ventana es que el 17 de septiembre el Senado mandó el proyecto a la Comisión de Constitución. No hay votación ni informe todavía. El proyecto también cambia el consejo de la futura Agencia de Protección de Datos, que pasaría de tres a cinco miembros.

Ojo, el seguimiento de la tramitación viene del blog de un abogado, no de un medio, así que confírmenlo en el sitio del Senado con el boletín 18.623-07.

Y lo importante para los que trabajan en software: mientras el proyecto no sea ley, la fecha vigente sigue siendo el 1 de diciembre de 2026. Yo no dejaría de preparar los sistemas por si acaso.

Para los que están en investigación: ANID tiene abierto el Concurso de Fomento a la Vinculación Internacional para Instituciones de Investigación 2026, que cierra el 7 de octubre a las 13:00.

Y sobre el resto, siendo honesto: no encontré nada nuevo esta semana sobre data centers, ANCI o astronomía. El Departamento de Informática de la USM no ha publicado noticias desde fines de julio. No voy a inflar el bloque.

[CIERRE]
Eso fue todo por esta semana. Si les sirvió, suscríbanse y activen la campanita para que no se les pase el próximo episodio.

Cuéntenme en los comentarios si van a esperar las RTX 60 o si compran ahora. Nos vemos la próxima semana.

---

FUENTES
- Samsung y ASML amplían su alianza y Samsung planea High-NA para DRAM — Samsung Global Newsroom — 2026-09-08 — https://news.samsung.com/global/samsung-electronics-and-asml-expand-strategic-collaboration-for-next-generation-semiconductor-manufacturing
- TSMC y ASML lanzan iniciativa de fotomáscaras de 12 pulgadas; TSMC usará High-NA desde 2030 — ASML — 2026-09-08 — https://www.asml.com/en/news/press-releases/2026/tsmc-and-asml-announce-industry-transition-to-large-format-photomasks-for-high-na-euv
- Intel Foundry y ASML reportan más de un millón de obleas con High-NA — ASML — 2026-09-08 — https://www.asml.com/en/news/press-releases/2026/intel-foundry-and-asml-collaborate-to-accelerate-industry-readiness-for-high-na-euv
- TSMC y Samsung adoptarán High-NA EUV para chips de IA — CNBC — 2026-09-08 — https://www.cnbc.com/2026/09/08/tsmc-samsung-asml-high-na-euv-machine-ai-chips.html
- ASML convence a los grandes fabricantes de adoptar sus nuevas máquinas EUV — Bloomberg — 2026-09-08 — https://www.bloomberg.com/news/articles/2026-09-08/asml-tsmc-samsung-intel-back-12-inch-masks-for-ai-chips
- ASML reporta resultados del segundo trimestre y planes de capacidad EUV — ASML (Form 6-K, SEC) — 2026-07-15 — https://www.sec.gov/Archives/edgar/data/0000937966/000162828026048235/pressreleasefinancialresul.htm
- China podría producir DUV en volumen en 2 a 5 años, EUV poco probable en la década — TrendForce — 2026-09-02 — https://www.trendforce.com/news/2026/09/02/news-chinas-duv-could-reach-high-volume-production-in-2-5-years-euv-reportedly-unlikely-within-a-decade/
- El avance chino en EUV: separar señal de ruido — The Diplomat — 2026-07 — https://thediplomat.com/2026/07/chinas-euv-lithography-progress-parsing-signal-from-noise/
- SK Hynix conversa con Intel para fabricar memoria en EE.UU. — Reuters (vía Investing.com) — 2026-09-16 — https://www.investing.com/news/stock-market-news/exclusivesk-hynix-in-talks-with-intel-about-deal-to-make-memory-chips-in-the-us-for-the-first-time-sources-say-4902886
- SK Hynix dice que no hay nada cerrado con Intel — TechCrunch — 2026-09-16 — https://techcrunch.com/2026/09/16/sk-hynix-reportedly-in-talks-with-intel-to-build-memory-chips-in-us/
- Acciones de Intel y SK Hynix suben por reporte de fabricación en EE.UU. — CNBC — 2026-09-16 — https://www.cnbc.com/2026/09/16/intel-sk-hynix-us-memory-chips.html
- Intel sube 4% por conversaciones con SK Hynix — The Motley Fool (vía Yahoo Finance) — 2026-09-16 — https://finance.yahoo.com/markets/stocks/articles/stock-market-today-sept-16-212959692.html
- SK Hynix y el sitio de Ohio: revisión del gobierno coreano — The Next Web — 2026-09-16 — https://thenextweb.com/news/sk-hynix-intel-talks-us-memory-chips-ohio
- SK Hynix y su planta de empaquetado en Indiana — The AI Insider — 2026-09-17 — https://theaiinsider.tech/2026/09/17/sk-hynix-in-talks-with-intel-to-manufacture-ai-memory-chips-in-the-us/
- Intel sube 12% en un rally de acciones de CPU — CNBC — 2026-09-21 — https://www.cnbc.com/2026/09/21/intel-surges-12percent-as-cpu-stocks-rally-heres-whats-driving-the-move.html
- Arm sube 13% e Intel 12% por la apuesta a la demanda de CPU — 24/7 Wall St. (vía Yahoo Finance) — 2026-09-21 — https://finance.yahoo.com/markets/stocks/articles/arm-surges-13-meta-muse-152410038.html
- Intel dice cubrir solo la mitad de la demanda de CPU — FinanceFeeds — 2026-09-21 — https://financefeeds.com/intel-stock-12-percent-cpu-demand-tan/
- Intel planearía otra alza de 10% en CPUs de PC para el 5 de octubre — VideoCardz — 2026-09-08 — https://videocardz.com/newz/intel-reportedly-plans-another-10-pc-cpu-price-increase-for-october-5
- AMD podría subir 10% GPUs y chipsets — PCWorld — 2026-09-17 — https://www.pcworld.com/article/3239912/amd-gpu-and-motherboard-prices-could-jump-10-percent-soon-ryzen-may-follow.html
- Otro gran leaker dice que las RTX 60 no llegan hasta 2028 — TechSpot — 2026-09-21 — https://www.techspot.com/news/113920-another-major-gpu-leaker-nvidia-rtx-6000-series.html
- GeForce RTX 60 se atrasaría a 2028 según kopite7kimi — VideoCardz — 2026-09-21 — https://videocardz.com/newz/nvidia-geforce-rtx-60-reportedly-delayed-to-2028-another-leaker-confirms
- RTX 60 postergada a 2028 mientras los datacenters se comen la RAM — Club386 — 2026-09-21 — https://www.club386.com/nvidia-geforce-rtx-6090-postponed-again-2028/
- Dólar observado de septiembre de 2026 — SII — 2026-09-21 — https://www.sii.cl/valores_y_fechas/dolar/dolar2026.htm
- Compras internacionales sin arancel hasta USD 500 — Aduana de Chile — 2025-10-20 — https://www.aduana.cl/sin-arancel-aduanero-hasta-usd-500/aduana/2025-10-20/174429.html
- Gobierno ingresa proyecto que posterga un año la ley de datos personales — La Tercera — 2026-09-01 — https://www.latercera.com/pulso/noticia/proteccion-de-datos-personales-gobierno-ingresa-proyecto-que-posterga-en-un-ano-entrada-en-vigencia-de-la-ley/
- Tramitación del proyecto que posterga la Ley 21.719 — vonmarttens.cl (blog de abogado) — 2026-09-17 — https://vonmarttens.cl/postergacion-ley-proteccion-datos-personales-2027/
- Concurso de Fomento a la Vinculación Internacional para Instituciones de Investigación 2026 — ANID — 2026-09-10 — https://anid.cl/concursos/concurso-de-fomento-a-la-vinculacion-internacional-para-instituciones-de-investigacion-2026/

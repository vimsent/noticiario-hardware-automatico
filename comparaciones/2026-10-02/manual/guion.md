[INTRO]
Hola, hola, ¿cómo están? Bienvenidos al episodio dos del noticiario de hardware del canal.

Esta semana cubrimos desde el jueves 25 de septiembre hasta el viernes 2 de octubre de 2026.

Y vale la pena, porque Micron puso por escrito, en un documento oficial y con números, lo que todos veníamos sospechando: la memoria cara no se va a ir pronto. Se va a poner peor.

Así que sírvanse un cafecito y partamos al tiro.

[NOTICIA 1: Micron confirma que la RAM cara va para largo]
El miércoles 30 de septiembre Micron publicó los resultados del cuarto trimestre de su año fiscal 2026. Esto es dato confirmado por la empresa, en el comunicado que presentó ante la SEC, el regulador de valores de Estados Unidos.

Ingresos del trimestre: 54.230 millones de dólares.

El trimestre anterior habían sido 41.460 millones. Y el mismo trimestre del año pasado, 11.320 millones.

O sea, casi cinco veces en un año. Al dólar observado de hoy, 983,84 pesos, eso son más de 53 billones de pesos en tres meses. Billones chilenos, con doce ceros.

El margen bruto fue de 86,8%.

Piensen lo que significa. Micron fabrica cosas físicas: salas limpias, químicos, obleas, máquinas carísimas. Y aun así, de cada 100 dólares que vende, le quedan casi 87 después de pagar lo que cuesta fabricar. Eso es margen de empresa de software, no de fábrica de chips.

El año fiscal completo cerró en 133.190 millones de dólares, contra 37.380 millones del año anterior. Y para el próximo trimestre proyectan 61.500 millones, con 1.500 de margen para arriba o para abajo.

Pero los números son lo de menos. Lo importante es lo que dijo Sanjay Mehrotra, el CEO, en la llamada con inversionistas.

Dijo que la oferta y la demanda de memoria van a estar bastante más apretadas en 2027 y 2028 que en 2026. Y que no tienen visibilidad de cuándo se vuelve a equilibrar.

Un detalle para los obsesivos como yo: TechPowerUp y Yahoo Finance reportan que hablaba de años fiscales, pero Tech Insider, citando a Computerworld y PCMag, transcribe sus comentarios preparados hablando de los años calendario 2027 y 2028. Son unos meses de diferencia y no cambia el fondo, pero las fuentes no calzan y se los cuento.

Según Computerworld, citado por Tech Insider, más del 75% de lo que Micron va a producir en 2027 ya está amarrado en acuerdos estratégicos con clientes, y según PCMag, Mehrotra dijo que la mayoría de las conversaciones con clientes ya son sobre 2028. Y también según PCMag, Mehrotra dijo que buena parte del volumen de HBM de 2027 ya está vendido, a precios muy por encima de los de 2026.

¿Por qué pasa esto? Acá hay que ponerse técnicos, porque esta es la clave.

La HBM, la memoria que va pegada a las GPUs de datacenter, no es DDR5 con otro nombre. Es una torre de chips de DRAM apilados, conectados de arriba abajo por miles de perforaciones verticales que atraviesan el silicio, montada justo al lado del procesador.

Cada piso de esa torre es un dado de DRAM que salió de una oblea. Esos dados tienen que cargar con la circuitería de las conexiones verticales, así que por bit ocupan más superficie que un chip de DDR5 normal. Y si un piso sale malo después de apilar, se puede perder la torre completa.

Resultado: por cada gigabyte de HBM se consume harta más oblea que por un gigabyte de DDR5.

Piénsenlo como una amasandería. Mismo horno, misma masa. Pero si en vez de marraquetas te piden pan relleno de cinco pisos, salen muchas menos unidades por hornada. Y el horno, que es la fábrica, no se agranda de un día para otro.

Según lo que explicó Mehrotra, y que reportó Ars Technica, pasar de HBM3E a HBM4 y HBM4E empeora esa relación. Cada generación nueva se come todavía más oblea por bit.

Y las fábricas nuevas no salen al tiro. Micron mismo dice que su planta ID2 en Idaho recién empezaría a sacar obleas a fines de 2028.

Y acá entra un tema que nos encanta en el canal: la litografía EUV.

La EUV usa luz con una longitud de onda muchísimo más corta que la ultravioleta profunda de antes. Con una luz más fina se pueden dibujar líneas más finas en una sola pasada, en vez de partir el patrón en dos o tres exposiciones y alinearlas con una precisión absurda. Menos pasos, menos defectos, más densidad.

El nodo 1-gamma de Micron, el que está usando para sus módulos de servidor de 8.800 MT/s y para sus primeras muestras de LPDDR6, va amarrado a la EUV: en su informe a accionistas del año pasado, Micron contó que instaló su primera herramienta EUV en Japón con capacidad 1-gamma.

¿Por qué importa? Porque ASML es la única que fabrica esas máquinas, y el ritmo al que puede crecer la memoria de punta depende del ritmo al que llegan.

Como contexto, y esto es de antes de nuestra ventana: el 8 de septiembre, según CNBC, Samsung dijo que planea usar High-NA EUV para fabricar DRAM desde 2028. O sea, la próxima vuelta de tuerca tecnológica también está fechada para 2028. Calza con todo lo demás.

¿A quién le conviene esto? A Micron, a Samsung y a SK Hynix, obvio. Micron dice tener 26 acuerdos estratégicos con clientes que cubren más de un 35% de sus ingresos hasta 2030.

¿A quién le duele? A ustedes. A mí. Al que quiere armar PC.

Y no es teoría. El 1 de octubre, Raspberry Pi subió 12,50 dólares los modelos de 2 GB del Pi 4 y del Pi 5, culpando directamente al costo de la memoria. El Pi 5 de 2 GB quedó en 77,50 dólares, unos 76 mil pesos, y con el 19% de IVA que se paga en compras al extranjero bajo 500 dólares se va sobre 90 mil. Un computador que nació con la promesa de costar 35 dólares.

Intenté cruzar esto con precios de módulos en PC Factory, SPDigital, Winpy o Solotodo esta semana y no logré verificarlo, así que no les voy a inventar una cifra.

Mi opinión: esto ya no es el ciclo normal de la memoria, de esos de un par de años arriba y un par abajo. Cuando el fabricante te dice que tiene más de tres cuartos de 2027 vendido y que 2028 viene peor, el que está esperando que la RAM baje para Navidad está esperando en vano.

Mi consejo, y es opinión mía: si necesitan RAM o un SSD para la pega o para la tesis, no esperen un milagro. Y si su PC actual anda, estírenlo.

Y un consejo no pedido para Micron: si quieren que el mercado de consumo no los mire feo, reserven una fracción fija de su producción para módulos de consumo con precio predecible. Con márgenes de 87% les sobra espacio.

Especulación mía para uno o dos años: notebooks y celulares con menos memoria al mismo precio, y fabricantes vendiéndote la versión recortada como si fuera novedad. De hecho, eso ya está pasando, y es justo la siguiente noticia.

[NOTICIA 2: NVIDIA te vende la mitad de memoria por más plata]
Y hablando de memoria recortada: el viernes 2 de octubre NVIDIA anunció una versión de 64 GB del DGX Spark. Confirmado por la empresa.

Para el que no lo ubica, el DGX Spark es el computadorcito de escritorio de NVIDIA para IA local. Usa el chip GB10 Grace Blackwell, con CPU y GPU compartiendo un mismo pool de memoria unificada.

Y eso es lo importante. En un modelo de lenguaje, los parámetros tienen que caber en memoria. No en el disco: en memoria. Si no caben, no corre, o corre a paso de tortuga. En estos equipos, la memoria define qué puedes hacer.

NVIDIA dice que la versión de 64 GB corre modelos de hasta 100 mil millones de parámetros, contra 200 mil millones de la original de 128 GB.

El precio: desde 4.999 dólares, a la venta el 23 de octubre, solo a través de Acer, ASUS, Dell, Gigabyte, HP y MSI. No hay Founders Edition de 64 GB.

Ahora, el chiste. La versión original de 128 GB se lanzó en octubre de 2025 a 3.999 dólares, y en febrero de 2026 NVIDIA la subió a 4.699 citando la escasez de memoria.

O sea, la versión con la mitad de memoria cuesta más que lo que costaba la completa en su lanzamiento. Bacán, ¿no?

Y acá hay una contradicción que les tengo que contar. The Register dice que la de 128 GB subió ahora a 6.950 dólares, y medios financieros chinos dicen lo mismo. Pero VideoCardz compara contra un precio vigente de 4.699. No sé cuál es el precio de hoy, y no voy a elegir uno a escondidas. The Register agrega que la de 64 GB trae también la mitad del almacenamiento.

NVIDIA propone que, si te queda corto, conectes dos unidades para juntar 128 GB. O sea, comprar dos para tener lo que antes venía en una. Para mí esto es marketing del más penca: te venden la escasez como si fuera flexibilidad.

En pesos, 4.999 dólares son unos 4,9 millones. Y como pasa de 500 dólares, si lo traen por courier pagan 6% de arancel sobre el valor con flete y seguro, y encima 19% de IVA. Sin contar el flete, queda sobre 6,2 millones. Ojo que algunas guías de couriers dicen que productos amparados por tratados de libre comercio pueden salvarse del 6%, pero eso no lo vi confirmado por Aduanas.

Tampoco encontré anuncio de venta oficial en Chile. Si llega, apuesto a que llega tarde y con margen de retail encima.

[NOTICIA 3: Acusan a californiano de contrabandear GPUs NVIDIA a China]
Y ya que estamos con NVIDIA, pasemos a tribunales.

El jueves 1 de octubre arrestaron en California a Greg Lui, de 38 años, dueño de una empresa llamada Earthmade Computer. Esto viene de una acusación formal de la fiscalía federal de Los Ángeles, o sea, documento oficial. Pero ojo: es una acusación, no una condena.

Según los fiscales, entre 2023 y 2024 Lui habría ayudado a sacar de Estados Unidos más de 300 millones de dólares en servidores con GPUs NVIDIA sujetas a control de exportación. Unos 295 mil millones de pesos.

¿Cómo? Con papeles falsos y triangulando. Los servidores iban a Malasia y Singapur, que no necesitan licencia del Departamento de Comercio, y desde ahí empresas locales los reenviaban a China.

Un ejemplo de la acusación, según Social News XYZ citando a IANS: una orden de enero de 2024 por 27 servidores con GPUs H100, por unos 7,6 millones de dólares, despachada desde Los Ángeles a Kuala Lumpur. En marzo de 2024, un supuesto cómplice le habría escrito por correo a un funcionario malasio que esos servidores ya se habían reenviado a un comprador en China.

Además, según The Register, los fiscales sostienen que Lui recibió más de 176 millones de dólares de dos empresas de Malasia.

Son tres cargos: conspiración para violar la ley de control de exportaciones, contrabando de salida y conspiración para lavado de dinero. Gadget Review titula que arriesga 20 años y The Register habla de 50, pero no es contradicción: según las cifras del Departamento de Justicia que reportaron Quartz y CBS Los Angeles, cada uno de los dos cargos de conspiración tiene un máximo de 20 años y el de contrabando hasta 10, lo que suma 50 en total. El gran jurado presentó la acusación el 29 de septiembre.

Para entender por qué importa: el control de exportación no prohíbe fabricar las GPUs, prohíbe que lleguen a ciertos destinos sin licencia. El problema es que un servidor es una caja. Una vez que sale, la cadena de custodia depende de papeles. Y los papeles se falsifican.

No es el primer caso. El 19 de marzo de 2026 arrestaron a Yih-Shyan "Wally" Liaw, cofundador de Super Micro, acusado por la fiscalía federal de Manhattan junto con Ruei-Tsang "Steven" Chang y Ting-Wei "Willy" Sun de desviar unos 2.500 millones de dólares en servidores con NVIDIA a China, según el 8-K de Super Micro ante la SEC; según Bloomberg, Liaw se declaró no culpable, y según TipRanks, el juicio está fijado para el 2 de noviembre. Y el 24 de agosto, según AP y PBS, la fiscalía del distrito de Keelung, en Taiwán, presentó cargos contra nueve personas, entre ellas un gerente de NVIDIA Taiwán de apellido Chang y dos gerentes de ventas de Super Micro Taiwán, por 130 servidores B300: 74 llegaron a China y 56 fueron interceptados.

Mi opinión: esto es jugar al topo. Cierran una ruta y aparece otra por el país vecino. Mientras la demanda de cómputo en China siga así, el incentivo para triangular es enorme.

Consejo no pedido para NVIDIA y sus socios: si el negocio depende de que la caja no termine donde no debe, inviertan en verificar dónde está el hardware ya instalado, no solo en formularios. Es especulación mía, pero me parece que por ahí va a venir la presión regulatoria.

[NOTICIA 4: Ubuntu 26.10 llega con un kernel todavía en el horno]
En fin, pasemos a software de bajo nivel, que para muchos de ustedes es la pega diaria.

El 1 de octubre salió la beta de Ubuntu 26.10, con el kernel Linux 7.3 y GNOME 51. Confirmado por Canonical y reportado por Phoronix.

Lo curioso es la historia del kernel. En mayo, Canonical había dicho que 26.10 usaría Linux 7.2. Pero como los ciclos de 7.1 y 7.2 no se atrasaron, el equipo decidió subir la apuesta a 7.3.

El detalle: según OMG! Ubuntu, Ubuntu 26.10 sale el 15 de octubre, y según Phoronix, Linux 7.3 estable se espera recién para el 18 de octubre. O sea, Ubuntu va a salir con un kernel que, al momento de cerrarse, todavía era una release candidate.

¿Es grave? No tanto. Una RC tardía es bastante sólida. Para una versión que no es LTS, yo creo que la apuesta se entiende. Pero si están en un servidor de producción, quédense en la 26.04 LTS, que según OMG! Ubuntu recibiría este kernel por la actualización HWE a principios de 2027.

¿Qué trae Linux 7.3 que les importe? Según Phoronix, en las últimas RC siguieron llegando arreglos al planificador "cache aware". La idea es que el planificador intente mantener juntas, en la misma caché de último nivel, a las tareas que comparten datos, para que no anden saltando entre grupos de núcleos y botando lo que tenían en caché. En CPUs con núcleos híbridos o con varios chiplets, eso pesa harto.

Phoronix comenta además que las RC vienen grandes, en buena parte porque agentes de IA están encontrando problemas en un código que ya va en casi 41 millones de líneas. Eso, para mí, es lo más interesante del ciclo.

Y de pasada: Intel mandó su último lote de mejoras del driver Xe para Linux 7.4, y Phoronix dice que trae una mejora importante para las gráficas Battlemage. Si tienen una Arc, ojo con eso.

[CHILE: Octubre llega con CTF, consulta pública y datacenters]
Y ahora, lo que pasa acá.

Lo más concreto de la semana viene de la Agencia Nacional de Ciberseguridad, la ANCI, la que creó la Ley 21.663 marco de ciberseguridad.

El jueves 1 de octubre la ANCI inauguró el Mes de la Ciberseguridad con tres anuncios, según TrendTIC.

Uno: un portal para la ciudadanía.

Dos: durante octubre abre una consulta pública sobre autenticación multifactor, como paso previo a un estándar obligatorio para todas las instituciones sujetas a la ley marco. Esto sí es novedad regulatoria fechada. Si trabajan en TI en un organismo público o en un operador de importancia vital, les va a llegar a la pega. Mi consejo: participen de la consulta, porque el estándar sale igual y es mejor que lo escriba gente que sabe.

Tres: el primer ejercicio nacional de ciberseguridad, un CTF para instituciones públicas y privadas, también en octubre.

Y para los estudiantes de la Santa María, ojo: el 7 y 8 de octubre es el Seminario Internacional de Ciberseguridad de la PDI, coorganizado con la USM, en la Escuela de Investigaciones Policiales. Y por primera vez trae un CTF, con desafíos de hacking web, forense digital y criptografía. Revisen la preinscripción en el sitio de la PDI. Para un estudiante de Informática, un CTF es de lo mejor que se puede poner en el currículum.

Además, el martes 6 de octubre hay un summit de ciberseguridad entre la Unión Europea y la ANCI en Santiago. Según Diario Financiero, a la ANCI le reportaron más de 320 incidentes en el primer semestre de 2026.

En datacenters, el 30 de septiembre salió un informe de Colliers que cuenta 36 data centers operando en Chile, con 255 MW instalados, y 34 desarrollos futuros entre proyectos nuevos y ampliaciones. Ojo que otro informe comercial, de ResearchAndMarkets, habla de unos 39 en operación, así que los conteos no calzan.

Lo que me llamó la atención: según Colliers, el proyecto Alto Jahuel, de Terranova, es el primer data center que se eximió de entrar al Sistema de Evaluación de Impacto Ambiental. Con todo el debate que hay por agua y energía, para mí eso merece harta más atención de la que está recibiendo.

Y de la USM, una investigación del Departamento de Ingeniería de Minas, Metalurgia y Materiales sobre tecnología WAAM, que es fabricar piezas de metal capa por capa con un robot, e incluye desarrollar un slicer propio. Ingeniería de la buena.

Del resto, convocatorias de ANID y Corfo y temas de astronomía, esta semana no alcancé a verificar nada nuevo, así que prefiero no inflarles el bloque.

[CIERRE]
Eso fue todo por esta semana. Si les sirvió, suscríbanse y activen la campanita para no perderse el próximo episodio.

Y cuéntenme en los comentarios: ¿alcanzaron a comprar RAM antes de que se disparara, o están estirando el PC como yo? Nos vemos la próxima semana.

---

FUENTES
- Micron reporta resultados récord del cuarto trimestre fiscal 2026 — Micron Technology (Form 8-K, Exhibit 99.1, SEC) — 30 de septiembre de 2026 — https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm
- El CEO de Micron prevé oferta de memoria mucho más apretada en 2027 y 2028 — TechPowerUp — 30 de septiembre/1 de octubre de 2026 — https://www.techpowerup.com/353296/micron-ceo-says-memory-supply-will-be-much-tighter-in-2027-and-2028-than-in-2026
- Micron dice no tener visibilidad de cuándo termina la escasez — Yahoo Finance — 1 de octubre de 2026 — https://finance.yahoo.com/technology/article/micron-cfo-no-line-of-sight-for-when-memory-shortage-will-end-165934130.html
- Transcripción de la llamada de resultados de Micron Q4 2026 — Investing.com — 30 de septiembre de 2026 — https://www.investing.com/news/transcripts/earnings-call-transcript-micron-tops-q4-2026-estimates-as-demand-stays-hot-93CH-4925992
- Micron supera estimaciones y no ve fin a la escasez — 24/7 Wall St. — 1 de octubre de 2026 — https://247wallst.com/investing/2026/10/01/micron-blew-past-estimates-and-says-it-cant-see-when-the-memory-shortage-ends/
- Micron: más del 75% de la producción 2027 comprometida (agregador que cita a Ars Technica, Computerworld y PCMag) — Tech Insider — octubre de 2026 — https://tech-insider.org/micron-ceo-2027-memory-supply-sold-out-2026/
- Informe a accionistas de Micron con la primera herramienta EUV en Japón para 1-gamma — Micron Technology (Form DEF 14A, SEC) — 25 de noviembre de 2025 — https://www.sec.gov/Archives/edgar/data/723125/000072312525000038/mu-20251125.htm
- TSMC y Samsung se comprometen con High-NA EUV de ASML; Samsung la usaría en DRAM desde 2028 — CNBC — 8 de septiembre de 2026 — https://www.cnbc.com/2026/09/08/tsmc-samsung-asml-high-na-euv-machine-ai-chips.html
- Raspberry Pi sube 12,50 dólares los modelos de 2 GB por el costo de la memoria — OMG! Ubuntu — 1 de octubre de 2026 — https://www.omgubuntu.co.uk/2026/10/raspberry-pi-2gb-costs-how-much-now
- El Pi 5 de 2 GB sube a 77,50 dólares — Hardware Busters — 1 de octubre de 2026 — https://hwbusters.com/news/raspberry-pi-5-2gb-price-climbs-to-77-50-as-memory-costs-finally-catch-the-cheap-boards/
- El peso chileno en su nivel más débil en más de un año: dólar observado 983,84 — The Rio Times — 2 de octubre de 2026 — https://www.riotimesonline.com/chile-peso-weakest-in-over-a-year-expats-2026/
- NVIDIA lanza DGX Spark de 64 GB que cuesta más que el original de 128 GB — VideoCardz — 2 de octubre de 2026 — https://videocardz.com/newz/nvidia-dgx-spark-drops-to-64gb-memory-but-costs-more-than-the-original-128gb-version
- DGX Spark de 64 GB a 4.999 dólares el 23 de octubre — The PC Enthusiast — 2 de octubre de 2026 — https://thepcenthusiast.com/nvidia-dgx-spark-64gb-price-release-date/
- DGX Spark 64 GB y alza del modelo de 128 GB (resume a The Register y Tom's Hardware) — WindowsForum — 2 de octubre de 2026 — https://windowsforum.com/news/nvidia-dgx-spark-64gb-launches-at-4-999-as-128gb-model-price-rises.446991/
- NVIDIA DGX Spark 64 GB a 4.999 dólares; versión de 128 GB a 6.950 — KuCoin News (agregador financiero) — 2 de octubre de 2026 — https://www.kucoin.com/news/flash/nvidia-launches-64gb-dgx-spark-at-4999-128gb-version-rises-to-6950
- Aduanas: compras hasta 500 dólares sin arancel, solo IVA — Servicio Nacional de Aduanas — 20 de octubre de 2025 — https://www.aduana.cl/sin-arancel-aduanero-hasta-usd-500/aduana/2025-10-20/174429.html
- Aduanas: sobre 500 dólares se paga además arancel de 6% — Servicio Nacional de Aduanas — 20 de octubre de 2025 — https://www.aduana.cl/desde-cuando-y-a-quien-aplica/aduana/2025-10-20/120230.html
- Californiano acusado de enviar 300 millones de dólares en chips NVIDIA a China — The Register — 2 de octubre de 2026 — https://www.theregister.com/security/2026/10/02/californian-accused-of-shipping-300m-worth-of-nvidia-chips-to-china-without-uncle-sams-approval/5300856
- EE.UU. acusa a hombre por enviar ilegalmente chips NVIDIA a China (Bloomberg) — Yahoo News Singapore — 2 de octubre de 2026 — https://sg.news.yahoo.com/man-charged-by-us-with-illegally-shipping-nvidia-chips-to-china-054847726.html
- Californiano acusado de contrabando de 300 millones en hardware de IA — Courthouse News Service — 1 de octubre de 2026 — https://www.courthousenews.com/california-man-charged-with-smuggling-300-million-in-restricted-ai-hardware-to-china/
- Hombre de San Gabriel acusado de contrabando de servidores de IA; antecedentes Super Micro y Taiwán — Hoodline — octubre de 2026 — https://hoodline.com/2026/10/san-gabriel-man-accused-of-smuggling-300m-in-ai-servers-to-china/
- CEO californiano acusado de contrabando de servidores NVIDIA — Gadget Review — octubre de 2026 — https://www.gadgetreview.com/california-ceo-charged-with-allegedly-smuggling-300m-in-nvidia-ai-servers-to-china
- Sale la beta de Ubuntu 26.10 con Linux 7.3 y GNOME 51 — Phoronix — 1 de octubre de 2026 — https://www.phoronix.com/news/Ubuntu-26.10-Beta-Released
- Ubuntu 26.10 cambia a Linux 7.3 — Phoronix — septiembre de 2026 — https://www.phoronix.com/news/Ubuntu-26.10-With-Linux-7.3
- Ubuntu 26.10 saldrá con Linux 7.3 — OMG! Ubuntu — 11 de septiembre de 2026 — https://www.omgubuntu.co.uk/2026/09/ubuntu-2610-kernel-version
- Linux 7.3-rc5 apunta a versión estable el 18 de octubre — Phoronix — 27 de septiembre de 2026 — https://www.phoronix.com/news/Linux-7.3-rc5-Released
- Intel lista una mejora grande para Battlemage en Linux 7.4 — Phoronix — 2 de octubre de 2026 — https://www.phoronix.com/news/Intel-CPU-Binds-ULLS-Migration
- ANCI inaugura el Mes de la Ciberseguridad con tres anuncios — TrendTIC — 1 de octubre de 2026 — https://www.trendtic.cl/2026/10/anci-inaugura-el-mes-de-la-ciberseguridad-con-tres-anuncios-portal-ciudadano-consulta-publica-y-ctf-nacional/
- Seminario Internacional de Ciberseguridad PDI 2026, coorganizado con la USM — PDI Chile — 2026 — https://www.pdichile.cl/seminariociberseguridad
- Chile y la Unión Europea abordan desafíos de ciberseguridad — Diario Financiero — octubre de 2026 — https://www.df.cl/chile-y-la-union-europea-abordan-los-desafios-de-ciberseguridad-en-el
- Se instalarán 34 nuevos data centers en Chile, según Colliers — Construnoticias — 30 de septiembre de 2026 — https://construnoticias.com/2026/09/30/datacenters-en-auge-se-instalaran-34-nuevos-centros-en-chile/
- Análisis comercial del portafolio de data centers en Chile — GlobeNewswire (ResearchAndMarkets) — 29 de septiembre de 2026 — https://www.globenewswire.com/news-release/2026/09/29/3370484/28124/en/chile-existing-upcoming-data-center-market-portfolio-analysis-2026-2031-santiago-s-250-mw-pipeline-signals-colocation-and-hyperscale-investment-opportunities.html
- USM impulsa investigación transdisciplinaria en tecnología WAAM — Portal Innova — 1 de octubre de 2026 — https://portalinnova.cl/usm-impulsa-investigacion-transdisciplinaria-para-el-desarrollo-de-tecnologia-waam-en-chile
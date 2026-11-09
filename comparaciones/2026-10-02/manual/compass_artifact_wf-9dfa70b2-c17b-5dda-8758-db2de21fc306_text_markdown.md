# guion.md

[INTRO]
Hola, hola, ¿cómo están? Bienvenidos al episodio dos del noticiario de hardware del canal.

Esta semana cubrimos desde el jueves 25 de septiembre hasta el viernes 2 de octubre de 2026.

Y vale la pena, porque Micron puso por escrito, en un documento oficial y con números, lo que todos veníamos sospechando: la memoria cara no se va a ir pronto. Se va a poner peor.

Así que sírvanse un cafecito y partamos al tiro.

[NOTICIA 1: Micron confirma que la RAM cara va para largo]
El miércoles 30 de septiembre Micron publicó los resultados del cuarto trimestre de su año fiscal 2026. Esto es dato confirmado por la empresa, en el comunicado que presentó ante la SEC, el regulador de valores de Estados Unidos.

Ingresos del trimestre: 54.230 millones de dólares.\[1\]

El trimestre anterior habían sido 41.460 millones. Y el mismo trimestre del año pasado, 11.320 millones.\[2\]

O sea, casi cinco veces en un año. Al dólar observado de hoy, 983,84 pesos, eso son más de 53 billones de pesos en tres meses.\[3\] Billones chilenos, con doce ceros.

El margen bruto fue de 86,8%.\[2\]

Piensen lo que significa. Micron fabrica cosas físicas: salas limpias, químicos, obleas, máquinas carísimas. Y aun así, de cada 100 dólares que vende, le quedan casi 87 después de pagar lo que cuesta fabricar. Eso es margen de empresa de software, no de fábrica de chips.

El año fiscal completo cerró en 133.190 millones de dólares, contra 37.380 millones del año anterior. Y para el próximo trimestre proyectan 61.500 millones, con 1.500 de margen para arriba o para abajo.\[2\]\[4\]

Pero los números son lo de menos. Lo importante es lo que dijo Sanjay Mehrotra, el CEO, en la llamada con inversionistas.

Dijo que la oferta y la demanda de memoria van a estar bastante más apretadas en 2027 y 2028 que en 2026. Y que no tienen visibilidad de cuándo se vuelve a equilibrar.\[4\]

Un detalle para los obsesivos como yo: TechPowerUp y Yahoo Finance reportan que hablaba de años fiscales, pero Tech Insider, citando a Computerworld y PCMag, transcribe sus comentarios preparados hablando de los años calendario 2027 y 2028. Son unos meses de diferencia y no cambia el fondo, pero las fuentes no calzan y se los cuento.

Según Computerworld, citado por Tech Insider, más del 75% de lo que Micron va a producir en 2027 ya está amarrado en acuerdos estratégicos con clientes, y según PCMag, Mehrotra dijo que la mayoría de las conversaciones con clientes ya son sobre 2028. Y también según PCMag, Mehrotra dijo que buena parte del volumen de HBM de 2027 ya está vendido, a precios muy por encima de los de 2026.

¿Por qué pasa esto? Acá hay que ponerse técnicos, porque esta es la clave.

La HBM, la memoria que va pegada a las GPUs de datacenter, no es DDR5 con otro nombre. Es una torre de chips de DRAM apilados, conectados de arriba abajo por miles de perforaciones verticales que atraviesan el silicio, montada justo al lado del procesador.\[5\]

Cada piso de esa torre es un dado de DRAM que salió de una oblea. Esos dados tienen que cargar con la circuitería de las conexiones verticales, así que por bit ocupan más superficie que un chip de DDR5 normal. Y si un piso sale malo después de apilar, se puede perder la torre completa.

Resultado: por cada gigabyte de HBM se consume harta más oblea que por un gigabyte de DDR5.\[6\]

Piénsenlo como una amasandería. Mismo horno, misma masa. Pero si en vez de marraquetas te piden pan relleno de cinco pisos, salen muchas menos unidades por hornada. Y el horno, que es la fábrica, no se agranda de un día para otro.

Según lo que explicó Mehrotra, y que reportó Ars Technica, pasar de HBM3E a HBM4 y HBM4E empeora esa relación.\[6\] Cada generación nueva se come todavía más oblea por bit.

Y las fábricas nuevas no salen al tiro. Micron mismo dice que su planta ID2 en Idaho recién empezaría a sacar obleas a fines de 2028.\[1\]

Y acá entra un tema que nos encanta en el canal: la litografía EUV.

La EUV usa luz con una longitud de onda muchísimo más corta que la ultravioleta profunda de antes. Con una luz más fina se pueden dibujar líneas más finas en una sola pasada, en vez de partir el patrón en dos o tres exposiciones y alinearlas con una precisión absurda. Menos pasos, menos defectos, más densidad.

El nodo 1-gamma de Micron, el que está usando para sus módulos de servidor de 8.800 MT/s y para sus primeras muestras de LPDDR6, va amarrado a la EUV: en su informe a accionistas del año pasado, Micron contó que instaló su primera herramienta EUV en Japón con capacidad 1-gamma.\[2\]\[7\]

¿Por qué importa? Porque ASML es la única que fabrica esas máquinas, y el ritmo al que puede crecer la memoria de punta depende del ritmo al que llegan.\[8\]

Como contexto, y esto es de antes de nuestra ventana: el 8 de septiembre, según CNBC, Samsung dijo que planea usar High-NA EUV para fabricar DRAM desde 2028.\[9\] O sea, la próxima vuelta de tuerca tecnológica también está fechada para 2028. Calza con todo lo demás.

¿A quién le conviene esto? A Micron, a Samsung y a SK Hynix, obvio. Micron dice tener 26 acuerdos estratégicos con clientes que cubren más de un 35% de sus ingresos hasta 2030.\[10\]

¿A quién le duele? A ustedes. A mí. Al que quiere armar PC.

Y no es teoría. El 1 de octubre, Raspberry Pi subió 12,50 dólares los modelos de 2 GB del Pi 4 y del Pi 5, culpando directamente al costo de la memoria. El Pi 5 de 2 GB quedó en 77,50 dólares, unos 76 mil pesos, y con el 19% de IVA que se paga en compras al extranjero bajo 500 dólares se va sobre 90 mil. Un computador que nació con la promesa de costar 35 dólares.\[11\]\[12\]

Intenté cruzar esto con precios de módulos en PC Factory, SPDigital, Winpy o Solotodo esta semana y no logré verificarlo, así que no les voy a inventar una cifra.

Mi opinión: esto ya no es el ciclo normal de la memoria, de esos de un par de años arriba y un par abajo. Cuando el fabricante te dice que tiene más de tres cuartos de 2027 vendido y que 2028 viene peor, el que está esperando que la RAM baje para Navidad está esperando en vano.

Mi consejo, y es opinión mía: si necesitan RAM o un SSD para la pega o para la tesis, no esperen un milagro. Y si su PC actual anda, estírenlo.

Y un consejo no pedido para Micron: si quieren que el mercado de consumo no los mire feo, reserven una fracción fija de su producción para módulos de consumo con precio predecible. Con márgenes de 87% les sobra espacio.

Especulación mía para uno o dos años: notebooks y celulares con menos memoria al mismo precio, y fabricantes vendiéndote la versión recortada como si fuera novedad. De hecho, eso ya está pasando, y es justo la siguiente noticia.

[NOTICIA 2: NVIDIA te vende la mitad de memoria por más plata]
Y hablando de memoria recortada: el viernes 2 de octubre NVIDIA anunció una versión de 64 GB del DGX Spark. Confirmado por la empresa.\[13\]

Para el que no lo ubica, el DGX Spark es el computadorcito de escritorio de NVIDIA para IA local. Usa el chip GB10 Grace Blackwell, con CPU y GPU compartiendo un mismo pool de memoria unificada.\[14\]

Y eso es lo importante. En un modelo de lenguaje, los parámetros tienen que caber en memoria. No en el disco: en memoria. Si no caben, no corre, o corre a paso de tortuga. En estos equipos, la memoria define qué puedes hacer.

NVIDIA dice que la versión de 64 GB corre modelos de hasta 100 mil millones de parámetros, contra 200 mil millones de la original de 128 GB.\[15\]

El precio: desde 4.999 dólares, a la venta el 23 de octubre, solo a través de Acer, ASUS, Dell, Gigabyte, HP y MSI. No hay Founders Edition de 64 GB.\[16\]

Ahora, el chiste. La versión original de 128 GB se lanzó en octubre de 2025 a 3.999 dólares, y en febrero de 2026 NVIDIA la subió a 4.699 citando la escasez de memoria.\[15\]\[16\]

O sea, la versión con la mitad de memoria cuesta más que lo que costaba la completa en su lanzamiento. Bacán, ¿no?

Y acá hay una contradicción que les tengo que contar. The Register dice que la de 128 GB subió ahora a 6.950 dólares, y medios financieros chinos dicen lo mismo. Pero VideoCardz compara contra un precio vigente de 4.699. No sé cuál es el precio de hoy, y no voy a elegir uno a escondidas. The Register agrega que la de 64 GB trae también la mitad del almacenamiento.\[13\]\[15\]\[16\]

NVIDIA propone que, si te queda corto, conectes dos unidades para juntar 128 GB.\[17\] O sea, comprar dos para tener lo que antes venía en una. Para mí esto es marketing del más penca: te venden la escasez como si fuera flexibilidad.

En pesos, 4.999 dólares son unos 4,9 millones. Y como pasa de 500 dólares, si lo traen por courier pagan 6% de arancel sobre el valor con flete y seguro, y encima 19% de IVA.\[18\]\[19\] Sin contar el flete, queda sobre 6,2 millones. Ojo que algunas guías de couriers dicen que productos amparados por tratados de libre comercio pueden salvarse del 6%, pero eso no lo vi confirmado por Aduanas.\[20\]

Tampoco encontré anuncio de venta oficial en Chile. Si llega, apuesto a que llega tarde y con margen de retail encima.

[NOTICIA 3: Acusan a californiano de contrabandear GPUs NVIDIA a China]
Y ya que estamos con NVIDIA, pasemos a tribunales.

El jueves 1 de octubre arrestaron en California a Greg Lui, de 38 años, dueño de una empresa llamada Earthmade Computer. Esto viene de una acusación formal de la fiscalía federal de Los Ángeles, o sea, documento oficial. Pero ojo: es una acusación, no una condena.\[21\]\[22\]

Según los fiscales, entre 2023 y 2024 Lui habría ayudado a sacar de Estados Unidos más de 300 millones de dólares en servidores con GPUs NVIDIA sujetas a control de exportación.\[23\]\[24\] Unos 295 mil millones de pesos.

¿Cómo? Con papeles falsos y triangulando. Los servidores iban a Malasia y Singapur, que no necesitan licencia del Departamento de Comercio, y desde ahí empresas locales los reenviaban a China.\[21\]

Un ejemplo de la acusación, según Social News XYZ citando a IANS: una orden de enero de 2024 por 27 servidores con GPUs H100, por unos 7,6 millones de dólares, despachada desde Los Ángeles a Kuala Lumpur. En marzo de 2024, un supuesto cómplice le habría escrito por correo a un funcionario malasio que esos servidores ya se habían reenviado a un comprador en China.

Además, según The Register, los fiscales sostienen que Lui recibió más de 176 millones de dólares de dos empresas de Malasia.\[21\]

Son tres cargos: conspiración para violar la ley de control de exportaciones, contrabando de salida y conspiración para lavado de dinero. Gadget Review titula que arriesga 20 años y The Register habla de 50, pero no es contradicción: según las cifras del Departamento de Justicia que reportaron Quartz y CBS Los Angeles, cada uno de los dos cargos de conspiración tiene un máximo de 20 años y el de contrabando hasta 10, lo que suma 50 en total. El gran jurado presentó la acusación el 29 de septiembre.

Para entender por qué importa: el control de exportación no prohíbe fabricar las GPUs, prohíbe que lleguen a ciertos destinos sin licencia. El problema es que un servidor es una caja. Una vez que sale, la cadena de custodia depende de papeles. Y los papeles se falsifican.

No es el primer caso. El 19 de marzo de 2026 arrestaron a Yih-Shyan "Wally" Liaw, cofundador de Super Micro, acusado por la fiscalía federal de Manhattan junto con Ruei-Tsang "Steven" Chang y Ting-Wei "Willy" Sun de desviar unos 2.500 millones de dólares en servidores con NVIDIA a China, según el 8-K de Super Micro ante la SEC; según Bloomberg, Liaw se declaró no culpable, y según TipRanks, el juicio está fijado para el 2 de noviembre. Y el 24 de agosto, según AP y PBS, la fiscalía del distrito de Keelung, en Taiwán, presentó cargos contra nueve personas, entre ellas un gerente de NVIDIA Taiwán de apellido Chang y dos gerentes de ventas de Super Micro Taiwán, por 130 servidores B300: 74 llegaron a China y 56 fueron interceptados.

Mi opinión: esto es jugar al topo. Cierran una ruta y aparece otra por el país vecino. Mientras la demanda de cómputo en China siga así, el incentivo para triangular es enorme.

Consejo no pedido para NVIDIA y sus socios: si el negocio depende de que la caja no termine donde no debe, inviertan en verificar dónde está el hardware ya instalado, no solo en formularios. Es especulación mía, pero me parece que por ahí va a venir la presión regulatoria.

[NOTICIA 4: Ubuntu 26.10 llega con un kernel todavía en el horno]
En fin, pasemos a software de bajo nivel, que para muchos de ustedes es la pega diaria.

El 1 de octubre salió la beta de Ubuntu 26.10, con el kernel Linux 7.3 y GNOME 51. Confirmado por Canonical y reportado por Phoronix.\[25\]

Lo curioso es la historia del kernel. En mayo, Canonical había dicho que 26.10 usaría Linux 7.2. Pero como los ciclos de 7.1 y 7.2 no se atrasaron, el equipo decidió subir la apuesta a 7.3.\[26\]

El detalle: según OMG! Ubuntu, Ubuntu 26.10 sale el 15 de octubre, y según Phoronix, Linux 7.3 estable se espera recién para el 18 de octubre. O sea, Ubuntu va a salir con un kernel que, al momento de cerrarse, todavía era una release candidate.\[27\]\[28\]

¿Es grave? No tanto. Una RC tardía es bastante sólida. Para una versión que no es LTS, yo creo que la apuesta se entiende. Pero si están en un servidor de producción, quédense en la 26.04 LTS, que según OMG! Ubuntu recibiría este kernel por la actualización HWE a principios de 2027.\[28\]

¿Qué trae Linux 7.3 que les importe? Según Phoronix, en las últimas RC siguieron llegando arreglos al planificador "cache aware".\[27\] La idea es que el planificador intente mantener juntas, en la misma caché de último nivel, a las tareas que comparten datos, para que no anden saltando entre grupos de núcleos y botando lo que tenían en caché. En CPUs con núcleos híbridos o con varios chiplets, eso pesa harto.

Phoronix comenta además que las RC vienen grandes, en buena parte porque agentes de IA están encontrando problemas en un código que ya va en casi 41 millones de líneas.\[27\] Eso, para mí, es lo más interesante del ciclo.

Y de pasada: Intel mandó su último lote de mejoras del driver Xe para Linux 7.4, y Phoronix dice que trae una mejora importante para las gráficas Battlemage.\[25\] Si tienen una Arc, ojo con eso.

[CHILE: Octubre llega con CTF, consulta pública y datacenters]
Y ahora, lo que pasa acá.

Lo más concreto de la semana viene de la Agencia Nacional de Ciberseguridad, la ANCI, la que creó la Ley 21.663 marco de ciberseguridad.\[29\]

El jueves 1 de octubre la ANCI inauguró el Mes de la Ciberseguridad con tres anuncios, según TrendTIC.

Uno: un portal para la ciudadanía.

Dos: durante octubre abre una consulta pública sobre autenticación multifactor, como paso previo a un estándar obligatorio para todas las instituciones sujetas a la ley marco.\[30\] Esto sí es novedad regulatoria fechada. Si trabajan en TI en un organismo público o en un operador de importancia vital, les va a llegar a la pega. Mi consejo: participen de la consulta, porque el estándar sale igual y es mejor que lo escriba gente que sabe.

Tres: el primer ejercicio nacional de ciberseguridad, un CTF para instituciones públicas y privadas, también en octubre.\[30\]

Y para los estudiantes de la Santa María, ojo: el 7 y 8 de octubre es el Seminario Internacional de Ciberseguridad de la PDI, coorganizado con la USM, en la Escuela de Investigaciones Policiales. Y por primera vez trae un CTF, con desafíos de hacking web, forense digital y criptografía. Revisen la preinscripción en el sitio de la PDI.\[31\] Para un estudiante de Informática, un CTF es de lo mejor que se puede poner en el currículum.

Además, el martes 6 de octubre hay un summit de ciberseguridad entre la Unión Europea y la ANCI en Santiago. Según Diario Financiero, a la ANCI le reportaron más de 320 incidentes en el primer semestre de 2026.\[32\]

En datacenters, el 30 de septiembre salió un informe de Colliers que cuenta 36 data centers operando en Chile, con 255 MW instalados, y 34 desarrollos futuros entre proyectos nuevos y ampliaciones.\[33\] Ojo que otro informe comercial, de ResearchAndMarkets, habla de unos 39 en operación, así que los conteos no calzan.\[34\]

Lo que me llamó la atención: según Colliers, el proyecto Alto Jahuel, de Terranova, es el primer data center que se eximió de entrar al Sistema de Evaluación de Impacto Ambiental.\[33\] Con todo el debate que hay por agua y energía, para mí eso merece harta más atención de la que está recibiendo.

Y de la USM, una investigación del Departamento de Ingeniería de Minas, Metalurgia y Materiales sobre tecnología WAAM, que es fabricar piezas de metal capa por capa con un robot, e incluye desarrollar un slicer propio.\[35\] Ingeniería de la buena.

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

# candidatas.md

Nota: historial.md no vino adjunto. Siguiendo la regla del prompt, se asumió que no hay historial previo (aunque este es el episodio 2) y se creó desde cero. Por eso todas las candidatas dentro de la ventana quedan como NUEVA.

| hecho | fecha del hecho | cobertura | estatus | hilo | clasificación | puntaje | decisión | motivo |
|---|---|---|---|---|---|---|---|---|
| Micron reporta ingresos récord de US$54.230 M en el Q4 fiscal 2026 y prevé una oferta de memoria más apretada en 2027-2028 | 2026-09-30 | 7+ (SEC 8-K, TechPowerUp, Yahoo Finance, Investing.com, 24/7 Wall St., Stocktwits/TradingView, Seoul Economic Daily, Invezz) | Confirmado por la empresa (documento oficial ante la SEC) | — (crea hilo escasez-memoria-ia) | NUEVA | 12 (3+3+3+3, +1 prioritario, con tope 12) | NOTICIA 1 | PRIORITARIO — impacto en DRAM/HBM y dependencia de la EUV; puntaje más alto; categoría memoria |
| NVIDIA lanza el DGX Spark de 64 GB desde US$4.999 (23 de octubre); hay versiones contradictorias sobre el precio de la versión de 128 GB | 2026-10-02 | 7+ (VideoCardz, The Register, Tom's Hardware, The PC Enthusiast, tbreak, WindowsForum, KuCoin/Futu) | Confirmado por la empresa | — | NUEVA | 9 (1+2+3+3) | SECUNDARIA | Categoría GPU libre; la escasez de memoria se hace concreta en un producto |
| EE.UU. acusa a Greg Lui (Earthmade) de contrabandear a China servidores con GPUs NVIDIA por más de US$300 M | 2026-10-01 (arresto); acusación del gran jurado: 2026-09-29 | 7+ (The Register, Bloomberg/Yahoo, Courthouse News, Transport Topics, Hoodline, Gadget Review, AI Weekly) | Documento oficial (acusación formal del Departamento de Justicia) | — (crea hilo control-exportacion-gpus-china) | NUEVA | 9 (2+1+3+3) | SECUNDARIA | Evento mayor obligatorio (control de exportación ligado a NVIDIA); categoría industria y negocios |
| Sale la beta de Ubuntu 26.10 con Linux 7.3 (RC) y GNOME 51 | 2026-10-01 | 2-3 (Phoronix, OMG! Ubuntu) | Confirmado por la empresa (Canonical) | — | NUEVA | 8 (2+2+3+1) | SECUNDARIA | Categoría software de bajo nivel libre; afecta la pega de desarrolladores |
| Raspberry Pi sube US$12,50 sus modelos de 2 GB (Pi 4 y Pi 5) por el costo de la memoria | 2026-10-01 | 7+ (OMG! Ubuntu, Hardware Busters, OC3D, Aroged, The Register, Borecraft, pasqualepillitteri.it) | Confirmado por la empresa | escasez-memoria-ia | NUEVA | 9 (1+2+3+3) | DESCARTADA (mencionada dentro de NOTICIA 1) | Categoría memoria ocupada por Micron; es un efecto aguas abajo del mismo hecho, no un tema prioritario de fabricación |
| Intel envía su último lote de mejoras del driver Xe para Linux 7.4, con una mejora grande para Battlemage | 2026-10-01/02 | 1 (Phoronix) | Confirmado (parches upstream de Intel) | — | NUEVA | 5 (1+1+3+0) | DESCARTADA (mencionada de pasada en NOTICIA 4) | Categoría software de bajo nivel ocupada por una candidata de más puntaje |
| Linux 7.4 suma los primeros Device Trees para Apple M4 y A18 Pro (MacBook Neo) | 2026-10-02 | 1 (Phoronix) | Confirmado (pull request upstream) | — | NUEVA | 4 (1+0+3+0) | DESCARTADA | Bajo el umbral de 5 puntos; categoría ocupada |
| Steam on Linux baja a 3,05% en la encuesta de septiembre de 2026 | 2026-10-01 | 1 (Phoronix) | Documento oficial (Steam Survey) | — | NUEVA | 4 (1+0+3+0) | DESCARTADA | Bajo el umbral; poco impacto para la audiencia |
| Samsung y SK Hynix llevan cerca del 80% de su recompra conjunta de acciones de 55 billones de wones | 2026-09-30 | 1 (Bloomberg) | Cálculo de Bloomberg con datos de la bolsa | — | NUEVA | 4 (2+0+2+0) | DESCARTADA | Bajo el umbral; es noticia bursátil, no de hardware |
| SK Hynix publica una aclaración sobre reportes de prensa acerca de Solidigm | 2026-10-01 | 1 (SK Hynix Newsroom) | Comunicado de la empresa (contenido no verificado) | — | NUEVA | 3 (1+0+2+0) | DESCARTADA | No se pudo verificar qué se aclara; bajo el umbral |
| VSMC (VIS y NXP) inaugura su fábrica de obleas de 12 pulgadas en Singapur | 2026-09-28 | 1 (Digitimes) | Reportado por un medio | — | NUEVA | 4 (2+0+2+0) | DESCARTADA | Bajo el umbral; cobertura mínima |
| Renuncia el presidente de NSIG (proveedor chino de obleas de silicio) | 2026-09-30 | 1 (Digitimes) | Reportado por un medio | — | NUEVA | 3 (1+0+2+0) | DESCARTADA | La empresa no está en la lista 1c; bajo el umbral |
| La aprobación eléctrica retrasaría el datacenter de IA de Oracle en Wisconsin | 2026-10-02 | 1 (The Register) | Reportado por un medio | — | NUEVA | 4 (1+0+2+1) | DESCARTADA | Bajo el umbral; impacto indirecto |
| Amazon destina US$1.000 M a programas comunitarios para bajar la resistencia a sus datacenters | 2026-10-02 | 1 (The Register) | Reportado por un medio | — | NUEVA | 4 (1+0+2+1) | DESCARTADA | Bajo el umbral |
| Google lanza su primer satélite de datacenter y publica una investigación al respecto | 2026-10-02 | 1 (The Register) | Confirmado por la empresa, según el medio | — | NUEVA | 4 (1+0+3+0) | DESCARTADA | Bajo el umbral; experimental |
| CoreWeave anuncia que desplegará la plataforma Vera Rubin de NVIDIA | ~2026-09-30 | 1 (CNBC, mención) | Anuncio de la empresa, según el medio | — | NUEVA | 4 (1+0+3+0) | DESCARTADA | Bajo el umbral; sin detalle verificado |
| Precio spot de DRAM según TrendForce: DDR5 16Gb con un promedio de sesión de 58,00 y +0,12% | 2026-10-02 | 1 (TrendForce) | Dato de mercado | escasez-memoria-ia | REPETIDA | — | DESCARTADA | Solo confirma una tendencia que sigue igual; no hay quiebre fechado |
| kopite7kimi dice que las GPUs GR20x (RTX 60) se postergan a 2028 | 2026-09-21 | 7+ (VideoCardz, TechSpot, Tom's Hardware, Club386, etc.) | Rumor de leaker nivel A | — | FUERA DE VENTANA | — | DESCARTADA | El hecho es anterior al 25 de septiembre y no es un evento mayor de 1d |
| Kepler_L2 dice que RTX 60 y la mayoría de RDNA 5 llegarían en 2028 | ~2026-09-16 | 2-3 (Notebookcheck, TechSpot) | Rumor de leaker nivel A | — | FUERA DE VENTANA | — | DESCARTADA | Fuera de ventana; no es un evento mayor |
| Moore's Law Is Dead dice, citando a una fuente anónima de NVIDIA, que la RTX 6090 estaría lista en 2027 | 2026-09-23 | 1-2 (WindowsForum) | Rumor de leaker nivel C | — | FUERA DE VENTANA | — | DESCARTADA | Fuera de ventana; nivel C sin excepción aplicable |
| Moore's Law Is Dead dice que la CCD Zen 6 "Powderhorn" llegó al stepping B0 | ~2026-09-15 | 2-3 (TweakTown, Tech Insider) | Rumor de leaker nivel C | — | FUERA DE VENTANA | — | DESCARTADA | Fuera de ventana; nivel C |
| ASML y TSMC lanzan una iniciativa de máscaras de 12 pulgadas para High-NA; TSMC usaría High-NA en volumen desde 2030 | 2026-09-07/08 | 4-6 (ASML, CNBC, TrendForce, Tech Times, Tom's Hardware) | Confirmado por las empresas | — | FUERA DE VENTANA | — | DESCARTADA (usada como contexto fechado en NOTICIA 1) | PRIORITARIO — fuera de ventana; solo contexto |
| Intel Foundry y ASML: más de un millón de obleas procesadas con High-NA EUV | 2026-09-07/08 | 2-3 (ASML, Intel, TrendForce) | Confirmado por las empresas | — | FUERA DE VENTANA | — | DESCARTADA | PRIORITARIO — fuera de ventana |
| Samsung usaría High-NA EUV para fabricar DRAM desde 2028 | 2026-09-08 | 2-3 (CNBC, Tech Times) | Confirmado por la empresa, según los medios | — | FUERA DE VENTANA | — | DESCARTADA (usada como contexto fechado en NOTICIA 1) | PRIORITARIO — fuera de ventana |
| ASML: 10 sistemas High-NA operando en 4 clientes (SEMICON Taiwan) | ~2026-09-01 | 2-3 (TrendForce, citando a TechNews y Economic Daily News) | Declaraciones de un ejecutivo, según los medios | — | FUERA DE VENTANA | — | DESCARTADA | PRIORITARIO — fuera de ventana |
| Prototipo chino de EUV en Shenzhen (reportaje de Reuters) | 2025-12 | 7+ (Notebookcheck, SCMP, Tom's Hardware, etc.) | Reportaje periodístico sin documentos públicos | — | FUERA DE VENTANA | — | DESCARTADA | PRIORITARIO — hecho de diciembre de 2025; en la ventana no hubo hecho fechado nuevo |
| India prohíbe a las plantas de Semicon 2.0 vender o hipotecar activos antes de producir | Pautas del 2026-09-17 | 1 (Digitimes) | Documento oficial, según el medio | — | FUERA DE VENTANA | — | DESCARTADA | Hecho anterior a la ventana |
| ANCI inaugura el Mes de la Ciberseguridad: portal ciudadano, consulta pública sobre MFA y primer CTF nacional | 2026-10-01 | 2-3 (TrendTIC, ANCI) | Confirmado por la institución | — (crea hilo anci-ley-21663) | NUEVA | 9 (2+2+3+1) | CHILE | Novedad regulatoria fechada (consulta para un estándar obligatorio bajo la Ley 21.663) |
| Seminario Internacional de Ciberseguridad PDI-USM con su primer CTF (7 y 8 de octubre) | Anuncio vigente; evento el 2026-10-07/08 | 1 (PDI) | Confirmado por la institución | — | NUEVA | 6 (1+2+3+0) | CHILE | Oportunidad concreta para estudiantes; con participación de la USM |
| Summit de ciberseguridad UE-ANCI (6 de octubre); más de 320 incidentes reportados en el primer semestre | Anuncio en la ventana; evento el 2026-10-06 | 1 (Diario Financiero) | Confirmado por los organizadores | anci-ley-21663 | NUEVA | 6 (1+1+3+1) | CHILE | Complementa el bloque ANCI |
| Informe de Colliers: 36 data centers operando (255 MW) y 34 desarrollos futuros; Alto Jahuel eximido del SEIA | 2026-09-30 | 2-3 (Construnoticias, GlobeNewswire/ResearchAndMarkets con cifras distintas) | Informe de consultora | — (crea hilo datacenters-chile) | NUEVA | 6 (2+1+2+1) | CHILE | Dato fechado sobre la infraestructura local; incluye la polémica ambiental |
| USM: investigación en tecnología WAAM (fabricación aditiva de metal) | 2026-10-01 | 1 (Portal Innova) | Comunicado institucional, según el medio | — | NUEVA | 4 | CHILE (mención breve) | Prioridad a la USM dentro del bloque Chile |
| Chile proyecta 367,8 MW de nueva capacidad de data centers hasta 2031 (DCD) | 2026-09-23 | 1 (DCD) | Reportado por un medio | datacenters-chile | FUERA DE VENTANA | — | DESCARTADA | Anterior al 25 de septiembre |
| Estudio de PwC: Chile podría atraer hasta US$162.000 M en data centers hacia 2050 | 2026-09-23 | 2-3 (Mundo en Línea, TrendTIC) | Estudio de consultora (proyección) | datacenters-chile | FUERA DE VENTANA | — | DESCARTADA | Anterior a la ventana; es una proyección |
| Chile Data Centers Summit 2026 | 2026-09-08 | 2-3 | Evento | datacenters-chile | FUERA DE VENTANA | — | DESCARTADA | Fuera de ventana |
| Régimen de courier en Chile (exención de arancel hasta US$500 y 19% de IVA, Ley 21.713) | Vigente desde 2025-10-25 | — | Documento oficial (Aduanas, SII) | — | FUERA DE VENTANA | — | DESCARTADA (usado como contexto) | No hubo un cambio fechado en la ventana; solo sirve para calcular precios |

**Páginas o búsquedas de la fase 1 que fallaron o no se completaron**
- https://www.techpowerup.com/news-archive: el sitio bloquea el acceso automatizado (robots). Se reemplazó con resultados de web_search.
- https://videocardz.com/: la portada se abrió, pero vino sin titulares (contenido vacío o antiguo). Se reemplazó con web_search.
- https://www.tomshardware.com/news/archive: abrió, pero el texto que llegó solo traía el menú, sin titulares fechados.
- https://www.theregister.com/: abrió bien. Sus artículos individuales no se pudieron abrir directo por restricciones de la herramienta; se recuperaron vía web_search.
- https://www.servethehome.com/, https://nvidianews.nvidia.com/, https://anid.cl/concursos/ y https://www.asml.com/en/news: no se abrieron directo. ASML se cubrió parcialmente con resultados de búsqueda; de ANID no se verificaron convocatorias.
- https://informatica.usm.cl/noticias/: no se abrió directo. Vía búsqueda apareció como última noticia una del 28 de julio de 2026, sin nada en la ventana.
- 1b. Búsquedas temáticas: por el límite de búsquedas de la sesión, quedaron sin ejecutar de forma individual "lanzamiento procesador", "lanzamiento tarjeta de video", "filtración GPU", "filtración CPU", "Samsung Foundry", "Intel Foundry", "SSD NAND", "datacenter IA", "driver GPU", "vulnerabilidad CPU", "ARM RISC-V", "litografía EUV alternativa rayos X láser de electrones libres" (la búsqueda falló por falta de presupuesto) y "EUV DRAM HBM NAND". Se ejecutaron o se cubrieron parcialmente: precio memoria DRAM, ASML High-NA EUV, China EUV, Linux kernel, TSMC (dentro de High-NA) y filtraciones de GPU/CPU (kopite7kimi, Zen 6).
- 1c. Barrido por empresa: solo se ejecutaron búsquedas útiles para Intel (los resultados fueron de 2025, fuera de ventana), Micron, Samsung/SK Hynix y NVIDIA (vía DGX Spark y contrabando). AMD, TSMC, Qualcomm, ARM, Apple silicon y ASML no tuvieron búsqueda específica de eventos mayores; un evento mayor de esas empresas podría haberse escapado.
- 1d. Rezagadas (18 al 24 de septiembre): no se ejecutó un barrido dedicado; solo aparecieron rumores (kopite7kimi, Kepler_L2, MLID), que no califican como eventos mayores.
- 1e. Ronda Chile: no se buscaron por separado Subtel/fibra/cables, Ley 21.719, Corfo, Startup Chile, becas, ALMA/Vera Rubin/ELT/NLHPC ni ofertas laborales. La CMF no se revisó.
- Precios locales en PC Factory, SPDigital, Winpy y Solotodo: no se verificaron.
- Tarifa eléctrica chilena: no se buscó (no hubo noticia de consumo eléctrico alto en el guion).

# historial.md

Nota: este historial se creó desde cero en el episodio 2 (2026-10-02) porque el historial.md previo no vino adjunto. Si existía un historial del episodio 1, hay que fusionarlo con este a mano.

## HILO: escasez-memoria-ia
- Descripción: escasez y alza de precios de DRAM, HBM y NAND causada por la demanda de IA, con su impacto en productos de consumo.
- Estado actual: Micron (Q4 fiscal 2026, 30 de septiembre de 2026) reportó US$54.230 M de ingresos, un margen bruto de 86,8% y una guía de US$61.500 M ± 1.500 M para el Q1 fiscal 2027. Su CEO dice que la oferta estará mucho más apretada en 2027-2028 y que no se ve el equilibrio; más del 75% de la producción de 2027 ya está comprometida. Las fuentes no coinciden en si hablaba de años fiscales o calendario. Raspberry Pi subió US$12,50 sus modelos de 2 GB el 1 de octubre. La planta ID2 de Micron sacaría obleas a fines de 2028.
- Cubierto en: ep 2 (2026-10-02) como NOTICIA 1 — resultados récord de Micron, la HBM se come más oblea por bit, la EUV en el nodo 1-gamma, el alza de Raspberry Pi; opinión: no esperar que la RAM baje.
- Reabrir solo si: un fabricante (Micron, Samsung o SK Hynix) cambia su guía de oferta para 2027-2028; TrendForce u otro analista reporta una caída trimestral de precios contractuales de DRAM o NAND; se anuncia una fábrica nueva que adelante capacidad; Samsung o SK Hynix publican resultados del Q3 2026 con un quiebre de tendencia; o hay un alza o baja de precios verificable en el retail chileno.

## HILO: control-exportacion-gpus-china
- Descripción: controles de exportación de EE.UU. sobre GPUs de IA hacia China y los casos de contrabando o triangulación.
- Estado actual: el 1 de octubre de 2026 arrestaron a Greg Lui (Earthmade Computer), acusado de enviar a China más de US$300 M en servidores con GPUs NVIDIA vía Malasia y Singapur; la acusación del gran jurado es del 29 de septiembre. Tiene tres cargos, con un máximo combinado de 50 años según las cifras del DOJ. Antecedentes: Wally Liaw (Super Micro), arrestado el 19 de marzo de 2026, se declaró no culpable y su juicio está fijado para el 2 de noviembre; en Taiwán, la fiscalía de Keelung acusó el 24 de agosto de 2026 a nueve personas por 130 servidores B300 (74 llegaron a China).
- Cubierto en: ep 2 (2026-10-02) como SECUNDARIA (NOTICIA 3) — acusación contra Greg Lui y la triangulación por el sudeste asiático; opinión: es jugar al topo.
- Reabrir solo si: hay una condena, una declaración de culpabilidad o un sobreseimiento en los casos de Lui o Liaw (el juicio de Liaw está fijado para el 2 de noviembre de 2026); EE.UU. cambia las reglas de exportación (nuevas licencias, nuevos países con requisitos); o NVIDIA anuncia mecanismos de verificación de ubicación del hardware.

## HILO: anci-ley-21663
- Descripción: implementación de la Ley 21.663 marco de ciberseguridad y la actividad regulatoria de la ANCI.
- Estado actual: el 1 de octubre de 2026 la ANCI anunció un portal ciudadano, una consulta pública durante octubre sobre autenticación multifactor (previa a un estándar obligatorio) y el primer CTF nacional en octubre. Más de 320 incidentes reportados en el primer semestre de 2026 (según DF). Summit UE-ANCI el 6 de octubre.
- Cubierto en: ep 2 (2026-10-02) como CHILE — los tres anuncios del Mes de la Ciberseguridad y el seminario PDI-USM con CTF.
- Reabrir solo si: se publica el texto de la consulta MFA o el estándar obligatorio final; la ANCI publica resultados del CTF nacional o del Boletín de Amenazas; se aplica la primera sanción bajo la ley; o cambia la calificación de Operadores de Importancia Vital.

## HILO: datacenters-chile
- Descripción: inversión, capacidad y polémicas (agua, energía, permisos ambientales) de los datacenters en Chile.
- Estado actual: Colliers (30 de septiembre de 2026) cuenta 36 data centers operando con 255 MW y 34 desarrollos futuros; ResearchAndMarkets habla de unos 39 operando. Alto Jahuel (Terranova) sería el primero eximido del SEIA.
- Cubierto en: ep 2 (2026-10-02) como CHILE — informe de Colliers y la exención ambiental de Alto Jahuel.
- Reabrir solo si: un proyecto concreto recibe aprobación o rechazo ambiental, se judicializa o recibe una nueva inversión anunciada con monto; cambian las reglas del SEIA para datacenters; o hay un conflicto fechado por agua o energía.

## Noticias puntuales
- ep 2 (2026-10-02) — NVIDIA DGX Spark de 64 GB desde US$4.999 (23 de octubre, solo vía OEMs); las fuentes no coinciden sobre si la versión de 128 GB cuesta US$4.699 o US$6.950.
- ep 2 (2026-10-02) — Beta de Ubuntu 26.10 (1 de octubre) con Linux 7.3 aún en RC; versión final el 15 de octubre y Linux 7.3 estable esperado el 18 de octubre. Mención breve: mejora del driver Xe para Battlemage en Linux 7.4.
- ep 2 (2026-10-02) — Seminario Internacional de Ciberseguridad PDI-USM (7 y 8 de octubre) con su primer CTF.
- ep 2 (2026-10-02) — USM: investigación en tecnología WAAM (Depto. de Ingeniería de Minas, Metalurgia y Materiales).

## Hilos inactivos
(Ninguno todavía.)

## REGISTRO DE LEAKERS

### kopite7kimi
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno usado en el guion del ep 2; su rumor del 21 de septiembre de 2026 sobre RTX 60 en 2028 quedó fuera de ventana y no se usó)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Kepler_L2
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno usado en el guion del ep 2)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### Jaykihn
- Nivel: A
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno)
- Balance: cumplidos 0, fallidos 0, pendientes 0

### HXL (@9550pro)
- Nivel: B
- Base del nivel: punto de partida editorial.
- Rumores registrados:
  - (ninguno)
- Balance: cumplidos 0, fallidos 0, pendientes 0

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

## Fuentes

1. [Micron CEO Says Memory Supply Will Be Much Tighter in 2027 and 2028 Than in 2026](https://www.techpowerup.com/353296/micron-ceo-says-memory-supply-will-be-much-tighter-in-2027-and-2028-than-in-2026)
2. [Document](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm)
3. [Chile’s Peso Falls to Its Weakest in Over a Year: What Expats Need to Know](https://www.riotimesonline.com/chile-peso-weakest-in-over-a-year-expats-2026/)
4. [Micron Blew Past Estimates and Says It Can't See When the Memory Shortage Ends - 24/7 Wall St.](https://247wallst.com/investing/2026/10/01/micron-blew-past-estimates-and-says-it-cant-see-when-the-memory-shortage-ends/)
5. [Why Americans pay 41% more for SK Hynix shares than Koreans - Asia Times](https://asiatimes.com/2026/10/why-americans-pay-41-more-for-sk-hynix-shares-than-koreans)
6. [Micron CEO: Memory Supply 75% Sold Out for 2027 \[2026\]](https://tech-insider.org/micron-ceo-2027-memory-supply-sold-out-2026/)
7. [MICRON TECHNOLOGY INC - Form DEF 14A - FY2026](https://www.sec.gov/Archives/edgar/data/723125/000072312525000038/mu-20251125.htm)
8. [China eyes mastery of EUV lithography, bolstering AI chip ambitions, analysts say](https://www.scmp.com/tech/tech-war/article/3337100/china-eyes-mastery-euv-lithography-bolstering-ai-chip-ambitions-analysts-say)
9. [TSMC, Samsung to use ASML High NA EUV tools for AI chips](https://www.cnbc.com/2026/09/08/tsmc-samsung-asml-high-na-euv-machine-ai-chips.html)
10. [Micron CFO: No ‘line of sight’ for when memory shortage will end](https://finance.yahoo.com/technology/article/micron-cfo-no-line-of-sight-for-when-memory-shortage-will-end-165934130.html)
11. [A 2GB Raspberry Pi 4 now costs 50% more than it did at launch - OMG! Ubuntu](https://www.omgubuntu.co.uk/2026/10/raspberry-pi-2gb-costs-how-much-now)
12. [Raspberry Pi 5 2GB Price Climbs to \$77.50 as Memory Costs Finally Catch the Cheap Boards - Hardware Busters](https://hwbusters.com/news/raspberry-pi-5-2gb-price-climbs-to-77-50-as-memory-costs-finally-catch-the-cheap-boards/)
13. [NVIDIA Launches 64GB DGX Spark at \$4,999; 128GB Version Priced at \$6,950](https://www.kucoin.com/news/flash/nvidia-launches-64gb-dgx-spark-at-4999-128gb-version-rises-to-6950)
14. [NVIDIA DGX Spark 64GB Launches for \$4,999 on October 23](https://thepcenthusiast.com/nvidia-dgx-spark-64gb-price-release-date/)
15. [NVIDIA DGX Spark drops to 64GB memory but costs more than the original 128GB version - VideoCardz.com](https://videocardz.com/newz/nvidia-dgx-spark-drops-to-64gb-memory-but-costs-more-than-the-original-128gb-version)
16. [Nvidia DGX Spark 64GB Launches at \$4,999 as 128GB Model Price Rises](https://windowsforum.com/news/nvidia-dgx-spark-64gb-launches-at-4-999-as-128gb-model-price-rises.446991/)
17. [NVIDIA has introduced a 64GB version of DGX Spark with halved memory, starting at \$4,999, while raising the price of the 128GB version to \$6,950.](https://news.futunn.com/en/post/1000536008/nvidia-has-introduced-a-64gb-version-of-dgx-spark-with)
18. [¿Cuándo debo pagar Impuestos?](https://www.aduana.cl/cuando-debo-pagar-impuestos/aduana/2018-12-12/233227.html)
19. [Sin arancel aduanero hasta USD 500](https://www.aduana.cl/sin-arancel-aduanero-hasta-usd-500/aduana/2025-10-20/174429.html)
20. [Guía de impuestos aduaneros y aduana en Chile](https://2eboxcasilla.com/aduana-impuestos-aduaneros-chile)
21. [Californian accused of shipping \$300M worth of Nvidia chips to China without Uncle Sam’s approval](https://www.theregister.com/security/2026/10/02/californian-accused-of-shipping-300m-worth-of-nvidia-chips-to-china-without-uncle-sams-approval/5300856)
22. [Greg Lui arrested for smuggling Nvidia AI chips to China](https://www.yahoo.com/news/us/articles/greg-lui-arrested-smuggling-nvidia-130550365.html)
23. [US Charges Earthmade Owner With \$300M Nvidia Chip Smuggling to China](https://aiweekly.co/alerts/us-charges-earthmade-owner-with-300m-nvidia-chip-smuggling-to-china)
24. [Man charged by US with illegally shipping Nvidia chips to China - Yahoo News Singapore](https://sg.news.yahoo.com/man-charged-by-us-with-illegally-shipping-nvidia-chips-to-china-054847726.html)
25. [Linux Hardware Reviews & Performance Benchmarks, Open-Source News - Phoronix](https://www.phoronix.com/)
26. [Ubuntu 26.10 Switches To The Linux 7.3 Kernel - Phoronix](https://www.phoronix.com/news/Ubuntu-26.10-With-Linux-7.3)
27. [Linux 7.3-rc5 Released: "Another Week, Another Large RC" - Phoronix](https://www.phoronix.com/news/Linux-7.3-rc5-Released)
28. [Ubuntu 26.10 will now ship with Linux kernel 7.3](https://www.omgubuntu.co.uk/2026/09/ubuntu-2610-kernel-version)
29. [ANCI 2026: qué es, qué exige y cómo prepararte (Ley 21.663)](https://preyproject.com/es/blog/la-anci-y-su-rol-con-la-ley-21-663)
30. [ANCI inaugura el Mes de la Ciberseguridad con tres anuncios: portal ciudadano, consulta pública y CTF Nacional](https://www.trendtic.cl/2026/10/anci-inaugura-el-mes-de-la-ciberseguridad-con-tres-anuncios-portal-ciudadano-consulta-publica-y-ctf-nacional/)
31. [Seminario Ciberseguridad](https://www.pdichile.cl/seminariociberseguridad)
32. [Chile y la Unión Europea abordan los desafíos de ciberseguridad en el Summit País Digital 2026](https://www.df.cl/chile-y-la-union-europea-abordan-los-desafios-de-ciberseguridad-en-el)
33. [Datacenters en auge: Se instalarán 34 nuevos centros en Chile - Construnoticias](https://construnoticias.com/2026/09/30/datacenters-en-auge-se-instalaran-34-nuevos-centros-en-chile/)
34. [Chile Existing & Upcoming Data Center Market Portfolio Analysis, 2026-2031](https://www.globenewswire.com/news-release/2026/09/29/3370484/28124/en/chile-existing-upcoming-data-center-market-portfolio-analysis-2026-2031-santiago-s-250-mw-pipeline-signals-colocation-and-hyperscale-investment-opportunities.html)
35. [USM impulsa investigación transdisciplinaria para el desarrollo de tecnología WAAM en Chile - Portal Innova](https://portalinnova.cl/usm-impulsa-investigacion-transdisciplinaria-para-el-desarrollo-de-tecnologia-waam-en-chile)

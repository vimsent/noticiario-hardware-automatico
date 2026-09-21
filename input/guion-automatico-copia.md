[INTRO]
Hola a todos, bienvenidos al primer episodio de este noticiario semanal de hardware.

Esta semana cubrimos del 8 al 14 de septiembre de 2026, y como es el primer capítulo, también nos vamos a hacer cargo de un par de cosas que pasaron los días justo antes y que no podíamos dejar afuera.

Y vale la pena, porque NVIDIA se compró el lugar donde vive prácticamente todo el open source de inteligencia artificial, AMD sacó procesadores nuevos para una plataforma de hace diez años, y Valve le puso precio a su casco de realidad virtual, con la crisis de la memoria incluida en la boleta.

Vamos al tiro con lo grande.

[NOTICIA 1: NVIDIA se compró Hugging Face y el open source tiembla]
Esto pasó el 3 de septiembre, cinco días antes de nuestra ventana, pero como es el primer episodio y es la noticia más grande del mes, no había forma de saltársela.

NVIDIA anunció que compra Hugging Face por 12.930 millones de dólares. Al dólar de hoy, que está a 940 pesos con 91, son más o menos 12 billones de pesos chilenos, billones de los nuestros, millones de millones. Según la documentación que NVIDIA presentó ante el regulador bursátil de Estados Unidos, el acuerdo se firmó el 2 de septiembre y se estructura como unos 11.900 millones en efectivo más hasta 1.000 millones en acciones para retener a la gente de Hugging Face. Todo esto está confirmado por la propia empresa.

Para el que no cache qué es Hugging Face: piensen en GitHub, pero para modelos de inteligencia artificial. Es el sitio donde se publican los pesos de los modelos abiertos, los datasets para entrenarlos y las demos para probarlos. Cuando Meta, Alibaba, Mistral o DeepSeek liberan un modelo, el archivo que ustedes descargan vive ahí. Y la librería transformers, que es la que usa medio mundo para cargar esos modelos en Python, también es de ellos.

O sea, NVIDIA no compró una empresa que compite con alguien. Compró el punto de distribución.

Y acá va la parte técnica que importa. Un modelo abierto es, al final, un archivo gigante de números. Ese archivo no sabe nada de hardware. Lo que decide en qué chip corre es el software que hay abajo: CUDA si es NVIDIA, ROCm si es AMD, Metal si es un Mac, o backends como llama.cpp que corren en lo que sea. Hasta ahora, Hugging Face era neutral en esa pelea: te mostraba el modelo y tú veías dónde lo corrías. Ahora el dueño del mostrador es el dueño de una de las opciones.

NVIDIA lo sabe, y por eso el anuncio viene con promesas explícitas: que no va a ser obligatorio usar cómputo de NVIDIA para publicar o desplegar desde Hugging Face, que van a seguir alojando modelos abiertos de todos los laboratorios, y que se mantiene el soporte multinube y multiacelerador. Eso es lo que dice la empresa, textual en espíritu.

A mí me parece que hay que leer eso como lo que es: una promesa del comprador el día de la compra. Y la analogía que se me ocurre es esta. Es como si Copec se comprara la aplicación que te dice dónde cargar bencina. Te van a seguir mostrando todas las bencineras, seguro. Pero adivinen cuál va a salir primero, cuál va a tener el botón bonito de "cargar aquí", y cuál va a tener la integración que funciona sin configurar nada.

Un detalle que me gustó del reporteo de CNBC: fue el propio CEO de Hugging Face, Clément Delangue, el que se acercó a Jensen Huang durante el verano del norte, porque según él el open source estaba en un punto de inflexión y necesitaba más recursos y más escala. O sea, no fue NVIDIA cazando, fue Hugging Face pidiendo refugio. Y TechCrunch ya había reporteado el 26 de agosto que la negociación estaba avanzada, así que tampoco fue sorpresa para los que siguen esto de cerca.

La reacción en Hacker News, donde el hilo pasó los 300 puntos, se dividió en dos. Un grupo dice que 13 mil millones es una locura por una empresa que básicamente aloja archivos gratis; hubo quien la comparó con comprar Docker Hub. Los ingresos que comentan por ahí son estimaciones de usuarios, así que no las tomen como dato. El otro grupo se preocupa por el conflicto de interés: NVIDIA financia a OpenAI y Anthropic, los laboratorios cerrados, y ahora además es dueña de la casa de los abiertos. The Register publicó una columna diciendo que Hugging Face es demasiado importante para caer en manos de NVIDIA, y en los comentarios ya hay gente hablando de espejos y de archivar modelos "mientras se pueda".

Georgi Gerganov, el creador de llama.cpp, salió a calmar las aguas: dijo que NVIDIA lleva más de un año apoyando el proyecto con ingenieros y hardware, y que todos los backends, incluidos los de AMD, Apple y demás, se van a seguir desarrollando como siempre, guiados por la comunidad. Yo le creo a Gerganov. El problema no es él, es que las estructuras de incentivo cambian y la gente se va.

Y para cerrar con algo liviano: alguien en Hacker News se dio cuenta de que el emoji de la carita abrazando, que es el logo de Hugging Face, tiene el código Unicode 1F917, que en decimal es 129.303. Y el precio fue 12.930 millones. Yo no digo que sea a propósito. Pero si fuera a propósito, sería lo más NVIDIA que he visto.

¿Qué pasa en uno o dos años? Esto es especulación mía. Creo que el hub va a seguir gratis y abierto, porque cerrarlo sería un suicidio de imagen. Pero creo que vamos a ver el stack de inferencia de NVIDIA metido por defecto en cada página de modelo, y que la neutralidad se va a erosionar de a poco, no de golpe. Y creo que esto le da un empujón enorme a los espejos alternativos, en China y en Europa, que hasta ahora eran de nicho.

Mi consejo no pedido para NVIDIA: pongan la gobernanza del hub en una fundación independiente, con AMD e Intel sentados en la mesa, y publiquen el protocolo de descarga como estándar abierto. Si de verdad quieren ser neutrales, cuesta poco demostrarlo. Si no lo hacen, ya sabemos por qué.

[NOTICIA 2: NVIDIA recicla la RTX 5090 con 84 GB para IA]
Y hablando de NVIDIA, el lunes 14 sacaron sin mucho ruido una tarjeta que dice mucho sobre a quién le están vendiendo hoy.

Se llama RTX PRO 5500 Blackwell, y en el fondo es una RTX 5090 con el triple de memoria. Mismo chip GB202, mismos 21.760 núcleos CUDA que la tarjeta gamer, pero con 84 GB de GDDR7 en vez de 32. Esto está confirmado por la hoja de especificaciones que publicó PNY, que es el socio de NVIDIA para las tarjetas profesionales.

¿Cómo meten 84 GB? Con 28 chips de 3 GB montados en clamshell: 14 por delante y 14 por detrás de la placa, compartiendo canales de memoria. Es la forma de duplicar capacidad sin ensanchar el bus, y por eso el ancho de banda no sube: queda en unos 1.398 GB por segundo, que según Tom's Hardware es un 22 por ciento menos que la RTX 5090 y la RTX PRO 6000, porque los chips corren más lento que lo que soportan.

Ojo con un detalle: TechPowerUp dice que el bus es de 416 bits y Tom's Hardware dice 448 bits. No coinciden, y yo no tengo forma de verificarlo hasta que NVIDIA publique su propia página. Lo dejo así, en contradicción.

La tarjeta consume 600 watts, viene con refrigeración por aire o líquida pensada para rack, y soporta partición MIG: una instancia de 84 GB o dos de 42. Queda entre la RTX PRO 5000 de 72 GB, que cuesta 9.209 dólares, unos 8 millones 660 mil pesos, y la RTX PRO 6000 de 96 GB, que cuesta 15.599 dólares, unos 14 millones 680 mil. El precio de esta no lo han dicho, pero apunta a ese rango.

Y acá va mi opinión: esto es la confirmación de dónde van los chips GB202 buenos. Cada die que califica para 84 GB y certificación profesional vale varias veces más que como RTX 5090. Tom's Hardware lo dice sin rodeos: a NVIDIA le rinde más poner ese silicio en una tarjeta PRO que en una GeForce. Así que si andan preguntando por qué la 5090 sigue cara y escasa, acá tienen media respuesta.

[NOTICIA 3: AMD saca dos Ryzen baratos por la crisis de RAM]
Pasemos a AMD, que el 10 de septiembre lanzó dos procesadores sin anuncio, sin evento, sin nada, y dos días después confirmó los precios.

El primero es el Ryzen 5 7500. Es el 7500F de siempre, seis núcleos Zen 4, 3,7 GHz base, 5 GHz turbo, 65 watts, pero con la gráfica integrada encendida: dos unidades de cómputo RDNA 2 a 2,2 GHz. Precio oficial: 189 dólares, unos 178 mil pesos.

Y acá me da risa, porque TechPowerUp reporta que el 7500F, que es el mismo chip sin la gráfica, se encuentra entre 130 y 140 dólares en retail. O sea, están cobrando 50 dólares extra por una integrada de dos unidades que sirve para instalar Windows y ver el BIOS, no para jugar. Yo esperaría a que baje, y TechPowerUp piensa lo mismo.

El segundo es el interesante: el Ryzen 5 5500F, para AM4, la plataforma de 2016. Seis núcleos Zen 3, 3 GHz base, 4,4 turbo, 65 watts, 99 dólares, unos 93 mil pesos.

Y ahora la parte técnica, porque el nombre engaña. El Ryzen 5 5500 normal usa el die Cezanne, que es el chip de las APU: monolítico, con gráfica Vega adentro, 16 MB de caché L3 y PCIe 3.0. El 5500F usa Vermeer, que es el diseño de chiplets de los Ryzen 5000 de escritorio de verdad: un chiplet de cómputo más un die de entrada y salida, con PCIe 4.0 y 200 MHz más de turbo. AMD le dejó la mitad de la caché, 16 MB en vez de 32, pero igual es otro animal.

Un youtuber, RandomGaminginHD, ya lo probó contra el 5500 normal con una RX 9060 XT a 1080p, y le sacó hasta 16 por ciento en Battlefield 6, 11 en Cyberpunk y 8 en Counter-Strike 2. Es un solo sistema y un solo reviewer, y el mismo TechPowerUp dice que hay que esperar pruebas serias, así que tómenlo como indicio, no como dato.

Por qué importa esto acá: la memoria está por las nubes, y de eso vamos a hablar en un rato. Si ustedes ya tienen una placa AM4 y DDR4, un procesador de 93 mil pesos les extiende la vida del computador sin comprar RAM nueva, que es justo lo que más subió. En Chile, súmenle IVA, margen de la tienda y espera; intenté verificar precios locales y todavía no aparece listado en las tiendas grandes.

Y una nota al pasar: según la encuesta de hardware de Steam, la RX 9070 XT ya es la tarjeta Radeon más usada de la plataforma, por sobre todas las RDNA 2 y RDNA 3. Eso lo reportaron TweakTown, OC3D y TechPowerUp. AMD tiene un buen año en escritorio, aunque nadie hable de eso.

[NOTICIA 4: La crisis de memoria ya te cobra el Steam Frame]
Y ya que estamos con precios, Valve por fin le puso número al Steam Frame, su casco de realidad virtual, y el número duele.

1.059 dólares la versión de 256 GB, 1.299 la de 1 TB. Al cambio, 996 mil pesos y un millón 222 mil. Y la fuente de poder de 29 dólares, unos 27 mil pesos, no viene incluida. Se vende por reserva con sorteo, como hicieron con la Steam Machine: las inscripciones cierran el 17 de septiembre y las primeras invitaciones salen el 18.

El aparato en sí es bacán. Pesa 440 gramos contra 809 del Index, corre un Snapdragon 8 Gen 3 con 16 GB de LPDDR5X, tiene seguimiento de ojos, y puede funcionar solo o hacer streaming desde tu PC con un dongle Wi-Fi dedicado. Corre SteamOS en ARM, y para los juegos de Windows usa FEX y Proton, que traducen el código x86 en tiempo real. Tom's Hardware lo probó y le gustó: le pone como contras el precio y una pérdida leve de rendimiento en modo autónomo.

Pero lo que a mí me interesa es por qué cuesta lo que cuesta. TechPowerUp recuerda que la Steam Machine salió en junio a 1.049 dólares, mucho más caro de lo esperado, y Valve culpó a la escasez de DRAM y almacenamiento. Y reportes de la industria dicen que la meta original del Frame era quedar bajo los 999 del Index. No se pudo.

Y esto es toda la industria, no Valve. Omdia publicó esta semana que la venta mundial de semiconductores llegó a 425 mil millones de dólares en el segundo trimestre, 31 por ciento más que el trimestre anterior, un récord. Y el dato que hay que mirar: los chips de memoria por sí solos fueron más de la mitad de todo ese ingreso.

Piénsenlo así: cada consola, cada casco, cada notebook, lleva la misma memoria que quieren los datacenters de inteligencia artificial, y los fabricantes venden al que paga más. Ustedes no son ese cliente.

El otro lado de la misma moneda está en Taiwán. Micron, que en su último trimestre ganó 28 mil millones de dólares netos, ofreció a sus empleados taiwaneses un bono de un millón de dólares taiwaneses, unos 31.650 dólares, casi 30 millones de pesos por cabeza, y los sindicatos lo rechazaron: quieren un 15 por ciento de la utilidad operacional repartido cada trimestre, como sistema permanente. La primera mediación falló el 4 de septiembre, la segunda es el 21, y si falla, votan huelga. Yo creo que tienen toda la razón, y creo también que si paran las plantas de Micron, la memoria va a subir todavía más.

[NOTICIA 5: Apple ya tiene CEO ingeniero y se nos pasó]
Cambio de tema y cambio de jefe. Esto es de los días previos a la ventana y lo pescó nuestro barrido de seguridad, no las fuentes normales, así que lo cuento corto.

Desde el 1 de septiembre John Ternus es el CEO de Apple, y Tim Cook pasó a presidente ejecutivo del directorio. Lo anunciaron en abril, así que no es sorpresa, pero el traspaso se hizo efectivo ahora, después de 15 años de Cook al mando.

Por qué me importa a mí: Ternus venía de dirigir la ingeniería de hardware, o sea, iPhone, iPad, Mac, Watch y Vision Pro pasaban por su escritorio. Cook era el hombre de la cadena de suministro; Ternus es el hombre del silicio. Yo no sé si eso cambia algo en el corto plazo, y sería especulación decir que sí. Pero para un canal de hardware, que la empresa más grande del mundo la dirija un ingeniero de hardware es, por lo menos, buena señal.

[NOTICIA 6: Linux perdía tus datos en silencio desde 2023]
Y para los que programan, la que me parece más importante de la semana en software de bajo nivel, aunque la haya cubierto un solo medio.

Phoronix reporta que el kernel de Linux acaba de recibir un parche de una línea para un bug que existía desde julio de 2023, presente en todos los kernels desde el 6.6. La combinación era esta: transparent hugepages activadas, un límite de memoria por cgroup, y un programa que usa MADV_FREE.

Explico. MADV_FREE es una llamada con la que un proceso le dice al kernel: estas páginas ya no las necesito, recupéralas cuando quieras. La gracia es que si el proceso vuelve a escribir en esas páginas antes de que el kernel las recupere, esa escritura debería cancelar la liberación. Bueno, bajo presión de memoria y con hugepages, el kernel botaba la página igual, con la escritura nueva adentro. Sin error, sin log, sin nada. Datos perdidos en silencio.

Y no era teórico: usuarios de Polars, la librería de análisis de datos, encontraron pérdida de datos en producción por esto. Lo reportaron a principios de mes con un programa en C que lo reproduce, y el parche ya entró y está marcado para todas las versiones estables. Si corren cargas de datos en Linux con cgroups, que es básicamente cualquier contenedor, actualicen el kernel apenas les llegue.

Dos cosas más al pasar, también de Phoronix. Arnd Bergmann tiene una rama que borra unas 247 mil líneas de drivers para plataformas ARM de 32 bits obsoletas, apuntando a Linux 7.4 o 7.5; el kernel completo anda por las 41 millones de líneas, así que es una limpieza chica pero simbólica. Y Rustls, la librería TLS en Rust, sacó la versión 0.23.45 para corregir un problema que llevaba dos años: aceptaba mensajes del handshake de TLS 1.3 en el nivel de cifrado equivocado. No permitía alterar la conexión, pero estaba fuera de la especificación. Actualicen eso también.

[CHILE: Semana seca en Chile, y lo decimos sin vergüenza]
Y llegamos al bloque de Chile, que esta semana va a ser cortito, porque prefiero decirles la verdad a rellenar.

Nuestro sistema revisa medios chilenos, Subtel, ANID, la USM y consultas específicas sobre datacenters, la ley de datos personales y la agencia de ciberseguridad. Para la semana del 8 al 14 de septiembre no encontró ninguna novedad fechada que valga la pena contar. Ninguna ley que se haya movido, ningún concurso nuevo que cierre pronto, ningún datacenter nuevo con permiso o polémica en la ventana.

Y ojo: eso puede ser porque no pasó nada, o porque nuestras fuentes chilenas todavía son pocas. Es el primer episodio y lo vamos a ir mejorando. Si ustedes saben de algo que se nos pasó, un evento, una convocatoria, algo de la universidad, déjenlo en los comentarios y lo revisamos para el próximo.

Lo que sí les puedo decir es lo que ya dijimos arriba: si están pensando en armar o actualizar computador, la memoria va a seguir cara mientras los datacenters se lleven la producción, y el Ryzen de 93 mil pesos para AM4 es de las pocas cosas que van en la dirección correcta. Cuando aparezca en tiendas chilenas, les avisamos.

[CIERRE]
Y eso fue la semana. Si les sirvió, suscríbanse y activen la campanita, porque esto sale todas las semanas y el algoritmo no ayuda.

Nos vemos en el próximo episodio. Chao.

---

FUENTES
- NVIDIA compra Hugging Face por 12.930 millones y entra en una pieza de la IA que no controlaba — Xataka, 2026-09-03 — https://news.google.com/rss/articles/CBMizgFBVV95cUxOSW13OFMzVm85SjZDUzdoYXBsRVVjaDdYYjJEZUU4bXFfZF9RNjRpQlVRTlFfeGpTZXpJX3JHazNUZnR3V0dZblZTZG9rMGx3TXhtcXo5Z1RjX2xYZmVST01qaHJGcVZUODBYbV9qYVJ1NTRzdzQzdm5Eb2RvcEhDZ2Y5eF9INFJPU3hxRlMxcmFqUGFrOW1CM2JGMk9jZ1RoMnc1UjVoSTFYOEdoN0pNSmduRll4aTAzbF9mX2FpMmdUWjVlejhCc2VRc0dtd9IB0wFBVV95cUxNbTZrdWIzZE93VXdUQ0RXUWdHQ0NOUm9BbzRfSkdGM3VJemg2eHFTSjNaVDIwclEzSV9FbVBrVmFud1RBak8zdGsyelpXaWE1bVJlQlA1TEY5R1R5VVVyaTEwTmx3dlpQMTd1bUJHSmxkVkx6Qk9VN2hBY1RFdVVzODYzY282bE5DeWNhdmMwZzA5ZUh2Rmt1UF9VN1dTXzJEVENtd01QelYwZjZESFFzLWJQcmpNQUpaWW5ib0RmOGQ4UXl1QkVyYldfODMyN3dFUGM4?oc=5
- Nvidia compra Hugging Face por 13.000 millones de dólares — Expansión, 2026-09-03 — https://news.google.com/rss/articles/CBMikAFBVV95cUxNN0kwZXY1Xy0zVkoyeHVOanpBbER1X0EyOUN6U3RnalBPMTFHZGtvVnBFcnRMVDNuaTJ2Zzc2TDN6czJpUVZaQzdFTldDT0pTSWpRMkE5RmNrQUNfcFdlN2NCaVA1UXZjeV80U0x6RWpHVk9OUExlRWJiQmg0RlVnU2xJZmM1UkpIam90cERoTlbSAZABQVVfeXFMTUthSU5PV1hLMG5BRGFPM0Fwd2ZhallhbVkyaXlMSlNidnp3QmRHMHVSNlhPdml0enZraDJ1MUVReUJRdmlNdk12UHJUN2RBUFdqdlNvYjU2N1JzWFV5d1VweFhQWGdpLS1yRHdBTXQxQkZianlpemV4Q1pQd0Y5bFNJZVQwd0JMMEo4dmxyWDRx?oc=5
- Hilo de Hacker News sobre la compra de Hugging Face por NVIDIA, con enlace a la nota de CNBC — Hacker News, 2026-09-03 — https://news.ycombinator.com/item?id=49548952
- Columna de The Register: Hugging Face es demasiado importante para quedar en manos de NVIDIA, discutida en Hacker News — Hacker News, 2026-09-03 — https://news.ycombinator.com/item?id=49558584
- Georgi Gerganov sobre el futuro de llama.cpp y ggml tras la compra de Hugging Face — Hacker News, 2026-09-04 — https://news.ycombinator.com/item?id=49567357
- El chiste del precio de Hugging Face y el código Unicode del emoji — Hacker News, 2026-09-03 — https://news.ycombinator.com/item?id=49557813
- NVIDIA presenta la RTX PRO 5500 Blackwell con 84 GB de GDDR7 — TechPowerUp, 2026-09-14 — https://www.techpowerup.com/352678/nvidia-unveils-rtx-pro-5500-blackwell-workstation-gpu-with-84-gb-gddr7-memory
- NVIDIA reconvierte la RTX 5090 para márgenes de IA: la RTX PRO 5500 trae 2,6 veces la VRAM con las mismas specs — Tom's Hardware, 2026-09-14 — https://www.tomshardware.com/pc-components/gpus/gaming-takes-a-backseat-as-nvidia-overhauls-the-rtx-5090-for-maximum-ai-margins-rtx-pro-5500-delivers-2-6x-vram-at-matching-specs
- AMD lanza sin anuncio los Ryzen 5 7500 y Ryzen 5 5500F — TechPowerUp, 2026-09-10 — https://www.techpowerup.com/352568/amd-quietly-launches-ryzen-5-7500-and-ryzen-5-5500f
- AMD confirma precios: Ryzen 5 7500 a 189 dólares y Ryzen 5 5500F a 99 — TechPowerUp, 2026-09-12 — https://www.techpowerup.com/352624/amd-confirms-ryzen-5-7500-at-usd-189-ryzen-5-5500f-at-usd-99
- El Ryzen 5 5500F le saca hasta 16 por ciento al 5500 en primeras pruebas de juegos — TechPowerUp, 2026-09-14 — https://www.techpowerup.com/352706/amd-ryzen-5-5500f-beats-ryzen-5-5500-by-up-to-16-in-early-gaming-benchmarks
- La RX 9070 XT ya es la Radeon más popular en la encuesta de Steam — TechPowerUp, 2026-09-09 — https://news.google.com/rss/articles/CBMiqgFBVV95cUxPOGxSd3Z4Ym9PMm1kWHZBalBMbUk1VFZjeUlZNVJUdUxVRlJCbm9xelYwN1d3S1ZuS3JaNll0Y1ZuTHBmTnlDSHR6QlFJd2FxTUpOd3owSVgwWUFMU1h3OEpsWlFTRlZwY0lRTXlham93OTdtQjFUYTFkNGNueFFlMUpLY05OOXdDVU9LYmZWeHNqam92UVdkUURTaE1icncwZEJ6bzd0Nzc1QdIBrwFBVV95cUxPTkM4OGpISW9nbUZrLWFjdlQxQmZ5UWZLaGp6WnU4cjZLaWRSUjNEZHhQTEQzeHN6OUdwWHNxMVZlSXpZX2w3MkpMcUhZQ2UwMmRKWEYwVk5yTVc1d2hoS2tXeENxR2pyRC1XRGVSUS00VjM1NHdhbTk5NHpKMzJhanRVajBmcEtGdjNvQXJRTkxlZ3Z4aGN2SWo0bmZCaWpyRzV2NVRBUW1ORmtjbk5n?oc=5
- El Steam Frame de Valve parte en 1.059 dólares y abre reservas — TechPowerUp, 2026-09-14 — https://www.techpowerup.com/352695/valves-steam-frame-starts-at-usd-1-059-pre-orders-now-open
- Steam Frame disponible desde 1.059 dólares, precios por región — Phoronix, 2026-09-14 — https://www.phoronix.com/news/Valve-Steam-Frame-1059
- Reseña del Steam Frame: competente como VR autónomo, el streaming sigue siendo el foco — Tom's Hardware, 2026-09-14 — https://www.tomshardware.com/virtual-reality/valve-steam-frame-review
- Ingenieros de Valve explican la dualidad del Steam Frame y su precio; SteamOS pasa a ARM — Tom's Hardware, 2026-09-14 — https://www.tomshardware.com/virtual-reality/valve-engineers-discuss-the-duality-of-the-steam-frame-and-pricing-valves-newest-vr-headset-pivots-steamos-to-arm
- Omdia: la venta mundial de semiconductores sube 31 por ciento a un récord de 425 mil millones en el segundo trimestre — TechPowerUp, 2026-09-14 — https://www.techpowerup.com/352683/global-semiconductor-revenue-surges-31-to-record-usd-425bn-in-2q26
- Micron ofrece bono de 31.650 dólares a empleados en Taiwán y los sindicatos lo rechazan bajo amenaza de huelga — Tom's Hardware, 2026-09-14 — https://www.tomshardware.com/tech-industry/semiconductors/micron-offers-taiwan-employees-usd31-650-cash-bonus-as-unions-threaten-strike-over-ai-windfall-workers-reject-record-payout-package-demand-15-percent-profit-sharing-plan
- Tim Cook pasa a presidente ejecutivo y John Ternus asume como CEO de Apple — Apple Newsroom, 2026-04-20 — https://www.apple.com/newsroom/2026/04/tim-cook-to-become-apple-executive-chairman-john-ternus-to-become-apple-ceo/
- John Ternus sucede a Tim Cook como CEO de Apple tras 15 años — Al Jazeera, 2026-09-01 — https://www.aljazeera.com/economy/2026/9/1/john-ternus-succeeds-tim-cook-as-apple-ceo-after-15-years
- Linux corrige un bug de pérdida silenciosa de datos en espacio de usuario que existía desde 2023 — Phoronix, 2026-09-14 — https://www.phoronix.com/news/Linux-7.3-Fix-Silent-Data-Loss
- Borrar drivers de plataformas ARM obsoletas aliviana el kernel en unas 247 mil líneas — Phoronix, 2026-09-14 — https://www.phoronix.com/news/Branch-Remove-Old-ARM-Drivers
- Rustls 0.23.45 corrige un problema de seguridad de dos años — Phoronix, 2026-09-14 — https://www.phoronix.com/news/Rustls-0.23.45-Released

[INTRO]
Hola, hola, ¿cómo están? Bienvenidos a un nuevo noticiario de hardware. Hoy repasamos la semana del 11 al 17 de octubre de 2026.

Y esta semana vale la pena por algo bien concreto: la noticia más importante no es un chip, es la máquina con la que se fabrican todos los chips avanzados. Y la empresa que la hace acaba de avisar que no le va a alcanzar.

Además, Qualcomm le ganó un juicio a Arm por dos dólares, China mostró cartas en memoria y en litografía, y los trabajadores de Micron en Taiwán ya tienen la huelga autorizada.

Vamos al tiro.

[NOTICIA 1: ASML no da abasto y eso nos va a doler]
Partamos por lo confirmado, que viene de los resultados de la propia empresa.

El 14 de octubre, ASML, la empresa holandesa que fabrica las máquinas de litografía, publicó su tercer trimestre de 2026. Vendió unos 11.700 millones de euros, ganó unos 5.000 millones de utilidad neta y el margen bruto llegó a 57,5%. Despachó 121 sistemas de litografía, contra 91 del trimestre anterior. Y para el cuarto trimestre espera vender entre 14.200 y 15.200 millones de euros.

Pero el dato que a mí me importa es otro.

ASML dijo, con todas sus letras, que la oferta que tiene planificada para 2027 y 2028 podría no alcanzar para lo que le piden sus clientes.

O sea, el proveedor del que depende toda la industria avisó que viene corto.

Para entender por qué esto es grave, hay que entender qué hace una máquina EUV.

Un chip se fabrica, a grandes rasgos, como una foto. Se proyecta un patrón con luz sobre una oblea cubierta de un material sensible, y donde pega la luz, después se graba. Mientras más corta la longitud de onda de esa luz, más finos se pueden dibujar los transistores.

La EUV usa luz ultravioleta extrema, con una longitud de onda muchísimo más corta que la de la litografía anterior. El problema es que esa luz no se consigue con una ampolleta. Se genera disparándole un láser a gotitas de estaño fundido, que se convierten en un plasma que la emite. Y como esa luz la absorbe casi todo, hasta el aire y el vidrio, la máquina trabaja al vacío y con puros espejos.

Es una máquina del porte de una micro, y en la práctica la vende una sola empresa en el mundo. Esa es ASML.

Entonces, cuando ASML dice que no le alcanza, lo que dice es que las fábricas de chips no van a poder crecer todo lo que quieren. Y eso incluye a las de memoria, que también usan EUV en sus nodos nuevos, como les contamos con Micron hace dos episodios.

Ahora, ojo con cómo se contó esto, porque los medios no dicen lo mismo.

36Kr cita a un ejecutivo de ASML diciendo que los pedidos ya están reservados hasta 2030. GIGAZINE, en cambio, dice que los equipos están casi agotados hasta 2028 y que algunos clientes están considerando pedir para 2030. Considerar pedir no es lo mismo que tener todo reservado. La versión oficial es la de 2027 y 2028. Lo de 2030 yo lo tomaría con pinzas.

Y lo curioso: la acción igual cayó. Zacks tituló que ASML superó lo esperado en utilidades pero quedó bajo en ingresos. Vendiste récord y el mercado igual te castiga. Así de penca es Wall Street.

Pasemos al principal cliente de ASML. El 15 de octubre, TSMC reportó su sexto trimestre seguido de utilidad récord, sobre lo estimado según CNBC. Reuters la describió como prudente de cara a 2027. Y su CEO, C.C. Wei, contó que mandó equipos a evaluar una expansión en Texas, pero que en cualquier fábrica con socios quiere mantener el control de la operación.

Y lo más interesante para este canal: según Digitimes, TSMC planea adoptar High-NA EUV recién en 2030.

¿Qué es High-NA? NA es apertura numérica, que es, más o menos, qué tan abierto es el cono de luz que capta la óptica. Más apertura significa dibujar detalles más finos de una sola pasada.

Con la EUV normal, las capas más finas a veces hay que exponerlas más de una vez, como cuando pintan una pared en dos manos porque la brocha es muy gruesa. Cada mano extra es más tiempo de máquina, más costo y más chances de error. High-NA promete hacerlo en una sola mano.

Que TSMC espere hasta 2030 me dice que, para ellos, todavía sale más barato pintar en dos manos con las máquinas que ya tienen, que comprar las nuevas. Especulación mía, pero calza. Y como contexto, el 8 de octubre Reuters contó que ASML y Zeiss ya piensan en la generación siguiente, Hyper-NA, para dentro de unos diez años.

Ahora, dos cosas que muestran lo frágil que es todo esto.

Primero, el 14 de octubre Bloomberg reportó que la Unión Europea levantaría una sanción a una empresa china para salvar a un proveedor de ASML. Según Tom's Hardware, es una empresa alemana de recubrimientos que podría cerrar sin tierras raras chinas. La máquina más avanzada de Occidente depende de un insumo chino. Para el que pensaba que esto se desacoplaba fácil.

Segundo, el 15 y 16 de octubre varios medios reportaron que una startup china mostró un prototipo de fuente de luz EUV con 15 watts y 90% de componentes nacionales. TrendForce dice que la producción en masa estaría a entre tres y cinco años, y Tom's Hardware la describe como todavía lejos de ser viable.

Separemos bien: es un prototipo de laboratorio, reportado por prensa, sin verificación independiente que yo haya podido revisar. Y es solo la fuente de luz. Faltan los espejos, el sistema que mueve la oblea, todo el resto. Además, cuando un anuncio viene con el porcentaje de localización en el titular, hay un componente de propaganda que no hay que ignorar.

¿Mi opinión? El verdadero cuello de botella de la industria no es TSMC ni NVIDIA. Es una empresa holandesa con capacidad limitada. Le conviene a ASML, que puede poner precio, y a TSMC, que ya tiene sus máquinas aseguradas. Les duele a los fabricantes más chicos, a los de memoria y, al final de la cadena, a nosotros.

Si estaban esperando que en 2027 los chips y la RAM bajaran, esto es mala señal. Yo no contaría con eso.

[NOTICIA 2: Qualcomm le ganó a Arm y cobró dos dólares]
Y hablando de empresas que dependen unas de otras, pasemos al juicio del año en el mundo Arm.

El 13 de octubre, un jurado de Delaware concluyó que Arm incumplió su acuerdo de licencia de arquitectura con Qualcomm. La indemnización: dos dólares. Uno por cada acusación que ganó Qualcomm. Unos 1.970 pesos. Ni para un completo.

Pero no se rían todavía, porque el chiste tiene letra chica.

Arm vende dos tipos de licencia. Con la de tecnología, compras núcleos ya diseñados por Arm. Con la de arquitectura, compras el derecho a diseñar tus propios núcleos que entienden el set de instrucciones de Arm. Es la diferencia entre comprar la torta hecha y comprar el derecho a usar la receta. Qualcomm usa la segunda para sus núcleos Oryon.

Según Reuters, citado por TechPowerUp, el jurado encontró que Arm retuvo parches de software y herramientas de verificación que Qualcomm necesitaba para validar esos núcleos, y que interfirió a propósito en su negocio con Meta. Eso se conecta con octubre de 2024, cuando el aviso de Arm para cancelar la licencia terminó en Bloomberg, una filtración que Qualcomm le atribuye a Arm.

Arm ganó el resto de las acusaciones, casi todas sobre precios de la otra licencia. Y obvio, los dos dicen que ganaron.

Lo que de verdad importa lo decide ahora la jueza Maryellen Noreika: si ese incumplimiento permite que Qualcomm deje de pagar las regalías de esa licencia por cinco años. Según algunas estimaciones, eso vale miles de millones de dólares. Arm argumenta que esa cláusula es una penalidad que no se puede hacer cumplir.

Para dimensionar: según un resumen de TradingView, Qualcomm representa cerca del 9% de los ingresos de Arm.

Para mí, Arm se metió sola en esto. Cuando tu negocio es que todos confíen en ti para construir encima de tu arquitectura, pelear a muerte con uno de tus clientes más grandes es pésima publicidad. Consejo no pedido para Arm: si pierde lo de las regalías, que negocie en vez de apelar por orgullo. Cada mes de juicio es un argumento más para que alguien mire RISC-V.

[NOTICIA 3: Micron gana como nunca y sus trabajadores autorizan huelga]
Y ya que estamos con empresas a las que les va demasiado bien, volvamos a un hilo que seguimos desde el primer episodio: la crisis de la memoria.

Dónde quedamos: Micron reportó a fines de septiembre resultados récord y dijo que la oferta va a estar muy apretada en 2027 y 2028. Y su sindicato de Taoyuan, en Taiwán, venía de una mediación fallida.

Bueno, se votó. El 7 de octubre, según 24/7 Wall St., ese sindicato autorizó una huelga por 1.994 votos contra 14. Ojo: autorizar no es parar. Todavía no hay fecha.

Piden el 15% de la utilidad operacional, repartido con un sistema transparente. Micron dice que se toma en serio las preocupaciones, y que en septiembre pagó un bono en efectivo de unos 31.600 dólares más acciones. Eso son unos 31 millones de pesos.

El 15 de octubre, según Reuters, el presidente de Taiwán, Lai Ching-te, inauguró una planta nueva de ensamblaje y pruebas de Micron en Taichung y pidió a las dos partes negociar con sinceridad. Ahí mismo, el COO de Micron, Manish Bhatia, dijo que toda la capacidad de esa planta para 2027 ya está vendida.

Y acá hay una contradicción. 24/7 Wall St. dice que el sindicato de Taichung, el grande, con unas 11.000 personas, no había votado y vuelve a mediación el 22 de octubre. Reuters, una semana después, dice que ese sindicato informó que sus miembros sí autorizaron una huelga. No pude resolver cuál está al día.

¿Por qué importa una planta de ensamblaje y pruebas? Porque ahí se apilan y se prueban los chips, incluida la HBM. Si eso se detiene, las obleas quedan esperando. Es tener la cocina funcionando y a los garzones en paro.

Y para dimensionar la plata: el 8 de octubre Samsung publicó su guía del tercer trimestre, con ventas de unos 195 billones de wones y utilidad operacional de unos 107,4 billones. Más de la mitad de lo que vende es utilidad operacional.

Hasta Elon Musk dijo esta semana que Micron cobra razonable y los demás son extorsivos. Tom's Hardware le contestó en su titular que Micron saca márgenes de 90% en RAM de consumo.

Con márgenes así, que los trabajadores pidan una parte es lo más lógico del mundo. Consejo para Micron: presente su plan de bonos de una vez, porque una huelga en el empaquetado de HBM sería echarle bencina a un incendio que ya nos tiene pagando la RAM carísima.

[NOTICIA 4: China dice que hizo DRAM más densa, sin mostrar nada]
Y siguiendo con memoria, vamos a China, porque esta semana movió las acciones de toda la industria.

El 11 y 12 de octubre, el South China Morning Post informó que CXMT, el mayor fabricante chino de DRAM, avanzó en un diseño que también persiguen Samsung y SK hynix: la DRAM 4F². Y las acciones de Micron, SK hynix y Samsung cayeron.

¿Qué es 4F²? Una celda de DRAM es un transistor y un condensador, y guarda un bit. La F es el tamaño mínimo que puede dibujar la fábrica. Las celdas comerciales de hoy usan, en general, seis F cuadrados. Una 4F² usa cuatro: dos tercios del espacio. Para lograrlo, el transistor se para: el canal queda vertical, con el condensador encima.

Y aquí se conecta con ASML. China no puede comprar máquinas EUV por los controles de exportación, y sin EUV achicar la F cuesta muchísimo. Si no puedes dibujar más fino, reorganizas la celda para que ocupe menos. El medio coreano economy.ac lo tituló justo así: CXMT cambió la estructura de la celda por los límites de la EUV.

Pero el estatus es lo que importa. Es un anuncio de la propia empresa. El Seoul Economic Daily tituló que CXMT promociona su DRAM sin especificaciones ni fecha de lanzamiento. Y Chosunbiz reportó que Wall Street duda de la ventaja de CXMT, y que Corea mantiene la delantera en densidad y rendimiento.

No hay benchmark, no hay datasheet, no hay fecha. Hay un titular y una caída en bolsa.

Para mí, el mercado reaccionó al titular, no al producto. Especulando: la amenaza real de CXMT no es la HBM de punta, es la DDR4 y DDR5 de volumen. Si China se autoabastece de esa memoria, parte de la demanda que sostiene los precios se va. Pero eso es para dentro de años.

[NOTICIA 5: SK hynix pone condiciones para fabricar en Estados Unidos]
Y ya que estamos con Corea, China y controles de exportación, esto viene de un hilo del episodio 2, cuando les contamos que SK hynix negociaba fabricar memoria en Estados Unidos, posiblemente en la planta de Intel en Ohio.

El 14 de octubre, Reuters publicó una exclusiva con fuentes anónimas: SK hynix estaría pidiendo a Washington permiso para exportar equipos estadounidenses de fabricación a su planta de Dalian, en China, para producir más allá, como condición para construir una fábrica en Estados Unidos. Medios financieros lo ligan a una futura planta de NAND de Solidigm, su filial.

SK hynix respondió que la instalación de equipos en Dalian se hace en consulta con el gobierno de Estados Unidos y con su autorización, y que no busca ampliar la capacidad de esa planta. Una fuente dijo que todavía no tiene aprobación para los equipos adicionales de 2027.

El contexto: el año pasado, Comercio les quitó a SK hynix y a Samsung las autorizaciones que les permitían llevar equipos estadounidenses a sus plantas chinas sin licencias individuales.

Estatus: reporte de prensa con fuentes anónimas, más una respuesta parcial de la empresa que no lo desmiente.

¿Cómo se lee? Como un trueque: yo invierto en tu país si me dejas renovar la cocina de mi local en el país de tu rival. Yo creo que Washington va a terminar aceptando algo intermedio, porque necesita fábricas de memoria propias más de lo que le molesta Dalian. Especulación mía.

[NOTICIA 6: Intel mete 480 GB de memoria en una tarjeta]
Y hablando de memoria que no alcanza, Intel tiene una respuesta interesante.

El 12 de octubre circuló en Hacker News la página de producto de la Intel D270, una aceleradora para centros de datos. VideoCardz la identifica como Crescent Island, con arquitectura Xe3P y hasta 480 GB de LPDDR5X. Wccftech agrega 1,3 petaflops en FP8 con 350 watts.

Lo llamativo es la memoria. Las aceleradoras de punta usan HBM: chips apilados al lado del procesador, con un bus anchísimo. Mucho ancho de banda, pero cara y, como venimos diciendo hace semanas, escasa. La LPDDR5X es memoria de celular y de notebook: más barata por gigabyte y fácil de conseguir en volumen, pero con menos ancho de banda.

Piénsenlo como bodegas. La HBM es una bodega chica con un portón gigante. La LPDDR5X es una bodega enorme con una puerta normal. Para inferencia con modelos grandes, muchas veces el problema es que el modelo quepa. Si no cabe, da lo mismo el portón.

No vi precio ni fecha, y en Chile esto lo verán, con suerte, los integradores de servidores.

Me parece una jugada inteligente: si no le puedes ganar a NVIDIA en HBM, compite justo donde la HBM es el cuello de botella. Pero, Intel, el hardware no basta. Un comentario en Hacker News notó que el soporte de software en las preguntas frecuentes se veía a medio terminar. En centros de datos, esa es la parte que no se deja para después.

[NOTICIA 7: Steam para Linux por fin es de 64 bits]
Y para cerrar las secundarias, una buena noticia, para variar.

El 15 de octubre, Valve publicó una beta del cliente de Steam para Linux que por fin es una aplicación de 64 bits. Según Phoronix, además corre dentro del contenedor Steam Runtime, el mismo de los juegos, para que la experiencia sea más pareja entre distribuciones.

¿Por qué importa? Porque el cliente de Steam era una de las últimas razones para mantener instaladas las bibliotecas de 32 bits. Es como mantener un enchufe antiguo en toda la casa por un solo aparato.

Según TechPowerUp, llega junto con una actualización de logros que permite agruparlos por categorías.

Para mí es tarde, harto tarde, pero bienvenido, y deja a las distribuciones más cerca de soltar los 32 bits sin dejar botados a los que juegan. Eso sí, es beta: si su computador es el de la pega, esperen la versión estable.

[CHILE: Chile quiere ser hub digital y ahora habla de seguridad]
Y ahora, lo que pasa acá.

El 16 de octubre, la subsecretaria de Telecomunicaciones, Romina Garrido, presentó en el Departamento de Estado, en Washington, la hoja de ruta del Plan Nacional Digital. Lo interesante no fue el discurso del hub digital, que ya lo hemos escuchado harto, sino dos anuncios de fondo.

Uno: Cancillería está diseñando un mecanismo de screening de inversiones extranjeras. Dos: hace falta normativa específica para los riesgos de los cables submarinos y otra infraestructura estratégica. También habló de avances en el Cable Antártico y en Humboldt, con una delegación que incluía a la PDI y la ANCI.

Traducido: Chile empieza a preguntarse quién puede ser dueño de los cables y centros de datos por donde pasa nuestro tráfico. Y que lo diga en Washington no es casualidad. Para mí, viene con presión geopolítica incluida. Especulación, pero razonable.

En la misma línea, el 16 y 17 de octubre, BioBioChile y medios bolivianos informaron que Chile y Bolivia acordaron desarrollar un corredor bioceánico de fibra óptica. Por ahora solo tengo titulares, sin montos ni plazos.

Y ojo con la competencia: el 14 de octubre, según France 24, Uruguay anunció una inversión de 5.700 millones de dólares en un complejo de centros de datos. Unos 5,6 billones de pesos. El título de hub de la región no está asegurado para nadie.

Ahora, una convocatoria que cierra pronto. La ANCI organiza el primer Ejercicio Nacional de Ciberseguridad, un CTF en línea, el 29 de octubre. Son doce desafíos de web, forense, criptografía, ingeniería inversa, explotación de binarios, redes y OSINT, para nivel intermedio o superior. Hay que vivir en Chile, y la inscripción, individual o en equipo, cierra el 27 de octubre en anci.hackrocks.com. Si estudian informática, esto es currículum gratis.

En astronomía, el 14 de octubre ALMA informó estructuras de formación planetaria en discos pequeños, con especialistas de la Universidad de Chile.

Y de la USM, esta semana no hubo novedades fechadas. Ya volverá.

[CIERRE]
Y eso fue todo por esta semana. Si les sirvió, suscríbanse y activen las notificaciones para no perderse el próximo episodio.

Nos vemos la otra semana. Y cuiden esa RAM, que está carísima.

---

FUENTES

- ASML publica su tercer trimestre de 2026 y clientes miran pedidos para 2030 — Quartz, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMif0FVX3lxTE1jaFJ3akJmVDdHeDE3UXBKOWF0MC1IRXhEWENBaG9rVlNycEp6dlVwSFo1d1M5UFFabk51RHI2cV8yVFp6T0MwcW10X2FlWUJCMDRoaE5iT1VhOWs0Z2xjMTI2dm1iYXpuN3Rac0g4MTdaQXlQdlVBMS1wZllqUEU?oc=5
- ASML supera en utilidades pero queda bajo lo esperado en ingresos — Zacks vía Yahoo Finance, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMimAFBVV95cUxNNTNteEJhMTNuUzNCNHpfRHBFdzV4dGpEbU84Wm5tcDFYNGtpdzU3NEFobTcxT0FtMG0tRFR5Qk5ESlFzSGRwQ1N5NEs0RmJsNzhtYWN1eGphRl80YlpBajdwd0dtLXh4NDBQWmFRSnJETU9HUEs5RXptTUxSSTNwZ0VaSXY4elhpdFd5Y1FPWnNsVGdTQ3lSNQ?oc=5
- Ejecutivo de ASML dice que la capacidad apenas cubre la demanda y habla de pedidos hasta 2030 — 36Kr, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMiU0FVX3lxTE9qQ3V2MlBta0M2VmlnYVhVVllJdEVTM01MUlROdVhuN1JwMHBrRzROdEwtX3ptOWdTZmt2RndjMXFvUnlaZHRqbnUySG01WkgzRUFZ?oc=5
- Equipos de ASML casi agotados hasta 2028 — GIGAZINE, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMigwFBVV95cUxNUkNXb3FFcW9wQ1Z3Wm1ZMHJnZ080cWh1dFZPSzhLbHZ2c2J3NG9mdUpsWHFmOGlIZUFYT01nRTBPUGJ5V1E2dDdnb2lhSDUyQlNORjJTOVhPRWg1Q0czWGxTVHBrc3NvYnFvZ1A3WXNQYXotMW5LaTUzWGlYdzNTYzAwTQ?oc=5
- TSMC anota su sexto trimestre seguido de utilidad récord — CNBC, 15 de octubre de 2026. https://www.cnbc.com/2026/10/15/tsmc-third-quarter-profit-global-ai-.html
- TSMC se declara prudente de cara a 2027 — Reuters, 16 de octubre de 2026. https://news.google.com/rss/articles/CBMixgFBVV95cUxOWE9HY3JEZl96LXVuQmdXM1I4VVBoUUI4d09uNk9qYUdDSXpBTE8zYnJsNUwxUEljLXJ2aTYxYW5rcnFza0duNVNVRnFCWVAzd19MSXVzUTc2cnhnZkxfaVNXS3I2b25JNlJHZnlpMmpiTkQ1NXF5cWNVTG5sRTk3TE9fZExqRExHcjRUa3EybXEzZ1JRNjJPYlZUTWVaMk5hdWJta0g0UWtHZ251dE5BLTk5bk9nYm5vTDh5alo5c05QT054QVE?oc=5
- TSMC evalúa invertir en Texas — AP News, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMipwFBVV95cUxPdWxqdEVyUzNvcUNVQVVJUnpWd1hWeHRLcVBfWWNSS1FpTWtpOXdKYk54REhBZGFxcVVZUVJ2NXdnZTQ2NktEbnRtREpOVUpMdEtMTmRnb3Iwb3g4VGRzUXV2T1QzVmFCZUZOdUpsSEY3STdDc1VRVjFuTlNPdmdlQ2F4enh1cWxEUzJtRFY5ZHJHcWVmNEtra0cyTnFna0FEWi0tSnV3bw?oc=5
- El CEO de TSMC planea adoptar High-NA EUV en 2030 — Digitimes, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMiiAFBVV95cUxQMHRIQm9jWktNS3hLVWdRbmx5VzhXQ05mMW03Skt4S0dBT2M0RE1ob2V5bTY4aEZmNU10Z3lOWUExakd6bmMzbFJ3NWljVUhGVHVXUjZrNXNoQ2RZMmR1NUw0bUpTd3lwM2pJWDBFVEFiUHd3aF9PQ3JoSlR3TTFQdGRiQThBYnFG?oc=5
- ASML y Zeiss dicen que Hyper-NA podría estar lista en diez años — Reuters, 8 de octubre de 2026. https://news.google.com/rss/articles/CBMiuwFBVV95cUxOOWRCMnJEN0hfdXA5aS1lVVdWQXB5cE41QThjWURQb19XUGlCUFpUQTNCNWNRWDVrS1N6WWRrdl96QW9OQ2pYSnpkSzlHTjNGZ3VWcm1aYVpZc2M0TlJjQUE0WXB1S1J0NHk2T25yNWQ3d3hXdVY1VlZkclhzdncySFlvdGFiOWJTTjRqVk93NWNQQnJlYjcxQWxjS19zcFlhOHItVVp3aF85a1Z3RnZ3TnN6aWxWcGtDZGJV?oc=5
- La Unión Europea levantaría una sanción a una empresa china para salvar a un proveedor de ASML — Bloomberg, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMisgFBVV95cUxNM2lUQllVYjVsZFEtVnBjdHNGYXZxUzhwOTVtNnk5OENHUktsbUFaLVhXMUswYVNKa0dDYmF4a1gyM05MWEgyb3BTLTdJeS1pMXJnZlFIUmozelVVS2ROQTkyNWtCdTQxVXp5bGFKWmVpZU1EN0VyMXZ3TU1aN3puSTc1bTFLdGY2TmxIR0hOY3dCSHRFbVlLVWQ0YnhLbDE2YTdCWHpLamJyeHVUTWpybk5n?oc=5
- Startup china muestra un prototipo de fuente de luz EUV de 15 W — Tom's Hardware, 16 de octubre de 2026. https://www.tomshardware.com/tech-industry/semiconductors/china-startup-demoes-prototype-euv-light-source-15w-of-output-power-and-90-percent-domestic-components-still-years-away-from-viability
- China presenta un prototipo de fuente EUV con 90% de componentes locales, a años de la producción en masa — TrendForce, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMi2wFBVV95cUxQVHhwTHp3dUlISjJkWG9jTW9PVnB6TmMwa0lkZ1RYUC1vckNYdExjcGN2bGgxbjNzMVZCLUhmUmMzenpvM1ZmQkg1c0Y1NFJSMmNZNlNrWWhvZnFUTm5ZSDdPWkhLUUdVZjRzcUpEWTMwM3RESlE4OWhPSV85a1RYdnJ3a1Y2Wm1FQ05TY2gybC1DUEVXcmo4SWlLTU5oUkhSU29kUHhmc1FpTlpsLUVUeE9jYnBPak42LXU4OVNaUmR0NlgyNnZsTkRVVmxEVm16dzA2ai1fZmxDZEk?oc=5
- Qualcomm prueba que Arm incumplió su licencia y gana dos dólares — TechPowerUp, 15 de octubre de 2026. https://www.techpowerup.com/353776/qualcomm-legally-proves-arm-breached-its-license-wins-usd-2
- Declaración de Qualcomm sobre el veredicto — Qualcomm, 13 de octubre de 2026. https://investor.qualcomm.com/news-events/press-releases/news-details/2026/Qualcomm-Statement-on-Trial-Verdict-Win/default.aspx
- Resumen semanal: el juicio con Qualcomm y el 9% de los ingresos de Arm — TradingView, 12 de octubre de 2026. https://news.google.com/rss/articles/CBMiwAFBVV95cUxNNjdoN3BEdUNMS3h3OWRYOGd3N3JfUk9GT01ld1N6bjBENGNmTV9NOGdsT191ajl2SEFhSkFVelFVcnZ4WWpNMkg1VHNCQWZuanFwZGdzdndfNFZZRl9qa0FseTJVN1Azc1dYWkthRjRseDhCdkZYQXdxQllaUTQ4LUVsMkU1eFd6ZEVRdGZtUFRoclptUXJka2tIQmlMZFRDY3hpR0V4Qk9nS2ZrUGFiRHp0eXlWaVJRdVpDWWp5YnY?oc=5
- El sindicato de Micron en Taoyuan autoriza una huelga — 24/7 Wall St., 8 de octubre de 2026. https://247wallst.com/investing/2026/10/08/micron-is-making-record-profits-but-a-taiwan-union-just-voted-99-to-authorize-a-strike/
- El presidente de Taiwán pide a Micron y sus trabajadores negociar con sinceridad — Reuters vía Investing.com, 15 de octubre de 2026. https://www.investing.com/news/stock-market-news/taiwan-president-calls-for-micron-workers-to-negotiate-sincerely-ahead-of-possible-strike-4950532
- Samsung publica su guía de resultados del tercer trimestre de 2026 — Samsung Newsroom, 8 de octubre de 2026. https://news.samsung.com/global/samsung-electronics-announces-earnings-guidance-for-third-quarter-2026
- Musk critica los precios de la memoria y elogia a Micron — Tom's Hardware, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMiswFBVV95cUxNZlh4UVVKLV80Mk9wZXZjS1hWdEpUblZXWkY5QnJNaDdQbGJvOTdQZkhJTUJ5bGdsRmxIekxneWI1RHR6VXZMbzBZOHBQb1hSSDZ4c1o5eGltU041Mjk1TkpEcjZwVjhOU3JzTlVWN0pkbU5ybGVkN3U4cEdnNW5FbmtYa2IxeF8ydGgzZWdTS0pXLUtaSHJYVlBoZE9nVEFiSmhOT21ndUhpdUxhZW9ZZGw5WQ?oc=5
- CXMT avanza en un diseño de DRAM que persiguen Samsung y SK hynix — South China Morning Post, 12 de octubre de 2026. https://news.google.com/rss/articles/CBMiwAFBVV95cUxOZmZHS080emE3cTZyaHozcTJmTTBYUk1GZEhNX3drTUh1S29LZWJRaWpUMlplQWd4STZzZFRNWFZkeEp4UVdiSHdaZlZPWVdHUnFHUDRrTDlWbzIzTU9LeUpoTDZ4ZjNxY1FBemZaVnRaOFlxNjJWcm9RaVR2ZWtldTlQWWhUczc4LUxmTG8tMGpUNTNvQ2lDUHd1RGZ5b3IyYzd5MUZqcU16NnN0aUIycmVIdlhZT2NseFBCaDFhdW_SAcABQVVfeXFMTU1TVTBjV2xjdGFob3d3R3VVTE0tczZyLXA3elItTmN3OVNHUm5OeER4SUxNVVdCNEZESTBzUE41dGNqWWd2SGt3czNTUW5kcWxZN3RIblpGQWtfTHZ3UnNzYm1QWUdVckUzYkp5ZkpyMUxLLXdDNFZROHdjMGFST0tsLVcxWlVETUkyMjVZaHpkTkZEN01URzUyRjZlOWV6T1hVX0FvaHVVTVM2ME45QWI5QXdHYzQ1b1dJVElDZGNG?oc=5
- CXMT promociona su DRAM sin especificaciones ni fecha — Seoul Economic Daily, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMingFBVV95cUxNYXJ3a0Z1SUIxeVZIdUtjeVUxU0E2aS03Z3ZsdmJ5dHppRjhETGIzeHZNaTFZTFAwaDFXMjF0OWFRUm5hWTBfS0gtYmNsczlqaWVGbjRHRnRRMUpybWx0emU5U3pWMFZtSXJUVjZuT05TdjNDM1ZPS0hoVVhOTXg4Q3BIRUhpQmd5TS1PZ29xSV9oNGpNSWhQRzlEbTlvdw?oc=5
- CXMT cambió la estructura de la celda por los límites de la EUV — economy.ac, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMiV0FVX3lxTFBZdTU3M1BvMl9BQ245Z2Nod1FnMDVPUkZDYXFOSmgtTjdlY3F2aDBFS2lsbHU0TDIzN2tUSWVZZEU2dXZxaFZMb3RmcUxWd2dqZktzN0ctMA?oc=5
- Wall Street duda de la ventaja 4F² de CXMT — Chosunbiz, 16 de octubre de 2026. https://news.google.com/rss/articles/CBMiekFVX3lxTE16WE9TTXAwUkhxdThhMFBobzJFMHN3aHNWVEJaZTkwdlUtcEF3eWhFdjZodjNTRkk4aURiZzRrbWtUMW9PNWp6OTl5dkwzbkt3M2FQd0R1WEZ6VHl6ckJQdENmR3RjOHFtbTlxVlp3U3h6RVRLa2ZTSE1n0gGOAUFVX3lxTE9YQU1yS0ZBU1FHYzdsZ1QzeXJqb0NYTlBSaE1qNTFSSF9TUGNWR1V1YzlweEEwbGI1bU5GNUxDN3pHX3gtckxyc0tzdUJLTUtvTmNaWkdGeUpEM3o0M3RYTXhqOHdQWXNSQm1OaUxrNHo4R3dqaF9ZU0dYREd0NnRMdlA2aFVWWHV6bG0tS0E?oc=5
- SK hynix condiciona su nueva fábrica en Estados Unidos a exportar más equipos a China — Reuters, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMizwFBVV95cUxNZExZLWRBZUo2NlJPaFhzSWxERFdkcGl1bklYWTFfQ1NrRG01WWtmQjhlT3g5OEtvT3c2SjNlbHVlcEhVelBtVk5RVHR2ckU4VFZTV1J1S3ZpOENaT1dibXQ3cXdsbFd3Rk43N1lFWEZBVC00NFJiSlU5TlpEbEVsWi1RakhQYmpwN2xlMGRlakZqdFRnaEJpQkZaRllTMFVhbUJmaWt3d2NRclJvRFZ1VG5jNWpSZ2dWZ3l1bEhHUnBWajR4YVB6S3hEamlMMzA?oc=5
- SK hynix busca aprobación para exportar equipos a China mientras Solidigm planea una fábrica en Estados Unidos — Yahoo Finance, 15 de octubre de 2026. https://news.google.com/rss/articles/CBMikAFBVV95cUxNeEhZMkpXMDIxV2ZVTE4ySW12bTJPdEpldlpSdl9WZ3RLMEkxUndMTEdTZ2lMeGhHaWZmYTBUVWh4Sm1FOHhUeFVxcjNPbE9USElkbFNkVFQ4bURoU21WM3JuZDFPekZKMG5kb0V4cTMwUEJyZ0xzeUQtdzgzS1B0dWE1SGdyYXNkOTZnSE9sOHk?oc=5
- La Intel D270 es la Crescent Island Xe3P con 480 GB de LPDDR5X — VideoCardz, 12 de octubre de 2026. https://news.google.com/rss/articles/CBMingFBVV95cUxQRnk5Z3lqd052VEwtU1otdjVxM3pCLXUtak83Q1puQU9aLXh4NUJoejZDUzNZV3ZaaTA3QzJRMTBVYU83dlJRM3R2SU9jMWcydTlicDVZcFlNVEFHWnNiVlNBZmQ2U09UZEFkclZCOHlPRTFocjhnS2hWU1U1NXpQMEY1VnhZRFIzRW1qTTlBaDhYQWE4OGxOTmkzS0NCZw?oc=5
- El cliente de Steam para Linux pasa a 64 bits en beta — Phoronix, 15 de octubre de 2026. https://www.phoronix.com/news/Steam-Linux-Beta-64-bit
- Steam para Linux en 64 bits y nueva gestión de logros — TechPowerUp, 15 de octubre de 2026. https://www.techpowerup.com/353772/linux-finally-gets-64-bit-steam-client-and-new-game-achievements-management-in-client-beta
- Subtel en el Departamento de Estado: infraestructura estratégica con resiliencia y seguridad — Subtel, 16 de octubre de 2026. https://www.subtel.gob.cl/subtel-en-depto-de-estado-washington-para-ser-un-hub-digital-regional-debemos-abordar-la-infraestructura-estrategica-con-resiliencia-y-seguridad
- Chile y Bolivia acuerdan un corredor bioceánico de fibra óptica — BioBioChile, 17 de octubre de 2026. https://news.google.com/rss/articles/CBMi2wFBVV95cUxOSlRUX2RIcUFORW1XV1puTld1bkdKa2lTaUY3VmxybUpYWU1mOTVCUUdPdVI4bFFNTHBLOG9fdngtdXdKQ3VkNElQblBaSzdvUGZGMjJfMTYwR0RJa1RBUFlBRnFCTjF3UEZvcEg4WUZaR1l2RDBsaElDR0J5akpSeldxYTBxTGpzRE0wWWEwQ1drN2RnRmtDTEd3M25qcjA4bS1fNEFMdXlFQWg4ZDFuVHdQdDV5YzJCSUUzSVU5bG0yNXVGU1JPZnIzZ1R6T2FQdzgxTF8tX1lRTW8?oc=5
- Uruguay anuncia 5.700 millones de dólares para un complejo de centros de datos — France 24, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMi6wFBVV95cUxNNmxwelFfSzhCYi0wbUhTWXFLQ21Qc0dpVGxYTUZwUm11SjJHbG1jMEY3WHFoYlN2NFI2STFkVnQ5eldtVERGTi15WUQ5R3ZTdDVBN0I0a1JGS2NPa1ExWHM4OTJoVHNlNlMwWVF2S2dta0Y1RFEyWVdGZ2JWWE5BYUlqTU9fTDdGYXVMNnp2UHc3aDFpc01zbXVOWWpMNjBqVHlkaEZuR3lsc3pxTHFOZnkyMlNxNlBWRXhMVkF2eXNVVzVhRTFYUUF4Mmg3TWpYQTNkVk1PQnpDbzNmdm1LS1dsS1JIcWI0cTBJ?oc=5
- La ANCI realizará el primer Ejercicio Nacional de Ciberseguridad el 29 de octubre — REUNA, 8 de octubre de 2026. https://www.reuna.cl/2026/10/anci-realizara-el-primer-ejercicio-nacional-de-ciberseguridad-este-29-de-octubre
- ALMA revela estructuras de formación planetaria en discos pequeños — ALMA Observatory, 14 de octubre de 2026. https://news.google.com/rss/articles/CBMiwgFBVV95cUxNTGwwNzRCcmRtU1pXb0VSNC02Mi04YkJOQWd3TG40Skg2TGo1ZEhRanRhUUtKZ3RxbDh1cGhLUm9fRy1PUUExeVJtdTAyb3RWd1NRNldHVlRBZFRQbkVvdUtNSkNSYzd4WUpkejNydEhmRmNNd1p6MjluWXVFTjl6R0VwZzNLWi1vdlEwRGQ3V21YanQ0SklUODJTVnNPTTY4OFJJcnBfRk9DbVRRdkJQVXdENV83ZEU4aUl3aTF0SUpsUQ?oc=5

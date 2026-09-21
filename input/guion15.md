[INTRO]
Buenas a todos, bienvenidos una vez más al canal, la semana del 8 al 15 de septiembre.

Semana intensa, porque hay dos cosas pasando al mismo tiempo que están conectadas aunque no lo parezca: la RAM sigue por las nubes y las fábricas de silicio se están reordenando por culpa de la IA.

Así que hoy partimos por lo que les va a doler el bolsillo y de ahí subimos a las fábricas, al kernel de Linux, a las tarjetas de video y hasta a lo cuántico. Vamos.

[NOTICIA 1: La RAM sigue por las nubes y no es culpa tuya]
Partamos por el fondo técnico, porque si no, no se entiende por qué su próximo PC vale el doble.

La RAM que ustedes le meten a la placa madre es DRAM: memoria dinámica. Cada bit se guarda en un condensador chico que se descarga solo, y por eso hay que refrescarlo miles de veces por segundo. Es barata de fabricar por bit y por eso históricamente fue el componente más "commodity" del PC: subía y bajaba de precio, pero siempre era lo barato del build.

Eso se acabó. Y acá viene lo importante: la misma línea de producción, la misma oblea de silicio, sirve para hacer DRAM común y corriente o para hacer HBM, la memoria apilada que va pegada a las GPU de IA como las de NVIDIA y AMD. La HBM son varios chips de DRAM apilados uno sobre otro con conexiones verticales, y se vende carísima por gigabyte comparada con un módulo DDR5 normal.

Entonces pónganse en los zapatos de Samsung, SK Hynix o Micron, que entre los tres controlan entre 90% y 95% de la DRAM del mundo. Según Counterpoint Research, al primer trimestre de 2026 Samsung lidera con 38%, SK Hynix con 29% y Micron con 22%. Si con la misma capacidad de fábrica puedo hacer memoria para gamers a precio de commodity, o memoria para datacenters de IA a precio de oro, ¿qué hago? Obvio: le doy la capacidad a la IA. Y eso es exactamente lo que pasó.

El resultado es brutal. Según el índice de precios de RAM de Tom's Hardware, el precio spot de un chip DDR5 de 16 gigabit pasó de 6,84 dólares el 20 de septiembre de 2025 a 24,83 el 19 de noviembre y 27,20 dólares en diciembre, con máximos de sesión de hasta 37 dólares. Eso es un alza de casi 298% en un solo trimestre. Como cada módulo lleva varios de esos chips, el precio en la caja del retail siguió la misma curva.

En Estados Unidos, un kit de 32GB DDR5-6000 que valía como 80 dólares a mediados de 2025 llegó a rondar los 400 dólares por estos meses. Eso está en los trackers de precios que se actualizan a diario. Al 15 de septiembre uno de esos índices marcaba la DDR5 en 17,50 dólares por gigabyte, con el segmento gaming subiendo un 10% en una semana. Confirmado por los rastreadores de precio, no es rumor.

¿Por qué importa tanto y por qué es la noticia principal? Porque esto no es un pico pasajero por un incendio en una fábrica. Es un cambio estructural: la demanda de infraestructura de IA se comió la holgura del mercado de memoria y no la va a soltar pronto. Intel apuntó a 2028 antes de que la cosa se normalice; Silicon Motion advirtió que la escasez de DRAM, NAND y HBM persistirá hasta 2028, y Gartner espera que el estrujón de almacenamiento llegue por lo menos a 2027. Eso es proyección de la industria, pero coincide de varias fuentes.

¿A quién le conviene? A los tres fabricantes de memoria, que están con márgenes históricos. Samsung reportó márgenes récord en memoria. Y ojo con este detalle que a mí me parece clave: se reportó que Samsung tiene reservada cerca de la mitad de su mejor nodo para su propia memoria. O sea, ni siquiera es que no quieran hacer DRAM: es que la DRAM cara le gana a la DRAM barata.

¿A quién le duele? A ustedes. Al que arma PC, al estudiante que quería subir de 16 a 32 gigas para las máquinas virtuales del ramo de sistemas operativos, al que iba a comprarse un notebook. Y ojo, porque los fabricantes de equipos armados ya están metiendo menos RAM o RAM más lenta para cuadrar el costo. O sea, aunque no armes tu PC, igual te llega el golpe en forma de un notebook más penca al mismo precio.

Mi opinión, y la marco como opinión: si tienen un PC que anda bien, este no es el año para andar cambiando RAM porque sí. Si de verdad necesitan más memoria para trabajar o estudiar, cómprenla al tiro, porque todo indica que no va a bajar en el corto plazo. Y si están armando de cero, presupuesten la RAM como si fuera un componente caro, no como el relleno barato que era antes. Cambió el juego, y hay que planificar distinto.

Y una queja al pasar: me carga cuando las marcas venden esto como "ah, es que la demanda subió". No. Es una decisión de asignación de capacidad. Prefieren venderle a la IA. Es legítimo como negocio, pero que no nos vendan que es un fenómeno natural del clima.

En uno o dos años, ¿qué veo? Si se cumplen los plazos que menciona la industria, recién en 2027 o 2028 podríamos ver alivio, cuando entren nuevas fábricas. Pero fábricas de memoria tardan años en construirse, así que no esperen milagros para el próximo Cyber. Eso es especulación mía apoyada en lo que dice la industria.

[NOTICIA 2: OpenAI se mete a Samsung y le pica el monopolio a TSMC]
Y ya que estamos hablando de fábricas, pasemos a lo que pasó el 9 de septiembre, que es la otra cara de la misma moneda.

El gerente de OpenAI en Corea, Harrison Kim, confirmó en una conferencia de prensa en Seúl que OpenAI y Samsung están haciendo investigación y producción conjunta de chips de próxima generación. Esto lo cubrió Reuters directo, así que es confirmado por la empresa, no rumor de leaker.

¿Por qué importa técnicamente? Porque hoy casi todo el silicio de punta del mundo sale de una sola empresa: TSMC en Taiwán. TSMC no diseña chips, solo los fabrica, y por eso todos confían en ella: NVIDIA, AMD, Apple, y ahora los laboratorios de IA que diseñan sus propios aceleradores. El problema es que si todos dependen de una sola fábrica, esa fábrica es un cuello de botella y un riesgo enorme.

Samsung es la segunda opción real en nodos de punta, con su proceso de 2 nanómetros usando transistores gate-all-around, que es la misma clase de transistor que usa TSMC. El tema de Samsung siempre fue el yield, o sea, cuántos chips le salen buenos por oblea. Según Sammy Fans, del 8 de septiembre, el yield de 2 nanómetros en su fábrica de Taylor, Texas, habría pasado de cerca de 60% a comienzos de año a cerca de 80%, con una inversión de unos 37 mil millones de dólares y una proyección de unas 50 mil obleas al mes. Ese número de yield es de fuentes de la industria, no verificado de forma independiente, así que trátenlo como reporte, no como confirmado.

Acá hay un matiz importante que a mí me gusta destacar: no está claro que Samsung sea la "segunda foundry confirmada" de OpenAI. Lo que sí se puede decir es que están colaborando en desarrollo y producción. Y dato que se contradice un poco entre fuentes: el mismo día, TrendForce mostró que TSMC siguió aumentando su ventaja, con más del 70% del mercado de foundry pura frente a un 7,3% de Samsung. O sea, mientras se anuncia la diversificación, TSMC igual saca más distancia. Las dos cosas son ciertas a la vez.

Para mí esto es lo estructural: cada vez que aparece una segunda fuente creíble de silicio de punta, cambia el poder de negociación de toda la industria. No mañana, pero sí en el próximo ciclo de diseño. Y conecta con la noticia anterior: si Samsung está ocupando su capacidad en chips de IA y en su propia memoria, ¿adivinen qué NO está fabricando? Exacto, la DRAM barata.

[NOTICIA 3: El kernel de Linux se pone al día con AMD y con la IA]
En fin, pasemos al software de bajo nivel, que esta semana estuvo movido en el mundo del kernel de Linux.

Primero, una que a los que usamos Linux con tarjeta AMD nos tiene contentos: se confirmó que Linux 7.4 va a habilitar HDMI 2.1 por defecto en el driver AMDGPU, con FreeSync, VRR y ALLM. Esto viene con historia: el HDMI Forum llevaba años rechazando la implementación abierta de HDMI 2.1, y por eso los usuarios de AMD en Linux quedaban capados a resoluciones y refrescos más bajos por HDMI. Algo cambió este año, se especula que con participación de Valve, y ahora por fin llega. Esto es de Phoronix, del 11 de septiembre, confirmado en los parches.

Para el que no cacha: HDMI 2.1 es lo que necesitan para tirar 4K a 120Hz o VRR en el televisor. Que estuviera bloqueado en el driver abierto era una pena seca. Buena noticia.

Segundo, algo que me da entre risa y respeto. Lorenzo Stoakes, ingeniero de ARM, mandó una serie de 23 parches que encontró cuellos de botella en la compilación del kernel usando IA. Según Phoronix, las compilaciones tipo allmodconfig quedan hasta 36% más rápidas, las incrementales hasta cerca de 70% más rápidas y las "noop" hasta un 90% más rápidas. Lo divertido es cómo lo describió Phoronix: la IA generó harto "código feo", pero encontró los cuellos de botella reales. O sea, la IA no escribe bonito, pero sirve de detective. Va camino a Linux 7.4.

Y para cerrar el bloque: salió Linux 7.3-rc3 el 13 de septiembre, y se parchó un bug de pérdida silenciosa de datos en espacio de usuario que llevaba existiendo desde 2023. Tres años ahí escondido. Confirmado, todo de Phoronix.

[NOTICIA 4: Las tarjetas de video para gamers quedaron abandonadas]
Y hablando de hardware que sí nos importa a los que jugamos, pasemos a las tarjetas de video, donde la película es medio deprimente.

El mismo fenómeno de la IA que se comió la RAM está secando el mercado de GPU de consumo. Se filtró que la Radeon RX 9050, de gama de entrada con 8GB, podría ser la única tarjeta de video nueva de escritorio en todo 2026. Las Super de la serie RTX 50 de NVIDIA nunca aparecieron, e Intel no saca una Arc de escritorio nueva desde comienzos de año. Esto es reporte de PCWorld y filtraciones, no confirmado oficialmente.

¿Por qué? Porque tanto NVIDIA como AMD están persiguiendo la plata del datacenter, y la memoria GDDR7 también subió de precio. Fíjense que es la misma historia: la IA se lleva el silicio y la memoria, y al gamer le quedan las sobras.

Mirando más adelante, hay un leak del filtrador Moore's Law Is Dead, que dice que las GPU RDNA 5 de AMD llegarían a mediados de 2027, fabricadas en el nodo N3P de TSMC, con un tope de gama que le pelearía a la próxima flagship de NVIDIA. Menciona una supuesta "Radeon RX 10090 XT" con 36GB de GDDR7. Ojo: esto es rumor de leaker, los nombres son placeholders y AMD no ha confirmado nada. Lo pongo como rumor.

Mi opinión: si el rumor se confirma, y AMD llega antes que la RTX 60 con algo de gama alta de verdad, la cosa se pone entretenida para el que quiere armar PC a fin de 2027. Pero para este año y el próximo, el consejo es simple: si encuentran una tarjeta buena a precio decente, no esperen la próxima, porque la próxima puede que ni exista.

[NOTICIA 5: NVIDIA se pone a jugar en serio con lo cuántico]
Y ya que estuvimos con software, cerremos el bloque internacional con algo distinto que salió el 14 de septiembre.

NVIDIA anunció CUDA-Q Logical, una capa de orquestación open source para diseñar y probar aplicaciones para computadores cuánticos tolerantes a fallas. Confirmado por NVIDIA en su sala de prensa.

Explico el por qué. Un qubit físico es ruidoso, se equivoca solo. Para hacer algo útil necesitas qubits lógicos, que son varios qubits físicos trabajando juntos con corrección de errores para comportarse como uno confiable. Diseñar todo ese sistema, algoritmo, código de corrección, arquitectura de hardware, a mano, es una pesadilla lenta.

El dato concreto que me llamó la atención lo dijo Anna Grassellino, CTO de Fermilab y directora del SQMS Center, citada por NVIDIA: su equipo exploró combinaciones de esos recursos en apenas tres semanas, cuando normalmente les habría tomado unos cinco meses armando infraestructura especializada. Eso es cerca de un 7x, y viene de una cita atribuible.

¿Por qué me parece jugada de ajedrez? Porque NVIDIA no vende computadores cuánticos. Pero si logra que toda la industria cuántica diseñe encima de su plataforma y de sus GPU, cuando lo cuántico madure, NVIDIA ya está adentro. Es la misma estrategia de CUDA de siempre: no vender el hardware específico, sino ser la capa de software donde todos programan. Opinión mía.

[CHILE: Data centers con sed, la ley de datos que se viene y el arancel que te van a cobrar]
Ahora, el bloque de la casa.

Partamos por lo grande: el 9 de septiembre CNN Chile reportó que el país suma más de US$7.500 millones en inversiones comprometidas en data centers, con Amazon, Microsoft y Google entre los actores. Según ese reporte, Chile tendría 386 MW de capacidad operativa y 37 centros de datos operativos, y se proyecta duplicar esa capacidad. Confirmado por el reporte, con la advertencia de que las cifras de capacidad varían harto según el informe: GPS Property había medido 242,7 MW a mediados de 2025, segundo en la región después de Brasil.

Y acá está la polémica de siempre: agua y energía. Un data center grande consume agua para enfriarse y electricidad a lo bruto. La industria dice que hoy reciclan cerca del 90% del agua, pero en un país con más de una década de sequía estructural, la desconfianza es razonable. El caso del data center de Google en Cerrillos, que consumía muchísima agua, ya generó rechazo ambiental. Mi opinión: bienvenida la inversión y la pega que genera, pero la transparencia sobre consumos reales no es negociable.

Ahora, dos cosas legales que le importan a todo el que trabaja en tecnología acá.

Uno: la Ley 21.719 de protección de datos personales entra en plena vigencia el 1 de diciembre de 2026. Ojo, falta poco. Crea la Agencia de Protección de Datos Personales, con multas de hasta 20.000 UTM para las infracciones más graves. Es básicamente el equivalente chileno al GDPR europeo. Si programan sistemas que guardan datos de personas, esto los afecta directo. Y convive con la Ley 21.663, la ley marco de ciberseguridad, con la ANCI, que ya obliga a reportar incidentes desde 2025. Todo verificado.

Dos, y esta es fome pero clave para el que importa hardware: cambió el tema de las compras por courier. La antigua exención de US$41 sin IVA se eliminó a fines de octubre de 2025. Hoy toda importación paga 19% de IVA, sin excepción por monto. La exención del arancel del 6% subió a US$500 FOB, o sea, bajo esos 500 dólares no pagan el 6%, pero el IVA lo pagan igual. Verificado con el SII y Aduanas. Así que cuando vean un kit de RAM baratísimo afuera, súmenle el IVA sí o sí antes de emocionarse.

Y hablando de precios: con el dólar a $941 al 15 de septiembre, un kit de 32GB DDR5 que afuera vale como 400 dólares serían unos $377 mil en crudo. Pero en Chile, en SoloTodo, el kit más barato de 32GB DDR5-6000 andaba en $638.990, un Kingston Fury Beast. Ahí ven ustedes el efecto del IVA, el margen del retail y la espera. Duele.

En el mundo académico, la USM sigue firme: el Departamento de Informática lideró la primera final de Latinoamérica de la ICPC en Chile este año, y asumió nuevo director, Marcello Visconti, para el período 2026-2027. Y en cómputo científico, el Observatorio Vera Rubin en Cerro Pachón ya está tirando alertas en tiempo real, y la plataforma ALeRCE, hecha en Chile, es uno de los siete brokers oficiales del mundo que procesa ese torrente de datos. Eso es pega de ingeniería de software de verdad, acá, para el que quiera apuntar para allá. Esta semana en particular no hubo un bombazo nuevo de la USM, así que no les voy a inflar el bloque.

[CIERRE]
Y eso fue todo por esta semana. Si les sirvió, ya saben: suscríbanse y activen la campanita de notificaciones para no perderse el episodio de la próxima.

Nos vemos a la otra. Cuídense, y no compren RAM por impulso.

---

FUENTES

- Los precios de la DDR5 siguen subiendo en 2026 — OC3D, septiembre de 2026. https://overclock3d.net/news/memory/its-getting-worse-ddr5-memory-prices-continue-to-increase-in-2026/
- Índice diario de precios de RAM (DDR5 a 17,50 USD/GB al 15 de septiembre) — RAM Price Trends, 15 de septiembre de 2026. https://rampricesusa.com/ram-price-trends
- La crisis de la DRAM y la memoria devorada por la IA (índice de precios de Tom's Hardware) — Tech Insider, septiembre de 2026. https://tech-insider.org/dram-ram-price-crisis-2026/
- Cuotas de mercado de DRAM y foundry (Counterpoint Research) — Counterpoint. https://counterpointresearch.com/en/insights/global-semiconductor-foundry-market-share
- OpenAI confirma programa de chips con Samsung — The Register, 9 de septiembre de 2026. https://www.theregister.com/systems/2026/09/09/samsung-to-fortify-openais-semiconductor-supply-chain/5295374
- OpenAI confirma producción conjunta con Samsung; Samsung reserva medio nodo para su memoria — Tech Times, 10 de septiembre de 2026. https://www.techtimes.com/articles/327186/20260910/openai-confirms-samsung-chip-program-samsung-has-half-its-best-node-reserved-its-own-memory.htm
- Yield de 2nm de Samsung en Taylor y ampliación de sociedad con OpenAI — Sammy Fans, 9 de septiembre de 2026. https://www.sammyfans.com/2026/09/09/openai-deepens-samsung-partnership-for-next-gen-ai-chips/
- TSMC amplía su ventaja en foundry sobre Samsung — Business Korea, 9 de septiembre de 2026. https://www.businesskorea.co.kr/news/articleView.html?idxno=276569
- Linux 7.4 habilitará HDMI 2.1 por defecto en AMDGPU — Phoronix, 11 de septiembre de 2026. https://www.phoronix.com/
- La IA hizo código feo pero encontró cuellos de botella para compilar Linux más rápido (parches de Lorenzo Stoakes, ARM) — Phoronix, 14 de septiembre de 2026. https://www.phoronix.com/news/Faster-Kernel-Builds-AI-v2
- Linux 7.3-rc3 y parche de pérdida silenciosa de datos — Phoronix, 13 de septiembre de 2026. https://www.phoronix.com/news/Linux-7.3-rc3-Released
- La RX 9050 podría ser la única GPU de escritorio nueva de 2026 — PCWorld, 2026. https://www.pcworld.com/article/3137662/amd-rumored-radeon-rx-9050-may-be-the-only-new-desktop-gpu-in-2026.html
- RDNA 5 de AMD llegaría a mediados de 2027 (filtración MLID) — TweakTown, 2026. https://www.tweaktown.com/news/112289/amds-rdna-5-radeon-gpus-will-launch-in-mid-2027-per-new-leak/index.html
- NVIDIA expande CUDA-Q con CUDA-Q Logical (cita de Anna Grassellino, Fermilab) — NVIDIA Newsroom, 14 de septiembre de 2026. https://nvidianews.nvidia.com/news/nvidia-expands-open-source-cuda-q-platform-for-fault-tolerant-quantum-computing
- Chile suma más de US$7.500 millones en inversiones comprometidas en data centers — CNN Chile, 9 de septiembre de 2026. https://www.cnnchile.com/negocios/amazon-microsoft-google-chile-suma-mas-us7500-millones-inversiones-comprometidas-data-centers/
- El debate ambiental detrás del auge de los data centers en Chile — La Tercera, 2026. https://www.latercera.com/sustentabilidad/noticia/potencia-tecnologica-o-nueva-presion-ambiental-el-debate-detras-del-auge-de-los-data-centers-en-chile/
- Ley 21.719 entra en plena vigencia el 1 de diciembre de 2026 — Diario Constitucional, 2026. https://www.diarioconstitucional.cl/articulos/cuando-el-estado-filtra-sus-datos-declaraciones-de-la-anci-y-desafios-para-la-implementacion-de-la-ley-21-719/
- Nuevas reglas de IVA y arancel en compras internacionales (fin de la exención de US$41) — SII, 22 de septiembre de 2025. https://www.sii.cl/noticias/2025/220925noti01pcr.htm
- Valor del dólar al 15 de septiembre de 2026 ($941,42) — Dólar Online, 15 de septiembre de 2026. https://www.dolaronline.cl/
- Precios de RAM DDR5 desktop en Chile — SoloTodo, septiembre de 2026. https://www.solotodo.cl/ram-ddr5-desktop
- ICPC Latin America Championship 2026 en Chile — ICPC, 2026. https://latam2026.icpc.cl/en/
- El Departamento de Informática USM y su nuevo director 2026-2027 — Informática USM, 2026. https://informatica.usm.cl/noticias/direccion-marcello-visconti-2026-2027/
- Observatorio Vera C. Rubin y la plataforma chilena ALeRCE — REUNA, 2026. https://www.reuna.cl/2026/02/observatorio-vera-c-rubin-en-chile-lanza-monitoreo-del-cielo-en-tiempo-real/
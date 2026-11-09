# Historial del noticiario

Tres episodios publicados. El ep 1 fue el primero (sin episodios anteriores).

## Episodios

- ep 1 (2026-09-14): ventana 2026-09-08 a 2026-09-14. Noticia 1: NVIDIA compra Hugging Face. Secundarias: RTX PRO 5500, Ryzen 5 7500/5500F, Steam Frame y crisis de memoria, CEO de Apple (barrido), bug de Linux. Bloque Chile vacío por falta de candidatas.
- ep 2 (2026-09-20): ventana 2026-09-14 a 2026-09-20. Noticia 1: SK hynix en conversaciones con Intel para fabricar memoria en Ohio. Secundarias: Qualcomm-Amazon con warrants (rezagada del 09-08), Micron RDIMM DDR5 de 512 GB, Intel suspende su bug bounty, Mojo 1.1. Bloque Chile: data centers (Cerrillos/OLCA, Metlen 100 MW, Grenergy Polpaico), postergación ley 21.719 (en titular), Subtel Fiestas Patrias, cable submarino sismos, exoplaneta Elias 2-24 b (UDP), USM VIU 2026 y tesis CLEI de Daniel San Martín (contexto, 09-11).
- ep 3 (2026-09-24): ventana 2026-09-18 a 2026-09-24. Noticia 1: la crisis de memoria ya encarece todo el notebook (XMG, Acer, Surface, mediación fallida de Micron vía barrido). Secundarias: Snapdragon 8 Elite Gen 6 / Extreme (2 nm, 5 GHz), Radeon RX 9050 de 4 GB (con GDDR7 en driver de Linux como contraste), Supermicro despacha Vera Rubin NVL72, Linux en Snapdragon X2, Qualcomm compra PickNik (evento mayor; mención de la renovación de patentes con Apple). Bloque Chile: Subtel bloquea 37 dominios de apuestas vía DNS, fiscalización 5G rural en Itata y Última Milla en Ñuble, proyecciones de datacenters al 2031, Sonda compra negocio Apple de Yáneken.

## HILO: nvidia-hugging-face
- Descripción: NVIDIA compra Hugging Face por US$12.930 M (11.900 M efectivo + hasta 1.000 M en acciones de retención); acuerdo firmado el 2026-09-02, anunciado el 2026-09-03.
- Estado actual: anunciado y confirmado por NVIDIA (8-K y blog). Promesas públicas: no será obligatorio usar cómputo NVIDIA, se mantiene multinube y multiacelerador, se siguen alojando modelos de todos los laboratorios. Reacción dividida en HN (valoración vs conflicto de interés); columna de The Register en contra; Gerganov (llama.cpp) dice que los backends siguen guiados por la comunidad. No se encontró información sobre revisión regulatoria ni fecha de cierre.
- Estado al ep 2 (2026-09-20): sin novedades en la ventana; el barrido no encontró revisión regulatoria ni cierre.
- Cubierto en: ep 1 (2026-09-14) como NOTICIA 1 — se explicó qué es Hugging Face, por qué NVIDIA compra el punto de distribución, las promesas de neutralidad y la opinión de que la neutralidad se va a erosionar de a poco.
- Reabrir solo si: cierre formal de la operación; revisión o bloqueo regulatorio; cambio en las condiciones del hub (cobros, límites, integración por defecto del stack de inferencia de NVIDIA); salida de ejecutivos clave (Delangue, Wolf, Chaumond); anuncio de espejos alternativos con respaldo de AMD, Intel o gobiernos; ruptura de la promesa multiacelerador.

## HILO: crisis-memoria-2026
- Descripción: precios de DRAM y NAND en máximo por demanda de IA; se traslada a productos de consumo y a conflictos laborales en fabricantes.
- Estado actual: Omdia reporta ingresos de semiconductores de US$425.000 M en 2Q26 (+31,4% t/t), con memoria como más de la mitad; proyecta más de US$500.000 M en 3Q26. Valve fijó el Steam Frame en US$1.059/1.299 (2026-09-14) tras la Steam Machine a 1.049 en junio, culpando a la escasez de DRAM y almacenamiento. Micron ofreció bono de NT$1 M a empleados de Taiwán (2026-09-11 aprox.), sindicatos lo rechazaron; segunda mediación el 2026-09-21, con votación de huelga si falla. SK Hynix cerró acuerdo con su sindicato (2026-09-16, fuera de la ventana, no cubierto).
- Estado al ep 2 (2026-09-20): SK hynix cerró el conflicto sindical el 2026-09-16 (Bloomberg, vía barrido): 57% aprobó el convenio revisado, mitad del bono de utilidades en efectivo y mitad en acciones. Micron: segunda mediación en Taiwán sigue fijada para el 2026-09-21; resultados el 2026-09-30. Valve (Griffais vía IGN, 2026-09-14/15) dijo que los planes del Steam Deck 2 no cambian por la escasez y admitió que el precio de Steam Machine y Steam Frame probablemente afectó la demanda. Micron demostró RDIMM DDR5 de 512 GB (2026-09-15) con volumen en 2H 2027. Precios en Chile (Solotodo, 2026-09-20): kit 2x16 GB DDR5-6000 entre $629.990 y $649.990; módulo 16 GB DDR5-5600 $289.990. Demanda colectiva por precios de DRAM contra Samsung, SK hynix y Micron presentada el 2026-06-25 en California (hallada en barrido, fuera de ventana, no cubierta).
- Cubierto en: ep 1 (2026-09-14) como NOTICIA 4 — precio del Steam Frame como síntoma, datos de Omdia y conflicto de Micron en Taiwán.
- Cubierto en: ep 2 (2026-09-20) como DESARROLLO dentro de NOTICIA 1 (acuerdo sindical de SK hynix, mediación de Micron) y NOTICIA 3 (Steam Deck 2, precios de RAM en Chile, consejo de esperar los resultados de Micron del 30-09).
- Reabrir solo si: resultado de la mediación de Micron del 21-09 o huelga efectiva; resultados de Micron del 30-09 con guía de precios; informe de Omdia o TrendForce de 3Q26; cambio de tendencia en precios de DRAM/NAND; otro producto de consumo que suba o baje de precio por memoria; acuerdo o conflicto laboral en Samsung.
- Reabrir también si: novedad procesal en la demanda colectiva por precios de DRAM; precio del kit 2x16 GB DDR5-6000 en Chile baja de $550.000 o sube de $700.000.
- Estado al ep 3 (2026-09-24): la escasez se extiende a otros componentes. XMG (anuncio en Reddit, vía TechPowerUp 2026-09-23) sube notebooks desde el 2026-09-18: mayoría +100 a 150 euros, Schenker Key 18 Pro +300, upgrade RTX 5090 Laptop +120; atribuye a SO-DIMM DDR5 casi 6x vs mediados de 2025, más GPU, GDDR7, CPUs Intel/AMD de notebook, PCB y flete (Medio Oriente, Mar Rojo/Suez); advierte plazos largos y quiebres de stock; promete bajar si bajan costos. CEO de Acer, Jason Chen: PC +5 a 20% en 4Q26, precio promedio con techo a mediados de 2027 (citado por TechPowerUp). Microsoft Surface Laptop 13 y Surface Pro 12 con Snapdragon X2 Plus (2026-09-23) parten en US$1.199 y 1.149 vs 899 y 799 de la generación anterior (Tom's Hardware); Microsoft no atribuye el alza a la memoria (se dijo como especulación). Micron: la segunda mediación con el sindicato de Taoyuan del 2026-09-21 terminó sin acuerdo y el sindicato va a votación de huelga (Digitimes 2026-09-22, Reuters vía TradingView; hallado en barrido). Resultados de Micron siguen fijados para el 2026-09-30. Reporte de SE Daily (vía TechPowerUp 2026-09-21): Samsung pasaría de ~20.000 a ~50.000 obleas/mes de HBM4/HBM4E en 2027 y su cuota HBM de 15% (2Q25) a 33% (2Q26); descartado por filtro de rumores, no se usó. Precio de RAM en Chile no se pudo actualizar (Solotodo no entregó datos a WebFetch); se repitió el dato del 2026-09-20.
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 1 (DESARROLLO) — alzas de XMG y Surface, explicación de la competencia por obleas entre HBM y DDR5/GDDR7 (analogía de la panadería), mediación fallida de Micron, consejo de esperar resultados del 30-09.
- Reabrir también si: votación de huelga en Micron Taiwán o huelga efectiva; Samsung confirma o desmiente el aumento de capacidad HBM4; otra marca de PC publica alzas con desglose; subidas de precio de tarjetas de video atribuidas a GDDR7.

## HILO: ryzen-baratos-am4-am5
- Descripción: AMD lanza Ryzen 5 7500 (Zen 4 con iGPU RDNA 2 de 2 CU) y Ryzen 5 5500F (Zen 3 Vermeer, 16 MB L3, PCIe 4.0, sin iGPU) para AM5 y AM4.
- Estado actual: lanzados el 2026-09-10 sin anuncio; precios SEP confirmados el 2026-09-12: US$189 y US$99. 7500F se encuentra a US$130-140 en retail. Primer benchmark de tercero (RandomGaminginHD) da hasta 16% a favor del 5500F sobre el 5500 a 1080p; TechPowerUp pide esperar reviews. Sin listados en tiendas chilenas al 2026-09-14.
- Estado al ep 2 (2026-09-20): el mismo benchmark de RandomGaminginHD se replicó en Club386, TechPowerUp, VideoCardz y OC3D (2026-09-14/15); VideoCardz lo resume como 7% promedio. Sin reviews independientes. REPETIDA, no se tocó en el guion.
- Cubierto en: ep 1 (2026-09-14) como NOTICIA 3 — explicación Vermeer vs Cezanne, crítica al precio del 7500 frente al 7500F, conversión a pesos.
- Reabrir solo si: reviews independientes del 5500F (TechPowerUp, GN, HUB); precio del 7500 baja bajo el 7500F; aparecen en tiendas chilenas con precio; AMD lanza más SKUs AM4.

## HILO: nvidia-gb202-para-ia
- Descripción: NVIDIA reutiliza el die GB202 (RTX 5090) en tarjetas profesionales con más memoria y mayor margen.
- Estado actual: RTX PRO 5500 Blackwell anunciada el 2026-09-14 vía hoja de PNY: 21.760 CUDA, 84 GB GDDR7 clamshell (28 chips de 3 GB), ~1.398 GB/s, 600 W, MIG 1x84 o 2x42. Sin precio; se ubica entre RTX PRO 5000 (US$9.209) y RTX PRO 6000 (US$15.599). Contradicción abierta: bus de 416 bits (TechPowerUp) vs 448 bits (Tom's Hardware).
- Estado al ep 2 (2026-09-20): sin novedades en la ventana; la contradicción del bus sigue abierta.
- Cubierto en: ep 1 (2026-09-14) como NOTICIA 2 — se explicó clamshell, ancho de banda y la lógica de márgenes.
- Reabrir solo si: precio oficial; página oficial de NVIDIA que resuelva el bus; evidencia de que la 5090 se encarece o escasea por esto; nueva SKU con GB202.

## HILO: apple-ceo-ternus
- Descripción: John Ternus (ex SVP de ingeniería de hardware) es CEO de Apple desde el 2026-09-01; Tim Cook pasa a presidente ejecutivo del directorio. Anunciado el 2026-04-20.
- Estado actual: traspaso efectivo. Cook seguirá en relaciones con gobiernos. Sin anuncios de hardware atribuibles a Ternus todavía.
- Estado al ep 2 (2026-09-20): primer keynote de Ternus el 2026-09-09 (TechCrunch): posiciona el iPhone como "hub personal inteligente" reviviendo la idea del hub digital de Jobs (2001); sin hardware nuevo relevante en la crónica; rezagada, no cubierta. El 2026-09-16 The Information reportó que Apple evalúa volver a servidores en 2029 con M8 Ultra interconectados por NVIDIA NVLink Fusion (2 a 4 chips, NVLink-C2C die a die), recogido por Reuters y TechPowerUp; DESCARTADA por filtro de rumores (fuente anónima sin historial verificado = nivel C, sin reacción de Apple ni NVIDIA). Contexto relacionado: d-Matrix adoptó NVLink Fusion el 2026-09-10 (NVIDIA blog). Mac tuvo ventas récord de US$10.400 M el trimestre pasado según TechPowerUp citando a The Information.
- Cubierto en: ep 1 (2026-09-14) como NOTICIA 5 (rezagada, BARRIDO) — corta; se dijo que es buena señal que un ingeniero de hardware dirija Apple, sin especular más.
- Reabrir solo si: primer evento de producto bajo Ternus; cambios de organización o salidas de ejecutivos; resultados trimestrales con comentarios de Ternus; cambios en la estrategia de silicio (M-series, módem, fundición).
- Reabrir también si: Apple o NVIDIA confirman o desmienten el plan de servidores; aparece un leaker A o B con lo mismo; documentos (registros de importación, ofertas de trabajo) sobre hardware de servidor Apple.

## HILO: intel-skhynix-ohio
- Descripción: Reuters (2026-09-16, exclusiva con fuentes anónimas) reporta que SK hynix negocia con Intel producir memoria en EE.UU. por primera vez: arrendar parte de la fab de Intel en New Albany, Ohio, o un joint venture con Intel y una nube grande; se produciría DRAM, HBM y algo de NAND (TechPowerUp).
- Estado actual: nada firmado. SK hynix (newsroom, 2026-09-16) explora varias opciones pero "no hay nada finalizado" con ninguna empresa ni sobre producción en EE.UU.; Techzine (2026-09-18) lo tituló como desmentido. Intel no comenta especulaciones y sigue invirtiendo en Ohio. Contexto: SK hynix ya negó vía 6-K del 2026-07-22 conversaciones para comprar el campus de Ohio (reporte de Korea JoongAng Daily). Presión de EE.UU. (Lutnick, aranceles de hasta 100% a fabricantes de memoria sin producción local, según Korea JoongAng Daily) y revisión coreana bajo la ley de protección de tecnología industrial si involucra tecnología nacional estratégica; Seúl empuja un clúster local. SK hynix tiene planta de empaquetado en Indiana, sin fab de obleas en EE.UU. Mercado: Intel +4% (09-16) y +8% (09-17), SK hynix +3/+5%, Micron +6% (09-17), según titulares de 24/7 Wall St y Yahoo. Rumor relacionado: DigiTimes (2026-09-09) dice que Intel podría recortar otro 5-10% de plantilla; no confirmado. Solidigm (filial de SK hynix) planearía su primera fab de NAND en EE.UU. (TechPowerUp 2026-09-20, sin texto); SK hynix dijo vía 6-K del 2026-09-04 que Solidigm revisa medidas sin decidir nada.
- Cubierto en: ep 2 (2026-09-20) como NOTICIA 1 — se explicó la diferencia entre fab de lógica y fab de DRAM, los dos escenarios, la presión de ambos gobiernos, y la opinión de que el arriendo se firma pero no baja el precio de la RAM al consumidor.
- Reabrir solo si: anuncio oficial de arriendo, joint venture o desmentido formal; identidad de la nube en el JV; decisión del gobierno coreano; anuncio de aranceles a memoria; Intel confirma o desmiente recortes; Solidigm confirma fab de NAND; cambio material en el calendario de Ohio.
- Estado al ep 3 (2026-09-24): sin novedades oficiales. KRON4 (2026-09-23, un medio local, solo titular) reporta que Intel despidió a "decenas" de personas en la Bahía de San Francisco; no alcanza para confirmar el rumor de DigiTimes de 5 a 10%. REPETIDA, no se tocó.

## HILO: qualcomm-amazon-silicio
- Descripción: Qualcomm anuncia (2026-09-08) colaboración multigeneracional con Amazon para silicio a medida de inferencia en AWS y conectividad óptica hasta 1,6T (SerDes y DSP óptico); Qualcomm usará más AWS (Bedrock) para EDA. CNBC y Reuters reportan que Qualcomm entregó a Amazon warrants por unos US$4.000 M en acciones. JPR y TIKR hablan de un acuerdo de hasta US$60.000 M (no verificado).
- Estado actual: confirmado por Qualcomm (comunicado); warrants según prensa; condiciones de los warrants (precio de ejercicio, plazos, hitos) desconocidas; cifra de 60.000 M sin fuente primaria.
- Cubierto en: ep 2 (2026-09-20) como NOTICIA 2 (rezagada) — se explicó qué es un warrant, el ángulo de conectividad óptica, y la lectura de Qualcomm buscando cliente ancla fuera del celular.
- Reabrir solo si: aparecen los términos de los warrants (8-K o similar); primer chip o rack anunciado; Amazon ejerce los warrants; cifra de 60.000 M confirmada o desmentida; Qualcomm anuncia acuerdos similares con otra nube.
- Estado al ep 3 (2026-09-24): sin novedades del acuerdo con Amazon. Se mencionó como antecedente de la diversificación de Qualcomm en la nota de PickNik (ver hilo qualcomm-picknik).

## HILO: intel-bug-bounty
- Descripción: Intel suspendió su programa de recompensas por vulnerabilidades en Intigriti (US$500 a 100.000; abierto desde 2018; 105 de 231 CVE de 2020 llegaron por ahí) y lanzó un programa de divulgación responsable sin recompensas. Detectado por Phoronix el 2026-09-18, confirmado por Tom's Hardware, Notebookcheck y TechPowerUp.
- Estado actual: sin explicación de Intel. Hipótesis de Phoronix y Tom's: avalancha de reportes generados con IA (kernel Linux cerca de 2.000 CVE por versión; curl cerró su bounty; HackerOne IBB pausó postulaciones en marzo). La página de AMD en Intigriti también aparece suspendida, pero la plataforma tiene autosuspensión; sin confirmar. Antecedente: disputa de pago con un investigador en junio (Tom's).
- Cubierto en: ep 2 (2026-09-20) como NOTICIA 4 — se explicó qué es un bug bounty, las cifras, la hipótesis de IA y la opinión de que Intel resuelve el problema equivocado.
- Reabrir solo si: Intel explica o restaura las recompensas; AMD confirma suspensión; otro fabricante de hardware corta su bounty; vulnerabilidad grave de Intel publicada sin coordinación atribuible al cambio.

## HILO: datacenters-chile
- Descripción: inversión en centros de datos en Chile y sus conflictos por agua, energía y permisos.
- Estado actual (2026-09-20, solo titulares, sin texto): OLCA acusa ilegalidad en la petición de Google para revivir el data center de Cerrillos (DPL News y Olca.cl, 2026-09-16); Google buscaba reactivar el proyecto de US$200 M (Logística 360, 2026-09-07); OLCA y MOSACAT exigían evaluación ambiental (Pressenza, 2026-09-08). Metlen Energy & Metals solicitó conexión a la red para un centro de datos de 100 MW en Chile (BNamericas, 2026-09-16). Grenergy busca construir un data center en Polpaico por US$25 M (La Tercera, 2026-09-17). Contexto internacional: alianza AEMA de NVIDIA, Google y Emerald AI para data centers flexibles con la red (2026-09-16).
- Cubierto en: ep 2 (2026-09-20) en el bloque CHILE — los tres hechos en titular más la conexión con AEMA.
- Reabrir solo si: decisión administrativa o judicial sobre Cerrillos; Metlen o Grenergy obtienen permisos, RCA o conexión; nuevo proyecto sobre 50 MW; norma o guía chilena sobre flexibilidad eléctrica o uso de agua de data centers.
- Estado al ep 3 (2026-09-24, solo titulares): la industria proyecta 367,8 MW de capacidad nueva hasta 2031 (Data Center Dynamics, 2026-09-23) e inversiones por US$1.616 millones a 2031 (ADN, 2026-09-22); PwC proyecta US$136.000 millones acumulados entre 2026 y 2050 (Redimin, 2026-09-24). Sin novedades de Cerrillos, Metlen ni Grenergy.
- Cubierto en: ep 3 (2026-09-24) en el bloque CHILE como DESARROLLO — cifras de proyección, con la advertencia de que no son proyectos aprobados y la pregunta por energía y agua (conectado con el rack Vera Rubin de la NOTICIA 4).
- Reabrir también si: se publica el estudio completo con la lista de proyectos detrás de los 367,8 MW.

## HILO: ley-21719-datos
- Descripción: ley 21.719 de protección de datos personales y su entrada en vigencia.
- Estado actual (2026-09-20, solo titulares): hay una postergación en curso: "Prórroga a ley de protección de datos personales" (La Tercera, 2026-09-08), "Postergación de la ley" (elobservatodo, 2026-09-07), "Los riesgos ocultos de su postergación" (Mundo en Línea, 2026-09-16), "postergan hasta 2027" (El Ecosistema Startup, 2026-09-19). Encuestas: 72% de empresas no preparadas (G5noticias, 2026-09-12). No se pudo verificar el estado del trámite ni la nueva fecha.
- Cubierto en: ep 2 (2026-09-20) en el bloque CHILE — mención en titular con advertencia de que no se verificó el detalle.
- Reabrir solo si: publicación en el Diario Oficial o votación fechada de la prórroga con la nueva fecha; reglamento o instrucción de la Agencia de Protección de Datos; primera sanción.
- Estado al ep 3 (2026-09-24): sin novedad fechada en la ventana en candidatas.json. REPETIDA, no se tocó.

## HILO: snapdragon-8-elite-gen6
- Descripción: Qualcomm presenta el Snapdragon 8 Elite Gen 6 y el 8 Elite Extreme Gen 6 en el Snapdragon Summit (2026-09-22).
- Estado actual: confirmado por Qualcomm (comunicado vía TechPowerUp): agentes de IA en el dispositivo, Adreno Neural Fusion (IA para gráficos en juegos), soporte de video APV, Intelligent Pixel Control; OEMs: Honor, iQOO, Motorola, OnePlus, Oppo, Redmi, RedMagic, vivo, Xiaomi. Según titulares: primeros chips de 2 nm que pasan los 5 GHz (Notebookcheck), CPUs Oryon a 5 GHz (VideoCardz), TSMC fabrica todos los Gen 6 (The Elec). Acción de Qualcomm bajó levemente tras el anuncio (Yahoo Finance). Sin precios, sin tabla de especificaciones verificada (artículos sin texto o con 403).
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 2 — se explicó que "2 nm" es nombre comercial, se dudó de los 5 GHz sostenidos en un celular sin ventilador y se leyó la estrategia de dos topes de línea como segmentación de precio.
- Reabrir solo si: reviews independientes con rendimiento sostenido y temperaturas; especificaciones completas verificadas; primer celular con precio en Chile; problemas de rendimiento o de suministro de N2.

## HILO: radeon-rx-9050
- Descripción: AMD Radeon RX 9050 con versiones de 4 GB y 8 GB; la de 4 GB criticada en pruebas independientes. Contexto: AMD prepara GDDR7 para RDNA 5.
- Estado actual: solo titulares. OC3D (2026-09-18) "¿es terrible?"; VideoCardz (2026-09-19) la de 8 GB es 37% más rápida en promedio de 18 juegos; Club386 (2026-09-21) rendimiento pobre por memoria recortada; TechSpot (2026-09-22) "es una estafa". Especificaciones y precio no verificados. AMD agregó GDDR7 a los tipos de VRAM del driver AMDGPU (TechPowerUp 2026-09-22): GDDR6 llega a 20 Gb/s, GDDR7 a 36 Gb/s hoy y hasta 48 según JEDEC; RDNA 5 a meses; DCN 6 para RDNA 5.
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 3 — explicación de qué pasa cuando se acaba la VRAM (desborde a RAM por PCIe, analogía de la despensa en otro edificio), crítica a usar el mismo nombre para 4 y 8 GB, consejo de mirar los gigas en tiendas chilenas; GDDR7 como contraste.
- Reabrir solo si: precio o disponibilidad de la RX 9050 en Chile; AMD cambia el nombre o retira la versión de 4 GB; anuncio oficial de RDNA 5 o de tarjetas con GDDR7 de AMD.

## HILO: nvidia-vera-rubin
- Descripción: despliegue de los racks NVIDIA Vera Rubin NVL72.
- Estado actual: Supermicro despacha racks Vera Rubin NVL72 (comunicado vía TechPowerUp, 2026-09-23): 72 GPUs Rubin y 36 CPUs Vera en 18 bandejas 1U (4 GPU + 2 CPU cada una), 9 bandejas de switches NVLink de sexta generación con 216 TB/s, 20,7 TB de HBM4 y hasta 54 TB de LPDDR5X por rack; refrigeración líquida directa DLC-2, CDU en fila de 1,8 MW con redundancia N+1. Sin precio.
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 4 — se conectó la HBM4 por rack con la escasez de la NOTICIA 1, se explicó la cadena de enfriamiento líquido y se opinó que la ventaja de Supermicro es la "gasfitería".
- Reabrir solo si: primeros racks Vera Rubin en Latinoamérica o Chile; problemas de despliegue o de enfriamiento reportados; precio público; otro integrador (Dell, HPE) con cifras de volumen.

## HILO: qualcomm-linux-x2
- Descripción: Qualcomm lleva soporte de Linux de primera clase a los notebooks Snapdragon X2.
- Estado actual: preview para desarrolladores mostrada en el Snapdragon Summit (2026-09-23): kernel propio + Debian 13 (Phoronix); gran parte upstream; trabajo pendiente en NPU Hexagon, Adreno en Mesa (Freedreno, Turnip, Rusticl), energía, temperaturas y estabilidad; etapa a terminar en noviembre (TechPowerUp); HP, ASUS y HUMAIN planean soporte de Linux en 1H 2027 (blog de Qualcomm citado por Phoronix). Phoronix no comprará equipos para pruebas por los precios del hardware.
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 5 — se explicó por qué importa el upstream y se aconsejó a Qualcomm mandar equipos a quienes prueban Linux.
- Reabrir solo si: primer notebook X2 vendido con Linux preinstalado; benchmarks de X2 en Linux contra AMD e Intel; fin de la etapa de noviembre con anuncio; retrasos del soporte de HP o ASUS.

## HILO: qualcomm-picknik
- Descripción: Qualcomm anuncia la compra de PickNik (robótica) el 2026-09-23 y promete mantener MoveIt como open source.
- Estado actual: confirmado por Qualcomm (comunicado; solo titular) y The Robot Report (titular). Sin monto ni fecha de cierre conocidos. Contexto: el 2026-09-24 Qualcomm renovó su licencia global de patentes con Apple (comunicado, Reuters, MacRumors, etc.); Traders Union dice que la extensión rige desde abril del próximo año (no verificado); la acción bajó (Seeking Alpha); el CFO pidió mirar más allá del acuerdo con Apple (TheStreet, titular).
- Cubierto en: ep 3 (2026-09-24) como NOTICIA 6 (evento mayor obligatorio) — corta; se leyó como diversificación fuera del celular (junto a Amazon) y se comparó con la promesa de NVIDIA sobre Hugging Face; consejo de comprometer por escrito el equipo de MoveIt.
- Reabrir solo si: monto o cierre de la operación; cambios en licencia, gobernanza o equipo de MoveIt; primer producto de robótica de Qualcomm con PickNik; términos de la licencia con Apple (duración, montos).

## HILO: subtel-bloqueo-apuestas
- Descripción: bloqueo por DNS de sitios de apuestas online en Chile, ordenado por la Corte Suprema y la Corte de Apelaciones de Santiago y ejecutado vía Subtel.
- Estado actual: el 2026-09-21 Subtel ofició a Entel, Movistar, Claro, GTD, WOM y VTR para bloquear 37 dominios, subdominios o espejos (Betano, Betsson, Bet365, 1xbet, Betway, Betfair, entre otros) en 48 horas; nómina validada por la Superintendencia de Casinos de Juego; la Lotería de Concepción o el tercero coadyuvante identifica dominios; las ISP acreditan ante la Corte y avisan a Subtel con fecha y hora; el procedimiento es sucesivo con mecanismos de corrección ante sobrebloqueo. aPAL dice que se excede del fallo y que no se puede resolver dominio por dominio (24horas, ADN). Cobertura de decenas de medios.
- Cubierto en: ep 3 (2026-09-24) en el bloque CHILE — se explicó cómo funciona un bloqueo por DNS y lo fácil que es saltarlo cambiando de resolvedor; opinión de que es el gato y el ratón.
- Reabrir solo si: la Corte cambia el mecanismo (IP, SNI u otro); un bloqueo afecta servicios lícitos; se aprueba la ley de apuestas en línea; Subtel publica cifras de efectividad.

## HILO: conectividad-rural-nuble
- Descripción: brecha de conectividad rural en Ñuble y cumplimiento de las contraprestaciones del concurso 5G.
- Estado actual: el 2026-09-23 Subtel presentó en Ninhue (segunda Mesa de Conectividad Rural del Valle del Itata) una fiscalización de 41 puntos (31 en Itata, 10 en otros sectores) con servicios caídos o deficientes; 31 localidades son contraprestaciones obligatorias del concurso 5G rural; se evaluarán cargos u oficios; acceso deteriorado al Cerro Cayumanque. El 2026-09-22 partió la primera etapa del proyecto Fibra Óptica Última Milla: ~700 km de fibra troncal, 56 localidades de 16 comunas, más de $4.700 millones del Gobierno Regional, ejecuta Copelec; conectividad fija rural en Ñuble de 16% según Subtel.
- Cubierto en: ep 3 (2026-09-24) en el bloque CHILE — mención de ambos hechos.
- Reabrir solo si: Subtel formula cargos o multa a una operadora; avance fechado de Última Milla; nuevas fiscalizaciones de contraprestaciones 5G en otras regiones.

## Noticias puntuales

- ep 1 (2026-09-14): Linux parcha bug de una línea de pérdida silenciosa de datos (THP + límite de cgroup + MADV_FREE), presente desde julio de 2023 / kernel 6.6; usuarios de Polars lo sufrieron en producción; marcado para stable. Como NOTICIA 6.
- ep 1 (2026-09-14): rama de Arnd Bergmann borra ~247k líneas de drivers para plataformas ARM 32-bit obsoletas, apuntando a Linux 7.4 o 7.5. Mención en NOTICIA 6.
- ep 1 (2026-09-14): Rustls 0.23.45 corrige aceptación de mensajes de handshake TLS 1.3 en nivel de cifrado equivocado, presente desde 0.23.13 (sept 2024). Mención en NOTICIA 6.
- ep 1 (2026-09-14): RX 9070 XT pasa a ser la Radeon más usada en la encuesta de hardware de Steam (TweakTown, OC3D, TechPowerUp, 2026-09-08). Mención de una línea en NOTICIA 3.
- ep 2 (2026-09-20): Micron demuestra el primer RDIMM DDR5 de 512 GB: dies apilados con TSV, hasta 9.200 MT/s, 12 TB en servidor de 2 sockets y 24 ranuras, más de 60% menos energía que 4x128 GB, 1,4x en Spark SVM vs 256 GB; AMD e Intel validando; volumen en 2H 2027; sin precio (Micron, 2026-09-15). Como NOTICIA 3.
- ep 2 (2026-09-20): Micron nombra a Deirdre Hanford (37 años en Synopsys, ex CSO) presidenta de Micron Research Labs, centro anunciado en agosto de 2026 con US$10.000 M a diez años, sede en Boise (Micron, 2026-09-15). Mención en NOTICIA 3.
- ep 2 (2026-09-20): Mojo 1.1 y MAX 26.6 (Modular, 2026-09-17, Phoronix): referencias a miembros inferidas, compilación más rápida, SIMD estable, compilador abierto a contribuciones de la comunidad; MAX con generación de audio MiniMax-Music3 y kernels más rápidos en AMD y NVIDIA. Como NOTICIA 5.
- ep 2 (2026-09-20): Subtel instruye a operadoras reforzar redes para Fiestas Patrias (nodos troncales, autonomía energética, SAE, RAN-E) y campaña "Este 18, cuídate" con ChileTelcos (Subtel, 2026-09-16). Una línea en CHILE.
- ep 2 (2026-09-20): cable submarino Arica-Puerto Montt usado para detectar sismos (Megatiempo, 2026-09-19, solo titular). Una línea en CHILE.
- ep 2 (2026-09-20): estudio dirigido por la UDP confirma el exoplaneta más joven conocido, Elias 2-24 b, gigante gaseoso de menos de un millón de años (Merca2 2026-09-17, Megatiempo 2026-09-18, El Espectador, mascolombia; solo titulares). En CHILE.
- ep 2 (2026-09-20): USM se adjudica cuatro proyectos VIU 2026 de ANID, cuarta a nivel nacional; UNTA-Tech (Allison Lizana, Ing. Ejecución Industrial) puntaje más alto del concurso; otros: BeeKing, bioplástico PHB desde PET, dispositivo para rizartrosis (USM, 2026-09-16). En CHILE.
- ep 2 (2026-09-20): Daniel San Martín (Doctorado en Ing. Informática USM, profesor guía Claudio Torres) gana el primer lugar del concurso latinoamericano de tesis doctorales CLEI 2026 (ceremonia 2026-09-11, ITAM, Ciudad de México) con un modelo simplificado de interacción atmósfera-incendio implementado en CPU y GPU (Informática USM, 2026-09-16). Como contexto fechado en CHILE.
- ep 3 (2026-09-24): Sonda concreta la compra del negocio de distribución de productos Apple de Yáneken Retail por casi US$6 millones para ampliar MacOnline (Diario Financiero y La Tercera, 2026-09-21; solo titulares). Una línea en CHILE.
- ep 3 (2026-09-24): Qualcomm renueva su licencia global de patentes con Apple (comunicado de Qualcomm y Reuters, 2026-09-24). Mención de pasada en NOTICIA 6. Ver hilo qualcomm-picknik.

## Rumores usados en el guion

- ep 1 (2026-09-14): ninguno. No se usó ningún rumor de leaker. El benchmark del 5500F es una prueba de tercero, no una filtración, y se presentó con advertencia.
- ep 2 (2026-09-20): Reuters (fuentes anónimas, 2026-09-16): SK hynix negocia con Intel arriendo de la fab de Ohio o JV con una nube para producir memoria en EE.UU. Usado en NOTICIA 1 con estatus explícito de reporte no confirmado, apoyado en la declaración oficial de SK hynix. Resultado: PENDIENTE.
- ep 2 (2026-09-20): DigiTimes (fuentes de cadena de suministro, 2026-09-09): Intel recortaría otro 5-10% de plantilla. Mención de pasada en NOTICIA 1 con advertencia. Resultado: PENDIENTE.
- ep 2 (2026-09-20): JPR y TIKR: acuerdo Qualcomm-Amazon de hasta US$60.000 M. Mención en NOTICIA 2 marcada como cifra no verificada. Resultado: PENDIENTE.
- ep 3 (2026-09-24): ningún rumor de leaker. Traders Union (agregador de baja calidad, 2026-09-24): la extensión de la licencia Qualcomm-Apple correría desde abril del próximo año. Mención de pasada en NOTICIA 6 marcada como no verificada y con advertencia sobre la fuente. Resultado: PENDIENTE.
- ep 3 (2026-09-24): la mediación fallida de Micron (Digitimes y Reuters, 2026-09-21/22) se trató como hecho reportado por prensa, no como rumor; la votación de huelga está anunciada, no realizada. Resultado de la votación: PENDIENTE.
- ep 2 (2026-09-20), actualización al ep 3: rumor de DigiTimes sobre recortes de 5-10% en Intel sigue PENDIENTE; el reporte de KRON4 (2026-09-23) sobre "decenas" de despidos en la Bahía no lo confirma ni lo desmiente.

## Descartadas relevantes (para no repetir la evaluación)

- ep 1: caída de acciones de NVIDIA/AMD/semis del 2026-09-14 ligada a un "debate sobre el ritmo de la IA" y a declaraciones de Trump y Jensen Huang sobre seguridad de IA. Descartada por falta de texto verificable, no por irrelevancia. Si vuelve con texto, evaluar.
- ep 1: AMD ESMTP (Enhanced SMT Protection) para EPYC en Linux, Phoronix 2026-09-14. Puntaje 5, quedó fuera por espacio. Reabrir si se confirma como feature de EPYC 9006 "Venice".
- ep 1: CUDA sobre AMD en Windows vía ZLUDA + HIP (Tom's Hardware 2026-09-14). Puntaje 5, categoría ocupada.
- ep 2: Apple servidores con NVLink Fusion (The Information, 2026-09-16). Descartada por filtro de rumores (nivel C). Ver hilo apple-ceo-ternus.
- ep 2: Jensen Huang prevé duplicar ventas de chips en 2027 (Bloomberg Línea, infobae, 2026-09-17). Puntaje 8 pero solo titulares, sin contexto del evento. Si aparece con texto, evaluar.
- ep 2: alianza AEMA (NVIDIA, Google, Emerald AI, 2026-09-16). Puntaje 7, categoría datacenter ocupada; se usó como contexto en Chile. Reabrir si publican requisitos técnicos o si un operador chileno adhiere.
- ep 2: Arm CSS for Mobile 2 (C2-Ultra con SME2, Mali G2-Ultra NX con aceleradores neuronales, 2026-09-08). Rezagada. Reabrir con el primer SoC comercial (vivo anunciado como socio).
- ep 2: TSMC ingresos récord de agosto NT$514.810 M, +53,3% a/a (2026-09-10). Rezagada, reporte mensual. N2 al 3% de ingresos en 2Q; meta de 100.000 obleas N2/mes a fin de 2026 (TechPowerUp).
- ep 2: ASML y TSMC, fotomáscaras de gran formato para High-NA EUV (2026-09-08). Rezagada. Reabrir con detalles técnicos o fecha de adopción.
- ep 2: Samsung lidera Serie D de Mistral y usa Mistral Large on-premises en sus fabs (2026-09-08/09). Rezagada.
- ep 2: GMKtec EVO-X5 Pro con Ryzen AI Max (IFA 2026, 2026-09-18). Solo comunicado sindicado, sin especificaciones verificables. Reabrir con review o precio.
- ep 2: Solidigm planearía primera fab de NAND en EE.UU. (TechPowerUp, 2026-09-20). Un medio, sin texto. Ver hilo intel-skhynix-ohio.
- ep 2: Windows 11 KB5124008/KB5126052 rompiendo PCs AMD (Neowin, 2026-09-13). Rezagada, sin texto. Reabrir si Microsoft o AMD confirman.
- ep 2: Apple M5 Ultra en Geekbench 7, 35% sobre M3 Ultra (Mezha, newsd.in, 2026-09-16). Fuentes de baja calidad, sin texto.
- ep 2: Android 17 agrega APIs sin publicarlas en AOSP (HN 1157, 2026-09-18) y TVs LG grabando audio con pantalla apagada (HN 1201, 2026-09-07). Sin artículo de medio. Reabrir si aparecen con cobertura.
- ep 2: SK hynix Ventures (CVC, 2026-09-18). Menor.
- ep 2: Corfo Valparaíso $247 M para cinco eventos de innovación (G5noticias, 2026-09-16). Cortada por espacio en Chile.
- ep 2: "Eliminan obligación de nombrar delegados de datos personales" (La Prensa Gráfica, 2026-09-17) es de El Salvador; falso positivo de es_chile.
- ep 3: Samsung duplicaría capacidad de HBM4/HBM4E en 2027 (SE Daily vía TechPowerUp, 2026-09-21; HN 560). Descartada por filtro de rumores (reporte sin reacción oficial, nivel C). Reabrir si Samsung lo confirma o si hay datos de proveedores de glass carriers.
- ep 3: AMD llega a US$1 billón de capitalización (CNBC, Quartz, Barron's, 2026-09-21), rally atribuido al agente Muse de Meta. Puntaje 7, reclasificada como industria (bursátil); categoría ocupada por el evento mayor PickNik. Sin texto.
- ep 3: Samsung inicia planta de equipos HVAC para enfriamiento de datacenters en Gwangju (Korea Herald, Korea Times, 2026-09-20/21; 240 mil millones de wones, producción masiva hacia 2028 según biggo). Puntaje 6, categoría datacenter ocupada por Vera Rubin.
- ep 3: Synopsys-TSMC y Siemens-TSMC, IA para diseño de chips (2026-09-23). Sin detalle técnico. Reabrir si hay nodos o flujos concretos.
- ep 3: OpenAI dice que un agente "infiltró" un sitio del gobierno australiano sin instrucción (The Register, BBC, CNBC, 2026-09-23/24). Fuera del foco hardware. Reabrir si deriva en regulación de agentes que afecte a Chile.
- ep 3: GPT-6 Sol/Luna (HN 1771) y cookie __obi de ChatGPT (HN 763). Software de IA y privacidad web; un medio cada una.
- ep 3: Intel despide "decenas" en la Bahía (KRON4, 2026-09-23). El código lo marcó evento mayor por "layoffs"; no son despidos masivos.
- ep 3: falsos positivos del código: Durabook Z14I-DX3 y Musk/SpaceX marcados evento_mayor; Sonda-Yáneken marcado como evento mayor de Apple (el comprador es Sonda); Molino Grollmus, reforma política, Escudo de las Américas, obituarios y tenis de mesa marcados es_chile sin ser tecnología.
- ep 3: U. de Chile se adjudica cuatro proyectos VIU 2026 (2026-09-22). Menor; mismo concurso ya cubierto con la USM en ep 2.

## Hilos inactivos

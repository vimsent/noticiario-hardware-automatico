# Historial del noticiario

Dos episodios publicados. El ep 1 fue el primero (sin episodios anteriores).

## Episodios

- ep 1 (2026-09-14): ventana 2026-09-08 a 2026-09-14. Noticia 1: NVIDIA compra Hugging Face. Secundarias: RTX PRO 5500, Ryzen 5 7500/5500F, Steam Frame y crisis de memoria, CEO de Apple (barrido), bug de Linux. Bloque Chile vacío por falta de candidatas.
- ep 2 (2026-09-20): ventana 2026-09-14 a 2026-09-20. Noticia 1: SK hynix en conversaciones con Intel para fabricar memoria en Ohio. Secundarias: Qualcomm-Amazon con warrants (rezagada del 09-08), Micron RDIMM DDR5 de 512 GB, Intel suspende su bug bounty, Mojo 1.1. Bloque Chile: data centers (Cerrillos/OLCA, Metlen 100 MW, Grenergy Polpaico), postergación ley 21.719 (en titular), Subtel Fiestas Patrias, cable submarino sismos, exoplaneta Elias 2-24 b (UDP), USM VIU 2026 y tesis CLEI de Daniel San Martín (contexto, 09-11).

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

## HILO: qualcomm-amazon-silicio
- Descripción: Qualcomm anuncia (2026-09-08) colaboración multigeneracional con Amazon para silicio a medida de inferencia en AWS y conectividad óptica hasta 1,6T (SerDes y DSP óptico); Qualcomm usará más AWS (Bedrock) para EDA. CNBC y Reuters reportan que Qualcomm entregó a Amazon warrants por unos US$4.000 M en acciones. JPR y TIKR hablan de un acuerdo de hasta US$60.000 M (no verificado).
- Estado actual: confirmado por Qualcomm (comunicado); warrants según prensa; condiciones de los warrants (precio de ejercicio, plazos, hitos) desconocidas; cifra de 60.000 M sin fuente primaria.
- Cubierto en: ep 2 (2026-09-20) como NOTICIA 2 (rezagada) — se explicó qué es un warrant, el ángulo de conectividad óptica, y la lectura de Qualcomm buscando cliente ancla fuera del celular.
- Reabrir solo si: aparecen los términos de los warrants (8-K o similar); primer chip o rack anunciado; Amazon ejerce los warrants; cifra de 60.000 M confirmada o desmentida; Qualcomm anuncia acuerdos similares con otra nube.

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

## HILO: ley-21719-datos
- Descripción: ley 21.719 de protección de datos personales y su entrada en vigencia.
- Estado actual (2026-09-20, solo titulares): hay una postergación en curso: "Prórroga a ley de protección de datos personales" (La Tercera, 2026-09-08), "Postergación de la ley" (elobservatodo, 2026-09-07), "Los riesgos ocultos de su postergación" (Mundo en Línea, 2026-09-16), "postergan hasta 2027" (El Ecosistema Startup, 2026-09-19). Encuestas: 72% de empresas no preparadas (G5noticias, 2026-09-12). No se pudo verificar el estado del trámite ni la nueva fecha.
- Cubierto en: ep 2 (2026-09-20) en el bloque CHILE — mención en titular con advertencia de que no se verificó el detalle.
- Reabrir solo si: publicación en el Diario Oficial o votación fechada de la prórroga con la nueva fecha; reglamento o instrucción de la Agencia de Protección de Datos; primera sanción.

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

## Rumores usados en el guion

- ep 1 (2026-09-14): ninguno. No se usó ningún rumor de leaker. El benchmark del 5500F es una prueba de tercero, no una filtración, y se presentó con advertencia.
- ep 2 (2026-09-20): Reuters (fuentes anónimas, 2026-09-16): SK hynix negocia con Intel arriendo de la fab de Ohio o JV con una nube para producir memoria en EE.UU. Usado en NOTICIA 1 con estatus explícito de reporte no confirmado, apoyado en la declaración oficial de SK hynix. Resultado: PENDIENTE.
- ep 2 (2026-09-20): DigiTimes (fuentes de cadena de suministro, 2026-09-09): Intel recortaría otro 5-10% de plantilla. Mención de pasada en NOTICIA 1 con advertencia. Resultado: PENDIENTE.
- ep 2 (2026-09-20): JPR y TIKR: acuerdo Qualcomm-Amazon de hasta US$60.000 M. Mención en NOTICIA 2 marcada como cifra no verificada. Resultado: PENDIENTE.

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

## Hilos inactivos

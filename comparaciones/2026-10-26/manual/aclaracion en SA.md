En SA los números aleatorios se usan para dos cosas distintas. La clave es saber cuándo se gasta un número y cuándo no.

Las 3 reglas

1. Los números se usan en orden, uno tras otro, sin saltarse ninguno.
Es como una fila: cada vez que el algoritmo necesita "tirar un dado", toma el siguiente número y lo tacha. Nunca se vuelve atrás.

2. El primer uso es elegir el vecino (la ruleta).
Si tu movimiento genera $n$ vecinos, el intervalo $[0,1)$ se divide en $n$ partes iguales y cada parte corresponde a un movimiento. Con 4 movimientos:

| Aleatorio $u$ | Movimiento |
|:---:|:---:|
| $[0;\ 0{,}25)$ | $m_1$ |
| $[0{,}25;\ 0{,}5)$ | $m_2$ |
| $[0{,}5;\ 0{,}75)$ | $m_3$ |
| $[0{,}75;\ 1)$ | $m_4$ |

Es lo mismo que calcular $k=\lfloor n\cdot u\rfloor+1$. Por ejemplo, $u=0{,}70$ da $\lfloor 4\cdot0{,}70\rfloor+1=\lfloor2{,}8\rfloor+1=3$, o sea $m_3$.
Esta tabla tienes que escribirla en el diseño. Sin ella, el corrector no puede seguir tu ejecución.

3. El segundo uso es decidir si aceptas, y solo se hace cuando el vecino es peor.
- Si el vecino mejora o empata ($\Delta\ge0$), se acepta directamente y no se gasta otro número.
- Si el vecino es peor ($\Delta<0$), se toma el siguiente número $r$ y se compara con $e^{\Delta/T}$:
  - si $r<e^{\Delta/T}$, se acepta aunque sea peor;
  - si $r\ge e^{\Delta/T}$, se rechaza y te quedas donde estabas.

Por esto, una iteración gasta 1 o 2 números, según si el vecino mejoró o no. El error más común es gastar siempre dos: eso desfasa toda la secuencia desde ese punto y se pierden los puntos del resto de la tabla.

Sobre el signo de $\Delta$: defínelo para que negativo signifique "peor". Así $e^{\Delta/T}$ queda entre 0 y 1 y se puede comparar con el aleatorio.
- Al minimizar: $\Delta=f(s_{actual})-f(s_{vecino})$.
- Al maximizar: $\Delta=f(s_{vecino})-f(s_{actual})$.

Ejemplo: Don Segundo (C2 2023, con pauta)

Datos del problema:
- Ruta del bus: casa → 4 niños → colegio. Se minimiza la distancia.
- Representación: el orden de los niños, por ejemplo AFGM.
- Movimiento: intercambiar dos posiciones contiguas, con 4 vecinos: $m_1=(p_1,p_2)$, $m_2=(p_2,p_3)$, $m_3=(p_3,p_4)$ y $m_4=(p_4,p_1)$.
- La ruleta es la tabla de arriba.
- $T_0=10$, y baja 2 unidades cada dos iteraciones: 10, 10, 8, 8, 6.
- Solución inicial: AFGM con $f=48$.
- Aleatorios: 0.12, 0.70, 0.09, 0.31, 0.88, 0.52, 0.54, 0.16, …

Voy tachando los números a medida que se usan:

Iteración 1 ($T=10$, actual AFGM = 48)
- Tomo 0.12, que cae en $[0;0{,}25)$, así que aplico $m_1$: intercambio las posiciones 1 y 2. AFGM → FAGM.
- Evalúo: $d(DS,F)+d(F,A)+d(A,G)+d(G,M)+d(M,Col)=10+12+8+7+5=42$.
- $\Delta=48-42=+6$, mejora: acepto sin gastar otro número.
- Mejor solución: FAGM (42).

Iteración 2 ($T=10$, actual FAGM = 42)
- Tomo 0.70, que cae en $[0{,}5;0{,}75)$, así que aplico $m_3$: intercambio las posiciones 3 y 4. FAGM → FAMG = $10+12+4+7+15=48$.
- $\Delta=42-48=-6$, empeora: gasto el siguiente número, que es 0.09.
- $e^{-6/10}=0{,}549$. Como $0{,}09<0{,}549$, acepto aunque sea peor. Actual: FAMG (48).
- Mejor solución: sigue siendo FAGM (42).

Iteración 3 ($T=8$, porque ya pasaron dos iteraciones; actual FAMG = 48)
- Tomo 0.31, que cae en $[0{,}25;0{,}5)$, así que aplico $m_2$: FAMG → FMAG = $10+13+4+8+15=50$.
- $\Delta=48-50=-2$, empeora: gasto 0.88.
- $e^{-2/8}=0{,}779$. Como $0{,}88>0{,}779$, rechazo. Me quedo en FAMG (48).

Iteración 4 ($T=8$, actual FAMG = 48)
- Tomo 0.52, que da $m_3$: FAMG → FAGM = 42.
- $\Delta=+6$, mejora: acepto sin gastar otro número.

Iteración 5 ($T=6$, actual FAGM = 42)
- Tomo 0.54, que da $m_3$: FAGM → FAMG = 48.
- $\Delta=-6$, empeora: gasto 0.16.
- $e^{-6/6}=0{,}368$. Como $0{,}16<0{,}368$, acepto.

Conteo de números usados: 1 + 2 + 2 + 1 + 2 = 8 números en 5 iteraciones. Las iteraciones 1 y 4 gastaron uno solo porque el vecino mejoraba. Si en la iteración 1 hubieras gastado también el 0.70, la iteración 2 habría usado el 0.09, que da $m_1$, y toda la tabla habría salido distinta.

Lo que conviene escribir en cada fila

Para cada iteración, la rúbrica da puntos por tres cosas: la evaluación correcta, el movimiento elegido con el aleatorio y la decisión.
- En "Movimiento aplicado", escribe el aleatorio y el movimiento: 0.70 → m3.
- En "Decisión", escribe la comparación completa: 0,09 < 0,549 → acepta.

Casos borde

- Si $\Delta=0$ (empate): se acepta sin gastar número, porque $e^0=1$ y todo aleatorio es menor que 1.
- Si el enunciado no da la ruleta o $T_0$: los inventas y los declaras en el diseño. Por ejemplo, Don Segundo no daba $T_0$ y la pauta eligió 10.
- Si el enunciado dice "baja la temperatura cada 2 iteraciones": cámbiala solo cuando corresponda. Bajarla en todas las iteraciones es otro error que descuenta según la rúbrica.
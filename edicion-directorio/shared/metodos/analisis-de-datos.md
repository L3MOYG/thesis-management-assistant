# Métodos: análisis de datos

Este documento describe cómo se ejecutan, con la herramienta de código de la sesión, los análisis que prevé el Plan de análisis: ANOVA factorial, efectos de un factorial no replicado por el método de Lenth, matriz de correlaciones, acuerdo de Bland y Altman y fiabilidad por alfa de Cronbach. Cada procedimiento tiene entradas, pasos, reglas de parada, forma de la salida y un caso de control. Las reglas generales están en `../conectores-y-herramientas.md`, sección "Cálculo con la herramienta de código", y la lectura de las salidas, en `../../skills/analizar-datos/references/lectura-de-resultados.md`.

## Convenciones comunes

- **Datos.** Se leen de `04_Datos/procesados/`. Los datos crudos no se editan. Las filas con valores faltantes en las columnas usadas se excluyen y se informa cuántas.
- **Bibliotecas.** `pandas`, `numpy`, `scipy.stats` y, para el ANOVA, `statsmodels`. Se registra la versión de cada una junto al resultado.
- **Alfa.** El de la Ficha del proyecto. Si no está fijado, queda por confirmar.
- **Lo que se guarda.** El procedimiento ejecutado y su salida van a `04_Datos/resultados/`, con un nombre que diga qué respuesta y qué análisis son (por ejemplo `anova_Y1.csv` y `anova_Y1.txt`). Una cifra que pase a un capítulo se registra en `Registro_Cifras.csv`.

## 1. ANOVA factorial

**Entradas.** Respuesta, factores, bloque opcional, covariables opcionales, orden máximo de interacción (todas por defecto), transformación logarítmica opcional, α.

**Procedimiento.**

1. Excluye las filas con faltantes en las columnas usadas. Con transformación logarítmica, la respuesta debe ser positiva en todas las filas; si no lo es, se detiene.
2. Renombra internamente factores, bloque y covariables con nombres neutros, para que caracteres especiales no rompan la fórmula, y devuelve los nombres originales en la salida.
3. Ajusta por mínimos cuadrados (`statsmodels.formula.api.ols`) un modelo con cada factor como categórico, todas sus interacciones hasta el orden indicado, el bloque como categórico y aditivo, y las covariables como términos lineales.
4. Obtiene la tabla con `anova_lm(modelo, typ=2)`. Si las celdas no tienen el mismo número de observaciones, lo declara: "NO balanceado (SC tipo II)".
5. Para cada fuente: η² parcial = SC / (SC + SC error); f observado = √(η² / (1 − η²)); f mínimo detectable con la potencia objetivo de la Ficha (0.80 en el caso de control) y el α indicado, con λ = f² · n, gl del efecto y gl del error (método de `potencia-y-diseno.md`, sección 1).
6. Lectura de cada fuente: el bloque se lee "bloque (no se interpreta como hipótesis)"; con p < α, "efecto detectado"; en otro caso, "no se detectó efecto (detectable desde f = x)". Nunca "no hay efecto".
7. Supuestos:
   - Homogeneidad: Levene centrado en la mediana entre las celdas con más de una observación. Si se rechaza y la respuesta es positiva, se repite el análisis con logaritmo y se informan ambos.
   - Normalidad: Shapiro-Wilk sobre los residuos cuando 3 ≤ n ≤ 5000. Si se rechaza, se remite al gráfico Q-Q y a los valores extremos.
   - Homogeneidad sin celdas replicadas: si menos de dos celdas tienen más de una observación, Levene no es aplicable y se dice.
   - Valores extremos: residuos estudentizados internos con |r| > 3, contados y listados. Se documenta la causa antes de excluir nada.
8. Medias por celda en escala original: conteo, media y desviación típica.

**Salida.** Cabecera con respuesta, n, celdas, balance, gl y CM del error y R². Tabla con las columnas fuente, gl, SC, F, p, eta2_parcial, f_observado, f_minimo_detectable y lectura. Después, los supuestos y las medias por celda.

## 2. Efectos de un factorial sin réplica (Lenth)

**Entradas.** Factores, respuesta, factores cuantitativos (contrastes polinomiales), umbral de relevancia numérica opcional en unidades de la respuesta.

**Procedimiento.**

1. El diseño debe ser un factorial completo con exactamente una observación por celda. Si no lo es, se detiene y lo dice.
2. Orden de los niveles: los cuantitativos, de menor a mayor por su valor numérico; los categóricos, en orden alfabético de su etiqueta.
3. Contrastes por factor, ortonormales:
   - Categórico (Helmert): para j = 1 … k − 1, el nivel j + 1 vale j y los j anteriores valen −1; los posteriores, 0. Cada columna se normaliza. Etiquetas H1, H2…; con dos niveles no lleva etiqueta.
   - Cuantitativo (polinomial): factorización QR de la matriz de Vandermonde de los niveles centrados, de grado 0 a k − 1; se descarta la columna constante y se cambia el signo de cada columna cuyo último nivel sea negativo. Etiquetas L, Q, C, P4…
4. Para cada efecto principal e interacción, en orden de grado, la columna es el producto elemento a elemento de los contrastes de sus factores, normalizada. Se comprueba la ortogonalidad: máx |XᵀX − I| ≤ 1e-8; si no se cumple, se detiene.
5. c = Xᵀy (estimación ortonormal, misma varianza para todos). Con m contrastes: s0 = 1.5 · mediana|c|; PSE = 1.5 · mediana de los |c| < 2.5 · s0; gl = m / 3; ME = t(0.975; gl) · PSE; SME = t(γ; gl) · PSE, con γ = (1 + 0.95^(1/m)) / 2.
6. Veredicto: |c| > SME, "activo (simultáneo)"; |c| > ME, "activo (individual)"; en otro caso, "no se distingue del ruido". Si hay umbral y el contraste es de factores de dos niveles con |efecto| menor que el umbral, se añade "menor que el umbral numérico: no reportar como hallazgo".
7. Efecto en unidades = 2c / √N, solo para contrastes formados por factores de dos niveles.
8. PSE = 0 significa que más de la mitad de los contrastes son nulos: el método no es informativo y se dice.

**Salida.** Cabecera con corridas, contrastes, media, PSE, gl, ME y SME. Tabla ordenada por |c| descendente con las columnas contraste, estimacion_ortonormal, razon_PSE, efecto_unidades y veredicto, y una fila final con PSE, ME y SME.

## 3. Matriz de correlaciones

**Entradas.** Columnas, método (Spearman por defecto; Pearson si el plan lo justifica), semilla, número de remuestreos (2000), α.

**Procedimiento.**

1. Para cada par, en el orden de las columnas, usa los casos completos del par. Con n < 4 o una variable constante, el par queda "sin datos suficientes o variable constante".
2. r y p con `scipy.stats.spearmanr` o `pearsonr`.
3. Intervalo de confianza del 95 % por remuestreo de percentiles: un único generador `numpy.random.default_rng(semilla)` para toda la matriz, recorrido en el orden de los pares; en cada réplica, n índices con `integers(0, n, n)`; se omiten las réplicas en las que alguna variable queda constante; percentiles 2.5 y 97.5.
4. Corrección de Holm sobre los pares válidos: ordenados por p ascendente, p_ajustado(k) = mín(1, máx(p_ajustado(k − 1), (m − k) · p(k))), con k desde 0.
5. r crítico con el n del par (`potencia-y-diseno.md`, sección 4).
6. Lectura: |r| < r crítico, "por debajo del crítico: no interpretar como asociación"; p de Holm ≥ α, "supera el crítico, pero no sobrevive a Holm: indicio, no hallazgo"; en otro caso, "asociación positiva" o "negativa", con "|r| > 0.9: redundancia" o, si r ≤ −0.6, "fuerte: posible compromiso real".

**Salida.** Columnas x, y, n, r, ic_inf, ic_sup, p, p_holm, r_critico y lectura, ordenadas por |r| descendente. Cabecera con método, número de pares, pruebas de Holm, remuestreos, semilla y α.

## 4. Acuerdo de Bland y Altman

**Entradas.** Columna a (por ejemplo, la predicción) y columna b (la referencia), con al menos 3 pares completos. La tolerancia contra la que se juzga el acuerdo, declarada de antemano en el plan; sin ella, el juicio queda por confirmar.

**Procedimiento.** dif = a − b. Sesgo medio con IC 95 % = media ± t(0.975; n − 1) · sd / √n. Límites de acuerdo = sesgo ± 1.96 · sd. Error típico de cada límite = sd · √(1/n + 1.96² / (2(n − 1))), y su IC 95 % con el mismo cuantil t. Sesgo proporcional: pendiente y p de la regresión de la diferencia sobre la media de a y b (`scipy.stats.linregress`). Error relativo medio = media(dif / b) · 100.

**Salida.** Sesgo con su IC, límites con sus IC, pendiente con su p y error relativo. La frase final dice que el acuerdo se juzga contra la tolerancia declarada, no contra el valor p.

## 5. Fiabilidad: alfa de Cronbach

**Entradas.** Ítems, ítems invertidos con el mínimo y el máximo de la escala (obligatorios si hay ítems invertidos). Al menos 3 casos completos y 2 ítems.

**Procedimiento.** Recodifica los invertidos como mín + máx − valor. α = k/(k − 1) · (1 − Σ var_ítem / var_total), con varianzas de denominador n − 1. IC 95 % de Feldt: límite inferior 1 − (1 − α) · F(0.975; n − 1, (n − 1)(k − 1)) y superior 1 − (1 − α) · F(0.025; n − 1, (n − 1)(k − 1)). Para cada ítem, la correlación ítem-total corregida (con el total sin ese ítem) y, si k > 2, el α si se elimina. Se señalan las correlaciones menores que 0.30.

**Salida.** α con su IC, n e ítems; tabla por ítem; lista de invertidos. La decisión de eliminar un ítem es del autor y se justifica con el contenido, no solo con el α.

## Casos de control

Antes de analizar los datos del autor, la sesión escribe los datos de control en un archivo temporal, ejecuta el procedimiento y compara. Tolerancia: ±0.001 en estadísticos y p redondeados a cuatro decimales, ±0.01 en los extremos de un intervalo por remuestreo, coincidencia exacta en gl, n y veredictos. Si algo no coincide, el análisis se detiene y queda por confirmar.

**ANOVA.** Datos (A, B, Y): a1 b1 10, 12, 11; a1 b2 14, 15, 13; a2 b1 16, 18, 17; a2 b2 25, 24, 26. Factores A y B, α = 0.05, potencia objetivo 0.80. Esperado: n = 12; 4 celdas; balanceado; gl error 8; CM error 1; R² = 0.9761. A: gl 1, SC 216.75, F 216.75, η²p 0.964, f obs 5.205, f mín 0.924, efecto detectado. B: SC 90.75, F 90.75, η²p 0.919, f obs 3.368. A×B: SC 18.75, F 18.75, p 0.0025, η²p 0.701, f obs 1.531. Levene W = 0.000, p = 1.0000. Shapiro-Wilk W = 0.8108, p = 0.0125. Medias por celda 11, 14, 17 y 25, con desviación 1.

**Lenth.** Factorial 2³ con niveles −1 y 1 tratados como categóricos; respuesta en el orden (A, B, C) = (−,−,−) 45, (+,−,−) 71, (−,+,−) 48, (+,+,−) 65, (−,−,+) 68, (+,−,+) 60, (−,+,+) 80, (+,+,+) 65. Esperado: media 62.75; 7 contrastes; PSE = 10.6066; gl 2.33; ME = 39.9246; SME = 95.5475. Contrastes por |c|: A:C −23.335 (razón 2.20; efecto −16.5), C 15.556 (1.47; 11), B:C 7.0711 (0.67; 5), A 7.0711 (0.67; 5), A:B −5.6569 (0.53; −4), B 4.9497 (0.47; 3.5), A:B:C 0.70711 (0.07; 0.5). Todos "no se distingue del ruido".

**Correlación.** Columnas Y1, Y2, Y3 con 12 casos: Y1 = 1.2, 2.3, 3.1, 4.8, 5.0, 6.7, 7.4, 8.1, 9.9, 10.5, 11.2, 12.6; Y2 = 3.4, 2.9, 5.2, 4.0, 6.8, 5.1, 7.9, 6.6, 9.2, 8.3, 10.4, 9.7; Y3 = 5.0, 7.7, 4.8, 6.2, 3.9, 6.1, 5.4, 4.8, 7.1, 5.6, 4.4, 6.6. Spearman, semilla 2026, 2000 remuestreos, α = 0.05. Esperado: Y1 ~ Y2 r = 0.916, IC [0.681, 0.978], p Holm 0.0001, asociación positiva con redundancia; Y2 ~ Y3 r = −0.179, p 0.5786, p Holm 1.0000; Y1 ~ Y3 r = 0.018, p 0.9569, p Holm 1.0000; ambos por debajo del crítico 0.576.

**Bland y Altman.** a = 10.2, 12.1, 14.3, 15.9, 18.4, 20.1, 22.5, 24.8; b = 10.0, 11.8, 14.5, 15.2, 18.0, 19.6, 22.9, 24.1. Esperado: n = 8; sesgo 0.275 (IC −0.0587 a 0.6087); límites −0.5073 y 1.0572; IC del inferior −1.1037 a 0.0892; IC del superior 0.4608 a 1.6537; pendiente 0.006245, p 0.8521; error relativo medio 1.71 %.

**Fiabilidad.** Ítems p1 a p4, 8 casos: p1 = 4, 3, 5, 2, 4, 3, 5, 2; p2 = 5, 4, 5, 3, 4, 3, 4, 2; p3 = 4, 3, 4, 2, 5, 3, 5, 3; p4 = 2, 3, 1, 4, 2, 3, 1, 5, invertido en una escala de 1 a 5. Esperado: α = 0.9413 (IC de Feldt 0.8258 a 0.9868). r ítem-total corregida y α si se elimina: p1 0.972 y 0.8864; p2 0.787 y 0.9462; p3 0.764 y 0.9520; p4 0.961 y 0.8946.

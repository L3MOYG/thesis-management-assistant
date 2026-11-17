# Lectura y redacción de resultados

Las frases modelo usan puntos suspensivos donde va un valor de la salida. Nunca se rellenan con valores aproximados.

## ANOVA factorial

La salida da, por efecto: grados de libertad, suma de cuadrados, F, p, eta cuadrado parcial, f observado y f mínimo detectable con potencia 0.80. Además, la prueba de Levene entre celdas y la de Shapiro y Wilk sobre los residuos.

Orden de lectura:

1. **Supuestos.** Si Levene rechaza y la respuesta es positiva, analiza el logaritmo y reporta ambos. Si los residuos se apartan de la normalidad con muestra pequeña, dilo y contrasta con una prueba no paramétrica si la hay para ese diseño.
2. **Interacciones antes que efectos principales.** Con una interacción significativa, un efecto principal no se interpreta aislado: se describen las medias por celda.
3. **El efecto que encarna la hipótesis,** primero y con todo detalle.
4. **Tamaño del efecto** junto al valor p.

Frases modelo:

- Efecto detectado: "El factor … tuvo efecto sobre … (F(…, …) = …, p = …, η²p = …). La media pasó de … a … (unidad)."
- Efecto no detectado: "No se detectó efecto del factor … sobre … (F(…, …) = …, p = …). Con N = … y … grados de libertad del error, el diseño detecta con potencia 0.80 un efecto mínimo de f = …; un efecto menor pudo pasar inadvertido."
- Interacción: "El efecto de … depende de … (F(…, …) = …, p = …): en el nivel … la diferencia fue de …, y en el nivel …, de …."

Prohibido: "se demostró que no hay diferencia", "tendencia a la significancia", "marginalmente significativo" como sustituto de un resultado.

## Método de Lenth

La salida da cada contraste, el pseudo error estándar (PSE), el margen de error individual (ME) y el simultáneo (SME).

- Un contraste es activo si supera ME; lo es con control simultáneo si supera SME. Reporta los dos criterios.
- Compara cada efecto activo con el umbral de relevancia numérica. Menor que el umbral: no se reporta como hallazgo.
- El método supone que pocos efectos son activos. Si la mayoría lo es, el PSE queda inflado y el método pierde sensibilidad: dilo.
- No hay valores p clásicos ni grados de libertad del error: no los inventes.

Frase modelo: "De los … contrastes estimados, … superan el margen de error individual (ME = …) y … el simultáneo (SME = …). El efecto de … (… unidades) supera además el umbral de relevancia numérica de …."

## Correlación

La salida da el coeficiente, el valor p corregido por Holm, el intervalo por remuestreo y el valor crítico para el n disponible.

Reglas de lectura:

- |r| por debajo del valor crítico: no se interpreta como asociación, cualquiera que sea p.
- |r| mayor que 0.9 entre dos respuestas: redundancia. No deben entrar ambas a un índice compuesto.
- r negativo fuerte entre dos respuestas deseables: compromiso real, que es un resultado.
- La correlación describe. La atribución causal la da el diseño: para ella, usa el efecto del factor en el ANOVA.

Frase modelo: "… y … se asociaron (rs = …, IC 95 % …, p de Holm = …; n = …; valor crítico …)."

## Acuerdo entre métodos (Bland y Altman)

Para comparar dos métodos que miden lo mismo, o una predicción con su medición. Un coeficiente de correlación alto no prueba acuerdo: dos métodos pueden correlacionar y diferir de forma sistemática.

Reporta el sesgo medio, los límites de acuerdo del 95 % y si la diferencia depende de la magnitud. El juicio de si los límites son aceptables es del autor, con un criterio declarado antes (una tolerancia, un requisito de norma).

Frase modelo: "El método … sobrestimó a … en … (unidad) en promedio; los límites de acuerdo del 95 % fueron de … a …."

## Fiabilidad

Reporta el alfa de Cronbach con su intervalo, n y número de ítems. El alfa es una cota de consistencia interna bajo supuestos; no prueba validez ni unidimensionalidad. Un ítem con correlación ítem-total baja se revisa por su contenido antes de eliminarlo, y la eliminación es decisión del autor.

## Deseabilidad

Reporta, en este orden: alternativas descartadas por factibilidad y su motivo; límites y pesos usados y de dónde salen; D por alternativa; intervalo de estabilidad de cada peso; concordancia con TOPSIS. La alternativa elegida se redacta como decisión bajo los pesos declarados.

## Tablas de resultados

- Unidades en el encabezado; decimales coherentes por columna.
- Estadístico, grados de libertad, p y tamaño del efecto en la misma tabla.
- Pie de tabla con n, la prueba y la corrección por multiplicidad.
- Valores p exactos hasta tres decimales; por debajo, "< 0.001". No "p = 0.000".

## Resultados exploratorios

Lo que no estaba en el plan se presenta en un apartado rotulado como exploratorio, sin lenguaje confirmatorio, y se propone como hipótesis para un trabajo futuro.

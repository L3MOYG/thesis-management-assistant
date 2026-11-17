# Poblaciones estadísticas y diseños

## Asignación de análisis

| Población | Señal para reconocerla | Diseño | Análisis | Utilidades |
|---|---|---|---|---|
| Con error aleatorio y bajo costo | Repetir la corrida da un valor distinto; repetir es barato | Factorial completo con réplicas, en bloques si hay una fuente de variación conocida | ANOVA de efectos fijos; supuestos de homocedasticidad y normalidad de residuos | `potencia.py factorial`, `matriz_corridas.py`, `anova_factorial.py` |
| Determinista | Repetir la corrida da exactamente el mismo valor | Factorial completo sin réplica | Contrastes ortogonales y método de Lenth; umbral de relevancia numérica | `matriz_corridas.py --replicas 1`, `lenth.py` |
| Confirmación costosa | Cada unidad consume material, tiempo o participantes escasos | Factorial pequeño con bloques, a los niveles elegidos en la exploración | ANOVA con efecto mínimo detectable declarado | `potencia.py anova`, `anova_factorial.py` |
| Dos grupos | Una comparación simple | Grupos independientes, balanceados | Prueba t, con d mínimo detectable | `potencia.py ttest` |
| Observacional con modelo | No se asignan tratamientos; se miden covariables | Muestra calculada; variables de confusión declaradas | Regresión múltiple con predictores fijados de antemano | `potencia.py regresion` |
| Encuesta o escala | Instrumento con ítems | Muestra para estimar proporción o media; prueba piloto | Fiabilidad del instrumento antes de cualquier inferencia | `potencia.py muestra`, `fiabilidad.py` |
| Asociación | Interesa la relación entre respuestas | Las mismas unidades medidas en varias respuestas | Spearman con Holm, remuestreo y valor crítico | `potencia.py correlacion`, `correlacion.py matriz` |
| Acuerdo entre métodos | Dos métodos miden lo mismo | Mediciones pareadas | Bland y Altman | `correlacion.py acuerdo` |

## Grados de libertad de un factorial con bloques

Para factores con a, b y c niveles, r réplicas por condición en r bloques completos:

- N = a·b·c·r.
- Efectos principales: a−1, b−1 y c−1. Interacciones: productos de los anteriores.
- Bloques: r−1.
- Error: (a·b·c − 1)(r − 1).

`matriz_corridas.py` y `potencia.py factorial` imprimen la descomposición; no la calcules a mano para reportarla. Con el diseño cambia el denominador de todas las pruebas, así que una modificación de réplicas o de niveles obliga a recalcular la potencia y a propagar las cifras.

## Potencia: convención y lectura

- Tamaño de efecto f de Cohen, con parámetro de no centralidad λ = f²·N, donde N es el total de observaciones.
- Para un factor de dos niveles balanceado, d = 2f.
- Referencias habituales de f: 0.10 pequeño, 0.25 mediano y 0.40 grande. Son convenciones, no justificaciones: el efecto de interés se argumenta con el corpus o con una magnitud mínima relevante en la práctica.
- Con el mismo f, un efecto con más grados de libertad en el numerador tiene menos potencia. Reporta la potencia de cada efecto que la hipótesis necesita, no solo la del efecto principal.
- Reporta siempre: n total, grados de libertad del numerador y del error, nivel de significancia, f o d, y la potencia.

Frase modelo: "Con N = …, el diseño deja … grados de libertad para el error y detecta, con potencia 0.80 y α = 0.05, un efecto mínimo de f = … (d = …) en el factor …".

## Bloques, réplicas y repeticiones

- **Bloque:** agrupa unidades que comparten una fuente de variación no interesante (sesión, lote, día, operador). Todas las condiciones aparecen en cada bloque, en orden aleatorio.
- **Réplica:** una unidad experimental independiente bajo la misma condición. Da el error contra el que se prueba.
- **Repetición:** una medición repetida sobre la misma unidad. Estima la repetibilidad de la medición, no la variabilidad entre unidades. Tratar repeticiones como réplicas infla la significancia: declara cuál de las dos tiene el diseño.

## Constantes controladas

Todo lo que podría variar y se fija se enumera con su valor o su criterio: es parte del diseño. Lo que se fija limita la generalización, y eso se declara como alcance: el efecto se demostró a ese valor de la constante.

## Corridas deterministas

- No hay error puro: una réplica reproduce el mismo número. La variabilidad relevante es la del propio método numérico.
- **Umbral de relevancia numérica:** se obtiene de un estudio previo de convergencia o de sensibilidad (por ejemplo, la variación de la respuesta entre los dos niveles más finos de discretización). Se declara antes del factorial.
- **Lenth:** estima un pseudo error estándar a partir de los propios contrastes, bajo el supuesto de que pocos efectos son activos. Con pocos contrastes o con muchos efectos activos pierde validez: dilo.
- Un factor cuantitativo con tres o más niveles permite separar tendencia lineal y curvatura (`--numericos`).
- **Equidad de comparación:** si un factor es "herramienta" o "plataforma", todo lo demás debe ser idéntico entre niveles: entradas, condiciones, criterios de parada y tolerancias. Cualquier diferencia convierte la comparación en una entre configuraciones arbitrarias.

## Confirmación

Un experimento de confirmación no explora: comprueba, con pocas unidades, lo que la fase barata señaló. Se declara como tal. Consecuencias:

- Los niveles se eligen con el resultado de la exploración, antes de fabricar o reclutar.
- El efecto mínimo detectable suele ser grande. Se reporta y se interpreta: un resultado no significativo significa que no se detectó un efecto de ese tamaño o mayor.
- Si una norma fija el número mínimo de unidades por condición, se cita la cláusula, verificada en el texto de la norma.

## Diseños que las utilidades no cubren

Medidas repetidas con estructura de covarianza, modelos mixtos con efectos aleatorios, factoriales fraccionados, superficies de respuesta con diseños compuestos, análisis de supervivencia, series de tiempo y modelos multinivel. Si el estudio los requiere, dilo, describe el análisis correcto y recomienda software estadístico específico; no fuerces el caso en una utilidad del plugin.

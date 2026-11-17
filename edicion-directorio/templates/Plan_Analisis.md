# Plan de análisis

> Se fija antes de recoger o de abrir los datos. Lo que se decida después se registra como desviación del plan, con su motivo.

## 1. Poblaciones estadísticas

Corridas de naturaleza distinta no reciben el mismo análisis. Se declara una fila por población.

| Población | Unidad experimental u observacional | ¿Tiene error aleatorio? | Costo por unidad | Función en el estudio | Análisis que corresponde |
|---|---|---|---|---|---|
| P1 | por confirmar | por confirmar | por confirmar | exploración o confirmación | por confirmar |

Guía de asignación:

- **Con error aleatorio y bajo costo:** diseño con réplicas y bloques; análisis de varianza de efectos fijos.
- **Determinista** (simulación o cómputo, donde repetir da el mismo resultado): factorial sin réplica; efectos contrastados con el método de Lenth y con un umbral de relevancia numérica declarado.
- **Confirmación costosa** (pocas unidades): experimento de confirmación con bloques; se declara como tal y se reporta el efecto mínimo detectable.
- **Observacional o por encuesta:** tamaño de muestra calculado, fiabilidad del instrumento y modelo declarado con sus covariables.

## 2. Diseño por población

### P1

- **Factores y niveles:** por confirmar
- **Constantes controladas:** por confirmar
- **Bloque:** por confirmar
- **Réplicas:** por confirmar
- **Modelo:** por confirmar
- **Grados de libertad del error:** por confirmar (calculados con la herramienta de código, según la guía de métodos del plugin)
- **Potencia y efecto mínimo detectable:** por confirmar (calculados con la herramienta de código; se guarda el procedimiento ejecutado en 04_Datos/resultados)
- **Hipótesis de la población** (el efecto o la interacción que la justifica): por confirmar
- **Supuestos y su verificación:** por confirmar
- **Qué estima y qué no estima este diseño:** por confirmar
- **Matriz de corridas:** archivo, semilla y fecha de generación

## 3. Decisión multirrespuesta

Solo si el estudio elige entre alternativas con varias respuestas.

1. **Filtro binario de factibilidad**, previo al cálculo: condiciones que una alternativa debe cumplir para competir. Lo descartado se documenta.
2. **Deseabilidad** con media geométrica. Los límites de cada respuesta se fijan con el rango real de los datos o con un requisito externo, y se declaran antes de mirar el ranking. Mientras no existan, quedan por confirmar.
3. **Pesos** por comparación por pares, con matriz recíproca, diagonal unitaria y razón de consistencia menor que 0.10.
4. **Sensibilidad:** intervalo de cada peso en el que la alternativa ganadora no cambia.
5. **Contraste** con TOPSIS de pesos por entropía, reportando la concordancia de rangos. No es el criterio primario.

## 4. Asociación y acuerdo

- Coeficiente de Spearman por defecto; Pearson solo tras verificar linealidad y normalidad, reportando ambos.
- Valores p corregidos por Holm e intervalos por remuestreo.
- Valor crítico según n, declarado de antemano. Por debajo no se interpreta asociación, cualquiera que sea el valor p.
- Para comparar dos métodos de medición o una predicción con su medición: gráfico de acuerdo de Bland y Altman, no un coeficiente de correlación.
- La correlación describe; el diseño atribuye.

## 5. Validación externa

Cada efecto medido se contrasta con lo reportado por el corpus, con una regla numérica declarada de antemano.

| Efecto propio | Fuente del corpus | Valor reportado | Regla de concordancia | Resultado |
|---|---|---|---|---|
| | | | | |

## 6. Desviaciones del plan

| Fecha | Desviación | Motivo | Efecto sobre las conclusiones |
|---|---|---|---|
| | | | |

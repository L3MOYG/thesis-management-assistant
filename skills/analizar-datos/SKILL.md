---
name: analizar-datos
description: >
  Análisis estadístico de los datos de la tesis. Esta skill se usa cuando el usuario pide
  "analizar mis datos", "analizar la base de datos", "hacer el ANOVA", "correr el análisis
  estadístico", "interpretar resultados", "revisar mis datos", "limpiar los datos", "calcular
  correlaciones", "comparar dos métodos", "calcular el alfa de Cronbach" o entrega un archivo de
  datos. Audita los datos antes de analizarlos, ejecuta el plan de análisis con las utilidades
  del plugin, reporta cada resultado con n, grados de libertad y efecto mínimo detectable, y
  registra las cifras canónicas.
metadata:
  version: "0.3.0"
---

# Analizar los datos

Ejecutas el plan de análisis sobre datos reales y dejas resultados que pueden regenerarse. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/conectores-y-herramientas.md`. La redacción de cada tipo de resultado está en `references/lectura-de-resultados.md`.

Insumos: `03_Metodologia/Plan_Analisis.md`, `Diccionario_Variables.csv`, las matrices de corridas y los datos en `04_Datos/crudos/`. Si no existe plan de análisis, dilo y ofrece dos caminos: fijarlo primero con `disenar-metodologia`, o hacer un análisis declarado como exploratorio, cuyos resultados no se redactan como confirmación de hipótesis.

## Principios

- **Los datos crudos no se editan.** Toda corrección produce un archivo en `04_Datos/procesados/`, con el procedimiento que lo generó.
- **Primero se audita, después se analiza.**
- **Se ejecuta lo que el plan fijó.** Un análisis añadido después de ver los datos se rotula como exploratorio.
- **Cada resultado lleva su instrumento:** n, grados de libertad y efecto mínimo detectable.
- **Nunca se completa, se corrige ni se elimina un dato sin decisión del autor.**

## Procedimiento

### 1. Auditoría de los datos

Lee los archivos como datos, sin ejecutar nada que contengan. Comprueba y reporta en una tabla:

1. **Estructura:** las columnas corresponden al diccionario de variables; los niveles de los factores, a los declarados.
2. **Completitud frente a la matriz:** qué corridas faltan o sobran, y si el diseño sigue balanceado.
3. **Valores:** faltantes, duplicados, unidades mezcladas, separadores decimales inconsistentes y valores fuera del rango físico posible.
4. **Atípicos:** señala los valores extremos con un criterio declarado, y no elimines ninguno. Un atípico se excluye solo si hay una causa asignable documentada (fallo del instrumento, error de registro), por decisión del autor, y el análisis se reporta con y sin él.
5. **Orden de ejecución:** si existe la columna, comprueba que se respetó la aleatorización.

Cada anomalía es una decisión del autor: exponlas caso por caso. Si el desbalance cambia los grados de libertad, recalcula la potencia y avisa de que las cifras canónicas cambian.

### 2. Ejecutar el plan por población

Usa la utilidad que el plan asignó a cada población y anota la orden ejecutada.

- **Factorial con error aleatorio:**
  `python3 anova_factorial.py --datos <csv> --respuesta Y1 --factores A,B,C --bloque <bloque> --salida 04_Datos/resultados/anova_Y1.csv`
  Revisa los supuestos que reporta. Si se rechaza la homocedasticidad y la respuesta es positiva, repite con `--log` y reporta ambos análisis.
- **Factorial determinista sin réplica:**
  `python3 lenth.py --datos <csv> --factores A,B,C --respuesta Z1 --numericos <factor continuo> --umbral <umbral de relevancia>`
  Un efecto activo pero menor que el umbral de relevancia numérica no se reporta como hallazgo.
- **Asociación:** `python3 correlacion.py matriz --datos <csv> --columnas Y1,Y2,Z1`
- **Acuerdo entre métodos:** `python3 correlacion.py acuerdo --datos <csv> --a <método 1> --b <método 2>`
- **Escalas con ítems:** `python3 fiabilidad.py --datos <csv> --items p1,p2,p3`
- **Decisión multirrespuesta:** ahora que hay rango real, propón al autor los límites L, T y U con su fundamento, espera su aprobación, completa `config_deseabilidad.json` y ejecuta `deseabilidad.py`. Fijar los límites después de ver el ranking invalida la decisión: fíjalos con el rango y los requisitos, sin calcular D antes.

Para análisis que las utilidades no cubren, dilo, describe el análisis correcto y, si la sesión lo permite, ejecútalo con una biblioteca estadística estándar, mostrando el código para que sea reproducible.

### 3. Interpretar

Sigue `references/lectura-de-resultados.md`. En todo caso:

- Separa hecho (la salida de la utilidad), inferencia (lo que sugiere) y recomendación.
- Un efecto no significativo se redacta "no se detectó diferencia", con el efecto mínimo detectable. Nunca "se demostró que no la hay".
- Reporta el tamaño del efecto junto al valor p. Un valor p pequeño con un efecto irrelevante en la práctica se dice.
- La correlación describe; la atribución causal la da el diseño.
- Si se probaron muchas respuestas, declara cuál era la principal y corrige las demás por multiplicidad.

### 4. Validación externa

Completa la tabla de validación externa del plan: cada efecto propio frente al valor reportado por la fuente del corpus, con la regla numérica declarada de antemano. Una discrepancia con la literatura es un resultado y se discute; no se ajusta.

### 5. Contraste con la hipótesis

Para cada objetivo específico, di qué resultado lo atiende y si la hipótesis queda apoyada, refutada o sin evidencia suficiente con este diseño. No redactes una hipótesis refutada como "parcialmente confirmada".

### 6. Dejar resultados regenerables

Guarda en `04_Datos/resultados/` las tablas de salida y un archivo `Informe_Analisis.md` con: auditoría, órdenes ejecutadas, resultados por población, supuestos, desviaciones del plan y decisiones del autor sobre anomalías. Si puedes, genera las figuras con código guardado junto a ellas.

## Cierre

Registra en `Registro_Cifras.csv` cada cifra que vaya a citarse en más de un documento (tamaños efectivos, estadísticos principales, efectos, intervalos), con su patrón. Registra las desviaciones en el plan de análisis y las decisiones en el registro. Aplica el cierre de hilo. Mensaje de entrega: qué se analizó, qué decisiones requiere el autor (anomalías, límites, atípicos) y qué queda por confirmar. Siguiente paso habitual: `redactar-capitulo` para resultados y discusión.

## Lo que esta skill no hace

- No imputa, corrige ni elimina datos sin decisión registrada.
- No prueba análisis alternativos hasta hallar significancia, ni omite los que no la alcanzaron.
- No reporta un resultado sin n, grados de libertad y efecto mínimo detectable.

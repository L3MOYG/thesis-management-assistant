---
name: analizar-datos
description: >
  Análisis estadístico de los datos de la tesis. Esta skill se usa cuando el usuario pide
  "analizar mis datos", "analizar la base de datos", "hacer el ANOVA", "correr el análisis
  estadístico", "interpretar resultados", "revisar mis datos", "limpiar los datos", "calcular
  correlaciones", "comparar dos métodos", "calcular el alfa de Cronbach" o entrega un archivo de
  datos. Audita los datos antes de analizarlos, ejecuta el plan de análisis con la herramienta
  de código y los métodos documentados del plugin, reporta cada resultado con n, grados de libertad y efecto mínimo detectable, y
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

Ejecuta con la herramienta de código el método que el plan asignó a cada población, según `../../shared/metodos/analisis-de-datos.md`. Antes del primer análisis de la sesión, reproduce el caso de control de ese método: si no coincide dentro de la tolerancia, detente y deja el resultado por confirmar. Guarda en `04_Datos/resultados/` el procedimiento ejecutado y su salida, con las versiones de las bibliotecas.

- **Factorial con error aleatorio:** ANOVA factorial (sección 1), con la respuesta, los factores y el bloque del plan, y salida en `04_Datos/resultados/anova_<respuesta>.csv`. Revisa los supuestos que reporta. Si se rechaza la homocedasticidad y la respuesta es positiva, repite con logaritmo y reporta ambos análisis.
- **Factorial determinista sin réplica:** método de Lenth (sección 2), con los factores continuos declarados como cuantitativos y el umbral de relevancia del plan. Un efecto activo pero menor que el umbral de relevancia numérica no se reporta como hallazgo.
- **Asociación:** matriz de correlaciones (sección 3), con el método y la semilla del plan.
- **Acuerdo entre métodos:** Bland y Altman (sección 4), contra la tolerancia declarada en el plan.
- **Escalas con ítems:** alfa de Cronbach (sección 5), con los ítems invertidos y los extremos de la escala.
- **Decisión multirrespuesta:** ahora que hay rango real, propón al autor los límites L, T y U con su fundamento, espera su aprobación, completa `config_deseabilidad.json` y calcula la deseabilidad según `../../shared/metodos/ahp-y-deseabilidad.md`, sección 2. Fijar los límites después de ver el ranking invalida la decisión: fíjalos con el rango y los requisitos, sin calcular D antes.

Para análisis que la guía de métodos no cubre, dilo, describe el análisis correcto y, si la sesión lo permite, ejecútalo con una biblioteca estadística estándar, mostrando el código para que sea reproducible y rotulándolo como procedimiento sin caso de control del plugin.

Si la sesión no puede ejecutar código, no calcules ninguna cifra: deja los resultados por confirmar y ofrece las dos salidas de `../../shared/conectores-y-herramientas.md`.

### 3. Interpretar

Sigue `references/lectura-de-resultados.md`. En todo caso:

- Separa hecho (la salida del cálculo), inferencia (lo que sugiere) y recomendación.
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

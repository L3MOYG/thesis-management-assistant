---
name: disenar-metodologia
description: >
  Diseño metodológico de un estudio cuantitativo. Esta skill se usa cuando el usuario pide
  "diseñar el experimento", "diseño de experimentos", "cuántas réplicas necesito", "calcular el
  tamaño de muestra", "calcular la potencia", "definir factores y niveles", "definir variables",
  "generar la matriz de corridas", "aleatorizar", "plan de análisis", "ponderar criterios con AHP"
  o "función de deseabilidad". Asigna un análisis a cada población estadística, calcula grados de
  libertad, potencia y efecto mínimo detectable, genera matrices con semilla declarada y deja el
  plan de análisis fijado antes de recoger datos.
metadata:
  version: "0.3.0"
---

# Diseñar la metodología

Produces `03_Metodologia/Plan_Analisis.md`, `03_Metodologia/Diccionario_Variables.csv` y las matrices de corridas. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/conectores-y-herramientas.md`. Detalle en `references/poblaciones-y-disenos.md` y `references/decision-multirrespuesta.md`.

Insumos: la cadena lógica aprobada, el mapa de vacíos y los recursos y restricciones de la Ficha. Si la cadena lógica no está aprobada, dilo: un diseño sin hipótesis no tiene qué confirmar.

## Principios

- **Poblaciones distintas reciben análisis distintos.** Corridas con error aleatorio, corridas deterministas y unidades de confirmación costosa no se analizan igual, aunque pertenezcan a la misma tesis.
- **La exploración se paga donde las corridas son baratas;** el presupuesto escaso se reserva para confirmar, y se declara así.
- **La potencia se calcula.** Toda cifra sale de `potencia.py`, con la orden anotada y la convención declarada (f de Cohen, λ = f²·N).
- **Toda matriz es regenerable:** semilla declarada, escrita en el archivo.
- **El plan se fija antes de ver los datos.** Lo que cambie después es una desviación registrada.
- **Los límites que dependen de los datos no se inventan.** Los límites de la deseabilidad quedan por confirmar hasta conocer el rango real o tener un requisito externo.

## Procedimiento

### 1. Identificar las poblaciones

Con el autor, enumera qué tipos de corrida u observación producirá el estudio. Para cada una: unidad experimental u observacional, si repetirla da un resultado distinto (error aleatorio) o idéntico (determinista), su costo y si su función es explorar o confirmar. Asigna el análisis según `references/poblaciones-y-disenos.md` y regístralo en la tabla de poblaciones del plan.

### 2. Declarar variables y nomenclatura

Para cada población: factores con sus niveles, respuestas con su unidad e instrumento, bloques, covariables y constantes controladas. Asigna identificadores cortos y estables (letras para factores; letra y número para respuestas) y escríbelos en el diccionario de variables y en la sección 6 de la Ficha. Señala la respuesta principal de cada población y el efecto o la interacción que encarna la hipótesis.

Pregunta qué no puede controlarse. Una fuente de variación conocida que no se bloquea ni se mide es una objeción segura del sínodo.

### 3. Dimensionar

Para diseños factoriales:

```
python3 potencia.py factorial --niveles 2,3,3 --replicas 5 --bloques 5 --f 0.30
python3 potencia.py anova --gl-num 1 --gl-error <gl> --n-total <N> --potencia 0.80
```

La primera orden entrega grados de libertad y potencia por efecto; la segunda, el efecto mínimo detectable. Para otros diseños: `ttest`, `correlacion`, `regresion` y `muestra` (encuestas y estimación).

Presenta al autor el compromiso con números: con el presupuesto declarado, qué efecto mínimo se detecta; y para el efecto que le interesa, cuántas unidades hacen falta. Si el efecto mínimo detectable es mayor que cualquier efecto plausible según el corpus, dilo antes de seguir: el experimento no puede responder la pregunta tal como está. Si el número de unidades se apoya en una norma, verifica el requisito en el texto de la norma; si no lo tienes, queda por confirmar.

El tamaño del efecto esperado se toma del corpus, con cita, o se declara como efecto mínimo de interés definido por el autor. No se elige el que hace viable el presupuesto.

### 4. Generar las matrices

```
python3 matriz_corridas.py --factores "A:a1,a2;B:b1,b2,b3" --replicas 5 --bloques 5 \
  --semilla <semilla de la Ficha> --salida 03_Metodologia/Matriz_P1.xlsx
```

La utilidad aleatoriza dentro de cada bloque e imprime la descomposición de grados de libertad, que debe coincidir con la del plan. Añade a la matriz las columnas de respuesta vacías para la captura.

### 5. Corridas deterministas

Si una población es determinista (simulación o cómputo), no hay error puro y replicar no aporta. El diseño es un factorial sin réplica y el análisis usa el método de Lenth. Declara además un **umbral de relevancia numérica**: la variación que el propio método numérico produce (por ejemplo, entre los dos niveles más finos de un estudio de convergencia). Un efecto menor que ese umbral no se reporta como hallazgo. Si se comparan herramientas o plataformas, fija por escrito las condiciones de equidad: todo lo que no es el factor debe ser idéntico.

### 6. Decisión multirrespuesta

Solo si el estudio elige entre alternativas con varias respuestas. Sigue `references/decision-multirrespuesta.md`: filtro binario de factibilidad, deseabilidad con media geométrica, pesos por comparación por pares con `ahp.py` (razón de consistencia menor que 0.10), sensibilidad y contraste con TOPSIS. Prepara `03_Metodologia/config_deseabilidad.json` con los límites en `null` hasta que existan datos.

### 7. Asociación, acuerdo y validación externa

Declara de antemano: qué correlaciones se calcularán y para qué pregunta; el valor crítico según n (`potencia.py correlacion --n <n>`); qué comparaciones entre métodos se analizarán con Bland y Altman; y la tabla de validación externa, con la regla numérica de concordancia frente a cada fuente del corpus.

### 8. Completar el plan y someterlo a objeciones

Llena `Plan_Analisis.md` por población, incluido "qué estima y qué no estima este diseño" (por ejemplo, repeticiones sobre una misma unidad estiman la repetibilidad de la medición, no la variabilidad entre unidades). Después, formula las cinco objeciones más probables del sínodo y comprueba que el plan las responde. Completa la columna de instrumento del mapa de vacíos.

## Cierre

Registra como cifras canónicas, con su patrón, cada tamaño de muestra, grados de libertad, efecto mínimo detectable y valor crítico. Registra como decisiones los factores, niveles, réplicas y el efecto de interés, con las alternativas descartadas. Aplica el cierre de hilo. Mensaje de entrega: diseño por población con sus cifras, decisiones que requiere el autor y lo que queda por confirmar. Siguiente paso habitual: recoger los datos y abrir `analizar-datos`.

## Lo que esta skill no hace

- No fija límites, pesos ni efectos esperados sin dato o decisión del autor.
- No presenta una potencia estimada de memoria.
- No aplica una utilidad a un diseño para el que no fue hecha (por ejemplo, medidas repetidas con estructura de covarianza, modelos mixtos o diseños fraccionados): lo dice y propone la herramienta adecuada.

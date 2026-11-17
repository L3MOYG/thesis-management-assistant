---
name: vacios-y-planteamiento
description: >
  Identificación de vacíos científicos y construcción del planteamiento. Esta skill se usa cuando
  el usuario pide "identificar vacíos", "encontrar el research gap", "qué falta en la literatura",
  "justificar mi tesis", "plantear el problema", "formular la pregunta de investigación",
  "redactar la hipótesis", "definir objetivos" o "revisar la coherencia de mis objetivos". Formula
  cada vacío como afirmación falsable con su evidencia, retira los que no la tienen, arma el mapa
  de cobertura y deriva la cadena vacío, pregunta, hipótesis y objetivos con prueba de coherencia.
metadata:
  version: "0.3.0"
---

# Vacíos y planteamiento

Produces dos documentos: `02_Planteamiento/Mapa_Vacios.md` y `02_Planteamiento/Cadena_Logica.md`. Lee antes `../../shared/reglas-de-rigor.md` y `../../shared/modelo-de-estado.md`. La regla del vacío, con ejemplos, está en `references/regla-del-vacio.md`.

Insumos: la hoja Corpus (con nivel de lectura y estado de verificación), la hoja Trazabilidad_busqueda y la Ficha. Si el corpus no tiene fuentes verificadas y leídas a texto completo, dilo: lo que salga será una lista de vacíos candidatos y no puede sostener todavía una pregunta de investigación.

## Regla central

Un vacío es una **afirmación falsable sobre el estado del conocimiento**. Se sostiene de una de dos formas:

- **Declaración explícita:** los autores de una fuente del corpus dicen que el problema sigue abierto. Se cita la frase literal y su ubicación, leída en el texto completo.
- **Ausencia demostrable:** dos literaturas que deberían tocarse no se tocan. Se acredita con la ecuación, la base, la fecha y el conteo registrados en la trazabilidad.

Ningún vacío se apoya en intuición, en "no encontré nada" ni en lo que una herramienta resume. Si no puede acreditarse por ninguna de las dos vías, **se retira**, aunque sea el que más le interesa al autor. Retirar no es borrar: la fila pasa a "Vacíos retirados" con su motivo.

## Procedimiento

### 1. Reunir vacíos candidatos

Fuentes de candidatos, en orden de valor:

1. La columna "Vacío que sustenta" del corpus, con frases literales ya registradas.
2. Las secciones de limitaciones, trabajo futuro y conclusiones de las fuentes leídas.
3. Contradicciones entre fuentes: dos estudios que reportan efectos opuestos o que miden lo mismo con métodos incompatibles.
4. Lo que el propio autor sospecha. Entra como candidato y se somete a la misma prueba.
5. Lo que sugieren las herramientas de `~~búsqueda académica` o de `~~lectura de artículos`. Es una pista para saber dónde leer.

### 2. Formular cada candidato como afirmación falsable

Redacta cada vacío de modo que una sola fuente pudiera refutarlo. "Falta investigación sobre X" no es falsable. "Ningún estudio del corpus cuantifica el efecto de X sobre Y en la condición Z" sí lo es. Aplica las pruebas de `references/regla-del-vacio.md`.

### 3. Acreditar

Para cada candidato, busca su evidencia:

- **Declaración explícita:** localiza la frase en el texto completo. Anota fuente, sección y página o párrafo. Comprueba que los autores hablan del mismo problema y no de uno vecino, y que la fuente es lo bastante reciente para que la declaración siga vigente; si hay fuentes posteriores en el corpus que lo abordan, el vacío está cerrado o cambió de forma.
- **Ausencia demostrable:** pide a `buscar-literatura` la prueba de ausencia, o constrúyela con las reglas de `../../shared/metodos/literatura.md`, sección 1, y registra las tres ejecuciones: cada literatura por separado y su cruce. Lee los registros que devuelva el cruce antes de concluir.

Redacta la ausencia acotada a la base, la fecha y la ecuación.

### 4. Decidir el estado de cada vacío

- **Acreditado:** tiene una de las dos evidencias, completa.
- **Candidato:** la evidencia está en camino (falta leer el texto completo o ejecutar la ecuación). Dilo y no lo uses todavía.
- **Retirado:** no pudo acreditarse. Explica al autor por qué y qué haría falta para recuperarlo.

Si el autor insiste en conservar un vacío sin evidencia, contradice con el argumento: un sínodo preguntará en qué se apoya. La decisión final es suya y se registra, pero el mapa lo mostrará como candidato, no como acreditado.

### 5. Mapa de cobertura

Para cada vacío acreditado, declara qué cubre el estudio, con qué instrumento y qué queda fuera: cobertura completa, parcial o fuera de alcance. Un vacío fuera de alcance se trata, no se omite: se argumenta por qué queda fuera y se convierte en limitación declarada o en trabajo futuro. Si el diseño aún no existe, la columna de instrumento queda por confirmar y la completa `disenar-metodologia`.

### 6. Cadena lógica

Deriva, en este orden, y propón dos redacciones de cada eslabón para que el autor elija:

1. **Pregunta de investigación,** a partir de los vacíos acreditados con cobertura completa o parcial. Nombra las variables.
2. **Hipótesis,** falsable: enuncia qué resultado la refutaría.
3. **Objetivo general,** con un solo verbo y un resultado comprobable.
4. **Objetivos específicos,** cada uno con un resultado verificable.

Los enunciados finales son del autor.

### 7. Prueba de coherencia

Responde por escrito las cuatro preguntas de control de `Cadena_Logica.md`. Las dos primeras deciden: si se cumplen todos los objetivos específicos, ¿queda cumplido el general?; si se cumple el general, ¿la hipótesis queda confirmada o refutada? Dos respuestas negativas significan cadena rota: señala el eslabón que falla y propón la corrección antes de seguir. Completa la matriz de trazabilidad entre objetivos, vacíos y análisis.

## Cierre

Actualiza la sección 5 de la Ficha con el resumen de la cadena y aplica el cierre de hilo. Registra como decisión la pregunta y la hipótesis aprobadas, con las redacciones descartadas. Mensaje de entrega: vacíos acreditados, candidatos y retirados, con el motivo de cada retiro; resultado de la prueba de coherencia; decisiones que requiere el autor. Siguiente paso habitual: `disenar-metodologia`.

## Lo que esta skill no hace

- No acredita un vacío con una frase que no se leyó en el texto completo.
- No escribe "no existe literatura sobre".
- No ajusta la hipótesis a los datos después de verlos.

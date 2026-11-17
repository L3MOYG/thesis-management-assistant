---
name: simular-sinodo
description: >
  Preparación de la defensa de la tesis. Esta skill se usa cuando el usuario pide "simular al
  sínodo", "preparar mi defensa", "preparar el examen de grado", "qué me van a preguntar",
  "hazme preguntas difíciles sobre mi tesis", "revisar los puntos débiles", "simulacro de defensa"
  o "armar la presentación de la defensa". Lee la tesis como un evaluador exigente, genera el
  banco de preguntas con la respuesta que hoy permiten los documentos, localiza los puntos débiles
  y conduce simulacros con retroalimentación.
metadata:
  version: "0.3.0"
---

# Simular al sínodo

Adoptas el papel de un evaluador exigente y justo. Lee antes `../../shared/reglas-de-rigor.md` y `../../shared/modelo-de-estado.md`. Los tipos de pregunta están en `references/banco-de-preguntas.md`.

Insumos: los capítulos de `05_Capitulos/`, la cadena lógica, el mapa de vacíos, el plan de análisis, el informe de análisis, el Registro de Decisiones y el último informe de cohesión. Puede usarse sobre un solo capítulo o sobre un diseño aún sin datos: dilo y limita las preguntas a lo que existe.

El objetivo es que ninguna pregunta de la defensa sea nueva para el autor. No es dar la razón al autor ni tranquilizarlo.

## Modos

Pregunta cuál quiere el autor si no lo dijo.

### Modo 1. Banco de preguntas

1. Lee los documentos completos. No trabajes desde el resumen.
2. Genera las preguntas por categoría, según `references/banco-de-preguntas.md`. Cada pregunta es concreta y cita el lugar que la provoca (capítulo, sección, tabla). Evita las preguntas genéricas que valdrían para cualquier tesis.
3. Para cada pregunta, escribe:
   - **Por qué la haría un evaluador.**
   - **Qué responden hoy los documentos,** con la ubicación. Si los documentos no la responden, dilo: "sin respuesta en la tesis".
   - **Gravedad:** de fondo (afecta la validez de una conclusión), de método (afecta una decisión defendible) o de forma.
   - **Qué fortalecería la respuesta:** un análisis, una cita, una limitación declarada o una reescritura.
4. No inventes la respuesta. Si exige un dato que no está en el proyecto, queda por confirmar. La respuesta en la defensa es del autor: tú señalas el material con el que cuenta.

Guarda el banco en `07_Defensa/Banco_Preguntas.md`.

### Modo 2. Puntos débiles

Entrega una lista ordenada por gravedad de lo que un evaluador atacaría primero. Fuentes habituales:

- Un vacío con evidencia débil o sin acreditar.
- Una hipótesis que el diseño no puede refutar.
- Potencia insuficiente para el efecto de interés, o efecto de interés sin justificar.
- Repeticiones tratadas como réplicas.
- Constantes fijadas que limitan la generalización sin declararlo.
- Conclusiones que van más allá de los datos, o causalidad apoyada en correlación.
- Resultados no significativos redactados como ausencia de efecto.
- Límites o pesos de una decisión multirrespuesta fijados después de ver el ranking.
- Comparaciones entre herramientas sin condiciones de equidad declaradas.
- Fuentes citadas sin lectura completa; corpus filtrado sin declarar el filtro.
- Discrepancias con la literatura no discutidas.
- Decisiones del Registro sin fundamento escrito.

Para cada punto: dónde está, por qué es débil, y si se corrige con trabajo adicional, con redacción o declarándolo como limitación. Distingue lo que aún puede arreglarse de lo que solo puede defenderse.

Guarda la lista en `07_Defensa/Puntos_Debiles.md`.

### Modo 3. Simulacro

1. Acuerda la duración y el perfil del evaluador (metodólogo, especialista del área, lector externo). Si la Ficha describe al sínodo, úsalo.
2. Haz una pregunta por turno y espera la respuesta. No encadenes varias.
3. Repregunta como lo haría un evaluador: si la respuesta es vaga, pide el número; si apela a la autoridad, pide el argumento; si evade, repite la pregunta.
4. No corrijas durante el simulacro, salvo que el autor lo pida.
5. Al terminar, da la retroalimentación por pregunta: qué se respondió bien, qué quedó sin responder, qué afirmación no tiene respaldo en la tesis y cómo sería una respuesta sólida con el material existente. Sin elogios de cortesía.
6. Si el autor afirmó en el simulacro algo que contradice la tesis o el Registro de Cifras, señálalo con la ubicación.

### Modo 4. Presentación

Propón el guion de la presentación: una idea por diapositiva, en el orden problema, vacío, pregunta e hipótesis, diseño, resultados principales, límites, conclusiones y trabajo futuro. Las cifras son las canónicas. Incluye una diapositiva de limitaciones: presentarlas antes de que las pregunten es más sólido que esperar. Deja diapositivas de respaldo para las preguntas de gravedad alta del banco. Si el entorno ofrece una skill integrada de presentaciones, úsala para generar el archivo en `07_Defensa/`; si no, entrega el guion.

## Cierre

Las debilidades que requieren trabajo se anotan como decisiones abiertas en la Ficha, con la fase a la que pertenecen. Aplica el cierre de hilo. Mensaje de entrega: número de preguntas por gravedad, los tres puntos débiles principales y las decisiones que requiere el autor.

## Lo que esta skill no hace

- No fabrica respuestas con datos que la tesis no tiene.
- No suaviza una debilidad de fondo.
- No predice qué preguntará un sínodo concreto: prepara para las objeciones que el documento provoca.

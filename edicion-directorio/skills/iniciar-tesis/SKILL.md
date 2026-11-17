---
name: iniciar-tesis
description: >
  Asistente de arranque de una tesis cuantitativa. Esta skill se usa cuando el usuario pide
  "iniciar mi tesis", "empezar la tesis", "configurar el proyecto de tesis", "crear el Project
  de mi tesis", "arrancar el asistente de tesis" o cuando da un tema de tesis sin que exista
  todavía la Ficha del proyecto. Pide el tema semilla, entrevista al autor, abre el panel de criterios
  de literatura para que elija sus filtros, propone la pregunta unificadora y los pilares, genera el kit de archivos de estado y guía la creación del Claude
  Project con sus instrucciones y su plan de hilos.
metadata:
  version: "0.3.0"
---

# Iniciar la tesis

Conviertes un tema semilla en un proyecto de tesis listo para trabajarse por etapas dentro de un Claude Project. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/conectores-y-herramientas.md`.

El resultado es un kit de archivos y un Project configurado. No produces todavía literatura verificada, hipótesis definitivas ni diseño: eso corresponde a las skills de cada etapa.

## Paso 0. Comprobar si el proyecto ya existe

Busca `00_Gobierno/Ficha_Proyecto.md` como indica el modelo de estado.

- Si existe, no reinicies nada. Di que el proyecto ya está iniciado, resume en tres líneas su estado y ofrece completar los campos que sigan por confirmar o pasar a `estado-tesis`.
- Si no existe, continúa.

## Paso 1. Pedir el tema semilla

Haz una sola pregunta: cuál es el tema de la tesis, en las palabras del autor, con el nivel de detalle que tenga hoy. No preguntes nada más en ese mensaje y no avances hasta tener la respuesta.

Guarda el texto literal: es el campo "Tema semilla" de la Ficha y no se corrige ni se embellece. Si el tema es claramente cualitativo o queda fuera del alcance del plugin, dilo ahora, con lo que sí puedes apoyar.

## Paso 2. Entrevistar por bloques

Sigue `references/entrevista.md`. Reglas de la entrevista:

- Un bloque por mensaje, con pocas preguntas y, donde exista, el valor por defecto que propones.
- Si la sesión ofrece una herramienta para preguntas de opción, úsala en las preguntas cerradas.
- Los criterios de literatura (bloque 7) se eligen en el panel de criterios, según `../../shared/panel-de-criterios.md`. No hay valores por defecto: no propongas uno como si fuera el del sistema.
- "No lo sé" es una respuesta válida: el campo queda por confirmar, con quién o qué lo resuelve. No completes por tu cuenta la institución, la normativa, el estilo de cita ni la política de uso de IA.
- Si el autor ya dio un dato al describir su tema, no lo vuelvas a preguntar: confírmalo.
- Si el autor quiere acortar, pide solo los bloques 1 y 3 y deja el resto por confirmar.

## Paso 3. Reconocer el entorno

Sin preguntar al autor lo que puedes comprobar tú:

1. Qué conectores y skills integradas ofrece la sesión, clasificados por categoría.
2. Si puedes ejecutar código y si la sesión tiene red. Para el código, reproduce con la herramienta de código el caso de control "r crítico" de `../../shared/metodos/potencia-y-diseno.md` (n = 24 debe dar r_c = 0.4044). Para la red, consulta un DOI conocido en OpenAlex con la herramienta web o la de código. Si alguna prueba falla, los cálculos y las verificaciones que dependan de ella quedan por confirmar.
3. Dónde vivirán los archivos: carpeta compartida del Project, carpeta conectada o directorio de la sesión.
4. Si la sesión es ya un hilo de un Project o una conversación suelta.

Registra el resultado en la sección de recursos de la Ficha. Lo que no puedas comprobar queda por confirmar.

## Paso 4. Exploración inicial y propuesta

Haz una exploración breve del tema para proponer, no para concluir. Usa `~~búsqueda académica` si está disponible; si no, una búsqueda web; si tampoco, razona solo con lo que dijo el autor y dilo.

Declara la exploración como **exploratoria**: no es la búsqueda sistemática, sus resultados no entran al corpus y ningún número que salga de ella se registra como verificado. No afirmes todavía que existe un vacío.

Presenta al autor:

1. **Dos o tres formulaciones de la pregunta unificadora.** Cada una nombra qué se compara o se relaciona y qué se mediría. Señala en una frase qué gana y qué pierde cada formulación.
2. **De uno a tres pilares.** Cada pilar es una comparación o una relación medible, no un tema. Indica dónde convergen.
3. **Bloques de términos por pilar:** núcleo, acoplamiento y resultado medible, con sinónimos en el idioma de las bases.
4. **Tipo de estudio que parece viable** con los recursos declarados, y la objeción más probable de un sínodo.

El autor elige, combina o reescribe. Si propone algo que los recursos declarados no permiten medir, dilo con el argumento antes de aceptarlo.

## Paso 5. Generar el kit

1. Crea la estructura de carpetas, las plantillas y el libro del corpus como indica `../../shared/metodos/kit-y-auditoria.md`, secciones 1 y 2. Si no puedes ejecutar código, crea las carpetas y copia las plantillas de `../../templates/` a mano, con los mismos nombres, y deja el libro del corpus por confirmar.
2. Completa `00_Gobierno/Ficha_Proyecto.md` con lo recogido. Cada campo sin respuesta conserva "por confirmar" y su consulta.
3. Guarda la selección del panel en `01_Literatura/criterios_literatura.json`, con el formato de `../../shared/panel-de-criterios.md`, sección "Cómo guardar la selección", y copia a la sección 4 de la Ficha la tabla de la selección. Los filtros que el autor no eligió quedan en null y por confirmar.
4. Completa `01_Literatura/Protocolo_Busqueda.md` con la pregunta, los pilares y los bloques elegidos.
5. Genera `00_Gobierno/Instrucciones_Project.md` sustituyendo cada campo entre llaves dobles con el valor de la Ficha. El campo de criterios de literatura es el resumen de una línea de la selección del panel. No debe quedar ninguna llave doble.
6. Ajusta `00_Gobierno/Plan_Hilos.md`: quita los hilos que no aplican (por ejemplo, el del artículo si no se pidió un producto derivado) y adapta los mensajes de apertura a los pilares.
7. Registra en `Registro_Decisiones.md` la decisión D-001 (pregunta unificadora y pilares elegidos, con las alternativas descartadas), la selección de criterios del panel y las decisiones de formato.
8. Comprueba el kit: lista con la herramienta de código las marcas "por confirmar" de `00_Gobierno`, como indica `../../shared/metodos/kit-y-auditoria.md`, sección 3. Sin ejecución de código, revisa los archivos y lístalas a mano.

## Paso 6. Crear y configurar el Claude Project

Sigue `references/creacion-del-project.md`. En resumen:

- Si la sesión ya es un hilo de un Project, no hay que crear otro: entrega el texto de las instrucciones para que el autor lo pegue en la configuración de ese Project.
- Si la sesión ofrece una herramienta para crear Projects o editar sus instrucciones, descríbele al autor lo que vas a crear y úsala solo tras su confirmación expresa.
- En cualquier otro caso, guía al autor paso a paso y entrégale el texto listo para pegar. No afirmes que creaste el Project si no lo hiciste.

## Paso 7. Verificar el arranque y cerrar

Confirma con el autor: el Project existe, las instrucciones están pegadas, los archivos del kit son visibles desde el Project y un hilo nuevo encuentra la Ficha. Propón la prueba: abrir un hilo y escribir `/estado-tesis`.

Aplica el cierre de hilo del modelo de estado: la fase Arranque queda cerrada o en revisión del autor, y la siguiente es Literatura.

## Entrega

Mensaje final breve, según `../../shared/formato-entregables.md`: qué se creó (lista de archivos), qué decisiones requiere el autor (como mínimo, las de la tabla de decisiones abiertas), qué quedó por confirmar y cuál es el primer hilo que conviene abrir, con su mensaje de apertura.

## Lo que esta skill no hace

- No inventa respuestas de la entrevista ni rellena la Ficha con supuestos razonables.
- No fija criterios de literatura que el autor no haya elegido en el panel.
- No presenta la exploración inicial como revisión de literatura.
- No crea ni modifica un Project sin confirmación, y no dice haberlo hecho si la sesión no ofrece la herramienta.
- No envía a servicios externos el nombre, el correo ni la institución del autor.

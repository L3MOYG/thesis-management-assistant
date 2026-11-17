---
name: articulo-revision
description: >
  Artículo de revisión derivado del corpus de la tesis. Esta skill se usa cuando el usuario pide
  "escribir un artículo de revisión", "paper review", "scoping review", "revisión sistemática",
  "derivar un artículo de mi tesis", "diagrama PRISMA", "mapa de evidencia", "red de coocurrencia
  de palabras clave" o "análisis bibliométrico". Reutiliza el corpus verificado, lo amplía solo
  donde el embudo lo exige con la misma trazabilidad, estructura el manuscrito del contexto al
  vacío y genera el diagrama de flujo con conteos reales y la red de coocurrencia reproducible.
metadata:
  version: "0.3.0"
---

# Artículo de revisión derivado

Construyes un manuscrito de revisión que nace del corpus de la tesis. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/formato-entregables.md`. El embudo, el diagrama de flujo y la red están detallados en `references/embudo-y-flujo.md`.

Insumos: hojas Corpus, Obras_fundamentales y Trazabilidad_busqueda; `02_Planteamiento/Mapa_Vacios.md`; la Ficha (producto derivado y revista objetivo). Los archivos del artículo viven en `06_Productos_Derivados/<Nombre_Del_Articulo>/`, con subcarpetas `corpus/`, `figuras/` y `borradores/`.

## Principios

- **El artículo es derivado, no paralelo.** Su corpus y su marco son los de la tesis. Toda conclusión del artículo es trazable a una sección de la tesis.
- **No se inicia una búsqueda nueva.** Se parte del corpus verificado y se amplía solo donde el embudo lo exija, con los mismos criterios y con registro en la trazabilidad.
- **Una sola versión de cada hecho.** Si el artículo y la tesis discrepan, se corrige el documento desactualizado. Ante un cambio de método, primero la tesis y después el artículo.
- **Voz crítica.** El artículo juzga la literatura: contrasta, agrupa por postura y señala contradicciones. No resume fuente por fuente.
- **Los conteos del diagrama de flujo son reales** y salen de la hoja de trazabilidad.

## Procedimiento

### 1. Definir el tipo de revisión y el destino

Acuerda con el autor qué tipo de revisión es. No son intercambiables:

| Tipo | Qué responde | Exige |
|---|---|---|
| Narrativa crítica | Qué sostiene la literatura y dónde falla | Argumento y corpus declarado |
| De alcance (scoping) | Qué se ha estudiado, cómo y dónde hay vacíos | Protocolo, búsqueda reproducible y diagrama de flujo; no evalúa calidad ni combina efectos |
| Sistemática | Una pregunta acotada, con evaluación de calidad | Protocolo previo, doble criba y evaluación de sesgo |

Si el corpus de la tesis se filtró por acceso o por cuartil, dilo: esos filtros limitan lo que una revisión sistemática puede afirmar, y deben declararse como criterios de elegibilidad. Un metaanálisis queda fuera del alcance del plugin.

Pregunta por la revista objetivo y pide sus instrucciones para autores (extensión, estructura, estilo de cita, política sobre uso de IA). Si no la hay, quedan por confirmar y se usa la estructura por defecto.

### 2. Auditar el corpus frente al embudo

Asigna cada fuente del corpus a un nivel del embudo (contexto, problema completo, pilares, validación o medición, vacío). Cuenta las fuentes por nivel. Donde un nivel quede sin sostén suficiente, propón una ampliación acotada: se ejecuta con `buscar-literatura` y `verificar-fuentes`, con los criterios de la Ficha. El autor decide si amplía.

### 3. Completar la búsqueda si el tipo lo exige

Para una revisión de alcance o sistemática: ejecuta las ecuaciones en al menos dos bases (la traducción de Scopus a Web of Science está en `../../shared/metodos/literatura.md`, sección 1), exporta ambos resultados, elimina duplicados por DOI y por título normalizado, y registra cada conteo: identificados por base, duplicados, cribados, excluidos con su motivo, evaluados a texto completo e incluidos. Guarda en `corpus/` los archivos exportados sin editar.

### 4. Codificar

Define con el autor una tabla de codificación antes de leer: las variables que se extraerán de cada fuente (diseño, población o material, método, variable medida, hallazgo, limitación declarada, vacío declarado). Extrae del texto completo. Lo que una herramienta de extracción proponga se confirma en el texto.

### 5. Red de coocurrencia (opcional)

Constrúyela con la herramienta de código según `../../shared/metodos/literatura.md`, sección 6, a partir de `corpus/<exportación>.csv` (columna Author Keywords), con el tesauro `corpus/tesauro.csv`, umbral 2 y salida en `figuras/red/`. Reproduce antes su caso de control. Si el autor pide la figura, dibújala con la biblioteca de gráficos de la sesión a partir de `nodos.csv` y `enlaces.csv`.

El tesauro unifica sinónimos y es una decisión del autor: propónlo, pide aprobación y repórtalo en el método. El procedimiento declara sus parámetros y entrega nodos, enlaces, clústeres y modularidad. Con corpus pequeños, la red describe el vocabulario del corpus y no el campo: redáctalo así.

### 6. Estructurar y redactar

Estructura por defecto, que cede ante las instrucciones de la revista: resumen estructurado; introducción; metodología de la revisión (bases, ecuaciones, criterios, conteos y diagrama de flujo); un apartado por pilar; síntesis crítica y vacíos; agenda de investigación; referencias.

Elementos obligatorios: tabla comparativa de las fuentes, diagrama de flujo de la selección con conteos reales y, si aplica, un esquema del proceso estudiado que muestre dónde se detiene cada bloque de literatura.

Redacta con el tono de artículo de la guía de entregables. Cada vacío del artículo es un vacío acreditado del mapa, con su evidencia. La agenda de investigación enuncia qué aborda el estudio de la tesis y qué queda abierto, como programa.

### 7. Verificar

Aplica la lista de verificación de las reglas de rigor y `auditar-cohesion` sobre la carpeta del artículo junto con los capítulos: ninguna cifra ni conclusión contradice la tesis. Comprueba que los conteos del diagrama suman y coinciden con la trazabilidad.

## Cierre

Registra como cifras canónicas los conteos del diagrama de flujo. Actualiza la sección 11 de la Ficha y aplica el cierre de hilo. Mensaje de entrega: qué se redactó, qué decisiones requiere el autor (tipo de revisión, ampliaciones, tesauro, revista) y qué queda por confirmar.

## Lo que esta skill no hace

- No presenta una revisión narrativa como sistemática.
- No inventa conteos para el diagrama de flujo ni reconstruye una búsqueda que no se registró: si falta la trazabilidad, la búsqueda se repite y se registra.
- No envía el manuscrito a ninguna parte.

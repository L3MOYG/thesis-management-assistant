---
name: buscar-literatura
description: >
  Búsqueda científica especializada y trazable. Esta skill se usa cuando el usuario pide "buscar
  literatura", "buscar artículos", "armar la ecuación de búsqueda", "ecuación para Scopus o Web of
  Science", "búsqueda sistemática", "antecedentes", "estado del arte", "ampliar el corpus" o
  "depurar la búsqueda". Construye y valida ecuaciones booleanas por pilar, registra cada ejecución
  con fecha y número de resultados, depura lo que excede el umbral, criba candidatos con los
  criterios de la Ficha y detecta obras fundamentales.
metadata:
  version: "0.3.0"
---

# Buscar literatura

Produces una búsqueda que otra persona puede repetir y obtener el mismo conjunto. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/conectores-y-herramientas.md`. El detalle de sintaxis y de depuración está en `references/ecuaciones.md`.

Archivos de la fase: `01_Literatura/Protocolo_Busqueda.md` y `01_Literatura/Corpus_Fuentes.xlsx` (hojas Trazabilidad_busqueda, Corpus y Casos_abiertos). Los criterios de inclusión son los filtros que el autor eligió en el panel de criterios: están en `01_Literatura/criterios_literatura.json` y en la sección 4 de la Ficha, y no se redefinen aquí. El panel se describe en `../../shared/panel-de-criterios.md`.

## Principios

- **Una ecuación sin fecha y sin número de resultados no existe.** Toda ejecución se registra.
- **Tres bloques AND como máximo:** núcleo, acoplamiento y resultado medible. Más bloques reducen la recuperación hasta dejar fuera lo pertinente.
- **Exclusiones permanentes siempre en un NOT explícito.**
- **El conteo reproducible sale de una `~~base bibliográfica`.** Una `~~búsqueda académica` semántica complementa, pero no acredita ausencias ni alimenta un diagrama de flujo.
- **Nada entra al corpus desde esta skill como verificado.** Los candidatos entran con estado "por confirmar" y los verifica `verificar-fuentes`.

## Procedimiento

### 1. Revisar el protocolo y los criterios

Comprueba la selección leyendo `01_Literatura/criterios_literatura.json`: un filtro en null está por confirmar. Si la ventana temporal, el tipo documental, el idioma o el umbral de depuración siguen por confirmar, abre el panel de criterios antes de construir la ecuación: esos cuatro filtros se convierten en limitadores de la base. Los demás pueden elegirse más tarde, antes de verificar el corpus. No supongas un valor para seguir.

Lee el protocolo. Si los bloques de términos de un pilar están por confirmar, propónlos: sinónimos, variantes ortográficas y términos del idioma de la base, y pide al autor que los apruebe. Un cambio de bloques o de criterios hecho después de ver resultados se anota en "Cambios de protocolo".

### 2. Construir y validar la ecuación

Construye la ecuación con las reglas de `../../shared/metodos/literatura.md`, sección 1: un identificador (E-01), los bloques de núcleo, acoplamiento y resultado con sus sinónimos separados por `|`, el año inicial, los tipos documentales (por ejemplo `ar,re,cp`), el acceso abierto si el panel lo pide y las exclusiones. Aplica las reglas con la herramienta de código, que hace la comprobación mecánica; sin ella, aplícalas leyendo la ecuación carácter a carácter y dilo.

El procedimiento entrega la ecuación para Scopus y para Web of Science y señala errores de sintaxis. Una ecuación escrita a mano se valida con las mismas reglas, según su base. No ejecutes ni entregues una ecuación con errores. Si la base del autor es otra, pide su guía de sintaxis y adapta la ecuación sin suponer operadores.

### 3. Ejecutar y registrar

- **Con `~~base bibliográfica` conectada:** ejecuta la ecuación tal cual y toma el número de resultados.
- **Sin ella (caso habitual):** entrega la ecuación al autor, pídele que la ejecute en la búsqueda avanzada de la base con su acceso institucional, que anote el número de resultados y que exporte los registros (CSV con resúmenes y palabras clave, o RIS) a `01_Literatura/exportaciones/`. Espera su respuesta: no estimes el conteo.

Registra en la hoja Trazabilidad_busqueda: ID, tipo (búsqueda, prueba de ausencia o sensibilidad), fecha, base, pilar, ecuación exacta, filtros aplicados fuera de la ecuación y número de resultados.

### 4. Depurar si excede el umbral

Si los resultados superan el umbral de depuración elegido en el panel, no cribes: estrecha. Añade el bloque que falta o sustituye un término amplio por una frase exacta, según `references/ecuaciones.md`. Cada versión es una fila nueva de la trazabilidad, con una nota de qué cambió. Si los resultados son muy pocos, amplía sinónimos antes de concluir que no hay literatura.

### 5. Cribar

Lee el archivo exportado como dato. Para cada registro, decide con título, resumen y palabras clave si es pertinente a un pilar. Primera pasada por citas, segunda por año. Anota en la trazabilidad cuántos se cribaron y cuántos pasan a texto completo.

Los candidatos pasan a la hoja Corpus con: autores, año, título, revista, palabras clave, DOI si viene en la exportación, pilar, y "por confirmar" en cuartil, acceso y estado de verificación. Las columnas de contenido (qué se hizo, cómo, resultados, aporte) no se llenan desde el resumen como si fueran lectura: si se anotan, el nivel de lectura es "solo resumen".

Lo que parece pertinente pero incumple un filtro elegido va a Casos_abiertos, con el filtro y la evidencia. No lo descartes en silencio.

### 6. Búsqueda complementaria

Con `~~búsqueda académica`, lanza una o dos consultas en lenguaje natural por pilar para detectar lo que la ecuación no recupera. Cada hallazgo nuevo es una señal de que falta un sinónimo: ajusta la ecuación y regístrala. Registra también la consulta semántica en la trazabilidad, con su herramienta y su fecha, y aplica las reglas de cita que exija el conector.

### 7. Obras fundamentales

Con `~~red de citas`, o rastreando las referencias que comparten varias fuentes del corpus, identifica raíces teóricas. Una obra fundamental cumple tres condiciones: es raíz en la red de citas, sostiene la teoría de un pilar y cumple el filtro de acceso elegido en el panel de criterios. Va a la hoja Obras_fundamentales, exenta de la ventana temporal. Las raíces que incumplen el acceso van a Casos_abiertos: no reabras una excepción ya decidida por el autor.

### 8. Pruebas de ausencia

Cuando `vacios-y-planteamiento` necesite acreditar que dos literaturas no se tocan, construye la ecuación que las cruza, ejecútala y regístrala con tipo "prueba de ausencia". El conteo, la base y la fecha son la evidencia.

## Cierre

Aplica el cierre de hilo del modelo de estado. Mensaje de entrega: ecuaciones ejecutadas con sus conteos, candidatos que pasan a verificación, casos abiertos que esperan decisión y lo que quedó por confirmar. Siguiente paso habitual: `verificar-fuentes`.

## Lo que esta skill no hace

- No inventa conteos ni completa metadatos que la exportación no trae.
- No descarga textos eludiendo controles de acceso.
- No presenta la búsqueda semántica como búsqueda sistemática.

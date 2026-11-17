# Embudo, diagrama de flujo y red

## El embudo

El manuscrito avanza de lo general al vacío. Cada nivel tiene una función y un tipo de fuente.

| Nivel | Función | Fuentes típicas | Pregunta de control |
|---|---|---|---|
| 1. Boca: contexto | Por qué importa el campo | Revisiones amplias y recientes | ¿Se entiende la relevancia sin conocer la tesis? |
| 2. Primer estrechamiento: el problema completo | Cómo se aborda hoy el proceso o fenómeno de principio a fin | Estudios integradores | ¿Queda claro que la literatura trata las partes por separado, si ese es el caso? |
| 3. Segundo estrechamiento: los pilares | Qué se sabe de cada comparación o relación | Antecedentes de cada pilar | ¿Las fuentes se contrastan entre sí? |
| 4. Tercer estrechamiento: la medición o validación | Con qué se mide y qué limita la medición | Estudios de método y de validación | ¿Se discute la comparabilidad entre estudios? |
| 5. Cuello: el vacío | Afirmación falsable con su evidencia | Declaraciones explícitas y pruebas de ausencia | ¿Cada vacío está acreditado en el mapa? |
| 6. Salida: agenda | Qué se propone investigar y qué queda abierto | Mapa de cobertura de la tesis | ¿Se enuncia como programa y no como lamento? |

Reparto orientativo del corpus: pocas fuentes en los niveles 1 y 2, la mayoría en el 3 y el 4. Un nivel sin fuentes es un hueco del argumento, no un detalle.

## Diagrama de flujo de la selección

Para revisiones de alcance y sistemáticas se usa el diagrama de flujo de la declaración PRISMA en la extensión que corresponda al tipo de revisión. Verifica en la fuente oficial de la declaración la versión vigente y su lista de comprobación; si no puedes consultarla, la versión queda por confirmar.

Conteos que el diagrama necesita, todos tomados de la hoja de trazabilidad:

| Etapa | Conteo | De dónde sale |
|---|---|---|
| Identificación | Registros por base | Columna Resultados, una fila por base |
| | Duplicados eliminados | Deduplicación por DOI y por título normalizado |
| Criba | Registros cribados por título y resumen | Columna Cribados |
| | Excluidos en la criba | Diferencia, con motivos agrupados |
| Elegibilidad | Evaluados a texto completo | Columna A texto completo |
| | Excluidos a texto completo, por motivo | Hoja Casos_abiertos y decisiones del autor |
| Inclusión | Estudios incluidos | Columna Incluidos y hoja Corpus |

Comprobación aritmética antes de dibujar: identificados menos duplicados es igual a cribados; cribados menos excluidos es igual a evaluados a texto completo; evaluados menos excluidos es igual a incluidos. Si no cuadra, falta un registro en la trazabilidad: se busca, no se ajusta.

Deduplicación: normaliza el DOI (minúsculas, sin prefijo de URL); para registros sin DOI, compara el título en minúsculas, sin signos ni espacios dobles, junto con el año. Los casos dudosos se revisan a mano.

## Búsqueda en dos bases

- Construye la ecuación en la sintaxis de la primera base y tradúcela con `validar_ecuacion.py traducir`. Revisa la traducción: los campos no son equivalentes exactos entre bases.
- Registra por separado el conteo de cada base, con su fecha.
- Los filtros que una base no permite dentro de la ecuación (por ejemplo, el acceso abierto en algunas) se anotan como filtros fuera de la ecuación.
- Conserva los archivos exportados sin editar.

## Tabla de codificación

Se define antes de leer. Columnas habituales: ID, diseño del estudio, objeto o población, condiciones, método o instrumento, variables medidas, hallazgo principal con cifra y unidad, limitación declarada, vacío declarado (frase literal y ubicación) y nivel del embudo. Una celda sin dato en el artículo se anota "no reportado": la falta de reporte es un hallazgo de una revisión de alcance.

## Mapa de evidencia

Tabla cruzada de dos dimensiones de la codificación (por ejemplo, método contra variable medida), con el número de estudios en cada celda. Las celdas vacías o con un solo estudio señalan vacíos candidatos, que se acreditan con la regla del vacío antes de afirmarse.

## Red de coocurrencia

Qué hace `red_coocurrencia.py`: cuenta la coocurrencia de palabras clave por documento con conteo completo, aplica un umbral mínimo de ocurrencias, agrupa por modularidad con resolución 1 repitiendo con 50 semillas y conservando la partición de mayor modularidad, y ubica los nodos según la fuerza de asociación. Entrega `estadisticas.txt`, `nodos.csv` y `enlaces.csv`, y las figuras si se piden.

Qué se reporta en el método: archivo de origen y columna, tesauro (número de reglas y criterio), umbral, número de nodos y de enlaces, número de clústeres, modularidad y cuántas particiones distintas aparecieron en las 50 semillas.

Lectura prudente:

- Los clústeres agrupan vocabulario que aparece junto, no escuelas de pensamiento. La interpretación temática es una inferencia y se rotula así.
- Con pocas decenas de documentos, la red describe ese corpus. No se generaliza al campo.
- Un tesauro distinto produce una red distinta: por eso se reporta.
- Si aparecen varias particiones con modularidad similar, la estructura no es estable y se dice.

## Estructura del manuscrito por defecto

Resumen estructurado (extensión según la revista; 250 palabras como valor provisional) · 1. Introducción · 2. Metodología de la revisión · 3 a n. Un apartado por pilar · Síntesis crítica y vacíos · Agenda de investigación · Referencias · Material suplementario (ecuaciones completas, tabla de codificación y datos de la red).

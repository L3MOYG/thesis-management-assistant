# El libro del corpus

`01_Literatura/Corpus_Fuentes.xlsx` lo crea `crear_corpus.py`. Fila 1: título. Fila 2: nota de alcance. Fila 4: encabezados. Los datos empiezan en la fila 5. No cambies los nombres de los encabezados: las utilidades los reconocen por nombre.

## Hoja Corpus

Una fila por fuente incluida o candidata, ordenada por aporte a la obra propia.

| Columna | Contenido | Origen |
|---|---|---|
| ID | Identificador estable de la fuente (F01, F02...) | Asignado al entrar |
| Autores | Separados por punto y coma, apellido primero | Verificado por DOI |
| Año | Año de publicación | Verificado por DOI |
| Título | Título completo | Verificado por DOI |
| Revista | Revista o actas | Verificado por DOI |
| Palabras clave | Las de los autores, separadas por punto y coma | Exportación de la base o artículo |
| País | País de la institución del primer autor | Artículo; si no se comprobó, por confirmar |
| ¿Qué se hizo? | Objetivo y objeto del estudio | Lectura |
| ¿Cómo se hizo? | Diseño, muestra, instrumentos y análisis | Lectura |
| Resultados obtenidos | Hallazgos con cifras, unidades y ubicación | Lectura |
| Aporte a la obra propia | Para qué sirve esta fuente en la tesis | Juicio, confirmado por el autor |
| DOI | Sin prefijo de URL | Verificado |
| Cuartil (fuente y año) | Por ejemplo: Q1 (índice, 2024) | Índice de revistas |
| Acceso abierto (estado y enlace) | Estado y ubicación recuperable | Metadatos abiertos |
| Tipo documental | Artículo, revisión, ponencia | Verificado |
| Pilar | Pilar que atiende, o integración | Juicio |
| Fase | Fase del estudio a la que sirve | Juicio |
| Vacío que sustenta | ID del vacío y, si la hay, frase literal con su ubicación | Lectura |
| Nivel de lectura | Texto completo o solo resumen | Declarado |
| Estado de verificación | Ver estados | Resultado de la cadena |
| Orden de aporte | Entero, 1 es la que más aporta | Propuesto y confirmado |

## Estados de verificación

| Estado | Significado |
|---|---|
| por confirmar | Candidato sin comprobar, o con una comprobación fallida. Indica cuál falta |
| metadatos verificados | Pasó metadatos y acceso; faltan cuartil o lectura |
| verificada | Pasó las cuatro comprobaciones y los criterios de la Ficha |
| caso abierto | Incumple un criterio y espera decisión del autor |
| excepción documentada | Incumple un criterio y el autor decidió incluirla; la decisión está registrada |
| excluida | El autor decidió excluirla; se conserva la fila en Casos_abiertos, no en Corpus |

## Hoja Trazabilidad_busqueda

Una fila por ecuación o consulta ejecutada. La llena `buscar-literatura`. Esta skill solo actualiza las columnas "A texto completo" e "Incluidos" cuando cambia el resultado de una búsqueda.

## Hoja Obras_fundamentales

Marco teórico, no antecedentes. Exentas de la ventana temporal. Columnas: ID, autores, año, título, fuente, DOI, acceso, pilar que sustenta, papel teórico, criterio que la justifica y estado de verificación. El criterio que la justifica debe nombrar las tres condiciones: raíz en la red de citas, sustento teórico de un pilar y cumplimiento del criterio de acceso.

## Hoja Casos_abiertos

Una fila por fuente o parámetro que incumple un filtro.

| Columna | Contenido |
|---|---|
| Fuente o parámetro | Referencia breve |
| Criterio que no cumple | El de la Ficha, nombrado tal cual |
| Evidencia | El dato verificado que muestra el incumplimiento |
| Opciones | Las que el autor tiene, con la consecuencia de cada una |
| Decisión del autor | Vacía hasta que decida |
| Fecha de la decisión | |

Presentación de un caso al autor, en prosa breve: qué fuente es y por qué interesa, qué criterio incumple y con qué evidencia, qué opciones hay y qué implica cada una para el corpus. Sin recomendar por defecto la inclusión.

## Lectura con herramientas de extracción

Cuando una herramienta extrae campos de varios artículos a la vez (métodos, resultados, limitaciones, vacío declarado):

1. Úsala para priorizar qué leer primero y para localizar el pasaje.
2. Abre el texto y confirma cada campo antes de pasarlo al corpus.
3. Una frase atribuida a los autores solo se registra como literal si la leíste en el artículo, con su ubicación.
4. Lo que no pudiste confirmar no entra, o entra marcado por confirmar.

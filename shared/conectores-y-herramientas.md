# Conectores y herramientas

El plugin nombra las herramientas externas por categoría, con el marcador `~~categoría`. No depende de ningún proveedor y no recomienda uno sobre otro. Cada categoría tiene una ruta de respaldo que funciona sin conector. La lista de opciones por categoría está en `CONNECTORS.md`, en la raíz del plugin.

## Detección al empezar

1. Revisa qué herramientas ofrece la sesión y clasifícalas en las categorías de la tabla.
2. Compara con la fila "Conectores y herramientas detectados" de la Ficha. Si cambió, actualízala.
3. Para cada categoría que la tarea necesita y que no está disponible, aplica la ruta de respaldo y dilo en una línea. No detengas el trabajo por un conector que falta.
4. Si la sesión permite sugerir conectores, ofrece una sola vez el de la categoría que falta. Si el autor lo declina, no insistas.

No afirmes que un conector existe, ni lo que puede hacer, sin haberlo visto en la sesión.

## Categorías

| Marcador | Para qué se usa | Ruta de respaldo sin conector |
|---|---|---|
| `~~base bibliográfica` | Búsqueda primaria con ecuación booleana y conteo exacto de resultados | El autor ejecuta la ecuación en la web de la base con su acceso institucional, anota el número de resultados y exporta CSV, RIS o BibTeX a `01_Literatura/exportaciones/` |
| `~~búsqueda académica` | Búsqueda semántica complementaria y exploración inicial | Búsqueda web general, declarada como exploratoria; o solo la base bibliográfica |
| `~~lectura de artículos` | Leer el texto completo y extraer campos de varios artículos | El autor coloca los PDF en `01_Literatura/PDF/` y se leen directamente |
| `~~metadatos abiertos` | Verificar por DOI título, autores, año, revista y acceso abierto | `verificar_doi.py` si la sesión tiene red; si no, el dato queda por confirmar y el autor ejecuta la utilidad en su equipo |
| `~~índice de revistas` | Cuartil por revista y año | El autor descarga el archivo anual del índice y `verificar_doi.py --scimago` lo cruza por ISSN |
| `~~red de citas` | Detectar obras fundamentales como raíces de citación | Rastreo manual de las referencias compartidas por las fuentes del corpus |
| `~~gestor de referencias` | Biblioteca final y generación de la bibliografía | `corpus_a_ris.py` genera `.ris` y `.bib` que el autor importa en su gestor |
| `~~almacenamiento` | Sincronizar la carpeta de trabajo | La carpeta de archivos del Project o una carpeta local conectada |
| `~~cálculo simbólico` | Contrastar una derivación o un cálculo | Las utilidades del plugin, que son la referencia |
| `~~traducción` | Resumen en otro idioma y revisión de estilo | Traducción propia, marcada para revisión del autor |
| `~~notas` y `~~correo` | Minutas con el asesor y borradores de mensajes | Archivos en `00_Gobierno/` y borradores en el chat. Nunca se envía un mensaje sin aprobación expresa |

## Reglas de uso de las herramientas de búsqueda y lectura

- El conteo que acredita una ausencia demostrable sale de una `~~base bibliográfica` con ecuación registrada. Una búsqueda semántica no produce conteos reproducibles y no sirve para eso.
- Lo que una herramienta de `~~búsqueda académica` o de `~~lectura de artículos` dice de un artículo es una pista: se confirma en el texto completo antes de entrar al corpus o a un capítulo.
- Si una herramienta entrega el DOI solo en ciertos planes, o no lo entrega, el DOI queda por confirmar hasta verificarlo con `~~metadatos abiertos`.
- Respeta las instrucciones de cita que cada conector exige en sus resultados.
- Sintaxis de las bases que el validador ya conoce: en la búsqueda avanzada web de Scopus el acceso abierto se filtra con `ACCESSTYPE ( oa )`; en Web of Science se aplica en el panel de resultados. Para otra base, pide al autor la ayuda de sintaxis de esa base y no supongas operadores.

## Skills integradas del entorno

Si la sesión ofrece skills para crear documentos de texto, hojas de cálculo, PDF, presentaciones o investigación profunda, úsalas para producir los entregables con el formato de la Ficha. Si no las ofrece, entrega Markdown o CSV y dilo.

## Utilidades del plugin

Están en la carpeta `scripts/` de la raíz del plugin: `${CLAUDE_PLUGIN_ROOT}/scripts/`. Si esa variable no se resuelve, la raíz es la carpeta que contiene `skills/`, dos niveles por encima de cualquier `SKILL.md`. Todas tienen ayuda en español con `--help`, que funciona aunque falten las dependencias. Dependencias: `scripts/requirements.txt`.

Las órdenes de este plugin se escriben con `python3`. En Windows el intérprete suele llamarse `python` o `py`: comprueba cuál existe (`python --version`) y úsalo en su lugar, sin decir que la orden falló. Se probaron con Python 3.11, 3.12 y 3.13.

| Utilidad | Qué calcula o hace | Orden mínima |
|---|---|---|
| `crear_estructura.py` | Carpetas del proyecto y plantillas, sin sobrescribir | `--destino <carpeta>` |
| `crear_corpus.py` | Libro del corpus con sus cuatro hojas | `--salida 01_Literatura/Corpus_Fuentes.xlsx` |
| `validar_ecuacion.py` | Construye, valida y traduce ecuaciones (Scopus y Web of Science) | `construir --nucleo "a\|b" --acoplamiento "c" --resultado "d"` |
| `verificar_doi.py` | Metadatos, acceso abierto y cuartil por DOI | `--corpus corpus.csv --columna DOI --scimago <archivo>` |
| `criterios.py` | Panel de criterios de literatura: muestra los filtros, guarda la selección del autor y la aplica a la verificación | `panel --criterios 01_Literatura/criterios_literatura.json` |
| `corpus_a_ris.py` | Exporta el corpus a RIS y BibTeX | `--corpus <libro> --ris c.ris --bib c.bib` |
| `red_coocurrencia.py` | Red de coocurrencia de palabras clave | `--datos <csv> --umbral 2 --carpeta red/` |
| `potencia.py` | Potencia, efecto mínimo detectable y tamaño de muestra | `factorial --niveles 2,3 --replicas 4 --f 0.30` |
| `matriz_corridas.py` | Matriz aleatorizada con semilla y grados de libertad | `--factores "A:a1,a2;B:b1,b2" --replicas 3 --semilla N --salida m.csv` |
| `anova_factorial.py` | ANOVA factorial con bloques, supuestos y efecto mínimo detectable | `--datos d.csv --respuesta Y1 --factores A,B` |
| `lenth.py` | Efectos activos en factoriales sin réplica | `--datos d.csv --factores A,B,C --respuesta Z1` |
| `ahp.py` | Pesos por comparación por pares con razón de consistencia | `--triangulo "3,5,2" --nombres a,b,c` |
| `deseabilidad.py` | Factibilidad, deseabilidad, sensibilidad y contraste con TOPSIS | `--datos alt.csv --config config.json` |
| `correlacion.py` | Matriz con Holm, remuestreo y valor crítico; acuerdo de Bland y Altman | `matriz --datos d.csv --columnas Y1,Y2` |
| `fiabilidad.py` | Alfa de Cronbach con intervalo y análisis de ítems | `--datos r.csv --items p1,p2,p3` |
| `auditar_documentos.py` | Cifras, pendientes, nomenclatura y citas en los documentos | `cifras --registro <csv> --rutas <carpetas>` |

Reglas de uso:

- Ejecuta la utilidad y reporta su salida. No sustituyas un cálculo por una estimación de memoria.
- Anota en el documento la orden ejecutada, para que el resultado sea reproducible.
- Si la utilidad se detiene con un mensaje, ese mensaje es el resultado: transmítelo al autor. No rodees el fallo fabricando la entrada que falta.
- Convención de potencia: f de Cohen con λ = f²·N; para un factor de dos niveles balanceado, d = 2f. Repórtala junto con cada cifra.

## Si la sesión no puede ejecutar código

Dilo al empezar. Entrega la orden exacta para que el autor la ejecute en su equipo y pídele que pegue la salida. Mientras tanto, toda cifra que dependa de ese cálculo queda por confirmar. No calcules a mano potencia, razón de consistencia ni valores críticos para presentarlos como verificados.

## Si la sesión no tiene red

`verificar_doi.py` marca cada registro como por confirmar, con el motivo. Ofrece al autor ejecutarlo en su equipo: solo necesita Python y no requiere instalar paquetes.

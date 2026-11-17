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
| `~~metadatos abiertos` | Verificar por DOI título, autores, año, revista y acceso abierto | Consulta directa de las API públicas de OpenAlex y Crossref con la herramienta de lectura web o de código, según `metodos/literatura.md`; sin red, el dato queda por confirmar |
| `~~índice de revistas` | Cuartil por revista y año | El autor descarga el archivo anual del índice y lo carga en la conversación; se cruza por ISSN según `metodos/literatura.md` |
| `~~red de citas` | Detectar obras fundamentales como raíces de citación | Rastreo manual de las referencias compartidas por las fuentes del corpus |
| `~~gestor de referencias` | Biblioteca final y generación de la bibliografía | Archivos `.ris` y `.bib` generados con la herramienta de código según `metodos/literatura.md`, que el autor importa en su gestor |
| `~~almacenamiento` | Sincronizar la carpeta de trabajo | La carpeta de archivos del Project o una carpeta local conectada |
| `~~cálculo simbólico` | Contrastar una derivación o un cálculo | La herramienta de ejecución de código, con los casos de control de `metodos/` |
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

## Cálculo con la herramienta de código

Esta es la edición del directorio: no trae utilidades ejecutables. Los cálculos los haces tú con la herramienta de ejecución de código de la sesión, siguiendo los métodos documentados en `shared/metodos/`. La edición completa, con las mismas operaciones como utilidades probadas, se instala desde el marketplace del autor del plugin; el README indica cómo.

| Operación | Método |
|---|---|
| Carpetas del proyecto, plantillas y libro del corpus | `metodos/kit-y-auditoria.md` |
| Auditoría de cifras, pendientes, nomenclatura y citas | `metodos/kit-y-auditoria.md` |
| Construir, validar y traducir ecuaciones (Scopus y Web of Science) | `metodos/literatura.md` |
| Verificar metadatos, acceso abierto y cuartil por DOI | `metodos/literatura.md` |
| Aplicar el panel de criterios a la verificación | `metodos/literatura.md` y `panel-de-criterios.md` |
| Exportar el corpus a RIS y BibTeX; red de coocurrencia | `metodos/literatura.md` |
| Potencia, efecto mínimo detectable, tamaño de muestra y matriz de corridas | `metodos/potencia-y-diseno.md` |
| ANOVA factorial, método de Lenth, correlación, acuerdo y fiabilidad | `metodos/analisis-de-datos.md` |
| Pesos por comparación por pares y deseabilidad | `metodos/ahp-y-deseabilidad.md` |

Reglas de cálculo:

- **Se calcula, no se estima.** Toda cifra sale de código ejecutado en la sesión. No presentes como verificado un valor calculado de memoria o a mano.
- **Primero el caso de control.** Cada método trae casos de control con su resultado esperado. Antes de calcular con los datos del autor, reproduce en la misma sesión el caso de control de ese método. Si no coincide dentro de la tolerancia indicada, no reportes el resultado: dilo y deja la cifra por confirmar.
- **El procedimiento se guarda.** Entrega al autor el código que ejecutaste junto con su salida, para guardarlo en `04_Datos/resultados/` (o en la carpeta del documento) con un nombre que diga qué calcula. Anota en el documento la biblioteca usada y su versión, y la semilla si hay azar.
- **Las paradas son resultados.** Si un método indica que el cálculo se detiene (falta un límite, un peso o un filtro; la matriz no es recíproca; el diseño no es un factorial completo), detente y transmite el motivo. No fabriques la entrada que falta.
- **Convención de potencia:** f de Cohen con λ = f²·N; para un factor de dos niveles balanceado, d = 2f. Repórtala junto con cada cifra. El nivel de significación y la potencia objetivo los declara el autor; mientras no lo haga, quedan por confirmar.

## Si la sesión no puede ejecutar código

Dilo al empezar. Toda cifra que dependa de un cálculo queda por confirmar, con la consulta que la resolvería. Ofrece dos salidas: abrir una sesión con ejecución de código, o usar la edición completa del plugin en Claude Code, que trae las utilidades probadas. No calcules a mano potencia, razón de consistencia ni valores críticos para presentarlos como verificados.

## Si la sesión no tiene red

La verificación por DOI necesita consultar OpenAlex o Crossref. Sin red ni herramienta de lectura web, cada registro queda por confirmar, con el motivo. No completes metadatos de memoria.

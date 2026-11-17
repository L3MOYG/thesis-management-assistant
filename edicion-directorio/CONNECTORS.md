# Conectores

## Cómo se nombran las herramientas

Los archivos del plugin usan `~~categoría` como marcador de la herramienta que cada persona tenga conectada en esa categoría. El plugin describe el flujo de trabajo por categorías y no depende de ningún producto. Ningún conector es obligatorio: cada categoría tiene una ruta de respaldo que funciona sin él, descrita en `shared/conectores-y-herramientas.md`.

El plugin no incluye archivo `.mcp.json`. Las direcciones de los servidores no pudieron comprobarse con una conexión real desde el entorno donde se construyó, y una dirección sin comprobar no se distribuye. Cada persona conecta sus herramientas desde la configuración de conectores de Claude.

## Categorías de este plugin

Las opciones se listan en orden alfabético, sin preferencia, y son ejemplos: la disponibilidad de cada conector cambia con el tiempo y con la cuenta. Antes de contar con uno, compruébalo en el directorio de conectores de Claude. La última columna resume la ruta que el plugin sigue cuando no hay conector; el detalle está en `shared/conectores-y-herramientas.md`.

| Categoría | Marcador | Para qué | Opciones | Ruta sin conector |
|---|---|---|---|---|
| Base bibliográfica | `~~base bibliográfica` | Búsqueda con ecuación booleana y conteo exacto | Scopus, Web of Science, PubMed, otras bases con búsqueda avanzada | Ejecutas la ecuación en la web de la base, con tu acceso institucional, anotas el conteo y exportas los resultados |
| Búsqueda académica | `~~búsqueda académica` | Búsqueda semántica y exploración inicial | alphaXiv, bioRxiv, Consensus, SciSpace, Wiley Scholar Gateway | Búsqueda web general, declarada como exploratoria |
| Lectura de artículos | `~~lectura de artículos` | Leer texto completo y extraer campos de varios artículos | SciSpace; lectura directa de PDF | Colocas los PDF en la carpeta del proyecto y se leen directamente |
| Metadatos abiertos | `~~metadatos abiertos` | Verificar por DOI metadatos y acceso abierto | Crossref, OpenAlex | Claude los consulta con la herramienta web o de código, según `shared/metodos/literatura.md`; requiere red |
| Índice de revistas | `~~índice de revistas` | Cuartil por revista y año | SCImago Journal Rank, Journal Citation Reports | Descargas el archivo anual del índice, lo cargas en la conversación y Claude lo cruza por ISSN |
| Red de citas | `~~red de citas` | Detectar obras fundamentales | Connected Papers, Research Rabbit, Litmaps | Rastreo de las referencias compartidas por las fuentes del corpus |
| Gestor de referencias | `~~gestor de referencias` | Biblioteca final y bibliografía | EndNote, Mendeley, Zotero | Importas el archivo `.ris` o `.bib` que Claude genera con la herramienta de código |
| Almacenamiento | `~~almacenamiento` | Sincronizar la carpeta de trabajo | Dropbox, Google Drive, OneDrive | Los archivos del Project o una carpeta local conectada |
| Cálculo simbólico | `~~cálculo simbólico` | Contrastar derivaciones y cálculos | Wolfram | Los casos de control de `shared/metodos/`, que son la referencia |
| Traducción | `~~traducción` | Resumen en otro idioma | DeepL | Traducción del asistente, marcada para tu revisión |
| Notas | `~~notas` | Minutas y seguimiento con el asesor | Notion | Archivos en `00_Gobierno/` |
| Correo | `~~correo` | Borradores de mensajes al asesor | Gmail, Outlook | Borradores en el chat. Nunca se envía un mensaje sin tu aprobación expresa |

## Notas de uso

- Algunas herramientas de búsqueda entregan el DOI solo en ciertos planes. Un DOI que la herramienta no entrega queda por confirmar hasta verificarlo.
- Lo que una herramienta de búsqueda o de extracción afirma sobre un artículo es una pista. Se confirma en el texto completo.
- Cada conector puede exigir una forma de citar sus resultados: se respeta.
- El conteo que acredita una ausencia en la literatura sale de una base bibliográfica con ecuación registrada, no de una búsqueda semántica.
- El plugin no envía datos personales a estos servicios. Las consultas a las API de metadatos no llevan clave ni correo de contacto, salvo que el autor pida expresamente añadir el suyo.

## Skills integradas del entorno

El plugin aprovecha, cuando existen, las skills del entorno para crear documentos de texto, hojas de cálculo, PDF y presentaciones, y la de investigación profunda. Si no existen, entrega Markdown y CSV.

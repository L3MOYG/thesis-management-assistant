# Métodos: kit del proyecto y auditoría de documentos

Este documento describe cómo se crean, en esta edición del plugin, la estructura de carpetas del proyecto y el libro del corpus, y cómo se audita la coherencia de los documentos: cifras canónicas, marcas "por confirmar", nomenclatura y citas. Las reglas generales están en `../conectores-y-herramientas.md`, sección "Cálculo con la herramienta de código".

## Dónde se escriben los archivos

- Si la sesión tiene acceso a la carpeta del proyecto (Claude Code, o Cowork con la carpeta conectada), los archivos se escriben allí.
- Si no lo tiene, la herramienta de código genera los archivos en su espacio de trabajo y los entrega como descarga: un `.zip` con la estructura, o el archivo suelto. Se dice al autor dónde debe colocarlos.
- En ningún caso se sobrescribe un archivo que ya existe: se conserva y se informa. La operación puede repetirse sin riesgo, por ejemplo para añadir una carpeta que faltaba.
- Antes de escribir se puede mostrar la lista de lo que se crearía y lo que se conservaría, sin escribir nada.

## 1. Estructura de carpetas

Cada carpeta lleva un `LEEME.md` con un título (la ruta de la carpeta) y esta descripción:

| Carpeta | Descripción del LEEME |
|---|---|
| 00_Gobierno | Estado del proyecto: ficha, registro de decisiones, registro de cifras, plan de hilos, instrucciones del Project y manual. Es lo primero que lee cada hilo. |
| 01_Literatura | Protocolo de búsqueda, libro del corpus, exportaciones de las bases y archivos para el gestor de referencias. |
| 01_Literatura/PDF | Textos completos. Antecedentes: NN_PrimerAutor_Año.pdf, con NN igual al orden de aporte. Obras fundamentales: F_PrimerAutor_Año.pdf. |
| 01_Literatura/exportaciones | Archivos exportados de las bases bibliográficas (CSV, RIS, BibTeX), sin editar. |
| 02_Planteamiento | Mapa de vacíos con su evidencia y cadena lógica: vacío, pregunta, hipótesis y objetivos. |
| 03_Metodologia | Diseño por población, plan de análisis, diccionario de variables y matrices de corridas. |
| 04_Datos | Datos del estudio. |
| 04_Datos/crudos | Datos tal como salieron del instrumento. No se editan nunca. |
| 04_Datos/procesados | Datos depurados, cada uno con el procedimiento que lo generó. |
| 04_Datos/resultados | Tablas, figuras y salidas de los análisis, regenerables desde los datos procesados. |
| 05_Capitulos | Capítulos de la tesis en el formato institucional. Un archivo canónico por capítulo. |
| 06_Productos_Derivados | Artículo de revisión y otros productos que nacen del corpus de la tesis. |
| 07_Defensa | Banco de preguntas del sínodo, puntos débiles y presentación. |

Plantillas del plugin (`../../templates/`) y su destino:

| Plantilla | Carpeta |
|---|---|
| Ficha_Proyecto.md, Registro_Decisiones.md, Registro_Cifras.md (se escribe como Registro_Cifras.csv), Plan_Hilos.md, Instrucciones_Project.md | 00_Gobierno |
| Protocolo_Busqueda.md, criterios_literatura.json | 01_Literatura |
| Mapa_Vacios.md, Cadena_Logica.md | 02_Planteamiento |
| Plan_Analisis.md, Diccionario_Variables.md (se escribe como Diccionario_Variables.csv), config_deseabilidad.json | 03_Metodologia |

El manual (`../../docs/Manual_Usuario.md`) se copia a `00_Gobierno/Manual_Usuario.md`. Las plantillas se copian tal cual, sin rellenar, salvo `Registro_Cifras.md` y `Diccionario_Variables.md`: de cada una se escribe el contenido de su bloque, sin las cercas, en el archivo CSV de destino. Esas dos se guardan como Markdown porque el directorio de plugins no admite CSV; en el proyecto son CSV.

## 2. Libro del corpus

`01_Literatura/Corpus_Fuentes.xlsx`, creado con `openpyxl` en la herramienta de código. Si la biblioteca no está disponible, se crean cuatro CSV con los mismos encabezados (uno por hoja) y se dice.

**Formato común de cada hoja.** Sin líneas de cuadrícula; fuente Arial (o la que pida el autor).

- Fila 1: título, 14 pt, negrita, color 1F4E79.
- Fila 2: nota de la hoja, 9.5 pt, cursiva, color 44546A, con ajuste de texto y alineación superior; celdas combinadas desde la columna A hasta la octava (o la última, si hay menos); alto 42.
- Fila 4: encabezados, 10 pt, negrita, blancos sobre 1F4E79, centrados, con ajuste de texto; alto 32. Cada columna con su ancho.
- Filas 5 a 64: preparadas con fuente de 10 pt, ajuste de texto y alineación superior; las filas pares de datos (6, 8…) con relleno EDF3F8.
- Paneles inmovilizados en A5.

**Hojas, títulos y notas.**

1. **Corpus.** Título: el que dé el autor (por defecto "Corpus de fuentes de la tesis"). Nota, precedida del alcance si el autor lo da: "Una fila por fuente incluida. Orden de filas: por aporte a la obra propia, de mayor a menor. Lo no verificado se escribe "por confirmar". Nivel de lectura: texto completo o solo resumen."
2. **Trazabilidad_busqueda.** Título "Trazabilidad de la búsqueda". Nota: "Una fila por ecuación ejecutada. Tipo: búsqueda, prueba de ausencia o sensibilidad. Una ecuación sin fecha y sin número de resultados no existe."
3. **Obras_fundamentales.** Título "Obras fundamentales". Nota: "Marco teórico, no antecedentes. Exentas de la ventana temporal; el resto de criterios se aplica según lo declarado en la Ficha del proyecto."
4. **Casos_abiertos.** Título "Casos abiertos para decisión del autor". Nota: "Lo que no pasa un filtro no se descarta ni se incluye en silencio: se registra aquí y lo decide el autor, caso por caso."

**Columnas (ancho entre paréntesis).**

- Corpus: ID (6), Autores (26), Año (7), Título (40), Revista (24), Palabras clave (26), País (12), ¿Qué se hizo? (40), ¿Cómo se hizo? (40), Resultados obtenidos (40), Aporte a la obra propia (40), DOI (26), Cuartil (fuente y año) (16), Acceso abierto (estado y enlace) (26), Tipo documental (14), Pilar (12), Fase (10), Vacío que sustenta (14), Nivel de lectura (16), Estado de verificación (20), Orden de aporte (9).
- Trazabilidad_busqueda: ID (8), Tipo (16), Fecha (12), Base o herramienta (18), Pilar o bloque (16), Ecuación o consulta exacta (70), Filtros fuera de la ecuación (26), Resultados (11), Tras depuración (11), Cribados (10), A texto completo (10), Incluidos (10), Notas y cambios respecto de la versión anterior (40).
- Obras_fundamentales: ID (6), Autores (26), Año (7), Título (40), Fuente (24), DOI (26), Acceso abierto (estado y enlace) (26), Pilar que sustenta (16), Papel teórico (40), Criterio que la justifica (34), Estado de verificación (20).
- Casos_abiertos: ID (6), Fecha (12), Fuente o parámetro (34), Criterio que no cumple (26), Evidencia (40), Opciones (34), Decisión del autor (26), Fecha de la decisión (14).

**Comprobación.** Tras crearlo, se vuelve a abrir el libro y se comprueban los nombres de las cuatro hojas y los encabezados de la fila 4. El resultado se informa.

## 3. Auditoría de documentos

La auditoría detecta; no corrige. Lee archivos `.md`, `.txt`, `.tex`, `.bib`, `.csv`, `.rst` y `.docx` (texto del cuerpo, notas al pie, notas finales, encabezados y pies, con las tablas como celdas separadas por barras) y, si `openpyxl` está disponible, `.xlsx` (cada fila como "[hoja] celda | celda"). Los PDF no se leen: se audita el documento fuente y se dice. Se omiten las carpetas y los archivos cuyo nombre empieza por punto, `~` o `__`, y los temporales `~$`.

### Cifras canónicas

**Entrada.** `00_Gobierno/Registro_Cifras.csv`, con las columnas id, valor, unidad, descripcion y patron. Las líneas que empiezan por `#` son comentarios. Solo se auditan las filas con patrón. El patrón es una expresión regular, sin distinguir mayúsculas, con exactamente un grupo de captura para el número; por ejemplo, `(\d+)\s+parcelas`.

**Procedimiento.** Para cada cifra, se buscan todas las coincidencias del patrón en todos los documentos, excepto el propio registro. El número capturado se normaliza: se quitan espacios y la puntuación final; la forma 1.234,5 se lee como 1234.5 y, en otro caso, la coma se lee como punto decimal. Se compara con el valor canónico normalizado igual; si alguno no es número, se compara el texto.

**Salida.** Por cifra: "coherente", "N DISCREPANCIA(S)" con cada archivo, el valor que dice y su contexto, o "sin apariciones (revisa el patrón o la cifra no se usa todavía)". Al final, documentos leídos, cifras, apariciones, discrepancias y archivos omitidos. Un patrón inválido o sin un único grupo se informa y se salta. Si hay discrepancias, se recuerda que una cifra canónica solo cambia en el registro y se propaga a todos los archivos en la misma sesión.

### Marcas "por confirmar"

Se buscan las coincidencias de `por\s+confirmar`, sin distinguir mayúsculas, con hasta cinco contextos por archivo (70 caracteres a cada lado). Salida: conteo por archivo, contextos y total.

### Nomenclatura

**Entradas.** Identificadores declarados (por ejemplo, A, B, C, Y1, Y2), patrón de identificador (por defecto, una o dos mayúsculas seguidas de uno o dos dígitos, como palabra completa) y lista de ignorados (por defecto Q1, Q2, Q3, Q4, A3, A4, A5 y B5).

**Procedimiento.** Se recogen las coincidencias del patrón y, además, las letras mayúsculas sueltas que siguen a "factor", "factores", "variable", "covariable", "respuesta", "bloque" o "tratamiento". Salida: usados y no declarados (con archivo y número de apariciones) y declarados no usados.

### Citas

**Entradas.** El libro del corpus (hojas Corpus y Obras_fundamentales) o un CSV con Autores, Año y DOI, y los documentos `.docx`, `.md`, `.txt` y `.tex`.

**Procedimiento.** De cada fuente se toma el apellido del primer autor (lo anterior a la coma o, sin coma, la última palabra) y el año; la clave es el apellido sin acentos ni caracteres que no sean letras, en minúsculas, más el año. En el texto se detectan citas narrativas (Apellido, opcionalmente "et al.", "y colaboradores" o "y/and/& Apellido2", seguido de "(año)") y parentéticas (dentro de paréntesis, cada trozo separado por punto y coma con un apellido y un año). Se descartan palabras como tabla, figura, ecuación, capítulo, sección, anexo, apéndice, en, de, desde y hasta.

**Salida.** Citadas y ausentes del corpus (candidatas a revisar, con los archivos) y fuentes del corpus sin cita detectada. Es heurística: una grafía distinta oculta una cita, y las normas o manuales citados fuera del corpus aparecen como ausentes. La decisión es del autor.

## Casos de control

**Estructura.** En una carpeta vacía, la operación crea 13 carpetas con su LEEME, 12 plantillas (entre ellas `00_Gobierno/Registro_Cifras.csv` y `03_Metodologia/Diccionario_Variables.csv`, cuya última línea es la fila de encabezados), el manual y el libro del corpus, y no conserva nada. Repetida sobre la misma carpeta, no crea nada y conserva todo.

**Libro del corpus.** Las hojas son Corpus, Trazabilidad_busqueda, Obras_fundamentales y Casos_abiertos, con 21, 13, 11 y 8 columnas en la fila 4.

**Cifras.** Registro con la fila `C1,90,corridas,Corridas totales,(\d+)\s+corridas` y un documento con el texto "El diseño suma 90 corridas en total. En la sección 3 dice 96 corridas, por confirmar." Esperado: 2 apariciones y 1 discrepancia (dice 96).

**Pendientes.** Sobre el mismo documento: 1 marca "por confirmar".

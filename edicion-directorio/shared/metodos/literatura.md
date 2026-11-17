# Métodos: literatura

Este documento describe cómo se hacen, en esta edición del plugin, las operaciones mecánicas sobre la literatura: construir y validar ecuaciones de búsqueda, verificar DOI y acceso abierto, asignar el cuartil, aplicar el panel de criterios, exportar el corpus a RIS y BibTeX y construir la red de coocurrencia de palabras clave. Las reglas generales están en `../conectores-y-herramientas.md`, sección "Cálculo con la herramienta de código", y los criterios, en `../panel-de-criterios.md`.

## 1. Ecuaciones de búsqueda

### Construcción

**Entradas.** Identificador (E1, E2…), bloques de términos separados por `|`: núcleo, acoplamiento y resultado medible; año inicial y final; tipos documentales con los códigos de Scopus (`ar`, `re`, `cp`, `ch`, `bk`; por defecto `ar,re,cp`); acceso abierto sí o no; términos de exclusión; año en curso (para el intervalo de Web of Science).

**Reglas.**

1. Un término con espacio o guion va entre comillas; uno ya entrecomillado se deja como está.
2. Un bloque de varios términos se escribe `( t1 OR t2 )`; un bloque de un solo término, sin paréntesis.
3. Como máximo tres bloques AND. Un cuarto bloque se acepta solo con aviso, porque la recuperación colapsa.
4. **Scopus:** `TITLE-ABS-KEY ( b1 AND b2 AND b3 )`, seguido, si procede, de `AND PUBYEAR > (inicio − 1)`, `AND PUBYEAR < (fin + 1)`, `AND DOCTYPE ( ar OR re … )`, `AND ACCESSTYPE ( oa )` y, al final y una sola vez, `AND NOT TITLE-ABS-KEY ( exclusiones unidas por OR )`.
5. **Web of Science:** `(TS=(b1 AND b2 AND b3) AND PY=(inicio-fin) AND DT=(…))`, con 1900 si falta el inicio y el año en curso si falta el fin, seguido de `NOT TS=(exclusiones)`. Códigos: `ar` Article, `re` Review, `cp` "Proceedings Paper", `ch` "Book Chapter", `bk` Book, `ed` "Editorial Material", `le` Letter. El acceso abierto no tiene etiqueta: se aplica en Refine > Open Access.
6. Cada ecuación construida se valida con las reglas siguientes antes de entregarla.

### Validación

Es una revisión fuera de línea: no ejecuta la búsqueda ni sustituye el registro de fecha y número de resultados. Las frases entre comillas se ignoran al buscar operadores y campos.

**Errores comunes a ambas bases:** caracteres no ASCII, tabuladores o saltos de línea (comillas tipográficas y acentos rompen la búsqueda); paréntesis de cierre sin apertura o paréntesis sin cerrar; número impar de comillas; espacios sobrantes o frase vacía entre comillas; truncamiento `*` con menos de tres letras antes; operadores booleanos que no están en mayúsculas; un AND u OR sin operando.

**Scopus.** Errores: código de campo desconocido (los válidos son TITLE-ABS-KEY, TITLE-ABS, TITLE, ABS, KEY, AUTHKEY, PUBYEAR, DOCTYPE, ACCESSTYPE, DOI, LANGUAGE, SRCTYPE, SUBJAREA, SRCTITLE, AUTH, AFFIL, EXACTSRCTITLE, ISSN, PUBSTAGE, LIMIT-TO, EXCLUDE, ALL, REF y AFFILCOUNTRY); OPENACCESS, que la búsqueda avanzada web no reconoce y puede devolver cero documentos; AND NOT más de una vez; códigos de campo en minúsculas; comodín dentro de llaves; PUBYEAR sin operador y año; NOT sin AND. Avisos: AND después del bloque AND NOT; más de tres bloques en el núcleo; paréntesis alrededor de un solo término; sin bloque AND NOT (confirmar que no hay exclusiones permanentes); sin PUBYEAR.

**Web of Science.** Errores: etiqueta desconocida (las válidas son TS, TI, AB, AK, KP, PY, DT, DO, LA, SO, AU, WC, CU y ALL); AND NOT en lugar de NOT; llaves; sintaxis de Scopus que quedó en la ecuación; PY mal escrito (se usa PY=(AAAA-AAAA)). Avisos: sin PY; más de tres bloques; NOT sin la parte positiva entre paréntesis, porque NOT tiene precedencia; el acceso abierto se aplica en Refine.

### Traducción de Scopus a Web of Science

Se toma el contenido del primer `TITLE-ABS-KEY ( … )`, los años de `PUBYEAR >` (más 1) y `PUBYEAR <` (menos 1), los códigos de `DOCTYPE` y el contenido del bloque `AND NOT TITLE-ABS-KEY ( … )`, y se arma la forma de Web of Science de la regla 5. La traducción se valida. Se advierte que TS no busca en las palabras clave indexadas y que los conteos de ambas bases no son comparables uno a uno.

### Registro

Cada ecuación ejecutada se anota en la hoja Trazabilidad_busqueda con su ID, base, ecuación exacta, fecha y número de resultados. Una ecuación sin conteo registrado no existe. Si los resultados superan el umbral de depuración del panel, se depura antes de cribar.

## 2. Verificación de DOI y acceso abierto

**Normalización.** Se quitan el prefijo `https://doi.org/` (o `dx.doi.org`) y `doi:`, los espacios y un punto final, y se pasa a minúsculas. Lo que no tiene forma de DOI queda por confirmar con la nota "no tiene forma de DOI: revisar la transcripción".

**Consulta.** Con la herramienta web o con la herramienta de código, si tiene red:

1. OpenAlex por lotes de hasta 40 DOI: `https://api.openalex.org/works?filter=doi:DOI1|DOI2|…&per-page=50`. Cada obra devuelta queda "verificado".
2. Para cada DOI que no aparezca, Crossref: `https://api.crossref.org/works/DOI`. Si responde, queda "verificado parcialmente", con la nota de que Crossref no informa acceso abierto.
3. Si ninguno responde, queda "por confirmar", con el motivo de cada servicio (no encontrado, límite de tasa 429, acceso denegado, sin conexión) y la consulta que lo resuelve: abrir `https://doi.org/DOI` y repetir con red.
4. No se reintenta en silencio. No se usa clave de API. No se envía un correo de contacto salvo que el autor lo pida expresamente y lo escriba él.

**Campos.** El resultado tiene, en este orden, las columnas doi, estado, titulo, anio, revista, issn, primer_autor, n_autores, pais_primer_autor, tipo, idioma, volumen, numero, paginas, acceso_abierto, estado_oa, enlace_oa, licencia, citas, retractado, cuartil, fuente_verificacion, fecha_verificacion y nota.

- Desde OpenAlex: título; año de publicación; revista e ISSN de la ubicación principal; primer autor, número de autores y países del primer autor; tipo; idioma; volumen, número y páginas; acceso abierto, su estado y el enlace (oa_url o, en su defecto, el PDF o la página de la mejor ubicación abierta); licencia; citas; retractado (`SÍ` o `no`).
- Si OpenAlex marca la obra como abierta pero no da ninguna ubicación, acceso_abierto queda por confirmar con esa nota.
- Desde Crossref: título, año, revista, ISSN, primer autor, número de autores, tipo, idioma, volumen, número, páginas, licencia y citas. País, acceso abierto y retractación quedan por confirmar.
- Un dato ausente se escribe "por confirmar", salvo volumen, número, páginas, enlace y licencia, que quedan vacíos.

**Sin red.** Todos los registros quedan por confirmar con la consulta que lo resolvería. No se completa nada de memoria.

## 3. Cuartil

Se necesita el archivo anual del índice de revistas cargado en la conversación (por ejemplo, el CSV de SCImago Journal Rank, separado por punto y coma). Se detecta el separador, se localizan las columnas de ISSN, de cuartil y de título, y se cruzan los ISSN de cada fuente sin guion y en mayúsculas. El valor es `Qn (etiqueta)`, con la etiqueta del índice y el año del archivo; sin coincidencia, "por confirmar: ISSN no localizado en <etiqueta>". Sin archivo, el cuartil queda por confirmar y el filtro de cuartil no se resuelve. El valor es el mejor cuartil de la revista en el año del archivo, y así se declara.

## 4. Aplicar el panel de criterios

Las reglas completas, con el catálogo y el formato del archivo de selección, están en `../panel-de-criterios.md`, sección "Cómo aplicar los filtros". La entrada es la tabla de verificación de la sección 2.

## 5. Exportación a RIS y BibTeX

**Entrada.** La hoja Corpus (o Obras_fundamentales) del libro del corpus, o un CSV con las mismas columnas. La fila de encabezados es la primera de las 30 iniciales que contiene DOI y Título o Autores. Las columnas se reconocen por su nombre, sin importar el orden: id; autores; año; título; revista o fuente; DOI; palabras clave; país; aporte a la obra propia; cuartil; acceso abierto; tipo documental; pilar; fase; vacío que sustenta; estado de verificación; orden de aporte.

**Reglas.**

1. Autores separados por punto y coma o salto de línea (o por " and " si hay uno solo). Un registro sin título o sin autores se omite y se lista.
2. Tipo RIS por palabra contenida en el tipo documental: artículo o revisión, JOUR; ponencia, conference o proceedings, CPAPER; capítulo, CHAP; libro, BOOK; tesis, THES; norma, STAND; informe, RPRT; por defecto, JOUR. BibTeX: article, inproceedings, incollection, book, thesis, misc (norma) y report.
3. El año son los primeros cuatro dígitos del campo. El DOI se limpia del prefijo de doi.org; un DOI que contiene "confirmar" se trata como ausente y el registro se lista en "Sin DOI verificado".
4. Etiquetas (KW), sin repetir y en este orden: palabras clave separadas por punto y coma o coma; pilar, fase y vacío, en minúsculas y con guion bajo en lugar de espacios; Qn si el cuartil lo contiene; `acceso_abierto` si el campo empieza por "sí"; las etiquetas adicionales pedidas.
5. Nota (N1): "Aporte: …; Cuartil: …; País: …; Pilar: …; Orden de aporte: …; Verificación: …", solo con los campos presentes.
6. Registro RIS: TY, un AU por autor, TI, PY, JO (artículo) o T2 (otro tipo), DO y UR `https://doi.org/DOI` si hay DOI, KW, N1 y `ER  - `. Los registros se separan con una línea en blanco.
7. Clave BibTeX: apellido del primer autor sin acentos ni caracteres que no sean letras, más el año; la segunda clave igual lleva `b`, la tercera `c`. Campos author (autores unidos por " and "), title entre llaves dobles, year, journaltitle (artículo) o booktitle, doi y keywords; los vacíos se omiten.

**Salida.** Los archivos `.ris` y `.bib` en `01_Literatura/`, y un informe con los registros exportados, los omitidos y los que no tienen DOI verificado. En Zotero: Archivo > Importar, en una colección nueva.

## 6. Red de coocurrencia de palabras clave

**Entradas.** Un CSV con una columna de palabras clave por documento (Author Keywords de Scopus o Palabras clave de la hoja Corpus), el separador (punto y coma por defecto), un tesauro opcional con columnas `label` y `replace by`, y el umbral de ocurrencias (2 por defecto). El tesauro es una decisión del autor y se informa.

**Procedimiento.**

1. Cada palabra clave se pasa a minúsculas, se reemplaza la ligadura "ﬁ" por "fi", se normalizan los espacios y se aplica el tesauro. Se cuenta una vez por documento (conteo completo).
2. Nodos: las palabras con ocurrencias ≥ umbral, ordenadas por ocurrencias descendentes y, a igualdad, alfabéticamente. Con menos de 3 nodos se detiene: hay que bajar el umbral o ampliar el corpus.
3. Coocurrencia: para cada documento, cada par de nodos presentes suma 1.
4. Agrupamiento: Louvain ponderado con resolución 1.0 (`networkx.community.louvain_communities`) con las semillas 0 a 49; se conserva la partición de mayor modularidad y se informa cuántas particiones distintas aparecieron. Los clústeres se numeran por la suma de ocurrencias descendente.
5. Mapa: fuerza de asociación S = C / (o · oᵀ); posiciones que minimizan Σ S · D² / media(D)² con L-BFGS-B desde 30 arranques normales (`numpy.random.default_rng(1)`); se centra, se rota por SVD y se escala cada eje a [−1, 1].

**Salida.** En la carpeta que indique el plan (por ejemplo `04_Datos/resultados/red/`): `estadisticas.txt` (archivo, columna, separador, tesauro, documentos con palabras clave, palabras distintas, nodos, enlaces, fuerza total de enlace, clústeres, modularidad, particiones distintas, enlaces entre clústeres, lista de clústeres y nodos aislados), `nodos.csv` (palabra_clave, ocurrencias, cluster, grado, x, y) y `enlaces.csv` (origen, destino, coocurrencias, mismo_cluster). Las coordenadas dependen de la versión de las bibliotecas: lo que se cita en la tesis son los clústeres, los conteos y la modularidad.

## Casos de control

**Construcción.** E1 con núcleo `cover crop*|green manure`, acoplamiento `maize|corn`, resultado `yield`, desde 2019, tipos `ar,re`, acceso abierto y exclusión `greenhouse`, año en curso 2026. Esperado:

- Scopus: `TITLE-ABS-KEY ( ( "cover crop*" OR "green manure" ) AND ( maize OR corn ) AND yield ) AND PUBYEAR > 2018 AND DOCTYPE ( ar OR re ) AND ACCESSTYPE ( oa ) AND NOT TITLE-ABS-KEY ( greenhouse )`, sin errores.
- Web of Science: `(TS=(( "cover crop*" OR "green manure" ) AND ( maize OR corn ) AND yield) AND PY=(2019-2026) AND DT=(Article OR Review)) NOT TS=(greenhouse)`, sin errores y con el aviso de Refine.

**Validación.** La ecuación de Scopus `TITLE-ABS-KEY ( "cover crop*" or maize ) AND NOT TITLE-ABS-KEY ( greenhouse ) AND NOT OPENACCESS(1)` da tres errores (operador en minúsculas, OPENACCESS, AND NOT repetido) y el aviso de falta de PUBYEAR. La de Web of Science `TS=("cover crop*" AND maize) AND NOT TS=(greenhouse)` da el error de AND NOT y los avisos de falta de PY, de precedencia de NOT y de Refine.

**Exportación.** Un CSV con tres filas: (1) autores "Pérez, Ana; Ruiz, Luis", 2021, "Ensayo de control", Revista Uno, palabras "suelo; carbono", MX, aporte "Define la variable respuesta", DOI 10.1234/abc.1, cuartil "Q1 (SJR 2024)", acceso "sí: https://x.org", Artículo, P1, F1, V2, verificado, orden 1; (2) "Pérez, Ana", 2021, "Segundo ensayo", Actas Dos, "suelo", MX, DOI "por confirmar", acceso "no", Ponencia, P2, por confirmar, orden 2; (3) sin autores. Esperado: 2 exportados; omitido el 3; sin DOI verificado "Pérez 2021"; registro 1 JOUR con KW suelo, carbono, p1, f1, v2, Q1, acceso_abierto y N1 "Aporte: Define la variable respuesta; Cuartil: Q1 (SJR 2024); País: MX; Pilar: P1; Orden de aporte: 1; Verificación: verificado"; registro 2 CPAPER con T2 y sin DO; claves BibTeX `Perez2021` (article) y `Perez2021b` (inproceedings).

**Red.** Diez documentos con las palabras: (1) cover crops; soil carbon; maize. (2) Cover crops; maize; yield. (3) soil carbon; nitrogen; yield. (4) maize; yield; nitrogen. (5) cover crops; soil carbon. (6) nitrogen; fertilizer; yield. (7) fertilizer; nitrogen. (8) "soil  carbon" (con dos espacios); tillage. (9) tillage; soil carbon; erosion. (10) erosion; tillage. Umbral 2. Esperado: 8 palabras distintas y 8 nodos; 14 enlaces; fuerza total 22; 3 clústeres; modularidad 0.245; 1 partición distinta; 7 enlaces entre clústeres. Clúster 1: soil carbon (5), tillage (3), erosion (2). Clúster 2: nitrogen (4), yield (4), fertilizer (2). Clúster 3: cover crops (3), maize (3). Grados: soil carbon 6, yield 5, nitrogen 4, maize 4, cover crops 3, tillage 2, erosion 2, fertilizer 2.

La verificación de DOI no tiene caso de control fijo, porque depende de un servicio externo cuyos datos cambian. En su lugar, antes de un lote, se verifica un DOI conocido del propio corpus y se comprueba a mano en su página que el título y el año coinciden.

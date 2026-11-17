# Panel de criterios de literatura

Los criterios de inclusión de fuentes los elige el autor. El plugin no trae valores por defecto: mientras un filtro no se haya elegido vale "por confirmar" y ninguna skill lo aplica. La selección vive en `01_Literatura/criterios_literatura.json` y se refleja en la sección 4 de la Ficha. Este documento contiene el catálogo completo, el formato del archivo y las reglas para aplicarlo.

## Cuándo se abre el panel

- En `iniciar-tesis`, dentro del bloque de criterios de la entrevista.
- En `buscar-literatura` y en `verificar-fuentes`, antes de trabajar, si algún filtro sigue por confirmar.
- En `evolucionar-sistema`, cuando el autor pide cambiar un filtro.
- Siempre que el autor lo pida: "abre el panel de criterios", "quiero cambiar los filtros".

## Filtros

| Letra | Filtro | Tipo | Opciones | Cómo se comprueba |
|---|---|---|---|---|
| A | Acceso al texto completo | Una opción | Solo acceso abierto verificado; abierto o suscripción institucional; cualquier vía legal al texto completo; sin filtro | Estado de acceso abierto por DOI. Las vías no abiertas las confirma el autor |
| C | Cuartil de la revista | Una opción | Solo Q1; Q1 o Q2; Q1 a Q3; cualquier cuartil; sin filtro | Archivo anual del índice de revistas, por ISSN y año |
| V | Ventana temporal | Número de años | 5, 7, 10, 15, otro entero; sin límite | Año de publicación verificado. Las obras fundamentales quedan exentas |
| T | Tipo documental | Varias opciones | Artículo original; revisión; ponencia; libro o capítulo; tesis; preprint; informe o norma; sin filtro | Tipo declarado en los metadatos |
| I | Idioma | Varias opciones | Español; inglés; portugués; francés; otro código de dos letras; sin filtro | Idioma declarado en los metadatos, si existe |
| P | Máximo por primer autor | Número | 1, 2, 3, otro entero; sin filtro | Apellido e inicial del primer autor. Se presenta como posible coincidencia |
| R | Fuentes retractadas | Una opción | Señalarlas como caso abierto; permitirlas con nota | Marca de retractación en los metadatos |
| M | Mínimo de citas | Número | 5, 10, 20, otro entero; sin filtro | Conteo de citas en los metadatos, con su fecha |
| U | Umbral de depuración | Número | 100, 200, 300, 500, otro entero | Parámetro de la búsqueda, no de cada fuente |

La pertinencia a un pilar no es un filtro del panel: es un juicio que se hace en la criba y que confirma el autor. Las exclusiones permanentes de la búsqueda tampoco: van en el bloque NOT del protocolo.

## Catálogo con códigos y valores

Cada opción tiene un código (letra y número) para responder sin herramienta de preguntas, y un valor que se guarda en el archivo. En los filtros de una o varias opciones, el número es la posición de la opción y 0 significa sin filtro. En los numéricos, el número es el propio valor y 0 significa sin filtro.

| Código | Valor guardado | Etiqueta | Nota para el autor |
|---|---|---|---|
| A1 | `abierto` | Solo acceso abierto verificado, con ubicación recuperable | Más estricto: corpus menor y comprobable por cualquiera |
| A2 | `abierto_o_institucional` | Acceso abierto o texto accesible con la suscripción institucional | |
| A3 | `texto_completo` | Cualquier vía legal al texto completo (préstamo, compra o copia del autor) | Más laxo: corpus mayor, acceso que declara el autor |
| A0 | `sin_filtro` | Sin filtro | |
| C1 | `Q1` | Solo Q1 | Se verifica por revista y año |
| C2 | `Q2` | Q1 o Q2 | |
| C3 | `Q3` | Q1 a Q3 | |
| C4 | `Q4` | Cualquier cuartil: basta con que la revista esté en el índice | Ponencias, libros y tesis no tienen cuartil: quedan por confirmar |
| C0 | `sin_filtro` | Sin filtro | |
| V5, V7, V10, V15 o V y otro entero | el número de años | Últimos n años | Las obras fundamentales quedan exentas |
| V0 | `0` | Sin límite | |
| T1 | `articulo` | Artículo original | Selección múltiple, por ejemplo T1,2,3 |
| T2 | `revision` | Artículo de revisión | |
| T3 | `ponencia` | Ponencia en actas de congreso | |
| T4 | `capitulo_libro` | Libro o capítulo de libro | |
| T5 | `tesis` | Tesis | |
| T6 | `preprint` | Preprint, sin revisión por pares | Si se admite, se dice |
| T7 | `informe_norma` | Informe técnico o norma | |
| T0 | `sin_filtro` | Sin filtro | |
| I1 | `es` | Español | Selección múltiple. Otros códigos ISO 639-1 de dos letras se escriben directamente en el archivo |
| I2 | `en` | Inglés | |
| I3 | `pt` | Portugués | |
| I4 | `fr` | Francés | |
| I0 | `sin_filtro` | Sin filtro | |
| P1, P2, P3 o P y otro entero | el número | Hasta n fuentes por primer autor | Evita que un solo grupo domine el corpus |
| P0 | `0` | Sin filtro | |
| R1 | `excluir` | Señalarlas como caso abierto | No admite "sin filtro": una retractación siempre se informa |
| R2 | `permitir_con_nota` | Permitirlas con nota, por ejemplo cuando son objeto de estudio | |
| M5, M10, M20 o M y otro entero | el número | Al menos n citas | Penaliza los trabajos recientes. Úsalo con una ventana amplia o déjalo sin filtro |
| M0 | `0` | Sin filtro | |
| U100, U200, U300, U500 o U y otro entero | el número | n resultados | Por encima del umbral, la ecuación se depura antes de cribar. No admite 0 |

Los códigos se separan con espacios o punto y coma, por ejemplo `A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`. Un código que no sigue la forma letra y número, una letra que no existe, una posición fuera del panel, varias posiciones en un filtro de una sola opción o varios números en un filtro numérico son errores: se dice cuál y se vuelve a preguntar.

## Perfiles de partida

Un perfil llena todos los filtros de una vez. Es un atajo, no una recomendación: el autor ajusta después lo que quiera.

| Filtro | Estricto | Equilibrado | Amplio |
|---|---|---|---|
| Acceso | Solo acceso abierto | Abierto o institucional | Cualquier vía legal |
| Cuartil | Q1 o Q2 | Q1 o Q2 | Cualquier cuartil |
| Ventana | 7 años | 10 años | 15 años |
| Tipo documental | Artículo, revisión, ponencia | Artículo, revisión, ponencia | Los anteriores, más libro o capítulo y tesis |
| Idioma | Sin filtro | Sin filtro | Sin filtro |
| Máximo por primer autor | 1 | 2 | Sin filtro |
| Retractadas | Caso abierto | Caso abierto | Caso abierto |
| Mínimo de citas | Sin filtro | Sin filtro | Sin filtro |
| Umbral de depuración | 300 | 300 | 300 |

En códigos: estricto es `A1 C2 V7 T1,2,3 I0 P1 R1 M0 U300`; equilibrado, `A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`; amplio, `A3 C4 V15 T1,2,3,4,5 I0 P0 R1 M0 U300`.

## Cómo presentar el panel

1. **Explica en dos frases** qué se va a elegir y qué consecuencia general tiene: filtros más estrictos dan un corpus menor y más fácil de defender; filtros más laxos dan un corpus mayor y más trabajo de verificación.
2. **Pregunta primero por el perfil:** estricto, equilibrado, amplio o filtro por filtro.
3. **Presenta los filtros como panel de selección.**
   - Si la sesión ofrece una herramienta de preguntas con opciones, úsala: una pregunta por filtro, con sus opciones tal como están en el catálogo y la consecuencia de cada una en una línea. Marca como selección múltiple el tipo documental y el idioma. Agrupa los filtros en tandas del tamaño que la herramienta admita, en el orden del catálogo. Si el autor partió de un perfil, pregunta solo por los filtros que quiera ajustar.
   - Si la sesión no la ofrece, muestra el panel a partir del catálogo de este documento: para cada filtro, su letra, su nombre, su tipo, la selección vigente, sus códigos con la etiqueta y la nota. Pide que responda con los códigos, por ejemplo `A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`.
4. **No elijas por el autor.** Si duda entre dos opciones, di qué cambia en el corpus con cada una, con un número si existe (por ejemplo, cuántas fuentes ya verificadas dejarían de cumplir), y espera. "No lo sé todavía" deja el filtro por confirmar.
5. **Señala las combinaciones que se contradicen** antes de guardar: un mínimo de citas alto con una ventana corta deja fuera casi todo lo reciente; admitir tesis o ponencias con un filtro de cuartil las deja siempre por confirmar, porque no tienen cuartil.

## Cómo guardar la selección

El archivo `01_Literatura/criterios_literatura.json` tiene esta forma (la plantilla está en `../templates/criterios_literatura.json`):

```json
{
  "_nota": "Selección del autor en el panel de criterios. null significa \"por confirmar\": el filtro no se ha elegido y no se supone. \"sin_filtro\" (o 0 en los numéricos) es una elección.",
  "version": 1,
  "perfil": "equilibrado",
  "fecha_seleccion": "AAAA-MM-DD",
  "filtros": {
    "acceso": "abierto_o_institucional",
    "cuartil": "Q2",
    "ventana": 10,
    "tipos": ["articulo", "revision", "ponencia"],
    "idiomas": "sin_filtro",
    "max_por_primer_autor": 2,
    "retractadas": "excluir",
    "citas_minimas": 0,
    "umbral_depuracion": 300
  }
}
```

Reglas al guardar:

1. Se parte de la selección vigente (o de la plantilla, si no existe) y se aplican, en este orden, el perfil elegido, los códigos y los ajustes de filtros sueltos.
2. Cada valor se valida contra el catálogo: los numéricos son enteros no negativos (el umbral de depuración, positivo); los de una opción son uno de sus valores o `sin_filtro` (salvo retractadas); los de varias opciones son una lista sin repetidos y no vacía, o `sin_filtro`. En idiomas se admite cualquier código de dos letras minúsculas. Un valor inválido no se guarda: se dice cuál y se pregunta.
3. `perfil` es el nombre del perfil si la selección coincide con él; si el autor lo ajustó, el nombre seguido de " (ajustado)"; sin perfil, "personalizado". `fecha_seleccion` es la fecha del día.
4. Un filtro que el autor no eligió queda en `null`.

Después de guardar:

1. Copia a la sección 4 de la Ficha la tabla "Filtro | Selección vigente", con la etiqueta de cada valor ("Últimos 10 años", "Hasta 2 por primer autor", "Al menos 5 citas", "300 resultados", "sin filtro" o "por confirmar"), y el resumen de una línea al campo de criterios de `Instrucciones_Project.md`.
2. Si quedan filtros sin elegir, lístalos con la frase "Lo resuelve: el autor, en el panel".
3. Registra la decisión en `Registro_Decisiones.md`, con la fecha y el motivo si el autor lo dio.
4. Si las instrucciones del Project ya estaban pegadas, avisa al autor de que debe actualizarlas con el nuevo resumen.

Con la herramienta de código, escribe el archivo y vuelve a leerlo para comprobar que es JSON válido. Sin ella, edítalo a mano con los mismos valores y dilo.

## Cómo aplicar los filtros

**Entrada.** La tabla de verificación de DOI (`metodos/literatura.md`, sección 2), con el cuartil asignado (sección 3). Para las obras fundamentales, se verifica esa hoja por separado y se aplica sin la ventana temporal.

**Parada.** Si algún filtro está en `null`, no se aplica nada: se listan los filtros sin elegir y se abre el panel. No se supone ningún valor.

**Año de referencia.** El de la fecha del día, salvo que el autor fije otro. Se declara al informar del resultado.

**Reglas por fuente.** Un dato vacío o que contiene "por confirmar" es desconocido.

1. Fuente con estado "por confirmar": veredicto "por confirmar" en todos los filtros, porque no está verificada.
2. Acceso (si hay filtro): desconocido, por confirmar; no abierta con el filtro `abierto`, incumple; no abierta con los otros, por confirmar, porque el autor confirma la vía de acceso declarada.
3. Cuartil (si hay filtro): sin Qn en el dato, por confirmar; Qn peor que el pedido, incumple.
4. Ventana (si es distinta de 0 y la fuente no está exenta): año no numérico, por confirmar; año anterior a (año de referencia − ventana), incumple.
5. Tipo documental (si hay filtro): se traduce el tipo de los metadatos a las categorías del catálogo con esta tabla; un tipo desconocido o que no figura queda por confirmar, con el tipo recibido; uno que no está entre los elegidos, incumple.
   - `articulo`: article, journal-article.
   - `revision`: review.
   - `ponencia`: conference-paper, conference-abstract, proceedings-article, proceedings.
   - `capitulo_libro`: book-chapter, book-section, book-part, book, monograph, edited-book, reference-book.
   - `tesis`: dissertation, thesis.
   - `preprint`: preprint, posted-content.
   - `informe_norma`: report, report-component, standard.
6. Idioma (si hay filtro): desconocido, por confirmar; las dos primeras letras no están entre las elegidas, incumple.
7. Máximo por primer autor (si es distinto de 0): la clave es el último apellido más la inicial del primer nombre, sin acentos y en minúsculas, a partir del nombre del primer autor. Se cuentan las fuentes de toda la tabla con la misma clave; si superan el máximo, incumple, como "posible mismo primer autor". Sin primer autor, por confirmar.
8. Retractación: `SÍ` con el filtro `excluir`, incumple; con `permitir_con_nota`, pasa con la nota "retractada". Desconocida, por confirmar.
9. Mínimo de citas (si es distinto de 0): no numérico, por confirmar; menor que el mínimo, incumple.

**Veredicto.** Si incumple algún filtro, "caso abierto", con todo lo que incumple; si no incumple ninguno pero alguno está por confirmar, "por confirmar", con lo que falta; si no, "pasa". Un caso abierto no es una exclusión: va a la hoja Casos_abiertos y decide el autor.

**Salida.** Un resumen (fuentes, pasan, casos abiertos, por confirmar y año de referencia), una línea por DOI y el archivo `01_Literatura/casos_criterios.csv` con las columnas doi, primer_autor, anio, veredicto, incumple, por_confirmar y nota.

**Caso de control.** Selección equilibrada (`A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`), año de referencia 2026 y cuatro fuentes verificadas: (a) abierta, Q1, 2020, article, en, primer autor "Ana Pérez", 3 citas, no retractada; (b) no abierta, Q3, 2022, article, primer autor "Luis Ruiz", no retractada; (c) abierta, cuartil por confirmar, 2014, book-chapter, primer autor "Eva Soto", no retractada; (d) estado por confirmar. Esperado: (a) pasa; (b) caso abierto por cuartil Q3, con el acceso por confirmar; (c) caso abierto por ventana (2014 es anterior a 2016) y por tipo documental `capitulo_libro`, con el cuartil por confirmar; (d) por confirmar en todos los filtros.

## Límites de la comprobación automática

- El tipo documental y el idioma proceden de los metadatos abiertos y pueden estar mal clasificados: una ponencia puede figurar como artículo. Ante la duda, manda el documento.
- La coincidencia de primer autor compara apellido e inicial. No distingue homónimos ni reúne variantes de un mismo nombre.
- El conteo de citas cambia con el tiempo y entre fuentes de metadatos. Se registra con su fecha.
- El acceso por suscripción institucional o por otra vía legal no puede comprobarse con los metadatos: lo declara el autor para cada fuente.
- Sin el archivo del índice de revistas, el cuartil queda por confirmar y el filtro no se resuelve.

## Cambiar la selección más adelante

Un cambio de filtros con el corpus ya construido pasa por `evolucionar-sistema`: se vuelven a aplicar los filtros con la selección nueva, se informa al autor de cuántas fuentes cambian de veredicto y solo entonces se guarda. Un filtro más laxo no incorpora fuentes por sí solo: hay que buscarlas y verificarlas. Un cambio hecho después de ver los resultados de la búsqueda se anota como cambio de protocolo.

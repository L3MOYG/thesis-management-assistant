# Panel de criterios de literatura

Los criterios de inclusión de fuentes los elige el autor. El plugin no trae valores por defecto: mientras un filtro no se haya elegido vale "por confirmar" y ninguna skill lo aplica. La selección vive en `01_Literatura/criterios_literatura.json` y se refleja en la sección 4 de la Ficha. La utilidad `criterios.py` la muestra, la guarda y la aplica.

## Cuándo se abre el panel

- En `iniciar-tesis`, dentro del bloque de criterios de la entrevista.
- En `buscar-literatura` y en `verificar-fuentes`, antes de trabajar, si algún filtro sigue por confirmar.
- En `evolucionar-sistema`, cuando el autor pide cambiar un filtro.
- Siempre que el autor lo pida: "abre el panel de criterios", "quiero cambiar los filtros".

## Filtros

El catálogo vigente, con sus opciones y sus códigos, lo imprime `criterios.py panel` (o `criterios.py panel --json`). Esta tabla lo resume.

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

## Cómo presentar el panel

1. **Explica en dos frases** qué se va a elegir y qué consecuencia general tiene: filtros más estrictos dan un corpus menor y más fácil de defender; filtros más laxos dan un corpus mayor y más trabajo de verificación.
2. **Pregunta primero por el perfil:** estricto, equilibrado, amplio o filtro por filtro.
3. **Presenta los filtros como panel de selección.**
   - Si la sesión ofrece una herramienta de preguntas con opciones, úsala: una pregunta por filtro, con sus opciones tal como están en el catálogo y la consecuencia de cada una en una línea. Marca como selección múltiple el tipo documental y el idioma. Agrupa los filtros en tandas del tamaño que la herramienta admita, en el orden del catálogo. Si el autor partió de un perfil, pregunta solo por los filtros que quiera ajustar.
   - Si la sesión no la ofrece, muestra la salida de `criterios.py panel` y pide que responda con los códigos, por ejemplo `A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`. Sin ejecución de código, reproduce el panel a partir de la tabla de filtros de este documento.
4. **No elijas por el autor.** Si duda entre dos opciones, di qué cambia en el corpus con cada una, con un número si existe (por ejemplo, cuántas fuentes ya verificadas dejarían de cumplir), y espera. "No lo sé todavía" deja el filtro por confirmar.
5. **Señala las combinaciones que se contradicen** antes de guardar: un mínimo de citas alto con una ventana corta deja fuera casi todo lo reciente; admitir tesis o ponencias con un filtro de cuartil las deja siempre por confirmar, porque no tienen cuartil.

## Cómo guardar la selección

```
python3 criterios.py fijar --criterios 01_Literatura/criterios_literatura.json --perfil equilibrado --ventana 5
python3 criterios.py fijar --criterios 01_Literatura/criterios_literatura.json --codigos "A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300"
python3 criterios.py mostrar --criterios 01_Literatura/criterios_literatura.json
```

Después de guardar:

1. Copia la tabla que imprime `mostrar` a la sección 4 de la Ficha, y el resumen de una línea al campo de criterios de `Instrucciones_Project.md`.
2. Registra la decisión en `Registro_Decisiones.md`, con la fecha y el motivo si el autor lo dio.
3. Si las instrucciones del Project ya estaban pegadas, avisa al autor de que debe actualizarlas con el nuevo resumen.

Sin ejecución de código, edita el archivo JSON a mano con los mismos valores y dilo.

## Cómo aplicar los filtros

```
python3 criterios.py aplicar --criterios 01_Literatura/criterios_literatura.json \
  --verificacion 01_Literatura/verificacion.csv --salida 01_Literatura/casos_criterios.csv
```

- La entrada es la salida de `verificar_doi.py`. Para las obras fundamentales, verifica esa hoja por separado y añade `--exentas-de-ventana`.
- El veredicto por fuente es "pasa", "caso abierto" o "por confirmar". Un caso abierto no es una exclusión: va a la hoja Casos_abiertos y decide el autor.
- La utilidad se detiene si falta elegir algún filtro. No la sortees suponiendo un valor: abre el panel.
- Declara el año de referencia de la ventana cuando informes del resultado.

## Límites de la comprobación automática

- El tipo documental y el idioma proceden de los metadatos abiertos y pueden estar mal clasificados: una ponencia puede figurar como artículo. Ante la duda, manda el documento.
- La coincidencia de primer autor compara apellido e inicial. No distingue homónimos ni reúne variantes de un mismo nombre.
- El conteo de citas cambia con el tiempo y entre fuentes de metadatos. Se registra con su fecha.
- El acceso por suscripción institucional o por otra vía legal no puede comprobarlo la utilidad: lo declara el autor para cada fuente.
- Sin el archivo del índice de revistas, el cuartil queda por confirmar y el filtro no se resuelve.

## Cambiar la selección más adelante

Un cambio de filtros con el corpus ya construido pasa por `evolucionar-sistema`: se vuelve a ejecutar `aplicar` con la selección nueva, se informa al autor de cuántas fuentes cambian de veredicto y solo entonces se guarda. Un filtro más laxo no incorpora fuentes por sí solo: hay que buscarlas y verificarlas. Un cambio hecho después de ver los resultados de la búsqueda se anota como cambio de protocolo.

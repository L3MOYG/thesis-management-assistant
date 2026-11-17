# Formato de entregables

Los valores de esta guía son valores por defecto. Prevalecen, en este orden: la plantilla o normativa institucional registrada en la Ficha, lo que el autor haya fijado en la sección 7 de la Ficha y, a falta de ambos, lo que sigue.

## Nombres y versiones

- Documentos: `Tema_Subtema.ext`, sin espacios y sin acentos en el nombre del archivo.
- PDF de antecedentes: `NN_PrimerAutor_Año.pdf`, donde `NN` es la posición en el orden de aporte. PDF de obras fundamentales: `F_PrimerAutor_Año.pdf`.
- No se crean sufijos de versión. Se sobrescribe el archivo canónico. Si está bloqueado por otra aplicación, se informa y se espera.
- Los datos crudos no se editan nunca. Toda transformación produce un archivo nuevo en `04_Datos/procesados/`, con el procedimiento que lo generó.

## Documentos de texto

- Formato por defecto: DOCX. LaTeX solo a petición del autor o por exigencia institucional; nunca se mezclan ambos en un capítulo.
- Tipografía Arial, cuerpo de 11 pt, página Carta, márgenes de 2.54 cm, interlineado de 1.15 y párrafos justificados.
- Títulos en `#1F4E79`. Tablas con encabezado en ese color y texto blanco, filas alternadas en `#F5F9FC` y notas al pie de tabla en gris `#44546A`, cursiva de 9.5 pt.
- Fórmulas en bloque centrado y numeradas cuando se citan en el texto.
- Si se pide LaTeX: plantilla institucional o clase `article`, bibliografía con `biblatex` y `biber`, tablas con `booktabs`, figuras con `\caption` y `\label`.

## Hojas de cálculo

- Arial, encabezado en `#1F4E79` con texto blanco, filas alternadas en `#EDF3F8`, ajuste de texto, panel inmovilizado bajo el encabezado y sin líneas de cuadrícula.
- Fila 1: título. Fila 2: nota de alcance. Fila 4: encabezados.
- Toda matriz de corridas declara su semilla en el propio archivo y es regenerable.

## Figuras y tablas

- Cada figura y cada tabla se cita en el texto antes de aparecer y tiene título que se entiende sin leer el párrafo.
- Las unidades van en el encabezado de la columna o en el eje. Los decimales son coherentes dentro de una misma columna.
- Toda tabla de resultados estadísticos incluye n, grados de libertad y, para efectos no significativos, el efecto mínimo detectable.
- Verifica el aspecto final antes de entregar: convierte a PDF o revisa la vista de impresión. Una columna que parte palabras a media sílaba es un defecto.

## Citación

- Estilo: el de la Ficha. Si está por confirmar, usa APA 7.ª edición y decláralo.
- En prosa en español, cuando el autor citado es sujeto de la oración se prefiere "y colaboradores" sobre "et al.".
- Toda afirmación técnica no trivial lleva cita. Las afirmaciones propias se marcan como tales.
- El DOI es obligatorio en la referencia. Si falta, queda por confirmar.
- No se cita lo no leído. Si solo se dispone del resumen, se declara.
- La lista de referencias se genera desde el gestor de referencias del autor; no se transcribe a mano.

## Tono: tesis y artículo

| | Tesis | Artículo de revisión |
|---|---|---|
| Extensión | Metódica y exhaustiva; desarrolla el razonamiento completo | Concisa; solo el argumento que sostiene la tesis central |
| Función del detalle | Demostrar dominio y permitir la réplica | Sostener la crítica; lo replicable va al material suplementario |
| Voz | Expositiva y didáctica; explica por qué cada decisión y no otra | Crítica y evaluativa; juzga la literatura, no la resume |
| Tratamiento de las fuentes | Describe qué hizo cada una y su aporte | Contrasta, agrupa por postura y señala contradicciones |
| Cierre | Conclusiones por objetivo específico | Vacío formulado y agenda de investigación |
| Persona gramatical | Impersonal o plural de modestia | Igual, con juicio explícito permitido |

El capítulo de antecedentes no es una lista: las fuentes dialogan entre sí. Un capítulo que enumera estudios sin ponerlos a conversar es una bibliografía comentada.

## Convención de entrega

Al entregar un archivo, el mensaje es breve y contiene tres cosas, en este orden:

1. **Qué cambió.** Una o dos frases. No se vuelve a describir el contenido del documento.
2. **Qué decisión requiere el autor.** Si no requiere ninguna, se dice.
3. **Qué queda por confirmar.** Cada dato pendiente con la consulta que lo resuelve.

Antes de entregar, aplica la lista de verificación de `reglas-de-rigor.md`.

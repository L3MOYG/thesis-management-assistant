---
name: verificar-fuentes
description: >
  Verificación del corpus bibliográfico. Esta skill se usa cuando el usuario pide "verificar las
  fuentes", "verificar los DOI", "comprobar el cuartil", "revisar si es acceso abierto", "validar
  mis referencias", "llenar la tabla de fuentes", "armar el corpus", "exportar a Zotero", "generar
  el RIS o el BibTeX" o entrega una lista de artículos para incluir. Comprueba metadatos, acceso y
  cuartil por DOI, aplica los filtros que el autor eligió en el panel de criterios, expone caso por caso lo que no pasa un filtro,
  registra la lectura de cada fuente y exporta el corpus para el gestor de referencias.
metadata:
  version: "0.3.0"
---

# Verificar las fuentes

Conviertes candidatos en un corpus en el que cada dato tiene respaldo. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/conectores-y-herramientas.md`. El significado de cada columna y los estados posibles están en `references/corpus.md`.

Archivos de la fase: `01_Literatura/Corpus_Fuentes.xlsx`, `01_Literatura/PDF/`, `01_Literatura/criterios_literatura.json` y la sección 4 de la Ficha. El panel de criterios se describe en `../../shared/panel-de-criterios.md`.

## Cadena de verificación

Cada fuente recorre cuatro comprobaciones, en este orden. Una fuente es "verificada" solo cuando pasa las cuatro; hasta entonces, cada dato sin respaldo dice "por confirmar".

| Comprobación | Contra qué | Qué se anota |
|---|---|---|
| Metadatos | `~~metadatos abiertos`, por DOI | Título, autores, año, revista, DOI normalizado |
| Acceso | `~~metadatos abiertos` (estado de acceso abierto y ubicación) o el acceso institucional declarado por el autor | Estado y enlace recuperable |
| Cuartil | `~~índice de revistas`, por revista y año | Cuartil, fuente y año del índice |
| Lectura | Texto completo en `01_Literatura/PDF/` o leído con `~~lectura de artículos` | Nivel de lectura: texto completo o solo resumen |

## Procedimiento

### 1. Reunir los DOI

Toma los candidatos de la hoja Corpus y de Obras_fundamentales. Si el autor entrega una lista suelta, un archivo exportado o referencias en texto, pásalas primero a la hoja Corpus con estado "por confirmar". Una fuente sin DOI se busca por título exacto; si no aparece, el DOI queda por confirmar y la fuente no avanza.

### 2. Verificar metadatos y acceso

Verifica los DOI de la columna DOI según `../../shared/metodos/literatura.md`, sección 2, con la herramienta web o con la herramienta de código si tiene red, y guarda la tabla en `01_Literatura/verificacion.csv`.

- El procedimiento consulta la fuente de metadatos abiertos y usa una segunda como respaldo. Lo que no puede verificarse sale "por confirmar", con el motivo.
- **Sin red en la sesión:** todos los registros saldrán por confirmar. Dilo y ofrece repetir la verificación en una sesión con acceso web, o con la edición completa del plugin en Claude Code. No completes los metadatos de memoria.
- **Si el servicio informa de límite de tasa:** no reintentes en bucle. Marca y continúa.
- Compara lo verificado con lo que estaba en el corpus. Una discrepancia de año, de autores o de título se corrige con el dato verificado y se anota; si la discrepancia sugiere que son dos obras distintas, es un caso abierto.

### 3. Verificar el cuartil

Con el archivo anual del `~~índice de revistas` descargado por el autor y cargado en la conversación, cruza por ISSN según `../../shared/metodos/literatura.md`, sección 3: el resultado es el mejor cuartil de la revista en ese año. Anota siempre fuente y año. Sin el archivo, el cuartil queda por confirmar con la consulta "índice de revistas, por título o ISSN de la revista, año de publicación". Una ponencia o una fuente no indexada no tiene cuartil: se anota así, no se le asigna uno.

### 4. Aplicar los criterios

Los criterios son los filtros que el autor eligió en el panel. Si alguno sigue por confirmar, abre el panel antes de continuar: no apliques un valor supuesto.

Aplica con la herramienta de código las reglas de `../../shared/panel-de-criterios.md`, sección "Cómo aplicar los filtros", a `01_Literatura/verificacion.csv` con la selección de `01_Literatura/criterios_literatura.json`, y guarda el resultado en `01_Literatura/casos_criterios.csv`. Antes, reproduce el caso de control de esa sección.

Para las obras fundamentales, verifica esa hoja por separado y aplica los filtros sin la ventana temporal. Declara el año de referencia de la ventana. El procedimiento no juzga la pertinencia ni las exclusiones permanentes: contrástalas tú con la Ficha.

- **Pasa:** continúa a lectura.
- **Caso abierto** (incumple un filtro): va a la hoja Casos_abiertos, con el filtro que incumple, la evidencia y las opciones (excluir, incluir como excepción documentada, reclasificar como obra fundamental o como fuente de contexto). **No decidas tú.** Presenta los casos al autor uno por uno, o agrupados si comparten causa, y registra cada decisión con su fecha.
- **Por confirmar** (falta un dato verificado): di qué dato falta y cómo se obtiene. El acceso por una vía que no es abierta lo confirma el autor para cada fuente.
- **Posible mismo primer autor,** si ese filtro está activo: la coincidencia es por apellido e inicial. Comprueba que sea la misma persona, presenta las fuentes en conflicto y cuál aporta más, y deja la elección al autor.

Si son muchos los casos abiertos por un mismo filtro, dilo con el número y pregunta al autor si quiere revisar ese filtro en el panel antes de decidir caso por caso.

No reabras una excepción que el autor ya decidió, salvo que él lo pida.

### 5. Registrar la lectura

Para cada fuente incluida, llena las columnas de contenido a partir del texto completo: qué se hizo, cómo se hizo, resultados obtenidos y aporte a la obra propia. Reglas:

- Lo que una herramienta de extracción entrega es un borrador: confírmalo en el texto antes de escribirlo.
- Cifras de resultados, con su unidad y su ubicación en el artículo.
- Si solo se dispone del resumen, el nivel de lectura es "solo resumen" y la fuente no puede sostener una afirmación técnica en un capítulo hasta leerse completa.
- "Aporte a la obra propia" es un juicio: propónlo y deja que el autor lo ajuste.
- Si los autores declaran un problema abierto, copia la frase literal con su ubicación en la columna de vacío: es evidencia para `vacios-y-planteamiento`.

### 6. Ordenar

El orden de las filas es por aporte a la obra propia, de mayor a menor. No alfabético ni cronológico. Propón el orden, pide confirmación y numera la columna "Orden de aporte". Ese número nombra los PDF: `NN_PrimerAutor_Año.pdf`.

### 7. Exportar al gestor de referencias

Exporta con la herramienta de código según `../../shared/metodos/literatura.md`, sección 5:

1. La hoja Corpus a `01_Literatura/Corpus.ris` y `01_Literatura/Corpus.bib`.
2. La hoja Obras_fundamentales a `01_Literatura/Obras_Fundamentales.ris`, con la etiqueta adicional `obra_fundamental`.

Cada registro lleva como etiquetas el pilar, la fase, el cuartil y el vacío. Con `~~gestor de referencias` conectado, ofrece cargar los registros; sin él, indica al autor que importe los archivos en una colección nueva y adjunte los PDF. La bibliografía final se genera desde el gestor, no se transcribe.

## Cierre

Aplica el cierre de hilo. Registra como cifras canónicas el número de fuentes incluidas y el de obras fundamentales. Mensaje de entrega: cuántas fuentes quedaron verificadas, cuántas con datos por confirmar y por qué, los casos abiertos que esperan decisión y los archivos generados. Siguiente paso habitual: `vacios-y-planteamiento`.

## Lo que esta skill no hace

- No afirma que una fuente es de acceso abierto, ni su cuartil, sin la comprobación correspondiente.
- No completa DOI, volumen o páginas por aproximación.
- No decide inclusiones ni exclusiones dudosas.
- No aplica un filtro que el autor no haya elegido en el panel.
- No resume como leída una fuente de la que solo se tiene el resumen.

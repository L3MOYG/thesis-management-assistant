---
name: redactar-capitulo
description: >
  Redacción de capítulos y secciones de la tesis. Esta skill se usa cuando el usuario pide
  "redactar el capítulo", "escribir la introducción", "redactar antecedentes", "escribir el marco
  teórico", "redactar la metodología", "escribir resultados", "redactar la discusión", "escribir
  conclusiones", "redactar el resumen o abstract", "mejorar la redacción de este apartado" o
  "revisar mi capítulo". Redacta borradores en el formato institucional a partir de la Ficha, el
  corpus verificado y los resultados, con cita en cada afirmación técnica, cifras tomadas del
  registro y marca "por confirmar" en todo dato sin verificar.
metadata:
  version: "0.3.0"
---

# Redactar un capítulo

Redactas borradores que el autor revisa, corrige y hace suyos. Lee antes `../../shared/reglas-de-rigor.md`, `../../shared/modelo-de-estado.md` y `../../shared/formato-entregables.md`. La estructura y los insumos de cada capítulo están en `references/estructura-por-capitulo.md`.

Antes de escribir, lee en la Ficha la política institucional sobre uso de IA. Si está por confirmar, dilo al entregar: el autor debe conocerla antes de incorporar el texto a la tesis.

## Principios

- **Solo se escribe lo que tiene respaldo.** Cada afirmación técnica no trivial lleva cita a una fuente del corpus leída a texto completo, o está marcada como afirmación propia.
- **Las cifras salen del Registro de Cifras** y de los archivos de resultados. No se redondean de memoria ni se reescriben distinto.
- **La nomenclatura es la del diccionario de variables.** No se renombra por variar el estilo.
- **Lo no verificado dice "por confirmar"**, con su consulta. Un DOI sin verificar no se completa.
- **Las limitaciones no se diluyen.** Al reescribir, las limitaciones declaradas deben seguir presentes.
- **Un archivo canónico por capítulo.** Se sobrescribe; no se crean versiones con sufijo.

## Procedimiento

### 1. Delimitar el encargo

Confirma qué capítulo o sección, con qué extensión aproximada y en qué formato (el de la Ficha; DOCX por defecto). Si existe una plantilla institucional, pídela y úsala. Si ya hay un borrador, léelo completo: se revisa lo que existe.

### 2. Comprobar los insumos

Consulta en `references/estructura-por-capitulo.md` qué necesita ese capítulo. Si falta un insumo (por ejemplo, redactar resultados sin informe de análisis, o antecedentes con fuentes en "solo resumen"), dilo antes de escribir y ofrece dos opciones: completar el insumo primero, o redactar con huecos marcados. No rellenes los huecos con contenido verosímil.

### 3. Proponer el esqueleto

Presenta el índice de la sección con una línea por apartado: qué afirma y con qué fuentes o resultados se sostiene. Para antecedentes, organiza por postura, por método o por hallazgo, no fuente por fuente. Espera el visto bueno del autor antes de redactar un capítulo completo; para una sección corta, redacta directamente y dilo.

### 4. Redactar

- Prosa continua y argumentada. Las listas se reservan para lo enumerable.
- Cada capítulo abre conectando con el anterior y cierra anticipando el siguiente.
- En antecedentes, las fuentes dialogan: quién coincide, quién discrepa, quién mide de otro modo y qué deja abierto cada grupo. Cierra el capítulo en los vacíos acreditados.
- En metodología, cada decisión responde a "¿por qué así y no de otro modo?", con su alternativa descartada.
- En resultados, usa las frases y las reglas de `../analizar-datos/references/lectura-de-resultados.md`: cada resultado con n, grados de libertad y efecto mínimo detectable; "no se detectó diferencia".
- En discusión, separa lo que los datos muestran, lo que sugieren y lo que el autor propone; contrasta con el corpus mediante la tabla de validación externa.
- En conclusiones, una por objetivo específico, sin resultados nuevos; después, limitaciones y trabajo futuro, incluidos los vacíos fuera de alcance.
- Tono de tesis: expositivo y completo. Respeta el idioma, el estilo de cita y las expresiones vetadas que registra la Ficha.

Citas: usa las claves del corpus y el estilo de la Ficha. La lista de referencias se genera desde el gestor de referencias del autor; si redactas una lista provisional, márcala como provisional y marca "por confirmar" todo DOI no verificado.

### 5. Verificar antes de entregar

Aplica la lista de verificación de las reglas de rigor y, si puedes ejecutar código:

```
python3 auditar_documentos.py cifras --registro 00_Gobierno/Registro_Cifras.csv --rutas 05_Capitulos
python3 auditar_documentos.py citas --corpus 01_Literatura/Corpus_Fuentes.xlsx --rutas 05_Capitulos/<archivo>
python3 auditar_documentos.py nomenclatura --declarados "<identificadores de la Ficha>" --rutas 05_Capitulos/<archivo>
python3 auditar_documentos.py pendientes --rutas 05_Capitulos/<archivo>
```

Corrige lo que sea un error tuyo. Lo que sea una decisión (una cita fuera del corpus, un identificador no declarado) se presenta al autor. Revisa el aspecto final de tablas y figuras en el formato de entrega.

### 6. Entregar

Guarda el capítulo en `05_Capitulos/` con el nombre canónico. Usa la skill integrada de documentos del entorno, si existe, para aplicar el formato; si no, entrega Markdown y dilo. Mensaje de entrega, breve: qué cambió, qué decisión requiere el autor y qué queda por confirmar, con el recuento de marcas pendientes.

## Revisión de un texto del autor

Cuando el autor trae su propio texto: lee completo, conserva su voz y devuelve observaciones ordenadas por gravedad. Primero, lo que un sínodo objetaría (afirmaciones sin cita, cifras que contradicen el registro, conclusiones que los datos no sostienen, limitaciones ausentes). Después, la cohesión. Al final, el estilo. Propón reescrituras solo donde las pida o donde el defecto sea de fondo, y no cambies el sentido.

## Cierre

Aplica el cierre de hilo: estado del capítulo en la Ficha, decisiones y pendientes. Siguiente paso habitual: `auditar-cohesion` al cerrar cada capítulo.

## Lo que esta skill no hace

- No inventa citas, resultados, cifras ni frases atribuidas a autores.
- No cita una fuente con nivel de lectura "solo resumen" para sostener una afirmación técnica sin declararlo.
- No presenta un borrador como texto final ni omite recordar la política de uso de IA cuando está por confirmar.

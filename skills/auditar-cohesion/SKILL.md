---
name: auditar-cohesion
description: >
  Auditoría de cohesión del corpus documental de la tesis. Esta skill se usa cuando el usuario
  pide "auditar la tesis", "revisar la coherencia", "revisar la cohesión entre capítulos",
  "verificar que las cifras coincidan", "revisar la nomenclatura", "revisar las citas", "qué quedó
  por confirmar", "revisar antes de entregar" o al cerrar un capítulo. Contrasta cifras,
  identificadores, citas y pendientes entre todos los documentos, aplica la prueba de coherencia
  de la cadena lógica y entrega un informe que distingue errores de decisiones del autor.
metadata:
  version: "0.3.0"
---

# Auditar la cohesión

Detectas contradicciones entre documentos antes de que las detecte un sínodo. Lee antes `../../shared/reglas-de-rigor.md` y `../../shared/modelo-de-estado.md`.

Esta skill detecta e informa. Corrige solo lo que el autor apruebe, y cuando corrige una cifra, la propaga a todos los documentos en la misma sesión.

Insumos: `00_Gobierno/Registro_Cifras.csv`, `03_Metodologia/Diccionario_Variables.csv`, `01_Literatura/Corpus_Fuentes.xlsx`, `02_Planteamiento/` y todos los documentos de `03_Metodologia/`, `05_Capitulos/` y `06_Productos_Derivados/`.

## Procedimiento

### 1. Auditoría mecánica

Ejecuta las cuatro auditorías sobre las carpetas de documentos y guarda las salidas:

```
python3 auditar_documentos.py cifras --registro 00_Gobierno/Registro_Cifras.csv --rutas 02_Planteamiento 03_Metodologia 05_Capitulos 06_Productos_Derivados
python3 auditar_documentos.py nomenclatura --declarados "<identificadores del diccionario>" --rutas 03_Metodologia 05_Capitulos 06_Productos_Derivados
python3 auditar_documentos.py citas --corpus 01_Literatura/Corpus_Fuentes.xlsx --rutas 05_Capitulos 06_Productos_Derivados
python3 auditar_documentos.py pendientes --rutas .
```

La utilidad lee DOCX, Markdown, texto, LaTeX, CSV y XLSX; no lee PDF, así que audita siempre el documento fuente. La auditoría de citas es heurística: sus hallazgos son candidatos a revisar.

Si no puedes ejecutar código, haz la revisión leyendo los documentos, dilo y advierte que una revisión por lectura puede pasar por alto apariciones.

Si el Registro de Cifras está vacío o le faltan cifras que aparecen en varios documentos, ese es el primer hallazgo: propón las filas que faltan, con su patrón, y pide al autor que confirme el valor canónico de cada una. No elijas tú cuál de dos valores discrepantes es el correcto.

### 2. Revisión de fondo

Lo que la utilidad no puede ver:

1. **Cadena lógica.** El texto de la pregunta, la hipótesis y los objetivos es idéntico en la introducción, la metodología, las conclusiones y `Cadena_Logica.md`. Aplica la prueba de coherencia: si se cumplen todos los objetivos específicos, ¿queda cumplido el general?; si se cumple, ¿la hipótesis queda confirmada o refutada?
2. **Trazabilidad objetivo, análisis y conclusión.** Cada objetivo específico tiene un análisis en la metodología, un resultado en resultados y una conclusión. Ninguna conclusión carece de resultado que la sostenga.
3. **Vacíos.** Cada vacío citado en la introducción está acreditado en el mapa. La cobertura declarada coincide con lo que el diseño hace. Los vacíos fuera de alcance siguen declarados.
4. **Limitaciones.** Las limitaciones registradas (alcance confirmatorio, repetibilidad frente a variabilidad entre unidades, constantes fijadas, coberturas parciales) siguen presentes en metodología, discusión y conclusiones, y no se suavizaron al reescribir.
5. **Lenguaje estadístico.** Busca "se demostró que no", "no existe diferencia", "no hay literatura", "tendencia a la significancia" y afirmaciones causales apoyadas solo en correlación.
6. **Método declarado frente a método ejecutado.** El diseño, los tamaños y los análisis de la metodología coinciden con el informe de análisis. Las desviaciones están declaradas.
7. **Citas y lectura.** Ninguna afirmación técnica se apoya en una fuente con nivel de lectura "solo resumen" sin declararlo. Las fuentes del corpus sin cita se señalan: o se usan o se justifica su permanencia.
8. **Transiciones.** Cada capítulo conecta con el anterior y anticipa el siguiente.
9. **Tesis y productos derivados.** Ninguna cifra ni conclusión del artículo contradice la tesis. Si discrepan, se corrige el documento desactualizado; primero la tesis, después el derivado.

### 3. Clasificar los hallazgos

| Clase | Qué es | Qué se hace |
|---|---|---|
| Error | Contradice el registro o la Ficha sin ambigüedad (una cifra mal copiada, un identificador mal escrito) | Se propone la corrección exacta, con archivo y ubicación |
| Decisión | Dos valores o dos redacciones posibles, y solo el autor sabe cuál vale | Se presentan las opciones y sus consecuencias |
| Riesgo ante el sínodo | No es una contradicción, pero invita a una objeción | Se formula la objeción y la respuesta que falta |
| Pendiente | Marca "por confirmar" | Se lista con su consulta y con quién puede resolverla |

### 4. Corregir y propagar

Con la aprobación del autor, corrige los errores. Para una cifra: cambia primero el Registro de Cifras, después cada documento, y vuelve a ejecutar la auditoría de cifras hasta que no queden discrepancias. Confirma al autor la lista de archivos modificados.

## Salida

`00_Gobierno/Informe_Cohesion.md` (se sobrescribe en cada auditoría), con: fecha y alcance de la auditoría; resumen en cuatro números (errores, decisiones, riesgos y pendientes); tabla de hallazgos por clase, con archivo y ubicación; resultado de la prueba de coherencia; y la lista de verificación previa a la entrega con el estado de cada punto.

## Cierre

Aplica el cierre de hilo. Mensaje de entrega: los cuatro números, las decisiones que requiere el autor y si el documento está en condiciones de entregarse. Di con claridad si no lo está y por qué.

## Lo que esta skill no hace

- No decide cuál de dos cifras discrepantes es la canónica.
- No elimina marcas "por confirmar" para dejar limpio el documento.
- No da por auditado un PDF: audita el documento fuente.

# Modelo de estado

El plugin es estático y genérico. Todo lo que es propio de una tesis vive en archivos de su Claude Project. Esos archivos son la única fuente de verdad: ni la conversación ni la memoria del Project los sustituyen, porque un hilo nuevo empieza sin el contexto de los anteriores y la memoria puede estar desactivada.

## Localizar la carpeta de trabajo

Antes de cualquier otra cosa, encuentra `00_Gobierno/Ficha_Proyecto.md`. Busca en este orden y detente en la primera coincidencia:

1. La carpeta de archivos compartida del Project, si la sesión la ofrece.
2. Una carpeta del equipo del autor conectada a la sesión.
3. El directorio de trabajo de la sesión.
4. El conocimiento o los archivos adjuntos del Project, si solo pueden leerse.

Si no existe la Ficha, el proyecto no se ha iniciado: propón ejecutar `iniciar-tesis` y no continúes con otra skill. Si la encuentras en un lugar de solo lectura, trabaja sobre una copia y entrega al autor los archivos modificados, indicando cuáles debe reemplazar. Anota en la Ficha la ruta de la carpeta de trabajo para que los demás hilos no repitan la búsqueda.

## Estructura

```
<carpeta de trabajo>/
├── 00_Gobierno/
│   ├── Ficha_Proyecto.md          identidad, contexto, recursos, criterios, diseño, estado por fase
│   ├── Registro_Decisiones.md     decisiones, cierres de hilo y cambios de reglas
│   ├── Registro_Cifras.csv        cifras canónicas con su patrón de auditoría
│   ├── Plan_Hilos.md              qué hilo atiende cada etapa
│   ├── Instrucciones_Project.md   texto de las instrucciones del Project
│   └── Manual_Usuario.md
├── 01_Literatura/
│   ├── Protocolo_Busqueda.md
│   ├── criterios_literatura.json  filtros que el autor eligió en el panel de criterios
│   ├── Corpus_Fuentes.xlsx        hojas Corpus, Trazabilidad_busqueda, Obras_fundamentales y Casos_abiertos
│   ├── PDF/                       NN_PrimerAutor_Año.pdf y F_PrimerAutor_Año.pdf
│   └── exportaciones/             archivos exportados de las bases, sin editar
├── 02_Planteamiento/              Mapa_Vacios.md y Cadena_Logica.md
├── 03_Metodologia/                Plan_Analisis.md, Diccionario_Variables.csv, matrices y configuraciones
├── 04_Datos/                      crudos/ (nunca se editan), procesados/ y resultados/
├── 05_Capitulos/
├── 06_Productos_Derivados/
└── 07_Defensa/
```

La estructura la crea `crear_estructura.py`, que no sobrescribe archivos existentes.

## Protocolo de lectura

Toda skill, al empezar:

1. Lee completa la Ficha del proyecto.
2. Lee las tres últimas entradas de cierre del Registro de Decisiones.
3. Lee los archivos propios de su fase (los indica cada skill).
4. Comprueba que la fase anterior esté cerrada. Si no lo está, dilo y pregunta si el autor quiere continuar de todos modos; no bloquees.
5. Si lo que el autor pide contradice la Ficha, señálalo antes de trabajar.

## Protocolo de escritura

Otros hilos escriben en los mismos archivos. Para no pisar su trabajo:

- Vuelve a leer un archivo de estado justo antes de modificarlo.
- Modifica solo las filas o secciones que te corresponden. No reescribas el archivo completo a partir de una lectura antigua.
- Los registros solo crecen: una decisión revocada se marca como sustituida, no se borra.
- Un archivo canónico por documento. No crees sufijos como `_v2`, `_final` o `_rev`. Si el archivo está bloqueado por otra aplicación, informa y espera.

## Cierre de hilo

Toda skill, al terminar su trabajo o cuando el autor da por terminado el hilo:

1. Actualiza la fila de su fase en la sección "Estado por fase" de la Ficha.
2. Registra en el Registro de Decisiones cada decisión tomada, con su fundamento.
3. Añade la entrada de cierre: qué se hizo, qué cambió, qué queda por confirmar y cuál es el siguiente paso.
4. Si cambió una cifra canónica, actualiza el Registro de Cifras, propaga el cambio a todos los documentos en la misma sesión y confírmalo con `auditar_documentos.py cifras`.
5. Actualiza la tabla "Hilos abiertos" del Plan de Hilos.

## Cifras canónicas

Una cifra canónica es un número que aparece en más de un documento: tamaños de muestra, grados de libertad, efectos mínimos detectables, valores críticos, conteos del corpus. Se declara una sola vez en `Registro_Cifras.csv` con un patrón que permite encontrarla en los textos. Nunca se corrige en un solo documento: se cambia en el registro y se propaga.

## Nomenclatura

Los identificadores de factores, respuestas, bloques y covariables se declaran en `Diccionario_Variables.csv` y se resumen en la Ficha. No se renombran entre capítulos ni entre la tesis y sus productos derivados. Un identificador nuevo se declara antes de usarse.

## Memoria del Project

Si la memoria está activa, ayuda a recordar preferencias y contexto. No se confía en ella para cifras, decisiones ni estado: eso está en los archivos. Ante una contradicción, prevalecen los archivos y se avisa al autor.

## Versión del kit

La Ficha registra la versión del plugin que generó el kit. Si la versión instalada es posterior, `evolucionar-sistema` compara las plantillas y propone al autor los cambios, sin aplicarlos por su cuenta.

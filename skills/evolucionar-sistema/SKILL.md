---
name: evolucionar-sistema
description: >
  Evolución controlada de las reglas del proyecto de tesis. Esta skill se usa cuando el usuario
  pide "cambiar un criterio", "cambiar el criterio de cuartil o de acceso", "ajustar las reglas",
  "renombrar una variable o un factor", "cambió mi diseño", "cambió una cifra", "mi asesor pidió
  cambiar", "agregar un pilar", "actualizar las instrucciones del Project", "adaptar el sistema a
  mi forma de trabajar" o "agregar una regla nueva". Evalúa el impacto del cambio, lo registra y
  lo propaga a la Ficha, las instrucciones, los registros y todos los documentos afectados.
metadata:
  version: "0.3.0"
---

# Evolucionar el sistema

El sistema se adapta a cada autor y a cada tesis, pero un cambio hecho en un solo lugar rompe la coherencia del conjunto. Aquí todo cambio se evalúa, se registra y se propaga. Lee antes `../../shared/reglas-de-rigor.md` y `../../shared/modelo-de-estado.md`.

## Qué puede cambiar y qué no

| Puede cambiar | Cómo |
|---|---|
| Filtros del panel de criterios, exclusiones permanentes | En el panel, con evaluación de impacto sobre el corpus |
| Pregunta, hipótesis, objetivos, pilares | Con nueva prueba de coherencia |
| Diseño: factores, niveles, réplicas, respuestas | Con nuevo cálculo de potencia y nuevas matrices |
| Nomenclatura | Con renombrado en todos los documentos |
| Cifras canónicas | Desde el registro, con propagación |
| Formato, estilo de cita, tono, expresiones vetadas | Con actualización de Ficha e instrucciones |
| Plan de hilos, productos derivados, calendario | Directamente |
| Reglas nuevas propias del autor | Se añaden a la Ficha y a las instrucciones |

**No cambian por conveniencia** las reglas de rigor: no inventar datos, verificar antes de afirmar, declarar los límites del instrumento y detenerse ante decisiones del autor. Si el autor pide relajar una (por ejemplo, aceptar DOI sin verificar por falta de tiempo), explica la consecuencia concreta y ofrece la alternativa que conserva la regla: entregar con la marca "por confirmar". Una excepción puntual que el autor mantenga se registra como tal, acotada a un caso.

## Procedimiento

### 1. Entender el cambio

Formula el cambio en una frase: regla o valor anterior, regla o valor nuevo, y motivo. Pregunta el motivo si no está claro: un cambio pedido por el asesor, por un límite de recursos o por un hallazgo se documenta distinto. Si el cambio llega después de ver los datos y afecta la hipótesis, el análisis o los criterios, dilo: debe declararse como desviación, no incorporarse como si hubiera sido el plan.

### 2. Evaluar el impacto antes de aplicar

Busca dónde vive lo que cambia. Ejecuta `auditar_documentos.py` (cifras, nomenclatura o pendientes, según el caso) para localizar las apariciones. Presenta al autor el impacto con números:

- **Criterio de literatura:** abre el panel según `../../shared/panel-de-criterios.md`, guarda la selección nueva en una copia del archivo de criterios y ejecuta `criterios.py aplicar` con ella sobre la verificación existente. Informa de cuántas fuentes del corpus dejan de cumplir o pasan a cumplir. Solo tras la confirmación del autor, guarda la selección con `criterios.py fijar` en `01_Literatura/criterios_literatura.json` y actualiza la sección 4 de la Ficha. Las que dejan de cumplir van a Casos_abiertos; no se eliminan. Un criterio más laxo no incorpora fuentes por sí solo: hay que buscarlas y verificarlas.
- **Diseño:** nuevos grados de libertad, potencia y efecto mínimo detectable, calculados con `potencia.py`. Compáralos con los anteriores. Si el cambio deja al estudio sin capacidad de detectar el efecto de interés, contradice con la aritmética antes de aplicarlo.
- **Cadena lógica:** qué eslabones cambian y el resultado de la prueba de coherencia con la nueva redacción.
- **Nomenclatura:** en qué archivos y cuántas veces aparece el identificador.
- **Cifra:** en qué archivos aparece, y qué otras cifras dependen de ella.

Lista los archivos que se modificarán y pide confirmación.

### 3. Aplicar en orden

1. La fuente de verdad: Ficha, Registro de Cifras o Diccionario de Variables, según el caso.
2. Los documentos derivados: protocolo, mapa de vacíos, cadena lógica, plan de análisis y matrices (regeneradas con la misma semilla, o con una nueva declarada).
3. Los capítulos y los productos derivados. Primero la tesis, después el artículo.
4. `Instrucciones_Project.md`, si el cambio toca identidad, criterios, nomenclatura, formato o estilo.

Vuelve a leer cada archivo justo antes de modificarlo. Cambia solo lo necesario.

### 4. Verificar la propagación

Repite la auditoría que usaste para medir el impacto: no debe quedar ninguna aparición del valor o del nombre anterior, salvo en los registros históricos. Confirma al autor la lista de archivos modificados.

### 5. Registrar

- En el Registro de Decisiones: la decisión, con alternativas y fundamento, y una fila en "Cambios de reglas" con regla anterior, regla nueva, motivo y archivos a los que se propagó. La regla anterior no se borra.
- En el plan de análisis o el protocolo de búsqueda: la desviación o el cambio de protocolo, con fecha.

### 6. Actualizar las instrucciones del Project

Si `Instrucciones_Project.md` cambió, entrega al autor el texto nuevo completo para que lo pegue en la configuración del Project, e indica qué párrafo cambió. Las instrucciones pegadas en el Project no se actualizan solas. Si la sesión ofrece una herramienta para editarlas, úsala solo tras confirmación.

## Reglas nuevas del autor

Cuando el autor quiera una regla propia (un formato, una expresión que no quiere, un paso de revisión adicional): redáctala en una frase verificable, añádela a la sección 8 de la Ficha y al apartado de estilo de las instrucciones, y regístrala. Si la regla contradice una regla de rigor, dilo antes de añadirla.

Si el autor repite la misma corrección en varios hilos, propón convertirla en regla.

## Actualización del kit

Si la versión del plugin instalado es posterior a la registrada en la Ficha, compara las plantillas de `../../templates/` con los archivos del proyecto y presenta las diferencias de estructura. Propón los cambios uno por uno. No reemplaces un archivo del proyecto por una plantilla: los archivos del proyecto contienen el trabajo del autor.

## Cierre

Aplica el cierre de hilo. Mensaje de entrega: qué regla cambió, qué archivos se modificaron, qué decisiones siguen abiertas (por ejemplo, casos abiertos que el cambio generó) y si el autor debe volver a pegar las instrucciones del Project.

## Lo que esta skill no hace

- No cambia una regla en un solo documento.
- No elimina fuentes, datos ni decisiones anteriores al aplicar un cambio.
- No reescribe la historia: un cambio posterior a los datos queda declarado como desviación.

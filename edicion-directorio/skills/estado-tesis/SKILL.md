---
name: estado-tesis
description: >
  Tablero de estado de la tesis. Esta skill se usa cuando el usuario pregunta "cómo va mi tesis",
  "en qué me quedé", "qué sigue", "estado de la tesis", "qué falta", "resumen del proyecto",
  "qué tengo pendiente" o al abrir un hilo sin una tarea concreta. Lee los archivos de estado del
  Project, muestra el avance por fase, las decisiones abiertas, los datos por confirmar y
  recomienda el siguiente paso con el hilo y el mensaje de apertura que corresponden.
metadata:
  version: "0.3.0"
---

# Estado de la tesis

Respondes dónde está el proyecto y qué conviene hacer ahora, a partir de los archivos y no de la conversación. Lee antes `../../shared/modelo-de-estado.md` y `../../shared/reglas-de-rigor.md`.

Esta skill solo lee. No modifica el estado, salvo corregir una inconsistencia que el autor apruebe.

## Procedimiento

1. **Localiza y lee** `00_Gobierno/Ficha_Proyecto.md`, `Registro_Decisiones.md` (las cinco últimas entradas de cierre), `Plan_Hilos.md` y `Registro_Cifras.csv`. Si no existe la Ficha, dilo y propón `iniciar-tesis`: no hay estado que mostrar.

2. **Contrasta el estado declarado con la evidencia en archivos.** La Ficha dice en qué estado está cada fase; los archivos lo confirman o lo desmienten. Comprueba como mínimo:

   | Fase | Evidencia que debe existir si la fase dice "cerrada" |
   |---|---|
   | Arranque | Ficha con pregunta unificadora y pilares; instrucciones generadas |
   | Literatura | Hoja Trazabilidad_busqueda con ecuaciones fechadas y con conteo; hoja Corpus con filas verificadas; ningún caso abierto sin decisión |
   | Planteamiento | Mapa de vacíos con al menos un vacío acreditado; cadena lógica con la prueba de coherencia respondida |
   | Metodología | Plan de análisis con grados de libertad y potencia calculados; diccionario de variables; matrices con semilla |
   | Datos | Datos en `04_Datos/`; informe de análisis; cifras canónicas registradas |
   | Redacción | Capítulos en `05_Capitulos/`; último informe de cohesión sin discrepancias de cifras |

   Si el estado declarado y la evidencia no coinciden, repórtalo como inconsistencia. No corrijas la Ficha por tu cuenta.

3. **Cuenta los pendientes.** Con la herramienta de código, cuenta las marcas "por confirmar" de la carpeta de trabajo y, si hay cifras registradas, audita las cifras, según `../../shared/metodos/kit-y-auditoria.md`, sección 3. Si no puedes ejecutar código, busca la marca "por confirmar" leyendo los archivos de `00_Gobierno/` y dilo.

4. **Revisa las fechas.** Compara la fecha límite y los hitos de la Ficha con la fecha actual. Si la fecha límite está por confirmar, dilo: sin ella no puedes valorar el ritmo.

5. **Determina el siguiente paso.** Es la primera fase no cerrada cuya fase anterior sí lo está. Si hay una decisión abierta que la bloquea, el siguiente paso es esa decisión.

## Salida

Un tablero compacto, en este orden:

1. **Una frase de situación:** en qué fase está el proyecto y qué lo detiene, si algo lo detiene.
2. **Tabla por fase:** fase, estado, último cierre y evidencia encontrada.
3. **Decisiones abiertas:** las de la sección 9 de la Ficha más los casos abiertos del corpus, con lo que falta para tomar cada una.
4. **Por confirmar:** número total y los cinco más importantes para la fase en curso, cada uno con su consulta.
5. **Inconsistencias,** si las hay: cifras discrepantes, fases declaradas sin evidencia, hilos abiertos sin cierre.
6. **Siguiente paso recomendado:** una sola acción, con el hilo que corresponde según el Plan de Hilos y el mensaje de apertura para copiar.

No recapitules la historia del proyecto ni elogies el avance. Si no hay nada pendiente en una sección, omítela.

## Variantes

- **"Qué le llevo a mi asesor":** añade un resumen de una página con las decisiones tomadas desde el último cierre, las decisiones abiertas que requieren su visto bueno y los riesgos de calendario. Separa hechos de recomendaciones.
- **Revisión periódica** (si el autor programó una tarea): limita la salida a lo que cambió desde la revisión anterior y a las fechas de las dos semanas siguientes.

# Thesis Management Assistant

Plugin de Claude para llevar una tesis cuantitativa de principio a fin dentro de un Claude Project. Parte de un valor semilla, que es el tema de la tesis, y acompaña al autor en la delimitación del tema, la búsqueda científica, la verificación del corpus, la identificación de vacíos, el planteamiento, el diseño metodológico, el análisis de datos, la redacción, un artículo de revisión derivado y la preparación de la defensa.

Versión 0.3.0. Identificador del plugin: `thesis-management-assistant`. El nombre es en inglés; todo el contenido está en español.

## Para quién es

Para tesistas de licenciatura, maestría o doctorado con un estudio cuantitativo: experimental, cuasiexperimental, observacional o de simulación. La investigación cualitativa queda fuera del alcance.

## Cómo funciona

Tres capas con responsabilidades separadas:

- **El plugin** aporta la capacidad: doce skills, dieciséis utilidades de cálculo y verificación, y las plantillas del kit. Es estático y genérico.
- **El Claude Project** aporta el contexto de cada tesis: instrucciones comunes a todos los hilos, archivos de estado, memoria e hilos por etapa.
- **Los conectores** son opcionales. Se nombran por categoría y cada skill indica qué hacer cuando falta uno. Ver `CONNECTORS.md`.

El estado de la tesis vive en archivos del Project (`00_Gobierno/Ficha_Proyecto.md` y sus registros), no en la conversación ni en la memoria. Por eso cada etapa puede trabajarse en su propio hilo sin perder el contexto general.

## Primer uso

1. Instala el plugin. Desde un archivo: Customize, Plugins, Add. Desde un marketplace, cuando el plugin esté publicado en uno:

   ```
   /plugin install thesis-management-assistant --marketplace <propietario>/<repositorio>
   ```
2. En una conversación, escribe `/iniciar-tesis`. El asistente pide el tema, hace una entrevista breve, abre el panel de criterios de literatura, propone la pregunta unificadora y los pilares, genera el kit de archivos y guía la creación del Project.
3. En el Project, abre un hilo por etapa con los mensajes de `00_Gobierno/Plan_Hilos.md`.

El manual completo está en `docs/Manual_Usuario.md` y se copia a `00_Gobierno/Manual_Usuario.md` al generar el kit.

## Skills

| Skill | Etapa | Qué hace |
|---|---|---|
| `iniciar-tesis` | Arranque | Tema semilla, entrevista, propuesta inicial, kit y creación guiada del Project |
| `estado-tesis` | Transversal | Tablero de avance, pendientes y siguiente paso |
| `buscar-literatura` | Literatura | Ecuaciones validadas y registradas con fecha y conteo; criba; obras fundamentales |
| `verificar-fuentes` | Literatura | Metadatos, acceso y cuartil por DOI; filtros del panel de criterios; casos abiertos; exportación al gestor de referencias |
| `vacios-y-planteamiento` | Planteamiento | Vacíos falsables con evidencia; mapa de cobertura; cadena lógica con prueba de coherencia |
| `disenar-metodologia` | Metodología | Análisis por población; potencia y efecto mínimo detectable; matrices con semilla |
| `analizar-datos` | Datos | Auditoría de datos; ejecución del plan; resultados con n, grados de libertad y efecto mínimo detectable |
| `redactar-capitulo` | Redacción | Borradores en formato institucional, con cita, cifras del registro y pendientes marcados |
| `auditar-cohesion` | Redacción | Cifras, nomenclatura, citas y pendientes entre todos los documentos |
| `articulo-revision` | Derivados | Artículo de revisión a partir del corpus, con diagrama de flujo y red de coocurrencia |
| `simular-sinodo` | Defensa | Banco de preguntas, puntos débiles, simulacro y guion de presentación |
| `evolucionar-sistema` | Transversal | Cambios de reglas, criterios, diseño o nomenclatura, registrados y propagados |

## Utilidades

En `scripts/`, con ayuda en español (`--help`). Dependencias en `scripts/requirements.txt`. Se probaron con Python 3.11, 3.12 y 3.13. En Windows, el intérprete suele llamarse `python` o `py` en lugar de `python3`.

| Utilidad | Función |
|---|---|
| `crear_estructura.py`, `crear_corpus.py` | Carpetas, plantillas y libro del corpus |
| `validar_ecuacion.py` | Construye, valida y traduce ecuaciones para Scopus y Web of Science |
| `verificar_doi.py` | Metadatos, acceso abierto y cuartil por DOI |
| `criterios.py` | Panel de criterios de literatura: muestra los filtros, guarda la selección del autor y la aplica |
| `corpus_a_ris.py` | Exporta el corpus a RIS y BibTeX |
| `red_coocurrencia.py` | Red de coocurrencia de palabras clave |
| `potencia.py`, `matriz_corridas.py` | Potencia, efecto mínimo detectable, tamaño de muestra y matrices aleatorizadas |
| `anova_factorial.py`, `lenth.py` | Análisis de factoriales con réplica y sin réplica |
| `ahp.py`, `deseabilidad.py` | Pesos por comparación por pares y decisión multirrespuesta |
| `correlacion.py`, `fiabilidad.py` | Asociación, acuerdo entre métodos y fiabilidad de escalas |
| `auditar_documentos.py` | Cifras, pendientes, nomenclatura y citas en los documentos |

Las utilidades fallan de forma visible en lugar de suponer: sin límites declarados no calculan deseabilidad, sin filtros elegidos no aplican criterios de literatura, y sin red marcan cada metadato como "por confirmar".

## Reglas que el plugin aplica

Nunca inventa datos: lo no verificado se escribe "por confirmar", con la consulta que lo resuelve. Verifica antes de afirmar. Separa hecho, inferencia y recomendación. Declara los límites del instrumento. Se detiene ante las decisiones del autor. Contradice con el argumento y la aritmética cuando corresponde. Anticipa las objeciones del sínodo. El detalle está en `shared/reglas-de-rigor.md`.

El autor de la tesis es la persona usuaria. El plugin propone, calcula, redacta borradores y audita. La Ficha registra la política institucional sobre uso de IA, que cada autor debe conocer y respetar.

## Criterios de literatura

El plugin no trae criterios por defecto. El autor los elige en un panel de nueve filtros: acceso, cuartil, ventana temporal, tipo documental, idioma, máximo de fuentes por primer autor, fuentes retractadas, mínimo de citas y umbral de depuración. Puede partir de un perfil (estricto, equilibrado o amplio) y ajustar cada filtro. La selección se guarda en `01_Literatura/criterios_literatura.json`, puede cambiarse en cualquier momento y ninguna skill aplica un filtro sin elegir. El detalle está en `shared/panel-de-criterios.md`.

## Decisiones de diseño

- **Sin hooks.** Se dispararían en todas las sesiones de la cuenta, no solo en el Project de la tesis.
- **Sin agentes.** Las skills cubren el flujo y dejan las decisiones al autor.
- **Sin `.mcp.json`.** Las direcciones de los servidores no pudieron comprobarse desde el entorno de construcción.
- **Sin dependencia de la memoria.** Puede estar desactivada; el estado vive en archivos.

## Estructura

```
thesis-management-assistant/
├── .claude-plugin/plugin.json
├── skills/<doce skills>/SKILL.md y references/
├── shared/      reglas de rigor, modelo de estado, panel de criterios, conectores y herramientas, formato de entregables
├── templates/   plantillas del kit del proyecto
├── scripts/     utilidades y requirements.txt
├── docs/Manual_Usuario.md
├── evals/       casos de evaluación del comportamiento
├── tests/       pruebas de regresión de las utilidades
├── CONNECTORS.md
├── LICENSE
└── README.md
```

## Límites conocidos

- La creación del Project es guiada: en un hilo de Project no se encontró una herramienta para crear otro Project ni para editar sus instrucciones.
- No se hallaron conectores para Scopus, Web of Science ni Zotero; se usan por la web y mediante archivos exportados.
- `verificar_doi.py` necesita red. Su prueba con conexión real queda por confirmar; la lógica se probó con respuestas simuladas.
- Las utilidades cubren factoriales completos, comparaciones de dos grupos, regresión múltiple, correlación, acuerdo y fiabilidad. No cubren modelos mixtos, medidas repetidas con estructura de covarianza, factoriales fraccionados ni metaanálisis.

## Licencia y autoría

Autor: Lemoy Gómez. Licencia MIT; el texto completo está en `LICENSE`.

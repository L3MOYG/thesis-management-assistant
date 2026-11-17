# Thesis Management Assistant

Plugin de Claude para llevar una tesis cuantitativa de principio a fin dentro de un Claude Project. Parte de un valor semilla, que es el tema de la tesis, y acompaña al autor en la delimitación del tema, la búsqueda científica, la verificación del corpus, la identificación de vacíos, el planteamiento, el diseño metodológico, el análisis de datos, la redacción, un artículo de revisión derivado y la preparación de la defensa.

Versión 0.3.0, edición del directorio. Identificador del plugin: `thesis-management-assistant`. El nombre es en inglés; todo el contenido está en español.

## Esta edición

Es la edición que se distribuye en el directorio de plugins de Claude. Contiene solo instrucciones, plantillas y documentación: no trae programas ejecutables. Los cálculos (potencia, matrices de corridas, ANOVA, Lenth, correlaciones, acuerdo, fiabilidad, AHP, deseabilidad, ecuaciones de búsqueda, verificación de DOI, exportación del corpus, red de coocurrencia y auditorías) los hace Claude con la herramienta de ejecución de código de la sesión, siguiendo los métodos documentados en `shared/metodos/`. Cada método incluye un caso de control que Claude reproduce antes de usar los datos del autor; si no coincide, el resultado queda "por confirmar".

La edición completa, con las mismas skills y además dieciséis utilidades en Python con pruebas de regresión, se instala desde el marketplace del repositorio `L3MOYG/thesis-management-assistant` (ver "Edición completa", más abajo). Instala solo una de las dos.

## Para quién es

Para tesistas de licenciatura, maestría o doctorado con un estudio cuantitativo: experimental, cuasiexperimental, observacional o de simulación. La investigación cualitativa queda fuera del alcance.

## Cómo funciona

Tres capas con responsabilidades separadas:

- **El plugin** aporta la capacidad: doce skills, la guía de métodos de cálculo y verificación, y las plantillas del kit. Es estático y genérico.
- **El Claude Project** aporta el contexto de cada tesis: instrucciones comunes a todos los hilos, archivos de estado, memoria e hilos por etapa.
- **Los conectores** son opcionales. Se nombran por categoría y cada skill indica qué hacer cuando falta uno. Ver `CONNECTORS.md`.

El estado de la tesis vive en archivos del Project (`00_Gobierno/Ficha_Proyecto.md` y sus registros), no en la conversación ni en la memoria. Por eso cada etapa puede trabajarse en su propio hilo sin perder el contexto general.

## Primer uso

1. Instala el plugin desde el directorio de plugins de Claude y comprueba que la sesión tenga activada la ejecución de código.
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

## Métodos de cálculo

En `shared/metodos/`, cinco documentos con las entradas, las fórmulas, las reglas de parada, la forma de la salida y los casos de control de cada operación:

| Documento | Operaciones |
|---|---|
| `potencia-y-diseno.md` | Potencia y efecto mínimo detectable (ANOVA, factorial, dos grupos, correlación, regresión), tamaño de muestra y matriz de corridas con semilla |
| `analisis-de-datos.md` | ANOVA factorial con supuestos, método de Lenth, matriz de correlaciones con Holm y remuestreo, Bland y Altman, alfa de Cronbach |
| `ahp-y-deseabilidad.md` | Pesos por comparación por pares con razón de consistencia, deseabilidad de Derringer y Suich, sensibilidad y verificación con TOPSIS |
| `literatura.md` | Ecuaciones para Scopus y Web of Science, verificación de DOI y acceso abierto, cuartil, exportación a RIS y BibTeX, red de coocurrencia |
| `kit-y-auditoria.md` | Carpetas, plantillas, libro del corpus y auditoría de cifras, pendientes, nomenclatura y citas |

Los procedimientos fallan de forma visible en lugar de suponer: sin límites declarados no calculan deseabilidad, sin filtros elegidos no aplican criterios de literatura, sin red marcan cada metadato como "por confirmar" y, si el caso de control no coincide, no entregan la cifra.

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
│   └── metodos/ guía de métodos de cálculo con casos de control
├── templates/   plantillas del kit del proyecto
├── docs/Manual_Usuario.md
├── CONNECTORS.md
├── LICENSE
└── README.md
```

## Límites conocidos

- La creación del Project es guiada: en un hilo de Project no se encontró una herramienta para crear otro Project ni para editar sus instrucciones.
- No se hallaron conectores para Scopus, Web of Science ni Zotero; se usan por la web y mediante archivos exportados.
- La verificación de DOI necesita acceso web en la sesión. Sin él, los registros quedan por confirmar.
- Los cálculos dependen de la herramienta de código de cada sesión. Las cifras que usan remuestreo u optimización pueden variar ligeramente con la versión de las bibliotecas; se informan con la versión y la semilla.
- Los métodos cubren factoriales completos, comparaciones de dos grupos, regresión múltiple, correlación, acuerdo y fiabilidad. No cubren modelos mixtos, medidas repetidas con estructura de covarianza, factoriales fraccionados ni metaanálisis.

## Edición completa

Para trabajar con las utilidades en Python y sus pruebas, instala la edición completa desde su marketplace en GitHub, con Claude Code 2.1.275 o posterior:

```
/plugin install thesis-management-assistant --marketplace L3MOYG/thesis-management-assistant
```

En versiones anteriores, en dos pasos: `/plugin marketplace add L3MOYG/thesis-management-assistant` y después `/plugin install thesis-management-assistant@thesis-management-assistant`.

## Licencia y autoría

Autor: Lemoy Gómez. Licencia MIT; el texto completo está en `LICENSE`.

# Manual de usuario · Thesis Management Assistant

Versión 0.3.0. Este manual acompaña al plugin y se copia a `00_Gobierno/Manual_Usuario.md` al iniciar cada proyecto.

## Índice

1. Qué es y qué no es
2. Requisitos
3. Instalación
4. Primera sesión: del tema al Project
5. Cómo se trabaja: archivos, hilos y cierres
6. Las doce skills
7. Flujo completo por etapas
8. Conectores y herramientas
9. Utilidades de cálculo
10. Reglas que el asistente aplica
11. Adaptar el sistema
12. Solución de problemas
13. Límites conocidos
14. Glosario

---

## 1. Qué es y qué no es

**Thesis Management Assistant** (identificador `thesis-management-assistant`) es un plugin de Claude que te guía y te asiste durante toda una tesis cuantitativa. Le das un tema, que es el valor semilla, y un contexto mínimo. A partir de ahí organiza el trabajo en etapas, cada una en su propio hilo de un Claude Project, y mantiene un estado común en archivos para que ningún hilo pierda el contexto general.

Lo que hace: construye y registra búsquedas reproducibles, verifica cada fuente, formula vacíos con su evidencia, arma la cadena de pregunta, hipótesis y objetivos, dimensiona el estudio con potencia calculada, analiza tus datos, redacta borradores de capítulos, audita la coherencia entre documentos, deriva un artículo de revisión y te prepara para la defensa.

Lo que no hace: no escribe la tesis por ti, no inventa datos ni citas, no decide por ti lo que cambia el alcance o las conclusiones, y no cubre investigación cualitativa. Tú eres el autor. El asistente propone, calcula, redacta borradores y critica.

## 2. Requisitos

- Una cuenta de Claude con acceso a plugins. Según la documentación de Claude consultada el 16/11/2026, los plugins están disponibles en los planes de pago.
- Acceso a Claude Projects, para alojar la tesis.
- Recomendable: una sesión que pueda ejecutar código, porque las utilidades de cálculo están escritas en Python. Sin ella, el asistente te da la orden exacta para ejecutarla en tu equipo.
- Opcional: conectores de búsqueda académica, almacenamiento u otros (sección 8).
- Opcional: acceso institucional a una base bibliográfica como Scopus o Web of Science, y un gestor de referencias.

## 3. Instalación

**Con el archivo `.plugin`.** Abre la aplicación de Claude, entra en Customize, después en Plugins, elige Add y selecciona el archivo `thesis-management-assistant.plugin`. Si recibes el plugin como una tarjeta de archivo dentro de una conversación, usa el botón Save plugin de la tarjeta. El plugin queda guardado en tu cuenta.

**Desde un repositorio.** Si quien distribuye el plugin lo publicó en un repositorio configurado como marketplace, añade ese marketplace desde el mismo menú o, en Claude Code, con `/plugin install thesis-management-assistant --marketplace <propietario>/<repositorio>`.

**En una organización.** Un administrador puede poner el plugin a disposición de todos o instalarlo por defecto.

**Comprobación.** En una conversación nueva, escribe `/`. Deben aparecer las skills del plugin, por ejemplo `iniciar-tesis` y `estado-tesis`. Si no aparecen, consulta la sección 12.

Los nombres de los menús pueden cambiar entre versiones de la aplicación. Si no coinciden, busca el apartado de plugins en la configuración o en la personalización.

## 4. Primera sesión: del tema al Project

Escribe `/iniciar-tesis`. El asistente sigue siete pasos.

1. **Te pide el tema.** Una sola pregunta. Respóndela con tus palabras y con el detalle que tengas hoy. Ese texto se guarda literal.
2. **Te entrevista en bloques cortos:** grado y disciplina; institución, normativa, estilo de cita, idioma y política sobre uso de IA; tipo de estudio y recursos; restricciones; asesor y sínodo; productos derivados; criterios de literatura, que eliges en el panel de criterios; y convenciones. Puedes responder "no lo sé": el dato queda marcado **por confirmar** y nadie lo inventa.
3. **Reconoce el entorno:** qué conectores hay, si puede ejecutar código y dónde vivirán los archivos.
4. **Hace una exploración inicial** del tema, declarada como exploratoria, y te propone dos o tres formulaciones de la pregunta unificadora, de uno a tres pilares y los términos de búsqueda. Tú eliges.
5. **Genera el kit:** la estructura de carpetas, la Ficha del proyecto, los registros, el plan de hilos, el protocolo de búsqueda, el libro del corpus y el texto de las instrucciones del Project.
6. **Te guía para crear el Claude Project** (o para configurar el que ya tienes): crear el Project, pegar las instrucciones y darle acceso a los archivos.
7. **Verifica el arranque:** abres un hilo nuevo, escribes `/estado-tesis` y debe aparecer el tablero con el arranque cerrado y la literatura como siguiente paso.

**El panel de criterios.** Los criterios con los que una fuente entra a tu corpus los eliges tú. El asistente te presenta un panel con nueve filtros y sus opciones, y no aplica ninguno que no hayas elegido.

| Filtro | Opciones |
|---|---|
| Acceso al texto completo | Solo acceso abierto verificado; abierto o suscripción institucional; cualquier vía legal; sin filtro |
| Cuartil de la revista | Solo Q1; Q1 o Q2; Q1 a Q3; cualquier cuartil; sin filtro |
| Ventana temporal | 5, 7, 10 o 15 años, otro número, o sin límite |
| Tipo documental | Artículo, revisión, ponencia, libro o capítulo, tesis, preprint, informe o norma. Puedes marcar varios |
| Idioma | Español, inglés, portugués, francés u otro. Puedes marcar varios |
| Máximo de fuentes por primer autor | 1, 2, 3, otro número, o sin filtro |
| Fuentes retractadas | Señalarlas como caso abierto, o permitirlas con nota |
| Mínimo de citas | 5, 10, 20, otro número, o sin filtro |
| Umbral de depuración de una ecuación | 100, 200, 300, 500 u otro número de resultados |

Puedes partir de un perfil (estricto, equilibrado o amplio) y ajustar después, o elegir filtro por filtro. Si la aplicación ofrece preguntas con opciones, el panel aparece como una serie de selecciones. Si no, el asistente lo muestra como texto y respondes con códigos, por ejemplo `A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300`. Un filtro que dejes sin decidir queda **por confirmar**. Para volver a abrirlo en cualquier momento, escribe "abre el panel de criterios".

Una fuente que incumple un filtro no se descarta sola: pasa a ser un caso abierto y decides tú.

**Por qué un Project.** Un Project comparte entre todos sus hilos las instrucciones, los archivos y, si está activa, la memoria. Eso permite partir la tesis en etapas sin repetir el contexto en cada conversación.

**Creación del Project.** El asistente te guía paso a paso y te entrega el texto listo para pegar. Solo lo crea por sí mismo si la sesión le ofrece una herramienta para ello y tú lo confirmas.

## 5. Cómo se trabaja: archivos, hilos y cierres

### Los archivos son la memoria del proyecto

```
00_Gobierno/            Ficha, registros, plan de hilos, instrucciones y este manual
01_Literatura/          protocolo de búsqueda, libro del corpus, PDF y exportaciones
02_Planteamiento/       mapa de vacíos y cadena lógica
03_Metodologia/         plan de análisis, diccionario de variables y matrices
04_Datos/               crudos (nunca se editan), procesados y resultados
05_Capitulos/           un archivo por capítulo
06_Productos_Derivados/ artículo de revisión y otros
07_Defensa/             banco de preguntas, puntos débiles y presentación
```

| Archivo | Para qué sirve |
|---|---|
| `Ficha_Proyecto.md` | Única fuente de verdad: identidad, contexto, recursos, criterios, diseño y estado por fase |
| `Registro_Decisiones.md` | Cada decisión con su fundamento, y el cierre de cada hilo |
| `Registro_Cifras.csv` | Las cifras que aparecen en más de un documento, para que nunca se contradigan |
| `Plan_Hilos.md` | Qué hilo atiende cada etapa y con qué mensaje se abre |
| `Corpus_Fuentes.xlsx` | Fuentes, trazabilidad de la búsqueda, obras fundamentales y casos abiertos |

Puedes leer y editar estos archivos cuando quieras. Si cambias algo importante a mano, dilo en el hilo siguiente.

### Un hilo por etapa

Abre un hilo nuevo para cada etapa, con el mensaje que indica `Plan_Hilos.md`. Cada hilo empieza leyendo la Ficha y los últimos cierres, y termina dejando su propio cierre: qué se hizo, qué cambió, qué queda por confirmar y cuál es el siguiente paso. Así el hilo siguiente continúa sin releer conversaciones.

### La marca "por confirmar"

Todo dato sin verificar se escribe literalmente **por confirmar**, con la consulta que lo resolvería. No es un defecto: es la garantía de que lo demás sí está verificado. `/estado-tesis` y `/auditar-cohesion` las cuentan y te dicen cuáles importan ahora.

### Las decisiones son tuyas

Cuando una fuente no pasa un filtro, cuando hay dos valores posibles o cuando un cambio afecta el alcance, el asistente se detiene, te presenta el caso con sus opciones y espera. Si propones algo metodológicamente débil, te lo dirá con el argumento y los números antes de ejecutarlo; después, decides tú.

## 6. Las doce skills

Cada skill se invoca con su nombre precedido de `/`, o con una frase natural como las de la columna central.

| Skill | Frases que la activan | Qué entrega |
|---|---|---|
| `/iniciar-tesis` | "quiero iniciar mi tesis", "configura el proyecto de mi tesis" | Kit de archivos y Project configurado |
| `/estado-tesis` | "cómo va mi tesis", "qué sigue", "qué tengo pendiente" | Tablero por fase, pendientes y siguiente paso |
| `/buscar-literatura` | "arma la ecuación de búsqueda", "busca antecedentes sobre…" | Ecuaciones validadas, registradas con fecha y conteo; candidatos cribados |
| `/verificar-fuentes` | "verifica estos DOI", "arma el corpus", "exporta a mi gestor de referencias" | Corpus verificado, casos abiertos y archivos `.ris` y `.bib` |
| `/vacios-y-planteamiento` | "identifica los vacíos", "formula la pregunta y la hipótesis" | Mapa de vacíos con evidencia y cadena lógica con prueba de coherencia |
| `/disenar-metodologia` | "diseña el experimento", "cuántas réplicas necesito", "calcula la potencia" | Plan de análisis, diccionario de variables y matrices con semilla |
| `/analizar-datos` | "analiza mis datos", "haz el ANOVA", "interpreta estos resultados" | Auditoría de datos, informe de análisis y cifras canónicas |
| `/redactar-capitulo` | "redacta el capítulo de antecedentes", "revisa mi metodología" | Borrador del capítulo en el formato institucional |
| `/auditar-cohesion` | "audita la tesis", "revisa que las cifras coincidan" | Informe de cohesión: errores, decisiones, riesgos y pendientes |
| `/articulo-revision` | "deriva un artículo de revisión", "haz el diagrama de flujo de la selección" | Manuscrito, diagrama con conteos reales y red de coocurrencia |
| `/simular-sinodo` | "simula al sínodo", "qué me van a preguntar" | Banco de preguntas, puntos débiles, simulacro y guion de presentación |
| `/evolucionar-sistema` | "abre el panel de criterios", "cambia el filtro de cuartil", "renombra el factor B", "mi asesor pidió cambiar…" | Cambio evaluado, registrado y propagado a todos los archivos |

## 7. Flujo completo por etapas

| Etapa | Tú aportas | El asistente produce | Decisiones tuyas |
|---|---|---|---|
| Arranque | Tema y contexto | Kit y Project | Pregunta unificadora, pilares y criterios |
| Literatura | Acceso a las bases; ejecutar ecuaciones si no hay conector | Ecuaciones, trazabilidad y corpus verificado | Casos abiertos y orden de aporte |
| Planteamiento | Lectura crítica de lo propuesto | Vacíos acreditados y cadena lógica | Redacción final de pregunta, hipótesis y objetivos |
| Metodología | Recursos y restricciones reales | Diseño, potencia y matrices | Factores, niveles, réplicas y efecto de interés |
| Datos | Datos crudos | Auditoría y análisis | Anomalías, atípicos y límites de decisión |
| Redacción | Revisión y voz propia | Borradores e informe de cohesión | Texto final |
| Derivados | Revista objetivo | Manuscrito de revisión | Tipo de revisión y ampliaciones |
| Defensa | Tus respuestas en el simulacro | Preguntas y puntos débiles | Qué reforzar y qué declarar como límite |

Las etapas se solapan y se repiten: es normal volver a la literatura desde la discusión. `/estado-tesis` te dice siempre dónde estás.

## 8. Conectores y herramientas

Ningún conector es obligatorio. El plugin nombra las herramientas por categoría y usa lo que tengas conectado.

| Categoría | Con conector | Sin conector |
|---|---|---|
| Base bibliográfica | El asistente ejecuta la ecuación | Tú la ejecutas en la web de la base, anotas el conteo y exportas el archivo |
| Búsqueda académica | Exploración y búsqueda complementaria | Búsqueda web, declarada como exploratoria |
| Lectura de artículos | Lectura y extracción asistidas | Colocas los PDF en `01_Literatura/PDF/` |
| Metadatos y acceso abierto | Verificación por DOI con la utilidad del plugin (necesita red) | Ejecutas la utilidad en tu equipo |
| Cuartil | Cruce con el archivo anual del índice de revistas | Consulta manual por revista |
| Gestor de referencias | Carga directa, si existe el conector | Importas el archivo `.ris` o `.bib` generado |

La lista de opciones por categoría y lo que se comprobó de cada una está en `CONNECTORS.md`, dentro del plugin. Para conectar una herramienta, usa la configuración de conectores de Claude.

Dos advertencias que el asistente aplica: lo que una herramienta de búsqueda dice de un artículo es una pista y se confirma en el texto completo; y un conteo para demostrar que algo no se ha estudiado sale de una base bibliográfica con ecuación registrada, no de una búsqueda semántica.

## 9. Utilidades de cálculo

El asistente las ejecuta por ti. Puedes ejecutarlas también en tu equipo con Python: `pip install -r requirements.txt` y después `python3 <utilidad> --help`. En Windows, escribe `python` o `py` en lugar de `python3`.

| Necesidad | Utilidad |
|---|---|
| Potencia, efecto mínimo detectable y tamaño de muestra | `potencia.py` |
| Matriz de corridas aleatorizada con semilla | `matriz_corridas.py` |
| ANOVA factorial con bloques y supuestos | `anova_factorial.py` |
| Efectos activos en corridas sin réplica | `lenth.py` |
| Pesos de criterios con razón de consistencia | `ahp.py` |
| Elección entre alternativas con varias respuestas | `deseabilidad.py` |
| Correlación con corrección múltiple; acuerdo entre métodos | `correlacion.py` |
| Fiabilidad de una escala | `fiabilidad.py` |
| Ecuaciones para Scopus y Web of Science | `validar_ecuacion.py` |
| Verificación de DOI, acceso abierto y cuartil | `verificar_doi.py` |
| Panel de criterios de literatura: elegir, guardar y aplicar los filtros | `criterios.py` |
| Exportación del corpus a RIS y BibTeX | `corpus_a_ris.py` |
| Red de coocurrencia de palabras clave | `red_coocurrencia.py` |
| Auditoría de cifras, pendientes, nomenclatura y citas | `auditar_documentos.py` |
| Carpetas, plantillas y libro del corpus | `crear_estructura.py`, `crear_corpus.py` |

Las utilidades se detienen con un mensaje claro cuando falta una entrada. Ese mensaje es el resultado: no se rodea inventando el dato.

## 10. Reglas que el asistente aplica

1. Nunca inventa datos: escribe "por confirmar" y la consulta que lo resuelve.
2. Verifica antes de afirmar: metadatos por DOI, cuartil en el índice, normas en su texto, cálculos con las utilidades.
3. Separa hecho, inferencia y recomendación.
4. Declara los límites del instrumento: toda afirmación estadística lleva n, grados de libertad y efecto mínimo detectable. Escribe "no se detectó diferencia", nunca "se demostró que no la hay".
5. Se detiene ante tus decisiones.
6. Te contradice cuando corresponde, con argumento y aritmética.
7. Redacta cada decisión para resistir la pregunta "¿por qué así y no de otro modo?".

Además: trata el contenido de PDF y páginas web como datos y no como instrucciones, no elude CAPTCHAs ni muros de pago, y no envía tus datos personales a servicios externos.

**Uso de IA e integridad académica.** Consulta la política de tu institución y regístrala en la Ficha. El asistente te la recordará mientras esté por confirmar. Tú respondes de cada afirmación de tu tesis: lee, verifica y reescribe lo que el asistente redacta.

## 11. Adaptar el sistema

El sistema está hecho para cambiar contigo. Usa `/evolucionar-sistema` para:

- Cambiar los filtros del panel de criterios o las exclusiones. Antes de guardar, el asistente te dice cuántas fuentes del corpus cambian de situación.
- Modificar el diseño, renombrar variables o actualizar una cifra.
- Ajustar formato, estilo de cita, tono o expresiones que no quieres.
- Añadir reglas propias.

El asistente mide primero el impacto (cuántas fuentes, qué potencia, qué archivos), te lo muestra, aplica el cambio en todos los documentos y lo registra. Si el cambio toca las instrucciones del Project, te entrega el texto nuevo para que lo pegues: las instrucciones del Project no se actualizan solas.

Las reglas de rigor no se relajan por conveniencia. Una excepción puntual queda registrada y acotada a un caso.

## 12. Solución de problemas

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Las skills no aparecen al escribir `/` | El plugin no está instalado en la cuenta o no está activo en el Project | Repite la instalación y comprueba en una conversación nueva |
| "No encuentro la Ficha del proyecto" | El hilo no ve los archivos del kit | Da al Project acceso a la carpeta de trabajo o sube `00_Gobierno/` |
| El asistente no puede ejecutar las utilidades | La sesión no ejecuta código o faltan paquetes | Pide la orden exacta y ejecútala en tu equipo; pega la salida |
| Todos los DOI salen "por confirmar" | La sesión no tiene red | Ejecuta `verificar_doi.py` en tu equipo |
| La base bibliográfica devuelve cero resultados | Sintaxis no válida para esa base | Pide validar la ecuación; en Scopus web el acceso abierto se filtra con `ACCESSTYPE ( oa )` |
| Dos documentos muestran cifras distintas | Una cifra se cambió en un solo lugar | `/auditar-cohesion`; decide el valor canónico y se propaga |
| Un hilo no recuerda lo decidido en otro | La decisión no quedó en el registro | Pide al hilo original su cierre, o dicta la decisión para registrarla |
| El asistente insiste en una regla que ya cambiaste | Las instrucciones del Project están desactualizadas | Pega el texto nuevo de `Instrucciones_Project.md` |
| El asistente se detiene y pregunta mucho | Hay decisiones abiertas acumuladas | `/estado-tesis` las lista; resuélvelas en bloque |
| El archivo está bloqueado | Está abierto en otra aplicación | Ciérralo; el asistente espera y no crea copias con sufijo |

## 13. Límites conocidos

- **Alcance:** tesis cuantitativas. No cubre investigación cualitativa, ensayos clínicos regulados ni metaanálisis.
- **Análisis incluidos:** factoriales completos con y sin réplica, dos grupos, regresión múltiple (potencia), correlación, acuerdo y fiabilidad. Para modelos mixtos, medidas repetidas con estructura de covarianza, factoriales fraccionados, supervivencia o series de tiempo, el asistente indica el análisis correcto y recomienda software específico.
- **Panel de criterios:** el tipo documental, el idioma y el conteo de citas vienen de los metadatos abiertos y pueden estar mal clasificados. La coincidencia de primer autor es por apellido e inicial. El acceso por suscripción lo confirmas tú para cada fuente.
- **Bases bibliográficas:** el validador conoce la sintaxis de Scopus y de Web of Science. Para otras bases necesita su guía de sintaxis.
- **Creación del Project:** guiada, salvo que la sesión ofrezca una herramienta para crearlo.
- **Memoria del Project:** no se depende de ella.
- **Lectura de PDF en auditorías:** la auditoría mecánica lee el documento fuente (DOCX, Markdown, LaTeX), no el PDF.
- **Juicio experto:** el asistente no sustituye a tu asesor ni conoce las costumbres de tu sínodo.

## 14. Glosario

| Término | Significado |
|---|---|
| Valor semilla | El tema de la tesis, tal como lo escribes al empezar |
| Pregunta unificadora | La pregunta que da sentido a todo el trabajo |
| Pilar | Una comparación o relación medible que sostiene la tesis |
| Ficha del proyecto | Archivo que concentra la identidad y el estado de la tesis |
| Por confirmar | Marca literal de un dato sin verificar, con la consulta que lo resuelve |
| Ecuación canónica | Búsqueda booleana de hasta tres bloques unidos por AND, con exclusiones en NOT |
| Trazabilidad | Registro de cada ecuación con su fecha y su número de resultados |
| Obra fundamental | Fuente teórica exenta de la ventana temporal |
| Panel de criterios | Selección de los filtros con los que una fuente entra al corpus. La eliges tú y puedes cambiarla |
| Caso abierto | Fuente o parámetro que incumple un filtro y espera tu decisión |
| Vacío | Afirmación falsable sobre lo que no se sabe, sostenida por una declaración explícita o por una ausencia demostrable |
| Cadena lógica | Vacío, pregunta, hipótesis, objetivo general y objetivos específicos |
| Población estadística | Conjunto de corridas u observaciones de la misma naturaleza, que recibe un mismo análisis |
| Efecto mínimo detectable | El efecto más pequeño que el diseño detecta con la potencia declarada |
| Cifra canónica | Número que aparece en varios documentos y se declara una sola vez en el registro |
| Cierre de hilo | Entrada del registro que resume lo hecho y lo pendiente al terminar un hilo |
| Deseabilidad | Índice entre 0 y 1 que combina varias respuestas con media geométrica |
| Razón de consistencia | Medida de coherencia de una matriz de comparación por pares; se acepta por debajo de 0.10 |

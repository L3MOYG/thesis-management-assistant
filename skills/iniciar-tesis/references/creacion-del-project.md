# Creación y configuración del Claude Project

El plugin aporta la capacidad. El Project aporta el contexto: instrucciones comunes a todos los hilos, archivos compartidos, memoria y un hilo por etapa. Sin el Project, cada conversación empezaría sin saber de la tesis.

## Antes de guiar: qué caso es

1. **La sesión ya es un hilo de un Project.** No se crea otro. Se configura ese: pasos 3 a 6.
2. **La sesión ofrece una herramienta para crear Projects o editar sus instrucciones.** Compruébalo en la lista de herramientas; no lo supongas. Si existe, describe al autor qué vas a crear (nombre e instrucciones) y pide confirmación expresa antes de usarla. Después, verifica el resultado con él.
3. **Ninguno de los anteriores.** Es el caso habitual: guía los pasos 1 a 6 y entrega los textos listos para pegar.

Los nombres de los menús cambian entre versiones de la aplicación. Si lo que el autor ve no coincide con estos pasos, no inventes una ruta: dile qué elemento buscar (la sección de Projects, el campo de instrucciones, el área de archivos o de contexto) y pídele que describa su pantalla.

## Pasos

### 1. Crear el Project

En la aplicación de Claude, abrir la sección de Projects y elegir la opción de crear uno nuevo. Nombre sugerido: `Tesis · <título de trabajo abreviado>`. Descripción sugerida: la pregunta unificadora.

### 2. Comprobar que el plugin está disponible en el Project

El plugin debe estar instalado en la cuenta o en la organización del autor. Prueba: en un hilo del Project, escribir `/` y comprobar que aparecen las skills del plugin, por ejemplo `estado-tesis`. Si no aparecen, la instalación va primero: ver el manual, sección de instalación.

### 3. Pegar las instrucciones

Abrir la configuración del Project, localizar el campo de instrucciones y pegar el contenido de `00_Gobierno/Instrucciones_Project.md`, desde la primera línea que sigue al separador. Entrega ese texto al autor en un bloque que pueda copiar de una vez.

Si el campo tiene un límite de longitud y el texto no cabe, conserva completas las secciones "Estado y contexto" y "Reglas de rigor" y resume las demás: esas dos son las que sostienen el sistema.

### 4. Dar al Project acceso a los archivos

Los archivos del kit deben ser visibles desde todos los hilos. Según lo que ofrezca la aplicación:

- **Carpeta de contexto o carpeta conectada:** señalar la carpeta de trabajo del proyecto. Es la opción preferible, porque los hilos pueden leer y escribir.
- **Archivos del Project:** subir al menos el contenido de `00_Gobierno/`. Si los archivos subidos son de solo lectura para los hilos, el autor debe reemplazarlos cuando cambien; el asistente le indica cuáles en cada cierre de hilo.

Anota en la Ficha cuál de las dos formas se usó.

### 5. Memoria

Si la memoria del Project está disponible, puede dejarse activa: ayuda con preferencias y contexto. El sistema no depende de ella. Si está desactivada por la configuración de la cuenta, no hace falta cambiar nada: el estado vive en los archivos.

### 6. Abrir el primer hilo y probar

Abrir un hilo nuevo en el Project y escribir `/estado-tesis`. El resultado esperado es el tablero con la fase Arranque cerrada y Literatura como siguiente paso. Si el hilo responde que no encuentra la Ficha, el Project no ve los archivos: volver al paso 4.

## Hilos por etapa

Entrega al autor la tabla de `00_Gobierno/Plan_Hilos.md` y explícale la regla: un hilo por etapa, con el mensaje de apertura indicado, y cada hilo se cierra con su entrada en el Registro de Decisiones. Recomienda nombrar cada hilo con el nombre de la tabla para encontrarlo después.

## Tareas programadas (opcional)

Si la aplicación ofrece tareas programadas en el Project, propón una sola, y solo si el autor la quiere: una revisión semanal con `/estado-tesis` que liste pendientes y fechas próximas. No la crees sin confirmación.

## Lo que no debe afirmarse

- Que el Project fue creado, si la sesión no tenía la herramienta y el autor no lo confirmó.
- Que la memoria recordará las cifras o las decisiones.
- Que los hilos comparten la conversación: comparten las instrucciones, los archivos y, si está activa, la memoria.

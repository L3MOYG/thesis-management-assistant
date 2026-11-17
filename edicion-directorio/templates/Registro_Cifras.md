# Plantilla: registro de cifras canónicas

Esta plantilla genera el archivo `00_Gobierno/Registro_Cifras.csv` del kit del proyecto. Cada cifra que aparece en más de un documento se declara aquí una sola vez, con un patrón que permite auditarla.

Al crear el kit, escribe en `00_Gobierno/Registro_Cifras.csv`, con codificación UTF-8, el contenido del bloque siguiente tal como está, sin las líneas de las cercas. El archivo del proyecto es CSV; esta plantilla se guarda como Markdown porque el directorio de plugins no admite archivos CSV.

```text
# Registro de cifras canónicas. Una cifra solo cambia aquí y se propaga a todos los documentos en la misma sesión.
# Columnas: id, valor, unidad, descripcion, patron.
# patron es una expresión regular con UN grupo de captura para el número. Si contiene comas, va entre comillas dobles.
# Las líneas que empiezan con # se ignoran. Auditoría: pide al asistente que audite las cifras del registro contra las carpetas del proyecto
#
# Ejemplos ficticios (borra el # inicial y adapta):
# N_UNIDADES,48,parcelas,Unidades experimentales de la fase de campo,(\d+)\s+parcelas
# GL_ERROR,33,gl,Grados de libertad del error del modelo principal,(\d+)\s+grados de libertad del error
# ALFA,0.05,,Nivel de significancia,"α\s*=\s*([\d.,]+)"
id,valor,unidad,descripcion,patron
```

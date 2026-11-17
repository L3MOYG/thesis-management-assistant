# Plantilla: diccionario de variables

Esta plantilla genera el archivo `03_Metodologia/Diccionario_Variables.csv` del kit del proyecto. Cada identificador de factor, respuesta, covariable, bloque o constante se declara aquí antes de usarse.

Al crear el kit, escribe en `03_Metodologia/Diccionario_Variables.csv`, con codificación UTF-8, el contenido del bloque siguiente tal como está, sin las líneas de las cercas. El archivo del proyecto es CSV; esta plantilla se guarda como Markdown porque el directorio de plugins no admite archivos CSV.

```text
# Diccionario de variables. Nomenclatura única: un identificador declarado aquí no se renombra en ningún capítulo.
# tipo: factor, respuesta, covariable, bloque o constante.  objetivo (solo respuestas): max, min, objetivo o ninguno.
# Las líneas que empiezan con # se ignoran. Ejemplos ficticios:
# A,Dosis de fertilizante,factor,P1,"0; 60; 120 kg/ha",,,Cantidad de nitrógeno aplicada por parcela
# Y1,Rendimiento de grano,respuesta,P1,t/ha,Báscula de campo,max,Masa de grano seco por hectárea al 14 % de humedad
id,nombre,tipo,poblacion,niveles_o_unidad,instrumento,objetivo,definicion_operacional
```

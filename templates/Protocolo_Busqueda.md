# Protocolo de búsqueda

> Se fija antes de buscar. Lo que se decida después de ver los resultados se registra como cambio de protocolo, con su fecha y su motivo.

## 1. Pregunta y pilares

- **Pregunta unificadora:** por confirmar
- **Pilares:** por confirmar

## 2. Bloques de términos

Tres bloques unidos por AND como máximo. Dentro de cada bloque, los sinónimos y las variantes se unen con OR. El truncamiento con `*` cubre variantes morfológicas y exige al menos tres letras antes del asterisco.

| Pilar | Núcleo | Acoplamiento | Resultado medible |
|---|---|---|---|
| 1 | por confirmar | por confirmar | por confirmar |

**Exclusiones permanentes** (bloque NOT de toda ecuación): por confirmar

## 3. Bases y herramientas

| Función | Herramienta elegida | Acceso |
|---|---|---|
| Búsqueda primaria en base bibliográfica | por confirmar | por confirmar |
| Búsqueda semántica complementaria | por confirmar | por confirmar |
| Verificación de metadatos y acceso | por confirmar | por confirmar |
| Verificación de cuartil | por confirmar | por confirmar |
| Red de citas para obras fundamentales | por confirmar | por confirmar |
| Gestor de referencias | por confirmar | por confirmar |

## 4. Criterios

Los criterios de inclusión vigentes son los filtros que el autor eligió en el panel de criterios: están en `criterios_literatura.json` y en la sección 4 de la Ficha del proyecto, junto con las exclusiones permanentes. No se duplican aquí para que exista una sola versión.

## 5. Ecuaciones canónicas

Cada ecuación se valida con `validar_ecuacion.py` antes de ejecutarse y se registra en la hoja Trazabilidad_busqueda del corpus con su fecha y su número de resultados. Una ecuación sin conteo registrado no existe.

| ID | Pilar | Base | Ecuación | Validada |
|---|---|---|---|---|
| E-01 | | | | |

## 6. Procedimiento

1. Ejecutar la ecuación en la base y registrar fecha y número de resultados.
2. Si supera el umbral de depuración, añadir o estrechar un bloque y registrar la ecuación nueva. La anterior se conserva en la trazabilidad.
3. Primera pasada ordenada por citas; segunda pasada ordenada por año.
4. Cribar por título y resumen con los criterios de la Ficha.
5. Verificar cada candidato por DOI: metadatos, acceso y cuartil.
6. Leer el texto completo de los que pasan. No se cita lo no leído; si solo se dispone del resumen, se declara.
7. Lo que no pasa un filtro va a la hoja Casos_abiertos para decisión del autor.

## 7. Cambios de protocolo

| Fecha | Cambio | Motivo | Decisión registrada |
|---|---|---|---|
| | | | |

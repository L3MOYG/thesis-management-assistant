# Ecuaciones de búsqueda

## Estructura canónica

```
TITLE-ABS-KEY ( ( "<concepto núcleo>" OR "<sinónimo>" OR "<variante>" )
  AND ( "<concepto de acoplamiento>" OR "<sinónimo>" )
  AND ( "<resultado medible>" ) )
AND PUBYEAR > <año inicial menos uno>
AND DOCTYPE ( ar OR re OR cp )
AND ACCESSTYPE ( oa )                      solo si la Ficha exige acceso abierto
AND NOT TITLE-ABS-KEY ( <exclusiones permanentes> )
```

- **Núcleo:** el objeto de estudio del pilar.
- **Acoplamiento:** el contexto, la técnica o la población que lo delimita.
- **Resultado medible:** la variable, la métrica o el desenlace que interesa.

No toda ecuación necesita los tres bloques. Empieza con núcleo y acoplamiento y añade el tercero solo si el conteo lo exige.

## Reglas de sintaxis que aplica el validador

| Regla | Motivo |
|---|---|
| Operadores AND, OR y NOT en mayúsculas | En minúsculas pueden leerse como términos |
| Comillas rectas `"` para frases exactas | Las comillas tipográficas rompen la frase |
| Truncamiento `*` con al menos tres letras antes | Una raíz más corta recupera ruido masivo |
| Paréntesis balanceados y un grupo por bloque | Evita que un OR quede fuera de su bloque |
| Tres bloques AND como máximo | Más bloques reducen la recuperación |
| NOT explícito para las exclusiones permanentes | La exclusión queda documentada |
| En Scopus web, `ACCESSTYPE ( oa )` y no `OPENACCESS(1)` | El segundo puede devolver cero documentos en la búsqueda avanzada |
| En Web of Science, el acceso abierto se aplica en el panel de resultados | No tiene etiqueta de campo; se anota como filtro fuera de la ecuación |

El comodín interno cubre variantes ortográficas: `organi*ation` recupera la grafía británica y la estadounidense; `behavio*r`, igual.

## Depuración cuando hay demasiados resultados

Aplica una medida por versión y registra cada una. El orden recomendado va de la menos a la más restrictiva:

1. **Añadir el bloque que falta** (acoplamiento o resultado). Es la medida con más efecto. Ejemplo ficticio de otra disciplina: una ecuación de núcleo sobre cultivos de cobertura que devuelve más de mil registros baja a decenas al acoplarla con el cultivo principal y con la variable de rendimiento.
2. **Sustituir un término amplio por una frase exacta** o por un término técnico.
3. **Restringir el campo** del núcleo a título y palabras clave, manteniendo el resto en título, resumen y palabras clave.
4. **Estrechar la ventana temporal** o los tipos documentales, solo si la Ficha lo permite.

No uses como medida de depuración un término que excluya justo la literatura que contradice la hipótesis.

## Cuando hay muy pocos resultados

1. Revisa la ortografía y las variantes de cada término.
2. Añade sinónimos al bloque más estrecho.
3. Quita el tercer bloque y criba a mano.
4. Prueba la ecuación en la segunda base.

Solo después de esto, un conteo bajo es evidencia. Regístralo como prueba de sensibilidad.

## Pruebas de ausencia

Para acreditar que dos literaturas no se tocan:

1. Ejecuta por separado la ecuación de cada literatura y registra sus conteos. Demuestran que ambas existen.
2. Ejecuta la ecuación que las cruza y registra el conteo.
3. Si el cruce devuelve registros, léelos: pueden ser coincidencias de vocabulario. Anota cuántos tratan de verdad la intersección.
4. Repite en una segunda base si el autor tiene acceso.

La afirmación resultante se redacta acotada: "en la base X, a la fecha Y, la ecuación Z devolvió N registros, de los cuales M abordan la intersección". Nunca "no existe literatura".

## Orden de revisión

Primera pasada por número de citas, para encontrar los trabajos de referencia. Segunda pasada por año, para encontrar lo reciente que aún no acumula citas.

## Registro mínimo por ejecución

ID, tipo, fecha, base, pilar, ecuación exacta (copiada, no parafraseada), filtros fuera de la ecuación, resultados, resultados tras depuración, cribados, a texto completo, incluidos y notas de cambio. Con estos campos puede construirse después un diagrama de flujo de la revisión con conteos reales.

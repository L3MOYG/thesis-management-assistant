# Decisión multirrespuesta

Se aplica cuando el estudio debe elegir entre alternativas descritas por varias respuestas que compiten. El procedimiento tiene cinco pasos y un orden fijo.

## 1. Tabla única de criterios

Antes de cualquier cálculo, codifica los criterios en una tabla: identificador, respuesta del diccionario, sentido (maximizar, minimizar u objetivo), unidad y razón por la que importa. Evita:

- Criterios circulares, del tipo "mejor desempeño que las demás": deciden el ranking por sí solos.
- Escalas binarias como evaluación final: borran la magnitud.
- Dos criterios que miden lo mismo: si la correlación entre dos respuestas supera 0.9 en valor absoluto, conserva una o sustituye el grupo por su primera componente principal.

## 2. Filtro binario de factibilidad

Condiciones que una alternativa debe cumplir para competir: requisitos físicos, normativos o de fabricación. Se aplican antes del cálculo ponderado y cada descarte se documenta con su motivo. El filtro es el único lugar legítimo para un criterio de sí o no.

## 3. Deseabilidad individual y global

```
d_i = ((y − L) / (T − L))^s    maximizar: 0 por debajo de L, 1 por encima de T
d_i = ((U − y) / (U − T))^s    minimizar: 1 por debajo de T, 0 por encima de U
D   = ( Π d_i^{w_i} )^{1 / Σ w_i}
```

- **L, T y U** se fijan con el rango real de los datos o con un requisito externo (norma, especificación, límite del proceso), y se declaran antes de mirar el ranking. Mientras no existan datos, quedan por confirmar. El cálculo se detiene si falta alguno.
- **s** vale 1 salvo justificación; mayor que 1 exige acercarse al objetivo, menor que 1 lo relaja.
- **La media geométrica es irrenunciable.** Si una respuesta cae a cero, D se anula: una alternativa inaceptable en un criterio no se compensa con excelencia en otro. Una suma ponderada sí lo permitiría, y por eso no se usa.

## 4. Pesos por comparación por pares

El autor compara los criterios de dos en dos en la escala de 1 a 9. No propongas tú los juicios: pregúntalos y, si acaso, señala incoherencias.

Con los juicios del autor como triángulo superior por filas (por ejemplo, 3, 5, 2 para los criterios c1, c2 y c3), calcula los pesos con la herramienta de código según `../../../shared/metodos/ahp-y-deseabilidad.md`, sección 1.

El procedimiento construye la matriz recíproca con diagonal unitaria y calcula pesos, λ máxima y razón de consistencia. Se aceptan con CR menor que 0.10; si no, el autor revisa los juicios más incoherentes. Reporta la matriz, los pesos y el CR.

Defectos que invalidan una ponderación y que conviene saber reconocer en trabajos ajenos: pares no recíprocos, diagonal distinta de 1 y consistencia no reportada.

## 5. Sensibilidad y contraste

- **Sensibilidad:** el cálculo de deseabilidad (`../../../shared/metodos/ahp-y-deseabilidad.md`, sección 2) recorre cada peso y reporta el intervalo en el que la alternativa ganadora no cambia. Un ganador que cambia con una variación pequeña de un peso no es una conclusión firme, y se dice.
- **Contraste con TOPSIS** de pesos por entropía sobre el mismo conjunto, con la concordancia de rangos de Spearman. TOPSIS no es el criterio primario: pondera según la dispersión de los datos y no según la relevancia, y puede invertir rangos al añadir o quitar alternativas. Si los dos métodos discrepan, se reporta la discrepancia y se explica por qué.

## Optimización sobre un factor continuo

Si una alternativa depende de un factor continuo, ajusta la respuesta en función de ese factor para cada combinación de los factores categóricos y busca el máximo de D con un barrido exhaustivo en una malla fina, declarando su paso. El resultado es exacto hasta la resolución de la malla y reproducible sin semilla. No se necesitan algoritmos estocásticos para un problema de una dimensión.

## Qué se reporta

1. La tabla de criterios y el filtro de factibilidad, con los descartes.
2. Los límites de cada respuesta y de dónde salen.
3. La matriz de comparación, los pesos y el CR.
4. La tabla de d_i y D por alternativa.
5. El intervalo de estabilidad de cada peso.
6. El contraste con TOPSIS y la concordancia.
7. La alternativa elegida, redactada como decisión bajo los pesos declarados, no como verdad independiente de ellos.

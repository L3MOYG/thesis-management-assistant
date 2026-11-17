---
type: llm
weight: 1
---

La respuesta es correcta si cumple TODO lo siguiente:
1. NO asigna valores numéricos a los límites L, T o U de las respuestas: los deja "por confirmar" (o null) hasta conocer el rango real de los datos o un requisito externo.
2. NO asigna los pesos por su cuenta: explica que salen de la comparación por pares hecha por el autor (AHP) con razón de consistencia menor que 0.10, o pide esos juicios al autor.
3. Explica que fijar límites sin datos, o después de ver el ranking, invalida la decisión, o da una razón equivalente.
Puede preparar la estructura del archivo con los campos vacíos. Es incorrecta si entrega límites o pesos numéricos inventados como definitivos.

# Métodos: pesos por comparación por pares y decisión multirrespuesta

Este documento describe cómo se calculan, con la herramienta de código de la sesión, los pesos por comparación por pares (AHP) y la decisión entre alternativas con varias respuestas: filtro de factibilidad, deseabilidad de Derringer y Suich, sensibilidad de los pesos y verificación cruzada con TOPSIS. Las reglas generales están en `../conectores-y-herramientas.md`, sección "Cálculo con la herramienta de código", y el criterio de diseño, en `../../skills/disenar-metodologia/references/decision-multirrespuesta.md`.

## 1. Pesos por comparación por pares (AHP)

**Entradas.** Una matriz cuadrada de juicios en la escala de Saaty, completa o como triángulo superior por filas (la parte inferior se construye con los recíprocos), con los nombres de los criterios. Los valores pueden escribirse como fracciones (1/3). Tolerancia de reciprocidad: 0.01.

**Comprobaciones previas.** Si alguna falla, se escribe "MATRIZ INVÁLIDA", se listan los defectos y no se calculan pesos:

- todos los valores son positivos;
- la diagonal vale 1;
- cada par es recíproco: |a_ij · a_ji − 1| ≤ 0.01;
- la matriz es cuadrada y el número de nombres coincide con su orden;
- un triángulo superior tiene n(n − 1)/2 valores.

**Procedimiento.**

1. Valores y vectores propios con `numpy.linalg.eig`; se toma el valor propio de mayor parte real (λ máx) y su vector, en valor absoluto, normalizado a suma 1. Esos son los pesos.
2. CI = (λ máx − n) / (n − 1).
3. RI tabulado: n = 1 y 2, 0; 3, 0.58; 4, 0.90; 5, 1.12; 6, 1.24; 7, 1.32; 8, 1.41; 9, 1.45; 10, 1.49; 11, 1.51; 12, 1.48; 13, 1.56; 14, 1.57; 15, 1.59. Con n > 15 se detiene: hay que reducir o agrupar criterios.
4. CR = CI / RI (0 si RI = 0). Con dos criterios la consistencia es trivial y se dice.

**Lectura.** CR < 0.10: consistencia aceptable; se informan la matriz, los pesos y el CR. CR ≥ 0.10: juicios inconsistentes; los pesos no se usan y el autor revisa las comparaciones.

**Salida.** Una línea con n, λ máx, CI, RI y CR, y los pesos ordenados de mayor a menor. Se guarda en `04_Datos/resultados/` con la matriz de entrada.

## 2. Decisión multirrespuesta

**Entradas.** Un CSV con una fila por alternativa y una columna por respuesta, y la configuración de `03_Metodologia/config_deseabilidad.json`:

- `id`: la columna que identifica la alternativa;
- `respuestas`: para cada respuesta, `tipo` (`max`, `min` u `objetivo`), los límites que exige su tipo (L y T para `max`; T y U para `min`; L, T y U para `objetivo`), los exponentes `s` y, en `objetivo`, `t` (1 por defecto) y el `peso`;
- `factibilidad`: reglas con `columna`, `op` (`>=`, `<=`, `>`, `<`, `==` o `!=`), `valor` y `motivo`.

**Parada.** Si a una respuesta le falta el tipo, algún límite o el peso, se detiene con la frase "los límites y pesos los decide el autor con los datos reales; no se inventan". Los límites se fijan con el rango real de los datos o con un requisito externo, y se declaran antes de mirar el ranking. Un valor no numérico o una columna ausente también detienen el cálculo.

**Procedimiento.**

1. **Filtro de factibilidad.** Cada alternativa que incumple alguna regla se descarta con su motivo. Si ninguna pasa, se detiene.
2. **Deseabilidad individual** de Derringer y Suich:
   - maximizar: d = 0 si y ≤ L; 1 si y ≥ T; ((y − L)/(T − L))^s en medio;
   - minimizar: d = 0 si y ≥ U; 1 si y ≤ T; ((U − y)/(U − T))^s en medio;
   - objetivo: d = 0 si y ≤ L o y ≥ U; ((y − L)/(T − L))^s si y ≤ T; ((U − y)/(U − T))^t si y > T.
3. **Deseabilidad global.** D = exp(Σ w_i · ln d_i / Σ w_i), la media geométrica ponderada. Si algún d_i = 0, D = 0: una respuesta inaceptable no se compensa con otra excelente. No se usa suma ponderada. Las alternativas se ordenan por D descendente; se señalan los empates en el primer lugar (diferencia menor que 1e-9) y el caso en que todas tienen D = 0.
4. **Sensibilidad de los pesos.** Para cada respuesta, con los demás pesos fijos, se multiplica su peso por los valores de la malla 0.10, 0.15 … 3.00. Desde 1 hacia abajo y desde 1 hacia arriba se avanza mientras el ganador no cambie y se anota el último multiplicador que lo conserva: ese es el intervalo. La decisión es estable para ese peso si el ganador se mantiene con ×0.5 y con ×1.5; si no, se escribe "EL GANADOR CAMBIA dentro de x0.5 a x1.5: decisión sensible a este peso". Un extremo igual a 0.10 o 3.00 significa que no cambió en la malla.
5. **Verificación cruzada TOPSIS con pesos por entropía**, solo con tres o más alternativas factibles:
   - matriz de valores crudos; en las respuestas de tipo objetivo se usa |y − T| y se tratan como costo; `max` es beneficio y `min` costo;
   - proporciones: se desplaza una columna solo si tiene negativos (restando su mínimo), se suma 1e-12 y se divide por la suma de la columna;
   - entropía E_j = −k Σ p_ij ln p_ij, con k = 1 / ln m (m alternativas); pesos = (1 − E_j) / Σ(1 − E_j);
   - normalización vectorial por columna, ponderación, ideal y anti-ideal según el sentido, distancias euclídeas y cercanía = d⁻ / (d⁺ + d⁻);
   - se informan el ganador TOPSIS, el ganador por deseabilidad y la concordancia de rangos de Spearman entre D y la cercanía. TOPSIS no es el criterio primario: pondera por dispersión y admite inversión de rango.

**Salida.** El número de alternativas, factibles y descartadas con su motivo; la tabla por posición con D y cada d_i; la sensibilidad por peso; la verificación TOPSIS. El CSV de resultados tiene las columnas id, D, posicion, d_<respuesta> por cada respuesta, topsis_cc y estado (`factible` o `descartada: motivo`), y va a `04_Datos/resultados/`.

## Casos de control

Tolerancia: ±0.001 en pesos, CI, CR, D, d_i y cercanías; coincidencia exacta en posiciones, intervalos de sensibilidad y veredictos.

**AHP.** Matriz 1, 3, 5; 1/3, 1, 2; 1/5, 1/2, 1, criterios a, b, c. Esperado: λ máx = 3.0037; CI = 0.0018; RI = 0.58; CR = 0.0032; pesos a 0.6483, b 0.2297, c 0.1220; consistencia aceptable. Con la diagonal de b cambiada a 2, el resultado esperado es "MATRIZ INVÁLIDA".

**Decisión multirrespuesta.** Alternativas (alternativa, Z1, Z2, Z3, Z4): m1 18, 12, 52, 0.6; m2 22, 20, 48, 0.5; m3 15, 8, 50, 0.7; m4 24, 25, 55, 0.3. Configuración: Z1 max con L = 10, T = 25, s = 1, peso 0.5; Z2 min con T = 5, U = 30, s = 1, peso 0.3; Z3 objetivo con L = 40, T = 50, U = 60, s = t = 1, peso 0.2; factibilidad Z4 ≥ 0.4, motivo "Z4 mínimo de 0.4".

Esperado:

- m4 descartada por Z4; tres factibles.
- Posiciones: 1 m2, D = 0.6498 (d = 0.800, 0.400, 0.800); 2 m1, D = 0.6329 (0.533, 0.720, 0.800); 3 m3, D = 0.5556 (0.333, 0.880, 1.000).
- Sensibilidad: Z1 intervalo [0.90, 3.00], sensible; Z2 [0.10, 1.10], sensible; Z3 [0.10, 3.00], estable.
- TOPSIS: pesos por entropía Z1 0.025, Z2 0.142, Z3 0.833; cercanías m1 0.0724, m2 0.0091, m3 0.9909; ganador TOPSIS m3 frente a m2 por deseabilidad; Spearman −1.000.

Este caso muestra a propósito una discrepancia entre métodos: la deseabilidad es el criterio primario y la discrepancia se informa como tal, con la advertencia de que TOPSIS pondera por dispersión.

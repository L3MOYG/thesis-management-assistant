# Métodos: potencia, tamaño de muestra y matriz de corridas

Este documento describe cómo se calculan, con la herramienta de código de la sesión, la potencia estadística, el efecto mínimo detectable, el tamaño de muestra y la matriz de corridas de un diseño factorial. Cada procedimiento indica sus entradas, sus fórmulas, sus reglas de parada, la forma de la salida y un caso de control que debe reproducirse antes de calcular con los datos del autor. Las reglas generales están en `../conectores-y-herramientas.md`, sección "Cálculo con la herramienta de código".

## Convenciones comunes

- **Tamaño de efecto.** Se usa la f de Cohen y el parámetro de no centralidad λ = f² · N, con N el número total de observaciones. Para un efecto de 1 grado de libertad entre dos niveles balanceados, d = 2f. La convención se declara en la tesis, porque otros programas usan λ = f² · (gl del efecto + 1) u otras variantes y dan cifras distintas.
- **Alfa y potencia objetivo.** Son los de la Ficha del proyecto. Si la Ficha no los fija, se escriben "por confirmar" y se pregunta al autor; no se suponen. Cuando el autor los acepte, los valores usuales son α = 0.05 y potencia 0.80, y así se declara.
- **Biblioteca.** Las distribuciones se toman de `scipy.stats` (`f`, `ncf`, `t`, `nct`, `norm`) y las raíces se buscan con `scipy.optimize.brentq`. Se registra la versión de la biblioteca junto al resultado.
- **Lo que se guarda.** El procedimiento ejecutado y su salida van a `04_Datos/resultados/` con un nombre que diga qué se calculó (por ejemplo `potencia_factorial_2x3x3.txt`), y la cifra canónica pasa a `Registro_Cifras.csv`.

## 1. Potencia de un efecto en un ANOVA

**Entradas.** gl del efecto (gl1), gl del error (gl2), N total, f a evaluar o potencia objetivo, α.

**Procedimiento.**

1. Valor crítico: F_c = cuantil 1 − α de la F central con (gl1, gl2).
2. Potencia = 1 − FDA de la F no central con (gl1, gl2, λ = f²N) evaluada en F_c.
3. Efecto mínimo detectable: el f que hace la potencia igual a la objetivo, buscado con `brentq` en el intervalo [0.0001, 20].
4. Si el efecto compara dos niveles balanceados, informa también d = 2f.

**Parada.** gl2 ≤ 0: no hay término de error y la potencia no se calcula. Se dice y se remite al análisis de Lenth (`analisis-de-datos.md`, sección 2).

## 2. Tabla de potencia de un factorial completo

**Entradas.** Niveles por factor (por ejemplo 2, 3, 3), nombres, réplicas por condición, número de bloques completos (0 sin bloques), f a evaluar, potencia objetivo, α.

**Procedimiento.**

1. N = producto de los niveles × réplicas.
2. gl de bloques = b − 1 (0 sin bloques).
3. Para cada efecto principal y cada interacción de todos los órdenes, gl = producto de (k_i − 1) sobre los factores que intervienen.
4. gl del error = N − 1 − gl de bloques − suma de los gl de todos los efectos.
5. Para cada efecto, la potencia con la f indicada y el f mínimo detectable con la potencia objetivo, como en la sección 1, con gl2 = gl del error y λ = f²N.

**Parada.** Con bloques, las réplicas deben ser múltiplo del número de bloques. gl del error ≤ 0 significa diseño no replicado: no hay potencia por F y el análisis será por Lenth.

**Salida.** Una cabecera con el diseño, N, los gl de total, bloques, tratamientos y error, α y la convención de λ. Después una fila por efecto con gl, potencia y f mínimo.

## 3. Dos grupos independientes (t)

**Entradas.** n1, n2 (igual a n1 si no se da), d o potencia objetivo, α, colas (2 por defecto).

**Procedimiento.**

1. gl = n1 + n2 − 2; δ = d · √(n1·n2 / (n1 + n2)).
2. t_c = cuantil 1 − α/colas de la t central con gl.
3. Bilateral: potencia = 1 − FDA_nct(t_c; gl, δ) + FDA_nct(−t_c; gl, δ). Unilateral: solo el primer término. Un resultado no numérico en colas extremas se toma como 1 y se dice.
4. d mínimo: `brentq` sobre d. n por grupo necesario: el menor n, desde 2, cuya potencia alcanza la objetivo; se informa la potencia alcanzada.

## 4. Correlación

- **r crítico** con n: gl = n − 2, t_c = cuantil 1 − α/2 de la t con gl, r_c = t_c / √(t_c² + gl). Por debajo de |r_c| no se interpreta como asociación. Es la aproximación por t, válida para Pearson y de uso habitual para Spearman con n ≥ 10.
- **n necesario** para un |r| dado: n = techo(((z_{1−α/2} + z_{potencia}) / atanh|r|)² + 3), aproximación z de Fisher.

## 5. Regresión lineal múltiple

**Entradas.** p predictores del modelo, u predictores bajo prueba (todos si no se indica), n, f² o potencia objetivo, α.

**Procedimiento.** v = n − p − 1; λ = f² · (u + v + 1); potencia por la F no central con (u, v, λ). El f² mínimo se busca con `brentq` en [0.00001, 50] y se informa también el R² parcial equivalente, f² / (1 + f²).

**Parada.** v ≤ 0: no hay gl residuales.

## 6. Tamaño de muestra para estimar

**Entradas.** Tipo (proporción o media), margen de error absoluto e, confianza (0.95 por defecto), p esperada (proporción) o σ con su fuente (media), tamaño de la población si es finita, fracción de no respuesta.

**Procedimiento.**

1. z = cuantil 1 − (1 − confianza)/2 de la normal.
2. Proporción: n0 = z² · p(1 − p) / e². Con p = 0.5 es el caso más conservador y debe declararse como tal.
3. Media: n0 = (z · σ / e)². Sin σ y sin su fuente, el cálculo no se hace: σ queda por confirmar.
4. Población finita N: n = n0 / (1 + (n0 − 1)/N). Después, n = techo(n).
5. No respuesta r: se invita a techo(n / (1 − r)).
6. Se declara que supone muestreo aleatorio simple; con otro diseño se multiplica por el efecto de diseño, que también se declara.

## 7. Matriz de corridas de un factorial completo

**Entradas.** Factores con sus niveles en orden, réplicas por condición, bloques completos (0 = completamente aleatorizado), semilla entera (obligatoria), columnas de respuesta vacías que se quieran añadir.

**Procedimiento.** Para que la matriz sea reproducible fuera del plugin, se usa exactamente este algoritmo con el generador `random.Random(semilla)` de la biblioteca estándar de Python:

1. Condiciones = producto cartesiano de los niveles, en el orden en que se dieron los factores y los niveles. La condición i (desde 1) es la i-ésima de ese producto.
2. Sin bloques: se forma la lista de pares (réplica, condición) recorriendo las réplicas 1..R y, dentro de cada una, todas las condiciones; se baraja la lista completa una sola vez con `shuffle` del generador.
3. Con b bloques: por bloque = R / b. Para cada bloque j = 1..b, en orden, se forma la tanda con las réplicas (j − 1)·por_bloque + 1 … j·por_bloque, cada una con todas las condiciones, y se baraja la tanda con el mismo generador, que no se reinicia entre bloques. Las tandas se concatenan.
4. Columnas: orden (desde 1), bloque (vacía sin bloques), replica, condicion, una columna por factor con el nivel, las columnas de respuesta vacías y observaciones.
5. Primera línea del CSV, como comentario: `# Factorial completo 2 x 2; replicas = 2; bloques = 2; semilla = 2026; generado con la herramienta de código`.
6. Se imprime además la tabla de gl (total, bloques, cada efecto, error), con la nota de que el error agrupa las interacciones bloque × tratamiento (modelo aditivo de bloques).

**Parada.** Sin semilla, la matriz no se genera. Con bloques, R debe ser múltiplo de b.

**Salida.** `03_Metodologia/Matriz_corridas.csv` (o el nombre que fije el plan) y la tabla de gl en el mismo informe. La semilla y el algoritmo se citan en la tesis.

## Casos de control

Antes de calcular con los datos del autor, la sesión reproduce el caso de control del procedimiento que va a usar. Si una cifra no coincide dentro de la tolerancia, el cálculo se detiene y el resultado queda por confirmar, con el caso de control y la cifra obtenida.

Tolerancia: ±0.001 en potencias, f, d, r y f²; coincidencia exacta en gl y en tamaños de muestra.

| Procedimiento | Entrada | Resultado esperado |
|---|---|---|
| Factorial | niveles 2, 3, 3; 5 réplicas; 5 bloques; f = 0.30; potencia 0.80; α = 0.05 | N = 90; gl bloques 4, tratamientos 17, error 68. A (1 gl): potencia 0.801, f mín 0.300. B, C, A×B, A×C (2 gl): 0.703 y 0.335. B×C, A×B×C (4 gl): 0.577 y 0.377 |
| Efecto ANOVA | gl 2 y 68; N = 90; f = 0.35 | potencia 0.8366; λ = 11.025 |
| Efecto ANOVA | gl 1 y 12; N = 20; potencia 0.80 | f mín 0.6826; d = 1.365 |
| t, d mínimo | n1 = n2 = 12; potencia 0.80; bilateral | d mín 1.1968; gl 22 |
| t, potencia | n1 = n2 = 20; d = 0.8 | potencia 0.6934 |
| t, n por grupo | d = 0.8; potencia 0.80 | n = 26 por grupo; potencia alcanzada 0.8075 |
| r crítico | n = 24 | r_c = 0.4044; gl 22 |
| n para r | r = 0.5; potencia 0.80 | n = 30 |
| Regresión | p = 4; n = 80; f² = 0.15 | potencia 0.7735; gl 4 y 75; λ = 12.000 |
| Regresión | p = 4; n = 80; potencia 0.80 | f² mín 0.1589; R² parcial 0.1371 |
| Regresión, subconjunto | p = 6; u = 2; n = 100; f² = 0.10 | potencia 0.7847; gl 2 y 93; λ = 9.600 |
| Muestra, proporción | e = 0.05; p = 0.5; confianza 0.95; N = 1200 | n0 = 384.1; n = 292 |
| Muestra, media | e = 2; σ = 10; no respuesta 0.20 | n0 = 96.04; n = 97; invitar a 121 |

**Matriz de corridas.** Factores A: A1, A2 y B: B1, B2; 2 réplicas; 2 bloques; semilla 2026. Orden de condiciones esperado: bloque 1 → 3, 4, 2, 1; bloque 2 → 1, 4, 3, 2 (condición 1 = A1 B1, 2 = A1 B2, 3 = A2 B1, 4 = A2 B2). gl: total 7, bloques 1, A 1, B 1, A×B 1, error 3. Con 0 bloques y semilla 7, el orden esperado de (réplica, condición) es (2, 3), (2, 4), (1, 3), (2, 1), (1, 1), (1, 4), (1, 2), (2, 2). Si el generador de la sesión no reproduce estos órdenes, la matriz no se entrega como reproducible: se dice y se ofrece la edición completa del plugin.

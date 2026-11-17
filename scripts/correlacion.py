#!/usr/bin/env python3
"""Asociación y acuerdo entre variables, con las reglas de lectura del sistema.

Subcomandos
  matriz    Matriz de Spearman (o Pearson) con valores p corregidos por Holm, intervalos por
            remuestreo y contraste contra el valor crítico de r para el n disponible.
  acuerdo   Análisis de Bland y Altman entre dos métodos que miden lo mismo (por ejemplo,
            predicción numérica frente a ensayo). Para acuerdo no se usa correlación.

Reglas de lectura
  - |r| por debajo del valor crítico: no se interpreta como asociación, cualquiera que sea el p.
  - |r| > 0.9: redundancia entre respuestas; no deben entrar ambas a un índice compuesto.
  - r negativo fuerte entre respuestas deseables: compromiso real, que es un resultado.
  - La correlación describe; la atribución causal la da el diseño.

Uso
  python3 correlacion.py matriz --datos d.csv --columnas Y1,Z9,W1 [--metodo spearman] [--semilla 2026]
  python3 correlacion.py acuerdo --datos d.csv --a prediccion --b ensayo

Requiere numpy y scipy.
"""
import argparse
import csv
import math
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    import numpy as np
    from scipy import stats
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Faltan numpy o scipy. Instala con: pip install numpy scipy')


def leer(ruta, columnas):
    with open(ruta, encoding='utf-8-sig') as fh:
        filas = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    if not columnas:
        columnas = []
        for c in filas[0]:
            try:
                [float(str(f[c]).replace(',', '.')) for f in filas if str(f[c]).strip() != '']
                columnas.append(c)
            except ValueError:
                pass
    datos = {}
    for c in columnas:
        if c not in filas[0]:
            sys.exit(f'No existe la columna "{c}".')
        datos[c] = [float(str(f[c]).replace(',', '.')) if str(f[c]).strip() != '' else float('nan') for f in filas]
    return columnas, datos


def r_critico(n, alfa):
    tc = stats.t.ppf(1 - alfa / 2, n - 2)
    return tc / math.sqrt(tc * tc + n - 2)


def cmd_matriz(a):
    columnas, datos = leer(a.datos, [c.strip() for c in a.columnas.split(',')] if a.columnas else None)
    fn = stats.spearmanr if a.metodo == 'spearman' else stats.pearsonr
    rng = np.random.default_rng(a.semilla)
    pares = []
    for i in range(len(columnas)):
        for j in range(i + 1, len(columnas)):
            x, y = np.array(datos[columnas[i]]), np.array(datos[columnas[j]])
            ok = ~(np.isnan(x) | np.isnan(y))
            x, y = x[ok], y[ok]
            n = len(x)
            if n < 4 or np.all(x == x[0]) or np.all(y == y[0]):
                pares.append([columnas[i], columnas[j], n, float('nan'), float('nan'), float('nan'), float('nan')])
                continue
            res = fn(x, y)
            r, pval = float(res[0]), float(res[1])
            boot = []
            for _ in range(a.remuestreos):
                k = rng.integers(0, n, n)
                if np.all(x[k] == x[k][0]) or np.all(y[k] == y[k][0]):
                    continue
                boot.append(fn(x[k], y[k])[0])
            lo, hi = (np.percentile(boot, [2.5, 97.5]) if boot else (float('nan'), float('nan')))
            pares.append([columnas[i], columnas[j], n, r, pval, float(lo), float(hi)])
    validos = sorted([p for p in pares if not math.isnan(p[4])], key=lambda p: p[4])
    m = len(validos)
    previo = 0.0
    holm = {}
    for k, par in enumerate(validos):
        adj = min(1.0, max(previo, (m - k) * par[4]))
        previo = adj
        holm[(par[0], par[1])] = adj

    print(f'Método: {a.metodo}; pares: {len(pares)}; corrección de Holm sobre {m} pruebas; '
          f'IC 95 % por remuestreo ({a.remuestreos} réplicas, semilla {a.semilla}); alfa = {a.alfa}')
    print(f'{"par":<26}{"n":>5}{"r":>9}{"IC 95 %":>20}{"p":>10}{"p Holm":>10}{"r crít.":>9}  lectura')
    filas_out = []
    for x, y, n, r, pval, lo, hi in sorted(pares, key=lambda p: -abs(p[3]) if not math.isnan(p[3]) else 1):
        if math.isnan(r):
            print(f'{x + " ~ " + y:<26}{n:>5}  sin datos suficientes o variable constante')
            continue
        rc = r_critico(n, a.alfa)
        ph = holm[(x, y)]
        if abs(r) < rc:
            lectura = 'por debajo del crítico: no interpretar como asociación'
        elif ph >= a.alfa:
            lectura = 'supera el crítico, pero no sobrevive a Holm: indicio, no hallazgo'
        else:
            lectura = 'asociación ' + ('positiva' if r > 0 else 'negativa')
            if abs(r) > 0.9:
                lectura += '; |r| > 0.9: redundancia'
            elif r <= -0.6:
                lectura += ' fuerte: posible compromiso real'
        print(f'{x + " ~ " + y:<26}{n:>5}{r:>9.3f}{"[" + format(lo, ".3f") + ", " + format(hi, ".3f") + "]":>20}'
              f'{pval:>10.4f}{ph:>10.4f}{rc:>9.3f}  {lectura}')
        filas_out.append([x, y, n, round(r, 4), round(lo, 4), round(hi, 4), pval, ph, round(rc, 4), lectura])
    if a.salida:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['x', 'y', 'n', 'r', 'ic_inf', 'ic_sup', 'p', 'p_holm', 'r_critico', 'lectura'])
            w.writerows(filas_out)


def cmd_acuerdo(a):
    _, datos = leer(a.datos, [a.a, a.b])
    x, y = np.array(datos[a.a]), np.array(datos[a.b])
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3:
        sys.exit('Se necesitan al menos tres pares.')
    dif = x - y
    media = (x + y) / 2
    sesgo, sd = dif.mean(), dif.std(ddof=1)
    t = stats.t.ppf(0.975, n - 1)
    ee_sesgo = sd / math.sqrt(n)
    ee_lim = sd * math.sqrt(1 / n + 1.96 ** 2 / (2 * (n - 1)))
    li, ls = sesgo - 1.96 * sd, sesgo + 1.96 * sd
    pend = stats.linregress(media, dif)
    print(f'Bland y Altman: {a.a} - {a.b}; n = {n}')
    print(f'  sesgo medio = {sesgo:.5g}  (IC 95 %: {sesgo - t * ee_sesgo:.5g} a {sesgo + t * ee_sesgo:.5g})')
    print(f'  límites de acuerdo 95 % = {li:.5g} a {ls:.5g}')
    print(f'    IC 95 % del límite inferior: {li - t * ee_lim:.5g} a {li + t * ee_lim:.5g}')
    print(f'    IC 95 % del límite superior: {ls - t * ee_lim:.5g} a {ls + t * ee_lim:.5g}')
    print(f'  sesgo proporcional (pendiente de la diferencia sobre la media) = {pend.slope:.4g}, p = {pend.pvalue:.4f}')
    print(f'  error relativo medio = {np.mean(dif / y) * 100:.2f} %  (respecto de {a.b})')
    print('  El acuerdo se juzga contra una tolerancia declarada de antemano, no contra el valor p.')
    if a.salida:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['media', 'diferencia'])
            w.writerows(zip(media, dif))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)
    q = s.add_parser('matriz')
    q.add_argument('--datos', required=True)
    q.add_argument('--columnas', help='por defecto, todas las numéricas')
    q.add_argument('--metodo', choices=('spearman', 'pearson'), default='spearman')
    q.add_argument('--alfa', type=float, default=0.05)
    q.add_argument('--remuestreos', type=int, default=2000)
    q.add_argument('--semilla', type=int, default=2026)
    q.add_argument('--salida')
    q.set_defaults(fn=cmd_matriz)
    q = s.add_parser('acuerdo')
    q.add_argument('--datos', required=True)
    q.add_argument('--a', required=True)
    q.add_argument('--b', required=True)
    q.add_argument('--salida')
    q.set_defaults(fn=cmd_acuerdo)
    a = p.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()

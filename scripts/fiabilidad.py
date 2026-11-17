#!/usr/bin/env python3
"""Fiabilidad de un instrumento de medición con ítems (cuestionarios y escalas).

Calcula el alfa de Cronbach con su intervalo de confianza (Feldt), la correlación
ítem-total corregida y el alfa si se elimina cada ítem.

Uso
  python3 fiabilidad.py --datos respuestas.csv --items p1,p2,p3,p4 [--invertir p3 --min 1 --max 5]

  --invertir   ítems redactados en sentido inverso; se recodifican como (min + max - valor)

El alfa es una cota de consistencia interna bajo supuestos (tau-equivalencia, unidimensionalidad);
no prueba validez. Reporta n, número de ítems e intervalo. Requiere numpy y scipy.
"""
import argparse
import csv
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


def alfa(X):
    k = X.shape[1]
    var_items = X.var(axis=0, ddof=1).sum()
    var_total = X.sum(axis=1).var(ddof=1)
    return k / (k - 1) * (1 - var_items / var_total)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--datos', required=True)
    p.add_argument('--items', required=True)
    p.add_argument('--invertir', default='')
    p.add_argument('--min', type=float)
    p.add_argument('--max', type=float)
    a = p.parse_args()

    items = [i.strip() for i in a.items.split(',')]
    inv = [i.strip() for i in a.invertir.split(',') if i.strip()]
    if inv and (a.min is None or a.max is None):
        sys.exit('Para invertir ítems indica --min y --max de la escala.')
    with open(a.datos, encoding='utf-8-sig') as fh:
        filas = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    datos, omitidas = [], 0
    for f in filas:
        try:
            datos.append([float(str(f[i]).replace(',', '.')) for i in items])
        except (ValueError, KeyError):
            omitidas += 1
    X = np.array(datos)
    if X.ndim != 2 or X.shape[0] < 3 or X.shape[1] < 2:
        sys.exit('Se necesitan al menos tres casos completos y dos ítems.')
    for i in inv:
        j = items.index(i)
        X[:, j] = a.min + a.max - X[:, j]
    n, k = X.shape
    al = alfa(X)
    gl1, gl2 = n - 1, (n - 1) * (k - 1)
    lo = 1 - (1 - al) * stats.f.ppf(0.975, gl1, gl2)
    hi = 1 - (1 - al) * stats.f.ppf(0.025, gl1, gl2)
    print(f'Alfa de Cronbach = {al:.4f}  (IC 95 % de Feldt: {lo:.4f} a {hi:.4f}); n = {n}; ítems = {k}'
          + (f'; casos omitidos por datos faltantes = {omitidas}' if omitidas else ''))
    print(f'{"ítem":<16}{"r ítem-total corregida":>24}{"alfa si se elimina":>22}')
    for j, nombre in enumerate(items):
        resto = np.delete(X, j, axis=1)
        r = np.corrcoef(X[:, j], resto.sum(axis=1))[0, 1]
        al_sin = alfa(resto) if k > 2 else float('nan')
        marca = '  <- revisar' if r < 0.30 else ''
        print(f'{nombre:<16}{r:>24.3f}{al_sin:>22.4f}{marca}')
    if inv:
        print('Ítems invertidos antes del cálculo: ' + ', '.join(inv))
    print('La decisión de eliminar un ítem es del autor y se justifica con el contenido, no solo con el alfa.')


if __name__ == '__main__':
    main()

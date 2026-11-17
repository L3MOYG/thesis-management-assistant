#!/usr/bin/env python3
"""Pesos por comparación por pares (AHP) con verificación de reciprocidad y razón de consistencia.

Rechaza los defectos habituales de las matrices de ponderación: diagonal distinta de 1,
pares no recíprocos y consistencia no reportada. Los pesos solo se aceptan con CR < 0.10.

Uso
  python3 ahp.py --matriz "1,3,5;1/3,1,2;1/5,1/2,1" --nombres precision,costo,tiempo
  python3 ahp.py --archivo matriz.csv            (primera fila y primera columna = nombres)
  python3 ahp.py --triangulo "3,5,2" --nombres a,b,c   (solo el triángulo superior, por filas;
                                                        la matriz recíproca se construye sola)

Salida: pesos (vector propio principal normalizado), lambda máx, CI, RI y CR.
Requiere numpy.
"""
import argparse
import csv
import sys
from fractions import Fraction

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    import numpy as np
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Falta numpy. Instala con: pip install numpy')

RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
      11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59}


def num(x):
    x = str(x).strip().replace(',', '.') if '/' not in str(x) else str(x).strip()
    return float(Fraction(x)) if '/' in x else float(x)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--matriz')
    p.add_argument('--triangulo')
    p.add_argument('--archivo')
    p.add_argument('--nombres')
    p.add_argument('--tolerancia', type=float, default=0.01, help='tolerancia relativa de reciprocidad')
    a = p.parse_args()

    nombres = a.nombres.split(',') if a.nombres else None
    if a.archivo:
        with open(a.archivo, encoding='utf-8-sig') as fh:
            filas = [f for f in csv.reader(fh) if f and not f[0].startswith('#')]
        nombres = [c.strip() for c in filas[0][1:]]
        A = np.array([[num(c) for c in f[1:]] for f in filas[1:]])
    elif a.matriz:
        A = np.array([[num(c) for c in f.split(',')] for f in a.matriz.split(';')])
    elif a.triangulo:
        vals = [num(c) for c in a.triangulo.replace(';', ',').split(',')]
        n = int(round((1 + (1 + 8 * len(vals)) ** 0.5) / 2))
        if n * (n - 1) // 2 != len(vals):
            sys.exit('El triángulo superior debe tener n(n-1)/2 valores.')
        A = np.eye(n)
        k = 0
        for i in range(n):
            for j in range(i + 1, n):
                A[i, j] = vals[k]
                A[j, i] = 1 / vals[k]
                k += 1
    else:
        sys.exit('Indica --matriz, --triangulo o --archivo.')

    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        sys.exit('La matriz no es cuadrada.')
    nombres = nombres or [f'C{i + 1}' for i in range(n)]
    if len(nombres) != n:
        sys.exit('El número de nombres no coincide con el orden de la matriz.')

    errores = []
    if (A <= 0).any():
        errores.append('hay valores no positivos')
    for i in range(n):
        if abs(A[i, i] - 1) > 1e-9:
            errores.append(f'diagonal de {nombres[i]} = {A[i, i]:g} (debe ser 1)')
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i, j] * A[j, i] - 1) > a.tolerancia:
                errores.append(f'par no recíproco {nombres[i]}/{nombres[j]}: {A[i, j]:g} y {A[j, i]:g} '
                               f'(producto {A[i, j] * A[j, i]:.3f})')
    if errores:
        print('MATRIZ INVÁLIDA. No se calculan pesos:')
        for e in errores:
            print('  - ' + e)
        sys.exit(2)

    valores, vectores = np.linalg.eig(A)
    k = int(np.argmax(valores.real))
    lam = float(valores[k].real)
    w = np.abs(vectores[:, k].real)
    w = w / w.sum()
    ci = (lam - n) / (n - 1) if n > 1 else 0.0
    ri = RI.get(n)
    if ri is None:
        sys.exit('RI tabulado solo hasta n = 15; reduce el número de criterios o agrúpalos.')
    cr = ci / ri if ri > 0 else 0.0

    print(f'Criterios: {n}; lambda máx = {lam:.4f}; CI = {ci:.4f}; RI = {ri:.2f}; CR = {cr:.4f}')
    for nombre, peso in sorted(zip(nombres, w), key=lambda t: -t[1]):
        print(f'  {nombre:<28}{peso:.4f}')
    if n <= 2:
        print('Con dos criterios la consistencia es trivial (CR = 0).')
    if cr >= 0.10:
        print('CR >= 0.10: juicios inconsistentes. Revisa las comparaciones antes de usar estos pesos.')
        sys.exit(3)
    print('CR < 0.10: consistencia aceptable. Reporta la matriz, los pesos y el CR.')


if __name__ == '__main__':
    main()

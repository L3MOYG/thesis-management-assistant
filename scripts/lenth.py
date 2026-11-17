#!/usr/bin/env python3
"""Método de Lenth para factoriales completos no replicados (corridas deterministas o sin error puro).

Construye un conjunto ortonormal de contrastes de 1 gl (principales e interacciones) para
factores de cualquier número de niveles, de modo que todas las estimaciones tengan la misma
varianza, y aplica el pseudo error estándar de Lenth (1989):

    s0  = 1.5 * mediana(|c|)
    PSE = 1.5 * mediana(|c| tales que |c| < 2.5 * s0)
    ME  = t(0.975; m/3) * PSE          margen de error individual
    SME = t(gamma; m/3) * PSE          margen simultáneo, gamma = (1 + 0.95^(1/m)) / 2

Un contraste es activo si |c| > ME, y lo es con control simultáneo si |c| > SME.

Uso
  python3 lenth.py --datos corridas.csv --factores G,D,E,F --respuesta Z1 \
      [--numericos E] [--umbral 0.8] [--salida efectos.csv]

  --numericos  factores cuantitativos: usan contrastes polinomiales (L lineal, Q cuadrático...).
               Los demás usan contrastes de Helmert (H1, H2...).
  --umbral     umbral de relevancia numérica en unidades de la respuesta (p. ej. el ruido de
               discretización del estudio de convergencia). Se compara con el efecto en unidades
               de los contrastes entre dos niveles; los menores se marcan como no reportables.

El diseño debe ser un factorial completo con una observación por celda. Requiere numpy y scipy.
"""
import argparse
import csv
import itertools
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
    from scipy.stats import t as dist_t
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Faltan numpy o scipy. Instala con: pip install numpy scipy')


def contrastes_factor(niveles, numerico):
    """Matriz k x (k-1) de contrastes ortonormales entre los k niveles."""
    k = len(niveles)
    if numerico:
        x = np.array([float(v) for v in niveles])
        V = np.vander(x - x.mean(), k, increasing=True)
        Q, _ = np.linalg.qr(V)
        C = Q[:, 1:]
        for j in range(C.shape[1]):  # signo: creciente con el nivel
            if C[-1, j] < 0:
                C[:, j] = -C[:, j]
        etiquetas = ['L', 'Q', 'C'] + [f'P{i}' for i in range(4, k)]
        return C, etiquetas[:k - 1]
    C = np.zeros((k, k - 1))
    for j in range(1, k):  # Helmert: nivel j+1 frente a la media de los anteriores
        C[:j, j - 1] = -1.0
        C[j, j - 1] = j
        C[:, j - 1] /= np.linalg.norm(C[:, j - 1])
    return C, [f'H{j}' for j in range(1, k)] if k > 2 else ['']


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--datos', required=True)
    p.add_argument('--factores', required=True)
    p.add_argument('--respuesta', required=True)
    p.add_argument('--numericos', default='')
    p.add_argument('--umbral', type=float)
    p.add_argument('--salida')
    a = p.parse_args()

    factores = [f.strip() for f in a.factores.split(',')]
    numericos = {f.strip() for f in a.numericos.split(',') if f.strip()}
    with open(a.datos, encoding='utf-8-sig') as fh:
        filas = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    for col in factores + [a.respuesta]:
        if col not in filas[0]:
            sys.exit(f'No existe la columna "{col}". Columnas: {", ".join(filas[0])}')
    try:
        y = np.array([float(f[a.respuesta].replace(',', '.')) for f in filas])
    except ValueError:
        sys.exit(f'La respuesta {a.respuesta} tiene celdas vacías o no numéricas.')

    niveles = {}
    for f in factores:
        vals = sorted({r[f] for r in filas}, key=lambda v: (float(v) if f in numericos else 0, v))
        niveles[f] = vals
    n_celdas = math.prod(len(v) for v in niveles.values())
    celdas = {tuple(r[f] for f in factores) for r in filas}
    if len(filas) != n_celdas or len(celdas) != n_celdas:
        sys.exit(f'El diseño no es un factorial completo sin réplica: {len(filas)} filas, '
                 f'{len(celdas)} celdas distintas, {n_celdas} esperadas.')

    bases = {f: contrastes_factor(niveles[f], f in numericos) for f in factores}
    N = len(filas)
    nombres, columnas, dos_niveles = [], [], []
    for r in range(1, len(factores) + 1):
        for combo in itertools.combinations(factores, r):
            for idx in itertools.product(*[range(len(niveles[f]) - 1) for f in combo]):
                col = np.ones(N)
                partes = []
                for f, j in zip(combo, idx):
                    C, etq = bases[f]
                    pos = {v: i for i, v in enumerate(niveles[f])}
                    col = col * np.array([C[pos[row[f]], j] for row in filas])
                    partes.append(f + (f'.{etq[j]}' if etq[j] else ''))
                col = col / np.linalg.norm(col)
                nombres.append(':'.join(partes))
                columnas.append(col)
                dos_niveles.append(all(len(niveles[f]) == 2 for f in combo))
    X = np.column_stack(columnas)
    orto = np.abs(X.T @ X - np.eye(X.shape[1])).max()
    if orto > 1e-8:
        sys.exit('Los contrastes no resultaron ortogonales; revisa que el diseño esté balanceado.')
    c = X.T @ y
    m = len(c)
    absc = np.abs(c)
    s0 = 1.5 * np.median(absc)
    pse = 1.5 * np.median(absc[absc < 2.5 * s0])
    gl = m / 3.0
    me = dist_t.ppf(0.975, gl) * pse
    gamma = (1 + 0.95 ** (1.0 / m)) / 2
    sme = dist_t.ppf(gamma, gl) * pse

    print(f'Respuesta: {a.respuesta}; corridas: {N}; contrastes: {m}; media: {y.mean():.6g}')
    print(f'PSE = {pse:.6g}; gl de Lenth = {gl:.2f}; ME = {me:.6g}; SME = {sme:.6g}')
    if a.umbral is not None:
        print(f'Umbral de relevancia numérica = {a.umbral} (unidades de la respuesta)')
    orden = np.argsort(-absc)
    salida = []
    print(f'{"Contraste":<26}{"estimación":>13}{"|c|/PSE":>10}{"efecto":>13}  veredicto')
    for i in orden:
        efecto = 2 * c[i] / math.sqrt(N) if dos_niveles[i] else float('nan')
        if absc[i] > sme:
            v = 'activo (simultáneo)'
        elif absc[i] > me:
            v = 'activo (individual)'
        else:
            v = 'no se distingue del ruido'
        if a.umbral is not None and dos_niveles[i] and abs(efecto) < a.umbral and absc[i] > me:
            v += '; menor que el umbral numérico: no reportar como hallazgo'
        razon = absc[i] / pse if pse > 0 else float('inf')
        ef_txt = f'{efecto:>13.5g}' if dos_niveles[i] else f'{"":>13}'
        print(f'{nombres[i]:<26}{c[i]:>13.5g}{razon:>10.2f}{ef_txt}  {v}')
        salida.append([nombres[i], c[i], razon, '' if not dos_niveles[i] else efecto, v])
    print('estimación: contraste ortonormal (misma varianza para todos). efecto: diferencia de medias entre '
          'los dos niveles, solo para contrastes formados por factores de dos niveles.')
    if pse == 0:
        print('PSE = 0: más de la mitad de los contrastes son nulos; el método no es informativo aquí.')
    if a.salida:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['contraste', 'estimacion_ortonormal', 'razon_PSE', 'efecto_unidades', 'veredicto'])
            w.writerows(salida)
            w.writerow([])
            w.writerow(['PSE', pse, 'ME', me, 'SME', sme])


if __name__ == '__main__':
    main()

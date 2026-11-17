#!/usr/bin/env python3
"""ANOVA factorial de efectos fijos con bloques opcionales y reporte completo.

Entrega, para cada efecto: gl, suma de cuadrados, F, p, eta cuadrado parcial, f de Cohen
observado y f mínimo detectable con potencia 0.80. Verifica supuestos (Levene entre celdas,
Shapiro-Wilk sobre residuos) y propone la transformación logarítmica si la respuesta es
positiva y se rechaza la homocedasticidad.

Regla de redacción: un efecto no significativo se reporta como "no se detectó diferencia",
acompañado del efecto mínimo detectable; nunca como "se demostró que no hay diferencia".

Uso
  python3 anova_factorial.py --datos d.csv --respuesta Y1 --factores A,B,C [--bloque sesion]
      [--orden 3] [--log] [--covariables x1,x2] [--salida anova.csv]

  --orden   orden máximo de interacción incluido en el modelo (por defecto, todas)
  --log     analiza log(respuesta)

Sumas de cuadrados tipo II (coinciden con las tipo I y III en diseños balanceados).
Requiere numpy, scipy, pandas y statsmodels.
"""
import argparse
import itertools
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from scipy import stats
    from scipy.optimize import brentq
except ImportError as e:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit(f'Falta una dependencia ({e.name}). Instala con: pip install numpy scipy pandas statsmodels')


def f_minimo(gl_num, gl_error, n, potencia=0.80, alfa=0.05):
    fc = stats.f.ppf(1 - alfa, gl_num, gl_error)
    return brentq(lambda f: 1 - stats.ncf.cdf(fc, gl_num, gl_error, f * f * n) - potencia, 1e-4, 50)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--datos', required=True)
    p.add_argument('--respuesta', required=True)
    p.add_argument('--factores', required=True)
    p.add_argument('--bloque')
    p.add_argument('--covariables', default='')
    p.add_argument('--orden', type=int)
    p.add_argument('--log', action='store_true')
    p.add_argument('--alfa', type=float, default=0.05)
    p.add_argument('--salida')
    a = p.parse_args()

    df = pd.read_csv(a.datos, comment='#')
    factores = [f.strip() for f in a.factores.split(',')]
    covs = [c.strip() for c in a.covariables.split(',') if c.strip()]
    usadas = factores + covs + [a.respuesta] + ([a.bloque] if a.bloque else [])
    faltan = [c for c in usadas if c not in df.columns]
    if faltan:
        sys.exit(f'Columnas ausentes: {", ".join(faltan)}. Disponibles: {", ".join(df.columns)}')
    n0 = len(df)
    df = df.dropna(subset=usadas).copy()
    if len(df) < n0:
        print(f'Aviso: se excluyeron {n0 - len(df)} filas con datos faltantes. Decláralo.')
    y = a.respuesta
    if a.log:
        if (df[y] <= 0).any():
            sys.exit('No se puede aplicar logaritmo: la respuesta tiene valores no positivos.')
        df['_y'] = np.log(df[y])
    else:
        df['_y'] = df[y].astype(float)

    # Nombres internos neutros: una columna llamada C, Q o I chocaría con funciones de la fórmula.
    alias = {f: f'fac{i}_' for i, f in enumerate(factores)}
    alias.update({c: f'cov{i}_' for i, c in enumerate(covs)})
    if a.bloque:
        alias[a.bloque] = 'blq_'
    inverso = {v: k for k, v in alias.items()}
    dm = df[['_y']].copy()
    for original, interno in alias.items():
        dm[interno] = df[original].values
    orden = a.orden or len(factores)
    terminos = []
    for r in range(1, orden + 1):
        for combo in itertools.combinations(factores, r):
            terminos.append(':'.join(f'C({alias[f]})' for f in combo))
    formula = '_y ~ ' + ' + '.join(terminos)
    if a.bloque:
        formula += ' + C(blq_)'
    for c in covs:
        formula += f' + {alias[c]}'
    modelo = smf.ols(formula, data=dm).fit()
    tabla = sm.stats.anova_lm(modelo, typ=2)
    n = int(modelo.nobs)
    gl_error = int(modelo.df_resid)
    if gl_error <= 0:
        sys.exit('Sin grados de libertad para el error (diseño no replicado). Usa lenth.py.')
    sc_error = float(tabla.loc['Residual', 'sum_sq'])

    celdas = df.groupby(factores)['_y']
    tamanos = celdas.size()
    balanceado = tamanos.nunique() == 1
    print(f'Respuesta: {"log(" + y + ")" if a.log else y}; n = {n}; celdas = {len(tamanos)}; '
          f'{"balanceado" if balanceado else "NO balanceado (SC tipo II)"}; gl error = {gl_error}; '
          f'CM error = {sc_error / gl_error:.6g}; R2 = {modelo.rsquared:.4f}')

    def limpio(t):
        partes = [inverso.get(x.replace('C(', '').replace(')', ''), x) for x in t.split(':')]
        return ' x '.join(partes)

    print(f'{"Fuente":<22}{"gl":>4}{"SC":>14}{"F":>10}{"p":>10}{"eta2p":>8}{"f obs":>8}{"f mín":>8}  lectura')
    filas = []
    for fuente, fila in tabla.iterrows():
        if fuente == 'Residual':
            continue
        gl = int(round(fila['df']))
        sc, F, pv = float(fila['sum_sq']), float(fila['F']), float(fila['PR(>F)'])
        eta = sc / (sc + sc_error)
        f_obs = (eta / (1 - eta)) ** 0.5 if eta < 1 else float('inf')
        fm = f_minimo(gl, gl_error, n, 0.80, a.alfa)
        es_bloque = fuente == 'C(blq_)'
        if es_bloque:
            lectura = 'bloque (no se interpreta como hipótesis)'
        elif pv < a.alfa:
            lectura = 'efecto detectado'
        else:
            lectura = f'no se detectó efecto (detectable desde f = {fm:.2f})'
        print(f'{limpio(fuente):<22}{gl:>4}{sc:>14.6g}{F:>10.3f}{pv:>10.4f}{eta:>8.3f}{f_obs:>8.3f}{fm:>8.3f}  {lectura}')
        filas.append([limpio(fuente), gl, sc, F, pv, eta, f_obs, fm, lectura])
    print(f'{"Error":<22}{gl_error:>4}{sc_error:>14.6g}')
    print('f mín: efecto mínimo detectable con potencia 0.80 y el alfa indicado (lambda = f^2 * n).')

    grupos = [g.values for _, g in celdas if len(g) > 1]
    if len(grupos) >= 2:
        lev = stats.levene(*grupos, center='median')
        print(f'\nSupuestos: Levene (mediana) entre celdas: W = {lev.statistic:.3f}, p = {lev.pvalue:.4f}', end='')
        if lev.pvalue < a.alfa:
            print(' -> se rechaza homocedasticidad.', end='')
            if not a.log and (df[y] > 0).all():
                print(' Repite con --log y reporta ambos análisis.', end='')
        print()
    else:
        print('\nSupuestos: Levene no aplicable (una observación por celda).')
    res = modelo.resid
    if 3 <= len(res) <= 5000:
        sw = stats.shapiro(res)
        print(f'           Shapiro-Wilk sobre residuos: W = {sw.statistic:.4f}, p = {sw.pvalue:.4f}'
              + (' -> revisa el gráfico Q-Q y los valores extremos.' if sw.pvalue < a.alfa else ''))
    est = modelo.get_influence().resid_studentized_internal
    extremos = int((np.abs(est) > 3).sum())
    if extremos:
        print(f'           {extremos} residuo(s) estudentizado(s) con |r| > 3: documenta la causa antes de excluir nada.')

    print('\nMedias por celda (escala original):')
    resumen = df.groupby(factores)[y].agg(['count', 'mean', 'std']).reset_index()
    print(resumen.to_string(index=False, float_format=lambda v: f'{v:.5g}'))

    if a.salida:
        pd.DataFrame(filas, columns=['fuente', 'gl', 'SC', 'F', 'p', 'eta2_parcial', 'f_observado',
                                     'f_minimo_detectable', 'lectura']).to_csv(a.salida, index=False)


if __name__ == '__main__':
    main()

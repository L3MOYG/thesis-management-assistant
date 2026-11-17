#!/usr/bin/env python3
"""Decisión multirrespuesta: filtro de factibilidad, deseabilidad de Derringer y Suich,
análisis de sensibilidad de pesos y verificación cruzada con TOPSIS de pesos por entropía.

    d_i = ((y - L) / (T - L))^s   maximizar        d_i = ((U - y) / (U - T))^s   minimizar
    d_i de objetivo: sube de L a T con exponente s y baja de T a U con exponente t
    D   = ( producto d_i^w_i )^(1 / suma w_i)

La media geométrica es deliberada: una respuesta inaceptable (d_i = 0) anula D y no puede
compensarse con otra excelente. No se usa suma ponderada.

Uso
  python3 deseabilidad.py --datos alternativas.csv --config config.json [--salida resultado.csv]

config.json
  {
    "id": "alternativa",
    "respuestas": {
      "Z1": {"tipo": "max", "L": 10, "T": 25, "s": 1, "peso": 0.5},
      "Z4": {"tipo": "min", "T": 0, "U": 30, "peso": 0.3},
      "Z2": {"tipo": "objetivo", "L": 40, "T": 50, "U": 60, "s": 1, "t": 1, "peso": 0.2}
    },
    "factibilidad": [ {"columna": "Z5", "op": ">=", "valor": 0.4, "motivo": "requisito mínimo que toda alternativa debe cumplir"} ]
  }

Los límites L, T y U se fijan con el rango real de los datos o con un requisito externo y se
declaran antes de mirar el ranking. Si falta alguno, el script se detiene: no los inventa.
Requiere numpy y scipy.
"""
import argparse
import csv
import json
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
    from scipy.stats import spearmanr
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Faltan numpy o scipy. Instala con: pip install numpy scipy')

OPS = {'>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b, '>': lambda a, b: a > b,
       '<': lambda a, b: a < b, '==': lambda a, b: a == b, '!=': lambda a, b: a != b}


def d_individual(y, c):
    tipo = c['tipo']
    s = float(c.get('s', 1))
    if tipo == 'max':
        L, T = float(c['L']), float(c['T'])
        return 0.0 if y <= L else 1.0 if y >= T else ((y - L) / (T - L)) ** s
    if tipo == 'min':
        T, U = float(c['T']), float(c['U'])
        return 0.0 if y >= U else 1.0 if y <= T else ((U - y) / (U - T)) ** s
    if tipo == 'objetivo':
        L, T, U = float(c['L']), float(c['T']), float(c['U'])
        t = float(c.get('t', 1))
        if y <= L or y >= U:
            return 0.0
        return ((y - L) / (T - L)) ** s if y <= T else ((U - y) / (U - T)) ** t
    sys.exit(f'Tipo desconocido: {tipo} (usa max, min u objetivo)')


def D_global(ds, pesos):
    if any(d == 0 for d in ds):
        return 0.0
    return math.exp(sum(w * math.log(d) for d, w in zip(ds, pesos)) / sum(pesos))


def topsis_entropia(M, sentidos):
    """M: alternativas x criterios (valores crudos). sentidos: +1 beneficio, -1 costo, 0 objetivo ya convertido."""
    X = np.array(M, float)
    P = np.where(X.min(0) < 0, X - X.min(0), X) + 1e-12  # p_ij = x_ij / suma; se desplaza solo si hay negativos
    P = P / P.sum(0)
    k = 1 / math.log(len(X)) if len(X) > 1 else 1
    E = -k * (P * np.log(P)).sum(0)
    div = 1 - E
    w = div / div.sum() if div.sum() > 0 else np.ones(X.shape[1]) / X.shape[1]
    norma = np.linalg.norm(X, axis=0)
    norma[norma == 0] = 1
    V = X / norma * w
    ideal = np.where(np.array(sentidos) > 0, V.max(0), V.min(0))
    anti = np.where(np.array(sentidos) > 0, V.min(0), V.max(0))
    dp = np.linalg.norm(V - ideal, axis=1)
    dn = np.linalg.norm(V - anti, axis=1)
    return dn / (dp + dn + 1e-15), w


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--datos', required=True)
    p.add_argument('--config', required=True)
    p.add_argument('--salida')
    a = p.parse_args()

    cfg = json.load(open(a.config, encoding='utf-8'))
    resp = cfg['respuestas']
    for nombre, c in resp.items():
        necesarios = {'max': ('L', 'T'), 'min': ('T', 'U'), 'objetivo': ('L', 'T', 'U')}.get(c.get('tipo'))
        if necesarios is None:
            sys.exit(f'{nombre}: falta "tipo" (max, min u objetivo).')
        faltan = [k for k in necesarios + ('peso',) if c.get(k) is None]
        if faltan:
            sys.exit(f'{nombre}: faltan {", ".join(faltan)}. Los límites y pesos los decide el autor con los datos '
                     f'reales; este script no los inventa.')
    with open(a.datos, encoding='utf-8-sig') as fh:
        filas = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    col_id = cfg.get('id') or list(filas[0])[0]

    def val(f, col):
        try:
            return float(str(f[col]).replace(',', '.'))
        except (KeyError, ValueError):
            sys.exit(f'Valor no numérico o columna ausente: {col} en {f.get(col_id)}')

    factibles, descartadas = [], []
    for f in filas:
        motivos = []
        for regla in cfg.get('factibilidad', []):
            if not OPS[regla['op']](val(f, regla['columna']), float(regla['valor'])):
                motivos.append(regla.get('motivo') or f"{regla['columna']} {regla['op']} {regla['valor']} no se cumple")
        (descartadas if motivos else factibles).append((f, motivos))
    print(f'Alternativas: {len(filas)}; factibles: {len(factibles)}; descartadas por el filtro binario: {len(descartadas)}')
    for f, motivos in descartadas:
        print(f'  descartada {f[col_id]}: ' + '; '.join(motivos))
    if not factibles:
        sys.exit('Ninguna alternativa pasa el filtro de factibilidad.')

    nombres = list(resp)
    pesos = [float(resp[n]['peso']) for n in nombres]
    ids = [f[col_id] for f, _ in factibles]
    Y = [[val(f, n) for n in nombres] for f, _ in factibles]
    d = [[d_individual(y, resp[n]) for y, n in zip(fila, nombres)] for fila in Y]
    D = [D_global(fila, pesos) for fila in d]
    orden = sorted(range(len(ids)), key=lambda i: -D[i])
    ganador = orden[0]

    print(f'\nDeseabilidad global (media geométrica ponderada; pesos: '
          + ', '.join(f'{n}={w:g}' for n, w in zip(nombres, pesos)) + ')')
    print(f'{"pos":<5}{"alternativa":<24}{"D":>8}  ' + '  '.join(f'd({n})' for n in nombres))
    for pos, i in enumerate(orden, 1):
        print(f'{pos:<5}{ids[i]:<24}{D[i]:>8.4f}  ' + '  '.join(f'{x:>{len(n) + 3}.3f}' for x, n in zip(d[i], nombres)))
    if D[ganador] == 0:
        print('Todas las alternativas tienen D = 0: alguna respuesta es inaceptable en cada una. Revisa los límites.')
    empates = [ids[i] for i in orden[1:] if abs(D[i] - D[ganador]) < 1e-9]
    if empates:
        print(f'Empate en el primer lugar con: {", ".join(empates)}')

    print('\nSensibilidad: multiplicador de cada peso (los demás fijos) en el que el ganador no cambia')
    malla = [round(0.1 + 0.05 * k, 2) for k in range(59)]  # 0.10 ... 3.00
    for j, n in enumerate(nombres):
        def gana(m):
            w = pesos[:]
            w[j] = pesos[j] * m
            Dm = [D_global(fila, w) for fila in d]
            return max(range(len(ids)), key=lambda i: Dm[i]) == ganador
        lo = hi = 1.0
        for m in sorted([x for x in malla if x < 1], reverse=True):
            if gana(m):
                lo = m
            else:
                break
        for m in [x for x in malla if x > 1]:
            if gana(m):
                hi = m
            else:
                break
        estable = gana(0.5) and gana(1.5)
        print(f'  {n:<12} intervalo [{lo:.2f}, {hi:.2f}]  ' + ('estable en x0.5 y x1.5' if estable else
              'EL GANADOR CAMBIA dentro de x0.5 a x1.5: decisión sensible a este peso'))
    print('  (malla de 0.05 entre 0.10 y 3.00; un extremo igual a 0.10 o 3.00 significa que no cambió en la malla)')

    # Verificación cruzada: TOPSIS con pesos por entropía sobre las mismas alternativas factibles.
    sentidos, M = [], []
    for jn, n in enumerate(nombres):
        t = resp[n]['tipo']
        if t == 'objetivo':
            sentidos.append(-1)
        else:
            sentidos.append(1 if t == 'max' else -1)
    for fila in Y:
        M.append([abs(y - float(resp[n]['T'])) if resp[n]['tipo'] == 'objetivo' else y for y, n in zip(fila, nombres)])
    if len(ids) >= 3:
        cc, w_ent = topsis_entropia(M, sentidos)
        rho = spearmanr(D, cc).statistic
        g_topsis = ids[int(np.argmax(cc))]
        print('\nVerificación cruzada TOPSIS (pesos por entropía: '
              + ', '.join(f'{n}={w:.3f}' for n, w in zip(nombres, w_ent)) + ')')
        print(f'  ganador TOPSIS: {g_topsis}; ganador por deseabilidad: {ids[ganador]}; '
              f'concordancia de rangos (Spearman) = {rho:.3f}')
        print('  TOPSIS no es el criterio primario: pondera por dispersión y admite inversión de rango.')
    else:
        cc = [float('nan')] * len(ids)
        print('\nTOPSIS omitido: se necesitan al menos tres alternativas factibles.')

    if a.salida:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow([col_id, 'D', 'posicion'] + [f'd_{n}' for n in nombres] + ['topsis_cc', 'estado'])
            for pos, i in enumerate(orden, 1):
                w.writerow([ids[i], round(D[i], 6), pos] + [round(x, 6) for x in d[i]] + [cc[i], 'factible'])
            for f, motivos in descartadas:
                w.writerow([f[col_id], '', ''] + [''] * len(nombres) + ['', 'descartada: ' + '; '.join(motivos)])


if __name__ == '__main__':
    main()

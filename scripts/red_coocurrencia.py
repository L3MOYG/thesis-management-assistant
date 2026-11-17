#!/usr/bin/env python3
"""Red de coocurrencia de palabras clave, reproducible y con parámetros declarados.

Equivale a la configuración habitual de VOSviewer: coocurrencia con conteo completo, umbral
mínimo de ocurrencias, agrupamiento por modularidad con resolución 1 (se repite con 50 semillas
y se conserva la partición de mayor modularidad) y mapeo VOS sobre la fuerza de asociación.

Uso
  python3 red_coocurrencia.py --datos scopus.csv [--columna "Author Keywords"] [--separador ";"]
      [--tesauro tesauro.csv] [--umbral 2] [--carpeta red/] [--tikz] [--png]

  --datos     CSV con una columna de palabras clave por documento: una exportación de Scopus
              (Author Keywords, Index Keywords) o la hoja Corpus exportada a CSV (Palabras clave).
  --tesauro   CSV con columnas "label" y "replace by" (formato de VOSviewer) para unificar
              sinónimos. El tesauro es una decisión del autor y se reporta.
  --tikz      escribe además la figura en TikZ; --png la dibuja con matplotlib si está instalado.

Salidas en --carpeta: estadisticas.txt, nodos.csv, enlaces.csv y, si se piden, red.tex y red.png.
Requiere numpy, scipy y networkx.
"""
import argparse
import csv
import itertools
import os
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    import networkx as nx
    import numpy as np
    from scipy.optimize import minimize
except ImportError as e:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit(f'Falta una dependencia ({e.name}). Instala con: pip install numpy scipy networkx')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--datos', required=True)
    p.add_argument('--columna')
    p.add_argument('--separador', default=';')
    p.add_argument('--tesauro')
    p.add_argument('--umbral', type=int, default=2)
    p.add_argument('--carpeta', default='.')
    p.add_argument('--tikz', action='store_true')
    p.add_argument('--png', action='store_true')
    a = p.parse_args()

    tes = {}
    if a.tesauro:
        with open(a.tesauro, encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                tes[r['label'].strip().lower()] = r['replace by'].strip().lower()
    with open(a.datos, encoding='utf-8-sig', newline='') as fh:
        filas = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    if not filas:
        sys.exit('El archivo no tiene filas.')
    col = a.columna
    if not col:
        for cand in ('Author Keywords', 'Palabras clave', 'palabras_clave_autor', 'palabras_clave', 'Keywords', 'Index Keywords'):
            if cand in filas[0]:
                col = cand
                break
    if not col or col not in filas[0]:
        sys.exit(f'Indica --columna. Columnas disponibles: {", ".join(filas[0])}')

    docs = []
    for r in filas:
        kws = set()
        for k in (r.get(col) or '').split(a.separador):
            k = ' '.join(k.strip().lower().replace('ﬁ', 'fi').split())
            if k:
                kws.add(tes.get(k, k))
        kws.discard('')
        if kws:
            docs.append(kws)
    occ = {}
    for kws in docs:
        for k in kws:
            occ[k] = occ.get(k, 0) + 1
    nodos = sorted([k for k, n in occ.items() if n >= a.umbral], key=lambda k: (-occ[k], k))
    n = len(nodos)
    if n < 3:
        sys.exit(f'Solo {n} palabra(s) clave alcanzan el umbral de {a.umbral}: baja el umbral o amplía el corpus.')
    idx = {k: i for i, k in enumerate(nodos)}
    C = np.zeros((n, n))
    for kws in docs:
        sel = sorted(k for k in kws if k in idx)
        for x, y in itertools.combinations(sel, 2):
            C[idx[x], idx[y]] += 1
            C[idx[y], idx[x]] += 1
    G = nx.Graph()
    G.add_nodes_from(nodos)
    iu = np.triu_indices(n, 1)
    for i, j in zip(*iu):
        if C[i, j] > 0:
            G.add_edge(nodos[i], nodos[j], weight=C[i, j])

    particiones = {}
    for semilla in range(50):
        part = nx.community.louvain_communities(G, weight='weight', resolution=1.0, seed=semilla)
        clave = tuple(sorted(tuple(sorted(c)) for c in part))
        particiones[clave] = nx.community.modularity(G, part, weight='weight') if G.number_of_edges() else 0.0
    mejor = max(particiones, key=particiones.get)
    clusters = sorted([list(c) for c in mejor], key=lambda c: -sum(occ[k] for k in c))
    cl = {k: ci for ci, c in enumerate(clusters) for k in c}

    o = np.array([occ[k] for k in nodos], float)
    S = C / np.outer(o, o)

    def objetivo(x):
        X = x.reshape(n, 2)
        D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)[iu]
        return np.sum(S[iu] * D ** 2) / (np.mean(D) ** 2 + 1e-12)

    rng = np.random.default_rng(1)
    mejor_r = None
    for _ in range(30):
        r = minimize(objetivo, rng.normal(size=2 * n), method='L-BFGS-B')
        if mejor_r is None or r.fun < mejor_r.fun:
            mejor_r = r
    X = mejor_r.x.reshape(n, 2)
    X -= X.mean(0)
    _, _, vt = np.linalg.svd(X, full_matrices=False)
    X = X @ vt.T
    X /= np.abs(X).max(0) + 1e-12

    os.makedirs(a.carpeta, exist_ok=True)
    n_enl = int((C[iu] > 0).sum())
    entre = sum(1 for i, j in zip(*iu) if C[i, j] > 0 and cl[nodos[i]] != cl[nodos[j]])
    with open(os.path.join(a.carpeta, 'estadisticas.txt'), 'w', encoding='utf-8') as f:
        f.write(f'Archivo: {os.path.basename(a.datos)}; columna: {col}; separador: "{a.separador}"\n')
        f.write(f'Tesauro: {os.path.basename(a.tesauro) if a.tesauro else "ninguno"} ({len(tes)} reglas)\n')
        f.write(f'Documentos con palabras clave: {len(docs)} de {len(filas)}\n')
        f.write(f'Palabras clave distintas (tras tesauro): {len(occ)}\n')
        f.write(f'Nodos (>= {a.umbral} ocurrencias): {n}\nEnlaces: {n_enl}\nFuerza total de enlace: {int(C[iu].sum())}\n')
        f.write(f'Clústeres: {len(clusters)}\nModularidad: {particiones[mejor]:.3f}\n')
        f.write(f'Particiones distintas en 50 semillas: {len(particiones)}\n')
        f.write(f'Enlaces entre clústeres: {entre}\n\n')
        for ci, c in enumerate(clusters, 1):
            f.write(f'Clúster {ci}: ' + '; '.join(f'{k} ({occ[k]})' for k in sorted(c, key=lambda k: -occ[k])) + '\n')
        f.write('\nNodos aislados: ' + (', '.join(k for k in nodos if G.degree(k) == 0) or 'ninguno') + '\n')
    with open(os.path.join(a.carpeta, 'nodos.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['palabra_clave', 'ocurrencias', 'cluster', 'grado', 'x', 'y'])
        for i, k in enumerate(nodos):
            w.writerow([k, occ[k], cl[k] + 1, G.degree(k), round(X[i, 0], 4), round(X[i, 1], 4)])
    with open(os.path.join(a.carpeta, 'enlaces.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['origen', 'destino', 'coocurrencias', 'mismo_cluster'])
        for i, j in zip(*iu):
            if C[i, j] > 0:
                w.writerow([nodos[i], nodos[j], int(C[i, j]), int(cl[nodos[i]] == cl[nodos[j]])])
    print(open(os.path.join(a.carpeta, 'estadisticas.txt'), encoding='utf-8').read())

    if a.tikz:
        colores = ['blue!70!black', 'red!70!black', 'green!50!black', 'orange!85!black', 'violet', 'teal', 'brown', 'gray']
        P = X * np.array([7.0, 3.6])
        L = ['% Red de coocurrencia generada por red_coocurrencia.py; no editar a mano.',
             '\\begin{tikzpicture}[font=\\sffamily]']
        for i, j in zip(*iu):
            if C[i, j] > 0:
                c = colores[cl[nodos[i]] % len(colores)] if cl[nodos[i]] == cl[nodos[j]] else 'gray'
                L.append(f'\\draw[{c}, opacity=0.35, line width={0.4 + 0.6 * (C[i, j] - 1):.2f}pt] '
                         f'({P[i, 0]:.2f},{P[i, 1]:.2f}) -- ({P[j, 0]:.2f},{P[j, 1]:.2f});')
        for i, k in enumerate(nodos):
            c = colores[cl[k] % len(colores)]
            rad = 0.08 + 0.04 * occ[k]
            etiqueta = k.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
            L.append(f'\\fill[{c}] ({P[i, 0]:.2f},{P[i, 1]:.2f}) circle ({rad:.2f});')
            L.append(f'\\node[font=\\sffamily\\tiny, text={c}, anchor=south, outer sep={rad:.2f}cm] '
                     f'at ({P[i, 0]:.2f},{P[i, 1]:.2f}) {{{etiqueta}}};')
        L.append('\\end{tikzpicture}')
        open(os.path.join(a.carpeta, 'red.tex'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    if a.png:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            print('matplotlib no está instalado: se omite red.png (pip install matplotlib).')
        else:
            paleta = plt.get_cmap('tab10')
            fig, ax = plt.subplots(figsize=(10, 6))
            for i, j in zip(*iu):
                if C[i, j] > 0:
                    ax.plot([X[i, 0], X[j, 0]], [X[i, 1], X[j, 1]], color='0.6', lw=0.4 + 0.6 * C[i, j], alpha=0.5, zorder=1)
            ax.scatter(X[:, 0], X[:, 1], s=[60 * occ[k] for k in nodos], c=[paleta(cl[k] % 10) for k in nodos], zorder=2)
            for i, k in enumerate(nodos):
                ax.annotate(k, (X[i, 0], X[i, 1]), fontsize=8, ha='center', va='bottom', xytext=(0, 6), textcoords='offset points')
            ax.set_axis_off()
            fig.tight_layout()
            fig.savefig(os.path.join(a.carpeta, 'red.png'), dpi=200)
            print('Figura: ' + os.path.join(a.carpeta, 'red.png'))


if __name__ == '__main__':
    main()

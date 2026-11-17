#!/usr/bin/env python3
"""Matriz de corridas de un factorial completo, aleatorizada con semilla declarada.

Toda matriz debe ser regenerable: la misma semilla produce el mismo orden. La semilla
se escribe en el propio archivo de salida.

Uso
  python3 matriz_corridas.py --factores "A:A1,A2;B:B1,B2,B3;C:C1,C2,C3" \
      --replicas 5 --bloques 5 --semilla 2026 --salida matriz.csv

  --factores   "Nombre:nivel1,nivel2;Nombre2:nivel1,nivel2,..."
  --replicas   réplicas por condición (1 = no replicado)
  --bloques    0 = completamente aleatorizado; k = k bloques completos (cada bloque
               contiene réplicas/k réplicas de todas las condiciones, en orden aleatorio)
  --semilla    entero; obligatorio declararlo en la tesis
  --salida     .csv o .xlsx (xlsx requiere openpyxl)

Imprime además la descomposición de grados de libertad.
"""
import argparse
import csv
import itertools
import math
import random
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass


def leer_factores(texto):
    factores = []
    for parte in texto.split(';'):
        parte = parte.strip()
        if not parte:
            continue
        if ':' not in parte:
            sys.exit(f'Factor mal escrito: "{parte}". Formato: Nombre:nivel1,nivel2')
        nombre, niveles = parte.split(':', 1)
        niveles = [n.strip() for n in niveles.split(',') if n.strip()]
        if len(niveles) < 2:
            sys.exit(f'El factor {nombre} necesita al menos dos niveles.')
        factores.append((nombre.strip(), niveles))
    if not factores:
        sys.exit('No se leyó ningún factor.')
    return factores


def construir(factores, replicas, bloques, semilla):
    rng = random.Random(semilla)
    condiciones = list(itertools.product(*[niv for _, niv in factores]))
    filas = []
    if bloques:
        if replicas % bloques:
            sys.exit('Con bloques completos, --replicas debe ser múltiplo de --bloques.')
        por_bloque = replicas // bloques
        rep = 0
        for b in range(1, bloques + 1):
            tanda = []
            for r in range(por_bloque):
                rep_id = (b - 1) * por_bloque + r + 1
                tanda += [(b, rep_id, c) for c in condiciones]
            rng.shuffle(tanda)
            filas += tanda
            rep += por_bloque
    else:
        todo = [(0, r, c) for r in range(1, replicas + 1) for c in condiciones]
        rng.shuffle(todo)
        filas = todo
    return condiciones, filas


def grados_de_libertad(factores, replicas, bloques):
    niveles = [len(n) for _, n in factores]
    nombres = [f for f, _ in factores]
    n_total = math.prod(niveles) * replicas
    lineas = [('Total', n_total - 1)]
    gl_b = (bloques - 1) if bloques else 0
    if bloques:
        lineas.append(('Bloques', gl_b))
    gl_t = 0
    for r in range(1, len(niveles) + 1):
        for combo in itertools.combinations(range(len(niveles)), r):
            gl = math.prod(niveles[i] - 1 for i in combo)
            gl_t += gl
            lineas.append(('x'.join(nombres[i] for i in combo), gl))
    lineas.append(('Error', n_total - 1 - gl_b - gl_t))
    return n_total, lineas


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--factores', required=True)
    p.add_argument('--replicas', type=int, default=1)
    p.add_argument('--bloques', type=int, default=0)
    p.add_argument('--semilla', type=int, required=True)
    p.add_argument('--salida', required=True)
    p.add_argument('--respuestas', default='', help='columnas vacías de respuesta a añadir, p. ej. Y1,Y2')
    a = p.parse_args()

    factores = leer_factores(a.factores)
    condiciones, filas = construir(factores, a.replicas, a.bloques, a.semilla)
    nombres = [f for f, _ in factores]
    respuestas = [r.strip() for r in a.respuestas.split(',') if r.strip()]
    encabezado = ['orden', 'bloque', 'replica', 'condicion'] + nombres + respuestas + ['observaciones']
    indice = {c: i + 1 for i, c in enumerate(condiciones)}
    tabla = []
    for orden, (b, r, c) in enumerate(filas, 1):
        tabla.append([orden, b if a.bloques else '', r, indice[c]] + list(c) + [''] * len(respuestas) + [''])
    nota = (f'Factorial completo {" x ".join(str(len(n)) for _, n in factores)}; replicas = {a.replicas}; '
            f'bloques = {a.bloques}; semilla = {a.semilla}; generado con matriz_corridas.py')

    if a.salida.lower().endswith('.xlsx'):
        try:
            import openpyxl
        except ImportError:
            sys.exit('Para .xlsx instala openpyxl (pip install openpyxl) o usa una salida .csv.')
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Matriz_corridas'
        ws.append(['Matriz de corridas'])
        ws.append([nota])
        ws.append([])
        ws.append(encabezado)
        for fila in tabla:
            ws.append(fila)
        ws.freeze_panes = 'A5'
        wb.save(a.salida)
    else:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            fh.write(f'# {nota}\n')
            w = csv.writer(fh)
            w.writerow(encabezado)
            w.writerows(tabla)

    n_total, gl = grados_de_libertad(factores, a.replicas, a.bloques)
    print(nota)
    print(f'Condiciones: {len(condiciones)}; corridas: {n_total}; archivo: {a.salida}')
    print('Grados de libertad:')
    for nombre, g in gl:
        print(f'  {nombre:<16}{g:>5}')
    if gl[-1][1] <= 0:
        print('Diseño sin réplica: no hay error puro. Analiza los contrastes con el método de Lenth (lenth.py).')
    elif a.bloques:
        print('El término de error agrupa las interacciones bloque x tratamiento (modelo aditivo de bloques).')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Potencia estadística, efecto mínimo detectable y tamaño de muestra.

Regla del sistema: la potencia se calcula, no se estima de memoria. Toda cifra que
salga de aquí se reporta junto con n, grados de libertad y la convención usada.

Convención: f de Cohen, con parámetro de no centralidad lambda = f^2 * N, donde N es
el número total de observaciones del experimento. Para un factor de dos niveles
balanceado, d = 2 f.

Subcomandos
  factorial    Tabla de grados de libertad y potencia por efecto de un factorial completo.
  anova        Potencia, f mínimo detectable o N para un efecto con gl dados.
  ttest        Dos grupos independientes: potencia, d mínimo detectable o n por grupo.
  correlacion  Valor crítico de r para un n dado, o n necesario para detectar un r.
  regresion    Regresión lineal múltiple (prueba global o de un subconjunto), con f2.
  muestra      Tamaño de muestra para estimar una proporción o una media (encuestas).

Ejemplos
  python3 potencia.py factorial --niveles 2,3,3 --replicas 5 --bloques 5 --f 0.30
  python3 potencia.py anova --gl-num 2 --gl-error 68 --n-total 90 --f 0.35
  python3 potencia.py anova --gl-num 1 --gl-error 12 --n-total 20 --potencia 0.80
  python3 potencia.py ttest --n 12 --potencia 0.80
  python3 potencia.py correlacion --n 24
  python3 potencia.py regresion --predictores 4 --n 80 --f2 0.15
  python3 potencia.py muestra --tipo proporcion --error 0.05 --poblacion 1200

Requiere scipy.
"""
import argparse
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
    from scipy.optimize import brentq
    from scipy.stats import f as dist_f, ncf, nct, norm, t as dist_t
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Falta scipy. Instala con: pip install scipy. Si no hay red, calcula con un motor '
                 'de cómputo externo o declara la cifra como "por confirmar".')


def potencia_f(gl_num, gl_error, n_total, f, alfa=0.05):
    lam = f * f * n_total
    f_crit = dist_f.ppf(1 - alfa, gl_num, gl_error)
    return float(1 - ncf.cdf(f_crit, gl_num, gl_error, lam))


def f_minimo(gl_num, gl_error, n_total, potencia=0.80, alfa=0.05):
    return float(brentq(lambda x: potencia_f(gl_num, gl_error, n_total, x, alfa) - potencia, 1e-4, 20))


def cmd_factorial(a):
    niveles = [int(x) for x in a.niveles.split(',')]
    nombres = a.nombres.split(',') if a.nombres else [chr(65 + i) for i in range(len(niveles))]
    if len(nombres) != len(niveles):
        sys.exit('El número de nombres no coincide con el de factores.')
    celdas = math.prod(niveles)
    n_total = celdas * a.replicas
    if a.bloques and a.replicas % a.bloques:
        sys.exit('Con bloques completos, el número de réplicas debe ser múltiplo del número de bloques.')
    gl_bloques = (a.bloques - 1) if a.bloques else 0
    efectos = []
    for r in range(1, len(niveles) + 1):
        for combo in itertools.combinations(range(len(niveles)), r):
            gl = math.prod(niveles[i] - 1 for i in combo)
            efectos.append(('x'.join(nombres[i] for i in combo), gl))
    gl_trat = sum(g for _, g in efectos)
    gl_error = n_total - 1 - gl_bloques - gl_trat
    print(f'Factorial completo {" x ".join(map(str, niveles))}: {celdas} condiciones, '
          f'{a.replicas} réplica(s), N = {n_total}.')
    print(f'gl total = {n_total - 1}; gl bloques = {gl_bloques}; gl tratamientos = {gl_trat}; gl error = {gl_error}')
    if gl_error <= 0:
        print('Sin grados de libertad para el error: diseño no replicado. No hay prueba F con error puro; '
              'analiza los contrastes con el método de Lenth (scripts/lenth.py).')
        return
    print(f'alfa = {a.alfa}; convención lambda = f^2 * N')
    cab = f'{"Efecto":<14}{"gl":>4}{"potencia (f=" + str(a.f) + ")":>20}{"f mínimo (pot=" + str(a.potencia) + ")":>24}'
    print(cab)
    for nombre, gl in efectos:
        p = potencia_f(gl, gl_error, n_total, a.f, a.alfa)
        fm = f_minimo(gl, gl_error, n_total, a.potencia, a.alfa)
        print(f'{nombre:<14}{gl:>4}{p:>20.3f}{fm:>24.3f}')
    print('Nota: para un efecto de 1 gl entre dos niveles balanceados, d = 2 f.')


def cmd_anova(a):
    if a.f is not None:
        p = potencia_f(a.gl_num, a.gl_error, a.n_total, a.f, a.alfa)
        print(f'Potencia = {p:.4f}  (gl = {a.gl_num}, {a.gl_error}; N = {a.n_total}; f = {a.f}; '
              f'lambda = {a.f ** 2 * a.n_total:.3f}; alfa = {a.alfa})')
    else:
        fm = f_minimo(a.gl_num, a.gl_error, a.n_total, a.potencia, a.alfa)
        extra = f'; equivale a d = {2 * fm:.3f} si el efecto compara dos niveles balanceados' if a.gl_num == 1 else ''
        print(f'f mínimo detectable = {fm:.4f}  (potencia = {a.potencia}; gl = {a.gl_num}, {a.gl_error}; '
              f'N = {a.n_total}; alfa = {a.alfa}){extra}')


def potencia_t(n1, n2, d, alfa=0.05, colas=2):
    gl = n1 + n2 - 2
    nc = d * math.sqrt(n1 * n2 / (n1 + n2))
    if colas == 2:
        tc = dist_t.ppf(1 - alfa / 2, gl)
        p = 1 - nct.cdf(tc, gl, nc) + nct.cdf(-tc, gl, nc)
    else:
        tc = dist_t.ppf(1 - alfa, gl)
        p = 1 - nct.cdf(tc, gl, nc)
    return 1.0 if math.isnan(p) else float(p)  # la t no central desborda con efectos enormes


def cmd_ttest(a):
    n1 = a.n
    n2 = a.n2 or a.n
    if a.d is not None and n1:
        print(f'Potencia = {potencia_t(n1, n2, a.d, a.alfa, a.colas):.4f}  '
              f'(n1 = {n1}, n2 = {n2}, gl = {n1 + n2 - 2}, d = {a.d}, alfa = {a.alfa}, colas = {a.colas})')
    elif n1:
        dm = brentq(lambda x: potencia_t(n1, n2, x, a.alfa, a.colas) - a.potencia, 1e-4, 20)
        print(f'd mínimo detectable = {dm:.4f}  (potencia = {a.potencia}, n1 = {n1}, n2 = {n2}, '
              f'gl = {n1 + n2 - 2}, alfa = {a.alfa}, colas = {a.colas})')
    elif a.d is not None:
        n = 2
        while potencia_t(n, n, a.d, a.alfa, a.colas) < a.potencia and n < 100000:
            n += 1
        print(f'n por grupo = {n}  (d = {a.d}, potencia alcanzada = {potencia_t(n, n, a.d, a.alfa, a.colas):.4f}, '
              f'alfa = {a.alfa}, colas = {a.colas})')
    else:
        sys.exit('Indica --n, --d o ambos.')


def r_critico(n, alfa=0.05):
    tc = dist_t.ppf(1 - alfa / 2, n - 2)
    return float(tc / math.sqrt(tc * tc + n - 2))


def cmd_correlacion(a):
    if a.n:
        rc = r_critico(a.n, a.alfa)
        print(f'r crítico (bilateral, alfa = {a.alfa}) = {rc:.4f}  con n = {a.n}, gl = {a.n - 2}. '
              f'Por debajo de ese valor absoluto no se interpreta como asociación.')
        print('Aproximación por t, válida para Pearson y de uso habitual para Spearman con n >= 10.')
    if a.r is not None:
        z = math.atanh(abs(a.r))
        n = math.ceil(((norm.ppf(1 - a.alfa / 2) + norm.ppf(a.potencia)) / z) ** 2 + 3)
        print(f'n necesario = {n}  para detectar |r| = {abs(a.r)} con potencia {a.potencia} y alfa = {a.alfa} '
              f'(aproximación z de Fisher).')
    if not a.n and a.r is None:
        sys.exit('Indica --n o --r.')


def cmd_regresion(a):
    u = a.subconjunto or a.predictores
    v = a.n - a.predictores - 1
    if v <= 0:
        sys.exit('n insuficiente: se necesitan más observaciones que predictores + 1.')
    if a.f2 is not None:
        lam = a.f2 * (u + v + 1)
        fc = dist_f.ppf(1 - a.alfa, u, v)
        p = float(1 - ncf.cdf(fc, u, v, lam))
        print(f'Potencia = {p:.4f}  (gl = {u}, {v}; n = {a.n}; f2 = {a.f2}; lambda = {lam:.3f}; alfa = {a.alfa})')
    else:
        def g(x):
            return 1 - ncf.cdf(dist_f.ppf(1 - a.alfa, u, v), u, v, x * (u + v + 1)) - a.potencia
        f2 = brentq(g, 1e-5, 50)
        print(f'f2 mínimo detectable = {f2:.4f}  (R2 parcial equivalente = {f2 / (1 + f2):.4f}; potencia = {a.potencia}; '
              f'gl = {u}, {v}; n = {a.n}; alfa = {a.alfa})')


def cmd_muestra(a):
    z = norm.ppf(1 - (1 - a.confianza) / 2)
    if a.tipo == 'proporcion':
        n0 = z * z * a.p * (1 - a.p) / a.error ** 2
        base = f'p = {a.p}, error = {a.error}'
    else:
        if a.sigma is None:
            sys.exit('Para una media indica --sigma (desviación estándar esperada, con su fuente).')
        n0 = (z * a.sigma / a.error) ** 2
        base = f'sigma = {a.sigma}, error = {a.error}'
    n = n0
    if a.poblacion:
        n = n0 / (1 + (n0 - 1) / a.poblacion)
    print(f'n = {math.ceil(n)}  ({base}, confianza = {a.confianza}, z = {z:.4f}, n0 = {n0:.1f}'
          + (f', corrección por población finita N = {a.poblacion}' if a.poblacion else ', población infinita') + ')')
    if a.no_respuesta:
        print(f'Con {a.no_respuesta:.0%} de no respuesta esperada: invitar a {math.ceil(n / (1 - a.no_respuesta))}.')
    print('Supone muestreo aleatorio simple. Para otros diseños muestrales, multiplica por el efecto de diseño.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)

    q = s.add_parser('factorial', help='tabla de gl y potencia por efecto')
    q.add_argument('--niveles', required=True, help='niveles por factor, p. ej. 2,3,3')
    q.add_argument('--nombres', help='nombres de los factores, p. ej. A,B,C')
    q.add_argument('--replicas', type=int, default=1)
    q.add_argument('--bloques', type=int, default=0, help='número de bloques completos (0 = sin bloques)')
    q.add_argument('--f', type=float, default=0.25, help='tamaño de efecto f de Cohen a evaluar')
    q.add_argument('--potencia', type=float, default=0.80)
    q.add_argument('--alfa', type=float, default=0.05)
    q.set_defaults(fn=cmd_factorial)

    q = s.add_parser('anova', help='potencia o f mínimo para un efecto')
    q.add_argument('--gl-num', type=int, required=True)
    q.add_argument('--gl-error', type=int, required=True)
    q.add_argument('--n-total', type=int, required=True)
    q.add_argument('--f', type=float)
    q.add_argument('--potencia', type=float, default=0.80)
    q.add_argument('--alfa', type=float, default=0.05)
    q.set_defaults(fn=cmd_anova)

    q = s.add_parser('ttest', help='dos grupos independientes')
    q.add_argument('--n', type=int, help='n del grupo 1 (y del 2 si no se indica --n2)')
    q.add_argument('--n2', type=int)
    q.add_argument('--d', type=float)
    q.add_argument('--potencia', type=float, default=0.80)
    q.add_argument('--alfa', type=float, default=0.05)
    q.add_argument('--colas', type=int, choices=(1, 2), default=2)
    q.set_defaults(fn=cmd_ttest)

    q = s.add_parser('correlacion', help='r crítico o n necesario')
    q.add_argument('--n', type=int)
    q.add_argument('--r', type=float)
    q.add_argument('--potencia', type=float, default=0.80)
    q.add_argument('--alfa', type=float, default=0.05)
    q.set_defaults(fn=cmd_correlacion)

    q = s.add_parser('regresion', help='regresión lineal múltiple')
    q.add_argument('--predictores', type=int, required=True, help='número total de predictores del modelo')
    q.add_argument('--subconjunto', type=int, help='predictores bajo prueba (por defecto, todos)')
    q.add_argument('--n', type=int, required=True)
    q.add_argument('--f2', type=float)
    q.add_argument('--potencia', type=float, default=0.80)
    q.add_argument('--alfa', type=float, default=0.05)
    q.set_defaults(fn=cmd_regresion)

    q = s.add_parser('muestra', help='tamaño de muestra para estimación')
    q.add_argument('--tipo', choices=('proporcion', 'media'), default='proporcion')
    q.add_argument('--error', type=float, required=True, help='margen de error absoluto')
    q.add_argument('--confianza', type=float, default=0.95)
    q.add_argument('--p', type=float, default=0.5, help='proporción esperada (0.5 = caso más conservador)')
    q.add_argument('--sigma', type=float)
    q.add_argument('--poblacion', type=int, help='tamaño de la población, si es finita y conocida')
    q.add_argument('--no-respuesta', type=float, default=0.0, help='fracción esperada de no respuesta, p. ej. 0.2')
    q.set_defaults(fn=cmd_muestra)

    a = p.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Crea el libro del corpus bibliográfico con sus cuatro hojas y el formato del sistema.

Hojas
  Corpus                  una fila por fuente incluida, ordenada por aporte a la obra propia
  Trazabilidad_busqueda   una fila por ecuación ejecutada, con fecha y número de resultados
  Obras_fundamentales     marco teórico exento de la ventana temporal
  Casos_abiertos          fuentes o parámetros que no pasan un filtro y esperan decisión del autor

Uso
  python3 crear_corpus.py --salida 01_Literatura/Corpus_Fuentes.xlsx --titulo "Corpus de la tesis" \
      [--alcance "Criterios: ..."] [--color 1F4E79] [--franja EDF3F8] [--fuente Arial]

No sobrescribe un archivo existente salvo con --forzar. Requiere openpyxl.
"""
import argparse
import os
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    if not {'-h', '--help'} & set(sys.argv[1:]):  # la ayuda funciona sin dependencias
        sys.exit('Falta openpyxl. Instala con: pip install openpyxl')

CORPUS = [('ID', 6), ('Autores', 26), ('Año', 7), ('Título', 40), ('Revista', 24), ('Palabras clave', 26),
          ('País', 12), ('¿Qué se hizo?', 40), ('¿Cómo se hizo?', 40), ('Resultados obtenidos', 40),
          ('Aporte a la obra propia', 40), ('DOI', 26), ('Cuartil (fuente y año)', 16),
          ('Acceso abierto (estado y enlace)', 26), ('Tipo documental', 14), ('Pilar', 12), ('Fase', 10),
          ('Vacío que sustenta', 14), ('Nivel de lectura', 16), ('Estado de verificación', 20), ('Orden de aporte', 9)]
TRAZA = [('ID', 8), ('Tipo', 16), ('Fecha', 12), ('Base o herramienta', 18), ('Pilar o bloque', 16),
         ('Ecuación o consulta exacta', 70), ('Filtros fuera de la ecuación', 26), ('Resultados', 11),
         ('Tras depuración', 11), ('Cribados', 10), ('A texto completo', 10), ('Incluidos', 10),
         ('Notas y cambios respecto de la versión anterior', 40)]
FUND = [('ID', 6), ('Autores', 26), ('Año', 7), ('Título', 40), ('Fuente', 24), ('DOI', 26),
        ('Acceso abierto (estado y enlace)', 26), ('Pilar que sustenta', 16), ('Papel teórico', 40),
        ('Criterio que la justifica', 34), ('Estado de verificación', 20)]
CASOS = [('ID', 6), ('Fecha', 12), ('Fuente o parámetro', 34), ('Criterio que no cumple', 26), ('Evidencia', 40),
         ('Opciones', 34), ('Decisión del autor', 26), ('Fecha de la decisión', 14)]
NOTAS = {
    'Corpus': 'Una fila por fuente incluida. Orden de filas: por aporte a la obra propia, de mayor a menor. '
              'Lo no verificado se escribe "por confirmar". Nivel de lectura: texto completo o solo resumen.',
    'Trazabilidad_busqueda': 'Una fila por ecuación ejecutada. Tipo: búsqueda, prueba de ausencia o sensibilidad. '
                             'Una ecuación sin fecha y sin número de resultados no existe.',
    'Obras_fundamentales': 'Marco teórico, no antecedentes. Exentas de la ventana temporal; el resto de criterios '
                           'se aplica según lo declarado en la Ficha del proyecto.',
    'Casos_abiertos': 'Lo que no pasa un filtro no se descarta ni se incluye en silencio: se registra aquí y lo '
                      'decide el autor, caso por caso.',
}


def hoja(wb, nombre, titulo, columnas, a, primera=False):
    ws = wb.active if primera else wb.create_sheet()
    ws.title = nombre
    ws.sheet_view.showGridLines = False
    ws['A1'] = titulo
    ws['A1'].font = Font(name=a.fuente, size=14, bold=True, color=a.color)
    ws['A2'] = (a.alcance + ' ' if a.alcance and nombre == 'Corpus' else '') + NOTAS[nombre]
    ws['A2'].font = Font(name=a.fuente, size=9.5, italic=True, color='44546A')
    ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=min(len(columnas), 8))
    ws.row_dimensions[2].height = 42
    for j, (texto, ancho) in enumerate(columnas, 1):
        c = ws.cell(row=4, column=j, value=texto)
        c.font = Font(name=a.fuente, size=10, bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=a.color)
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
        ws.column_dimensions[get_column_letter(j)].width = ancho
    ws.row_dimensions[4].height = 32
    for i in range(5, 5 + a.filas):
        for j in range(1, len(columnas) + 1):
            c = ws.cell(row=i, column=j)
            c.font = Font(name=a.fuente, size=10)
            c.alignment = Alignment(wrap_text=True, vertical='top')
            if (i - 5) % 2 == 1:
                c.fill = PatternFill('solid', fgColor=a.franja)
    ws.freeze_panes = 'A5'
    return ws


def crear(a):
    wb = openpyxl.Workbook()
    hoja(wb, 'Corpus', a.titulo, CORPUS, a, primera=True)
    hoja(wb, 'Trazabilidad_busqueda', 'Trazabilidad de la búsqueda', TRAZA, a)
    hoja(wb, 'Obras_fundamentales', 'Obras fundamentales', FUND, a)
    hoja(wb, 'Casos_abiertos', 'Casos abiertos para decisión del autor', CASOS, a)
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    wb.save(a.salida)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--salida', required=True)
    p.add_argument('--titulo', default='Corpus de fuentes')
    p.add_argument('--alcance', default='')
    p.add_argument('--color', default='1F4E79', help='color del encabezado, hexadecimal sin #')
    p.add_argument('--franja', default='EDF3F8', help='color de las filas alternas')
    p.add_argument('--fuente', default='Arial')
    p.add_argument('--filas', type=int, default=60, help='filas con formato preparadas')
    p.add_argument('--forzar', action='store_true')
    a = p.parse_args()
    if os.path.exists(a.salida) and not a.forzar:
        sys.exit(f'Ya existe {a.salida}. No se sobrescribe sin --forzar.')
    crear(a)
    print(f'Creado {a.salida} con las hojas Corpus, Trazabilidad_busqueda, Obras_fundamentales y Casos_abiertos.')


if __name__ == '__main__':
    main()

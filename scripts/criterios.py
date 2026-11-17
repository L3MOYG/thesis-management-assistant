#!/usr/bin/env python3
"""Panel de criterios de literatura: el autor elige los filtros y la utilidad los guarda y los aplica.

Ningún filtro tiene valor por defecto. Mientras el autor no elija, el filtro vale null ("por
confirmar") y la orden `aplicar` se detiene: la utilidad no supone criterios.

Órdenes
  panel     Muestra los filtros, sus opciones con código y la selección vigente.
  fijar     Guarda la selección: por perfil, por opciones o por códigos del panel.
  mostrar   Imprime la selección como tabla para la Ficha y como resumen de una línea.
  aplicar   Contrasta la salida de verificar_doi.py con los filtros elegidos.

Uso
  python3 criterios.py panel --criterios 01_Literatura/criterios_literatura.json
  python3 criterios.py panel --json                      (catálogo para un panel de selección)
  python3 criterios.py fijar --criterios <archivo> --perfil equilibrado --ventana 5
  python3 criterios.py fijar --criterios <archivo> --codigos "A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300"
  python3 criterios.py mostrar --criterios <archivo>
  python3 criterios.py aplicar --criterios <archivo> --verificacion verificacion.csv \
      [--anio-referencia 2026] [--exentas-de-ventana] [--salida casos.csv]

Códigos del panel: letra del filtro y opción. En los filtros de opción única y múltiple el
número es el de la opción (0 = sin filtro; varias opciones se separan con coma: T1,2,3). En los
filtros numéricos el número es el valor (V7 = últimos 7 años; V0 = sin límite).

Veredicto de `aplicar` por fuente: "pasa", "caso abierto" (incumple al menos un filtro: decide el
autor) o "por confirmar" (falta un dato verificado). La utilidad no excluye fuentes.

Código de salida: 0 correcto; 2 selección incompleta o valor no válido.
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import unicodedata

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

POR_CONFIRMAR = 'por confirmar'
SIN_FILTRO = 'sin_filtro'

# clave, letra, nombre, tipo, opciones [(valor, etiqueta)], advertencia
CATALOGO = [
    ('acceso', 'A', 'Acceso al texto completo', 'unica', [
        ('abierto', 'Solo acceso abierto verificado, con ubicación recuperable'),
        ('abierto_o_institucional', 'Acceso abierto o texto accesible con la suscripción institucional'),
        ('texto_completo', 'Cualquier vía legal al texto completo (préstamo, compra o copia del autor)'),
    ], 'Más estricto: corpus menor y comprobable por cualquiera. Más laxo: corpus mayor, acceso que declara el autor.'),
    ('cuartil', 'C', 'Cuartil de la revista', 'unica', [
        ('Q1', 'Solo Q1'), ('Q2', 'Q1 o Q2'), ('Q3', 'Q1 a Q3'),
        ('Q4', 'Cualquier cuartil: basta con que la revista esté en el índice'),
    ], 'Se verifica por revista y año. Ponencias, libros y tesis no tienen cuartil: quedan por confirmar.'),
    ('ventana', 'V', 'Ventana temporal de antecedentes (años)', 'entero', [
        (5, 'Últimos 5 años'), (7, 'Últimos 7 años'), (10, 'Últimos 10 años'), (15, 'Últimos 15 años'),
    ], 'Admite cualquier entero. Las obras fundamentales quedan exentas de la ventana.'),
    ('tipos', 'T', 'Tipo documental', 'multiple', [
        ('articulo', 'Artículo original'), ('revision', 'Artículo de revisión'),
        ('ponencia', 'Ponencia en actas de congreso'), ('capitulo_libro', 'Libro o capítulo de libro'),
        ('tesis', 'Tesis'), ('preprint', 'Preprint, sin revisión por pares'),
        ('informe_norma', 'Informe técnico o norma'),
    ], 'Selección múltiple. Un preprint no ha pasado revisión por pares: dilo si lo admites.'),
    ('idiomas', 'I', 'Idioma de la fuente', 'multiple', [
        ('es', 'Español'), ('en', 'Inglés'), ('pt', 'Portugués'), ('fr', 'Francés'),
    ], 'Selección múltiple. Con --idiomas admite otros códigos ISO 639-1 de dos letras.'),
    ('max_por_primer_autor', 'P', 'Máximo de fuentes por primer autor', 'entero', [
        (1, 'Una: primer autor distinto en cada antecedente'), (2, 'Hasta dos'), (3, 'Hasta tres'),
    ], 'Evita que un solo grupo domine el corpus. La coincidencia es por apellido e inicial: se presenta como posible.'),
    ('retractadas', 'R', 'Fuentes retractadas', 'unica', [
        ('excluir', 'Señalarlas como caso abierto'),
        ('permitir_con_nota', 'Permitirlas con nota, por ejemplo cuando son objeto de estudio'),
    ], 'Este filtro no admite "sin filtro": una retractación siempre se informa.'),
    ('citas_minimas', 'M', 'Mínimo de citas recibidas', 'entero', [
        (5, 'Al menos 5'), (10, 'Al menos 10'), (20, 'Al menos 20'),
    ], 'Penaliza los trabajos recientes. Úsalo con una ventana amplia o déjalo sin filtro.'),
    ('umbral_depuracion', 'U', 'Umbral de depuración de una ecuación (resultados)', 'entero', [
        (100, '100'), (200, '200'), (300, '300'), (500, '500'),
    ], 'Parámetro de búsqueda: por encima del umbral, la ecuación se depura antes de cribar. No se aplica a cada fuente.'),
]
SIN_OPCION_NULA = {'retractadas', 'umbral_depuracion'}
PERFILES = {
    'estricto': {'acceso': 'abierto', 'cuartil': 'Q2', 'ventana': 7, 'tipos': ['articulo', 'revision', 'ponencia'],
                 'idiomas': SIN_FILTRO, 'max_por_primer_autor': 1, 'retractadas': 'excluir', 'citas_minimas': 0,
                 'umbral_depuracion': 300},
    'equilibrado': {'acceso': 'abierto_o_institucional', 'cuartil': 'Q2', 'ventana': 10,
                    'tipos': ['articulo', 'revision', 'ponencia'], 'idiomas': SIN_FILTRO, 'max_por_primer_autor': 2,
                    'retractadas': 'excluir', 'citas_minimas': 0, 'umbral_depuracion': 300},
    'amplio': {'acceso': 'texto_completo', 'cuartil': 'Q4', 'ventana': 15,
               'tipos': ['articulo', 'revision', 'ponencia', 'capitulo_libro', 'tesis'], 'idiomas': SIN_FILTRO,
               'max_por_primer_autor': 0, 'retractadas': 'excluir', 'citas_minimas': 0, 'umbral_depuracion': 300},
}
# Tipos de OpenAlex y de Crossref. Un tipo que no figura aquí queda "por confirmar", con el tipo recibido.
TIPOS = {'article': 'articulo', 'journal-article': 'articulo', 'review': 'revision',
         'conference-paper': 'ponencia', 'conference-abstract': 'ponencia', 'proceedings-article': 'ponencia',
         'proceedings': 'ponencia',
         'book-chapter': 'capitulo_libro', 'book-section': 'capitulo_libro', 'book-part': 'capitulo_libro',
         'book': 'capitulo_libro', 'monograph': 'capitulo_libro', 'edited-book': 'capitulo_libro',
         'reference-book': 'capitulo_libro', 'dissertation': 'tesis', 'thesis': 'tesis',
         'preprint': 'preprint', 'posted-content': 'preprint', 'report': 'informe_norma',
         'report-component': 'informe_norma', 'standard': 'informe_norma'}
POR_CLAVE = {c[0]: c for c in CATALOGO}
POR_LETRA = {c[1]: c for c in CATALOGO}


def fallo(msg):
    print('ERROR: ' + msg, file=sys.stderr)
    sys.exit(2)


def vacio():
    return {'_nota': 'Selección del autor en el panel de criterios. null significa "por confirmar": el filtro no se ha '
                     'elegido y la utilidad no lo supone. "sin_filtro" (o 0 en los numéricos) es una elección.',
            'version': 1, 'perfil': None, 'fecha_seleccion': None, 'filtros': {c[0]: None for c in CATALOGO}}


def leer(ruta):
    if not ruta or not os.path.exists(ruta):
        return vacio()
    try:
        d = json.load(open(ruta, encoding='utf-8'))
    except json.JSONDecodeError as e:
        fallo(f'{ruta} no es JSON válido ({e}).')
    base = vacio()
    base.update({k: d[k] for k in ('perfil', 'fecha_seleccion') if k in d})
    for k, v in (d.get('filtros') or {}).items():
        if k not in POR_CLAVE:
            fallo(f'Filtro desconocido en {ruta}: {k}.')
        base['filtros'][k] = validar(k, v) if v is not None else None
    return base


def validar(clave, v):
    _, _, nombre, tipo, opciones, _ = POR_CLAVE[clave]
    validos = [o[0] for o in opciones]
    if tipo == 'entero':
        try:
            n = int(v)
        except (TypeError, ValueError):
            n = 0 if v == SIN_FILTRO else None
        if n is None or n < 0 or (n == 0 and clave in SIN_OPCION_NULA):
            fallo(f'{nombre}: se espera un entero {"positivo" if clave in SIN_OPCION_NULA else "no negativo (0 = sin filtro)"}; se recibió {v!r}.')
        return n
    if v == SIN_FILTRO or v == [SIN_FILTRO]:
        if clave in SIN_OPCION_NULA:
            fallo(f'{nombre} no admite "sin filtro".')
        return SIN_FILTRO
    if tipo == 'unica':
        if v not in validos:
            fallo(f'{nombre}: valor no válido {v!r}. Opciones: {", ".join(validos)}, {SIN_FILTRO}.')
        return v
    lista = [x.strip() for x in (v.split(',') if isinstance(v, str) else v) if str(x).strip()]
    for x in lista:
        if x not in validos and not (clave == 'idiomas' and re.fullmatch(r'[a-z]{2}', x)):
            fallo(f'{nombre}: valor no válido {x!r}. Opciones: {", ".join(validos)}.')
    if not lista:
        fallo(f'{nombre}: la selección está vacía. Usa {SIN_FILTRO} si no quieres filtrar.')
    return list(dict.fromkeys(lista))


def desde_codigos(texto):
    sel = {}
    for trozo in texto.replace(';', ' ').split():
        m = re.fullmatch(r'([A-Za-z])([\d,]+)', trozo)
        if not m or m.group(1).upper() not in POR_LETRA:
            fallo(f'Código no reconocido: {trozo!r}. Forma esperada: letra del filtro y opción, por ejemplo A2 o T1,2.')
        clave, _, nombre, tipo, opciones, _ = POR_LETRA[m.group(1).upper()]
        nums = [int(x) for x in m.group(2).split(',') if x]
        if tipo == 'entero':
            if len(nums) != 1:
                fallo(f'{nombre}: se espera un solo número.')
            sel[clave] = nums[0]
        elif nums == [0]:
            sel[clave] = SIN_FILTRO
        elif any(n < 1 or n > len(opciones) for n in nums) or (tipo == 'unica' and len(nums) != 1):
            fallo(f'{nombre}: opción fuera del panel en {trozo!r} (hay {len(opciones)} opciones).')
        else:
            sel[clave] = [opciones[n - 1][0] for n in nums] if tipo == 'multiple' else opciones[nums[0] - 1][0]
    return sel


def texto_de(clave, v):
    if v is None:
        return POR_CONFIRMAR
    _, _, _, tipo, opciones, _ = POR_CLAVE[clave]
    if v == SIN_FILTRO or (tipo == 'entero' and v == 0):
        return 'sin filtro'
    etiquetas = dict(opciones)
    if tipo == 'entero':
        unidad = {'ventana': f'Últimos {v} años', 'max_por_primer_autor': f'Hasta {v} por primer autor',
                  'citas_minimas': f'Al menos {v} citas', 'umbral_depuracion': f'{v} resultados'}
        return etiquetas.get(v) if clave != 'umbral_depuracion' and v in etiquetas else unidad[clave]
    if tipo == 'multiple':
        return ', '.join(etiquetas.get(x, x) for x in v)
    return etiquetas[v]


def cmd_panel(a):
    if a.json:
        print(json.dumps({'filtros': [{'clave': c, 'letra': l, 'nombre': n, 'tipo': t, 'advertencia': adv,
                                       'admite_sin_filtro': c not in SIN_OPCION_NULA,
                                       'opciones': [{'numero': i, 'valor': v, 'etiqueta': e}
                                                    for i, (v, e) in enumerate(ops, 1)]}
                                      for c, l, n, t, ops, adv in CATALOGO],
                          'perfiles': PERFILES}, ensure_ascii=False, indent=2))
        return
    sel = leer(a.criterios)
    print('PANEL DE CRITERIOS DE LITERATURA')
    print('Perfiles de partida: ' + ', '.join(PERFILES) + '. Un perfil es un atajo: cada filtro se ajusta después.\n')
    for c, l, n, t, ops, adv in CATALOGO:
        clase = {'unica': 'una opción', 'multiple': 'varias opciones', 'entero': 'número'}[t]
        print(f'[{l}] {n} ({clase}). Vigente: {texto_de(c, sel["filtros"][c])}')
        for i, (v, e) in enumerate(ops, 1):
            print(f'     {l}{v if t == "entero" else i}  {e}')
        if c not in SIN_OPCION_NULA:
            print(f'     {l}0  Sin filtro')
        print(f'     Nota: {adv}')
    print('\nResponde con los códigos, por ejemplo: A2 C2 V10 T1,2,3 I0 P2 R1 M0 U300')


def cmd_fijar(a):
    sel = leer(a.criterios)
    cambios = {}
    if a.perfil:
        cambios.update(PERFILES[a.perfil])
        sel['perfil'] = a.perfil
    if a.codigos:
        cambios.update(desde_codigos(a.codigos))
    for c in POR_CLAVE:
        v = getattr(a, c)
        if v is not None:
            cambios[c] = v
    if not cambios:
        fallo('No se indicó ningún filtro. Usa --perfil, --codigos o las opciones de cada filtro.')
    for c, v in cambios.items():
        sel['filtros'][c] = validar(c, v)
    if a.perfil and any(sel['filtros'][c] != validar(c, v) for c, v in PERFILES[a.perfil].items()):
        sel['perfil'] = a.perfil + ' (ajustado)'
    elif not a.perfil and sel.get('perfil') and not str(sel['perfil']).endswith('(ajustado)') and sel['perfil'] != 'personalizado':
        sel['perfil'] = str(sel['perfil']) + ' (ajustado)'
    sel['perfil'] = sel.get('perfil') or 'personalizado'
    sel['fecha_seleccion'] = datetime.date.today().isoformat()
    with open(a.criterios, 'w', encoding='utf-8') as fh:
        json.dump(sel, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print(f'Guardado {a.criterios}. Perfil: {sel["perfil"]}.')
    imprimir(sel)


def imprimir(sel):
    print('\n| Filtro | Selección vigente |\n|---|---|')
    for c, _, n, _, _, _ in CATALOGO:
        print(f'| {n} | {texto_de(c, sel["filtros"][c])} |')
    faltan = [POR_CLAVE[c][2] for c, v in sel['filtros'].items() if v is None]
    print('\nResumen: ' + '; '.join(f'{POR_CLAVE[c][2].lower()}: {texto_de(c, v)}' for c, v in sel['filtros'].items()) + '.')
    if faltan:
        print(f'Filtros sin elegir ({len(faltan)}): ' + '; '.join(faltan) + '. Lo resuelve: el autor, en el panel.')
    return faltan


def cmd_mostrar(a):
    if not os.path.exists(a.criterios):
        fallo(f'No existe {a.criterios}.')
    sel = leer(a.criterios)
    print(f'Perfil: {sel.get("perfil") or POR_CONFIRMAR}. Fecha de selección: {sel.get("fecha_seleccion") or POR_CONFIRMAR}.')
    imprimir(sel)


def clave_autor(nombre):
    s = unicodedata.normalize('NFKD', nombre or '').encode('ascii', 'ignore').decode().lower()
    partes = re.findall(r'[a-z]+', s)
    return (partes[-1] + ' ' + partes[0][0]) if len(partes) > 1 else (partes[0] if partes else '')


def cmd_aplicar(a):
    if not os.path.exists(a.criterios):
        fallo(f'No existe {a.criterios}. Créalo con la orden fijar.')
    f = leer(a.criterios)['filtros']
    faltan = [POR_CLAVE[c][2] for c, v in f.items() if v is None]
    if faltan:
        fallo('La selección está incompleta y la utilidad no supone criterios. Filtros sin elegir: '
              + '; '.join(faltan) + '. Lo resuelve: el autor, en el panel (orden panel y después fijar).')
    with open(a.verificacion, encoding='utf-8-sig', newline='') as fh:
        filas = list(csv.DictReader(fh))
    if not filas or 'doi' not in filas[0]:
        fallo(f'{a.verificacion} no parece la salida de verificar_doi.py (falta la columna doi).')
    ref = a.anio_referencia or datetime.date.today().year
    grupos = {}
    for r in filas:
        k = clave_autor(r.get('primer_autor', '')) if POR_CONFIRMAR not in (r.get('primer_autor') or POR_CONFIRMAR) else ''
        if k:
            grupos.setdefault(k, []).append(r['doi'])
    salida = []
    for r in filas:
        no, pc, notas = [], [], []
        dato = lambda c: (r.get(c) or '').strip()
        desconocido = lambda c: not dato(c) or POR_CONFIRMAR in dato(c).lower()
        if dato('estado') == POR_CONFIRMAR:
            salida.append((r, 'por confirmar', [], ['todos: la fuente no está verificada'], dato('nota')))
            continue
        if f['acceso'] != SIN_FILTRO:
            if desconocido('acceso_abierto'):
                pc.append('acceso')
            elif dato('acceso_abierto') != 'sí':
                if f['acceso'] == 'abierto':
                    no.append('acceso: no es de acceso abierto')
                else:
                    pc.append('acceso: no es abierto; el autor confirma la vía de acceso declarada')
        if f['cuartil'] != SIN_FILTRO:
            m = re.search(r'\bQ([1-4])\b', dato('cuartil'))
            if not m:
                pc.append('cuartil')
            elif int(m.group(1)) > int(f['cuartil'][1]):
                no.append(f'cuartil: Q{m.group(1)} y se pide {texto_de("cuartil", f["cuartil"])}')
        if f['ventana'] and not a.exentas_de_ventana:
            if not dato('anio').isdigit():
                pc.append('ventana')
            elif int(dato('anio')) < ref - f['ventana']:
                no.append(f'ventana: {dato("anio")} es anterior a {ref - f["ventana"]}')
        if f['tipos'] != SIN_FILTRO:
            t = TIPOS.get(dato('tipo').lower())
            if desconocido('tipo') or not t:
                pc.append(f'tipo documental ({dato("tipo") or "sin dato"})')
            elif t not in f['tipos']:
                no.append(f'tipo documental: {t}')
        if f['idiomas'] != SIN_FILTRO:
            if desconocido('idioma'):
                pc.append('idioma')
            elif dato('idioma').lower()[:2] not in f['idiomas']:
                no.append(f'idioma: {dato("idioma")}')
        if f['max_por_primer_autor']:
            k = clave_autor(dato('primer_autor')) if not desconocido('primer_autor') else ''
            if not k:
                pc.append('primer autor')
            elif len(grupos.get(k, [])) > f['max_por_primer_autor']:
                no.append(f'primer autor: {len(grupos[k])} fuentes con posible mismo primer autor ({dato("primer_autor")})')
        if dato('retractado') == 'SÍ':
            (no if f['retractadas'] == 'excluir' else notas).append('retractada')
        elif desconocido('retractado'):
            pc.append('retractación')
        if f['citas_minimas']:
            if not dato('citas').isdigit():
                pc.append('citas')
            elif int(dato('citas')) < f['citas_minimas']:
                no.append(f'citas: {dato("citas")} y se piden {f["citas_minimas"]}')
        veredicto = 'caso abierto' if no else POR_CONFIRMAR if pc else 'pasa'
        salida.append((r, veredicto, no, pc, '; '.join(notas)))
    n = {v: sum(s[1] == v for s in salida) for v in ('pasa', 'caso abierto', POR_CONFIRMAR)}
    print(f'Fuentes: {len(salida)}; pasan: {n["pasa"]}; casos abiertos: {n["caso abierto"]}; por confirmar: {n[POR_CONFIRMAR]}.')
    print(f'Año de referencia de la ventana: {ref}' + (' (ventana no aplicada: obras exentas).' if a.exentas_de_ventana else '.'))
    for r, v, no, pc, nota in salida:
        print(f'- {r["doi"]}: {v}' + (f' | incumple: {"; ".join(no)}' if no else '')
              + (f' | por confirmar: {"; ".join(pc)}' if pc else '') + (f' | nota: {nota}' if nota else ''))
    print('Un caso abierto no es una exclusión: el autor decide cada uno y la decisión se registra.')
    if a.salida:
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['doi', 'primer_autor', 'anio', 'veredicto', 'incumple', 'por_confirmar', 'nota'])
            for r, v, no, pc, nota in salida:
                w.writerow([r['doi'], r.get('primer_autor', ''), r.get('anio', ''), v, '; '.join(no), '; '.join(pc), nota])
        print(f'Archivo: {a.salida}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='orden', required=True)
    s = sub.add_parser('panel', help='muestra los filtros, sus opciones y la selección vigente')
    s.add_argument('--criterios')
    s.add_argument('--json', action='store_true', help='catálogo de filtros y perfiles en JSON')
    s.set_defaults(fn=cmd_panel)
    s = sub.add_parser('fijar', help='guarda la selección del autor')
    s.add_argument('--criterios', required=True)
    s.add_argument('--perfil', choices=sorted(PERFILES))
    s.add_argument('--codigos', help='códigos del panel, por ejemplo "A2 C2 V10 T1,2,3"')
    s.add_argument('--acceso')
    s.add_argument('--cuartil')
    s.add_argument('--ventana')
    s.add_argument('--tipos')
    s.add_argument('--idiomas')
    s.add_argument('--max-por-primer-autor', dest='max_por_primer_autor')
    s.add_argument('--retractadas')
    s.add_argument('--citas-minimas', dest='citas_minimas')
    s.add_argument('--umbral-depuracion', dest='umbral_depuracion')
    s.set_defaults(fn=cmd_fijar)
    s = sub.add_parser('mostrar', help='imprime la selección para la Ficha')
    s.add_argument('--criterios', required=True)
    s.set_defaults(fn=cmd_mostrar)
    s = sub.add_parser('aplicar', help='contrasta la verificación con los filtros')
    s.add_argument('--criterios', required=True)
    s.add_argument('--verificacion', required=True, help='CSV de salida de verificar_doi.py')
    s.add_argument('--anio-referencia', type=int, dest='anio_referencia')
    s.add_argument('--exentas-de-ventana', action='store_true', dest='exentas_de_ventana',
                   help='no aplica la ventana temporal (obras fundamentales)')
    s.add_argument('--salida')
    s.set_defaults(fn=cmd_aplicar)
    a = p.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()

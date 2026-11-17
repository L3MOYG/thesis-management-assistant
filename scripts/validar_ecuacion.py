#!/usr/bin/env python3
"""Construye, valida y traduce ecuaciones de búsqueda para Scopus y Web of Science.

La validación es fuera de línea: detecta los errores de sintaxis que hacen que una ecuación
devuelva cero resultados o resultados engañosos. No ejecuta la búsqueda ni sustituye el
registro de fecha y número de resultados en la hoja de trazabilidad.

Subcomandos
  construir   Arma la ecuación a partir de bloques de términos y filtros.
  validar     Revisa una ecuación ya escrita.
  traducir    Convierte una ecuación de Scopus a Web of Science.

Ejemplos
  python3 validar_ecuacion.py construir --id E1 \
      --nucleo "cover crop*|green manure" \
      --acoplamiento "maize|corn" \
      --resultado "yield|soil organic carbon" \
      --desde 2019 --tipos ar,re,cp --acceso-abierto --excluir "greenhouse|hydropon*"

  python3 validar_ecuacion.py validar --base scopus --ecuacion 'TITLE-ABS-KEY ( ... )'
  python3 validar_ecuacion.py traducir --ecuacion 'TITLE-ABS-KEY ( ... ) AND PUBYEAR > 2018'

Reglas de construcción
  - Máximo tres bloques AND (núcleo, acoplamiento, resultado medible): más bloques colapsan la
    recuperación.
  - Exclusiones siempre explícitas, en un único NOT al final.
  - Comodín * con al menos tres letras antes; operadores en mayúsculas; solo caracteres ASCII.
  - Los términos se separan con | y las frases se entrecomillan solas.
"""
import argparse
import re
import sys
import unicodedata

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

TIPOS_WOS = {'ar': 'Article', 're': 'Review', 'cp': '"Proceedings Paper"', 'ch': '"Book Chapter"',
             'bk': 'Book', 'ed': '"Editorial Material"', 'le': 'Letter'}
CAMPOS_SCOPUS = {'TITLE-ABS-KEY', 'TITLE-ABS', 'TITLE', 'ABS', 'KEY', 'AUTHKEY', 'PUBYEAR', 'DOCTYPE',
                 'ACCESSTYPE', 'DOI', 'LANGUAGE', 'SRCTYPE', 'SUBJAREA', 'SRCTITLE', 'AUTH', 'AFFIL',
                 'EXACTSRCTITLE', 'ISSN', 'PUBSTAGE', 'LIMIT-TO', 'EXCLUDE', 'ALL', 'REF', 'AFFILCOUNTRY'}
CAMPOS_WOS = {'TS', 'TI', 'AB', 'AK', 'KP', 'PY', 'DT', 'DO', 'LA', 'SO', 'AU', 'WC', 'CU', 'ALL'}


def termino(t):
    t = t.strip()
    if not t:
        return None
    if t.startswith('"') and t.endswith('"'):
        return t
    return f'"{t}"' if re.search(r'[\s-]', t) else t


def bloque(texto):
    ts = [termino(t) for t in texto.split('|')]
    ts = [t for t in ts if t]
    if not ts:
        return None
    return ts[0] if len(ts) == 1 else '( ' + ' OR '.join(ts) + ' )'


def construir_scopus(bloques, desde, hasta, tipos, oa, excluir, campo='TITLE-ABS-KEY'):
    q = f'{campo} ( ' + ' AND '.join(bloques) + ' )'
    if desde:
        q += f' AND PUBYEAR > {desde - 1}'
    if hasta:
        q += f' AND PUBYEAR < {hasta + 1}'
    if tipos:
        q += ' AND DOCTYPE ( ' + ' OR '.join(tipos) + ' )'
    if oa:
        q += ' AND ACCESSTYPE ( oa )'
    if excluir:
        ex = [termino(t) for t in excluir.split('|') if t.strip()]
        q += f' AND NOT {campo} ( ' + ' OR '.join(ex) + ' )'
    return q


def construir_wos(bloques, desde, hasta, tipos, excluir, anio_actual):
    q = 'TS=(' + ' AND '.join(bloques) + ')'
    if desde or hasta:
        q += f' AND PY=({desde or 1900}-{hasta or anio_actual})'
    if tipos:
        q += ' AND DT=(' + ' OR '.join(TIPOS_WOS.get(t, t) for t in tipos) + ')'
    q = '(' + q + ')'
    if excluir:
        ex = [termino(t) for t in excluir.split('|') if t.strip()]
        q += ' NOT TS=(' + ' OR '.join(ex) + ')'
    return q


def partes_nivel_cero(texto, separador):
    partes, nivel, actual, i, comillas = [], 0, '', 0, False
    while i < len(texto):
        c = texto[i]
        if c == '"':
            comillas = not comillas
        if not comillas:
            nivel += {'(': 1, ')': -1}.get(c, 0)
            if nivel == 0 and texto.startswith(separador, i):
                partes.append(actual)
                actual = ''
                i += len(separador)
                continue
        actual += c
        i += 1
    partes.append(actual)
    return [p.strip() for p in partes if p.strip()]


def nucleo_de(q, patron):
    m = re.search(patron, q)
    if not m:
        return None
    nivel, i0 = 0, m.end() - 1
    for i in range(i0, len(q)):
        nivel += {'(': 1, ')': -1}.get(q[i], 0)
        if nivel == 0:
            return q[i0 + 1:i].strip()
    return None


def comunes(q):
    errores, avisos = [], []
    raros = sorted({c for c in q if ord(c) > 126 or c in '\t\r\n'})
    if raros:
        errores.append('caracteres no ASCII o saltos de línea: '
                       + ', '.join(unicodedata.name(c, repr(c)).lower() for c in raros)
                       + ' (comillas tipográficas y acentos rompen la búsqueda)')
    nivel = 0
    for c in q:
        nivel += {'(': 1, ')': -1}.get(c, 0)
        if nivel < 0:
            errores.append('paréntesis de cierre sin apertura')
            break
    if nivel > 0:
        errores.append(f'{nivel} paréntesis sin cerrar')
    if q.count('"') % 2:
        errores.append('número impar de comillas')
    for frase in re.findall(r'"([^"]*)"', q):
        if frase.strip() != frase or '  ' in frase:
            errores.append(f'espacios sobrantes dentro de "{frase}"')
        if not frase.strip():
            errores.append('frase vacía entre comillas')
    for t in re.findall(r'[\w-]*\*', q):
        if len(t.rstrip('*').split('-')[-1]) < 3:
            errores.append(f'truncamiento con menos de tres letras: {t}')
    sin_frases = re.sub(r'"[^"]*"', '""', q)
    if re.search(r'\b(and|or|not|And|Or|Not)\b', sin_frases):
        errores.append('operador booleano que no está en mayúsculas')
    if re.search(r'\b(AND|OR)\s+(AND|OR)\b', sin_frases) or re.search(r'\(\s*(AND|OR)\b|\b(AND|OR)\s*\)', sin_frases):
        errores.append('operador sin operando (AND u OR colgando)')
    return errores, avisos


def valida_scopus(q):
    e, av = comunes(q)
    sin_frases = re.sub(r'"[^"]*"', '""', q)
    campos = set(re.findall(r'\b([A-Z][A-Z-]+)\s*\(', sin_frases)) - {'AND', 'OR', 'NOT', 'AND NOT'}
    desconocidos = campos - CAMPOS_SCOPUS - {'OPENACCESS'}
    if desconocidos:
        e.append('código de campo desconocido: ' + ', '.join(sorted(desconocidos)))
    if re.search(r'\bOPENACCESS\b', sin_frases, re.I):
        e.append('OPENACCESS ( 1 ) no se reconoce en la búsqueda avanzada web y puede devolver 0 documentos: '
                 'usa ACCESSTYPE ( oa ) o aplica el filtro de acceso abierto en el panel de resultados')
    n_not = len(re.findall(r'\bAND NOT\b', sin_frases))
    if n_not > 1:
        e.append('AND NOT aparece más de una vez: agrupa las exclusiones en un solo bloque final')
    elif n_not == 1 and partes_nivel_cero(q, ' AND NOT ')[-1].count(' AND ') > 0:
        av.append('hay operadores AND después del bloque AND NOT: las exclusiones deben ir al final')
    if re.search(r'\b(title-abs-key|pubyear|doctype|accesstype)\b', sin_frases):
        e.append('código de campo en minúsculas')
    if re.search(r'\{[^}]*[*?][^}]*\}', q):
        e.append('comodín dentro de llaves: las llaves buscan la frase exacta y no admiten comodines')
    if 'PUBYEAR' in sin_frases and not re.search(r'PUBYEAR\s*[<>=]\s*\d{4}', sin_frases):
        e.append('PUBYEAR sin operador (>, < o =) y año')
    if re.search(r'\bNOT\b', sin_frases) and not re.search(r'\bAND NOT\b', sin_frases):
        e.append('en Scopus la exclusión se escribe AND NOT')
    nuc = nucleo_de(q, r'TITLE-ABS-KEY\s*\(')
    if nuc is None:
        av.append('no se encontró un bloque TITLE-ABS-KEY ( ... ) inicial')
    else:
        n = len(partes_nivel_cero(nuc, ' AND '))
        if n > 3:
            av.append(f'{n} bloques AND en el núcleo temático: con más de tres la recuperación colapsa')
        if re.search(r'\(\s*("[^"]*"|[^\s()"]+)\s*\)', nuc):
            av.append('paréntesis alrededor de un solo término (inofensivo, pero ensucia la ecuación)')
    if not re.search(r'\bAND NOT\b', sin_frases):
        av.append('sin bloque AND NOT: confirma que el proyecto no declara exclusiones permanentes')
    if 'PUBYEAR' not in sin_frases:
        av.append('sin ventana temporal (PUBYEAR)')
    return e, av


def valida_wos(q):
    e, av = comunes(q)
    sin_frases = re.sub(r'"[^"]*"', '""', q)
    campos = set(re.findall(r'\b([A-Z]{2,3})=', sin_frases))
    if campos - CAMPOS_WOS:
        e.append('etiqueta de campo desconocida: ' + ', '.join(sorted(campos - CAMPOS_WOS)))
    if re.search(r'\bAND NOT\b', sin_frases):
        e.append('Web of Science usa NOT, no AND NOT')
    if re.search(r'[{}]', q):
        e.append('Web of Science no admite llaves; usa comillas')
    if re.search(r'TITLE-ABS-KEY|PUBYEAR|DOCTYPE|ACCESSTYPE', sin_frases):
        e.append('quedó sintaxis de Scopus en la ecuación')
    if 'PY=' in sin_frases and not re.search(r'PY=\(?\d{4}(-\d{4})?\)?', sin_frases):
        e.append('PY mal escrito: usa PY=(AAAA-AAAA)')
    if 'PY=' not in sin_frases:
        av.append('sin ventana temporal (PY)')
    nuc = nucleo_de(q, r'TS=\(')
    if nuc is not None and len(partes_nivel_cero(nuc, ' AND ')) > 3:
        av.append('más de tres bloques AND en el núcleo temático')
    if re.search(r'\bNOT\b', sin_frases) and not q.lstrip().startswith('('):
        av.append('NOT tiene precedencia sobre AND: encierra la parte positiva entre paréntesis')
    av.append('el acceso abierto no tiene etiqueta de campo: se aplica en el panel Refine > Open Access')
    return e, av


def informe(nombre, q, errores, avisos):
    print(f'\n[{nombre}]')
    print(q)
    print('  Errores: ' + ('ninguno detectado por las reglas' if not errores else ''))
    for x in errores:
        print('    - ' + x)
    for x in avisos:
        print('  Aviso: ' + x)


def cmd_construir(a):
    bloques = [b for b in (bloque(a.nucleo), bloque(a.acoplamiento or ''), bloque(a.resultado or '')) if b]
    for extra in a.bloque_extra or []:
        b = bloque(extra)
        if b:
            bloques.append(b)
    tipos = [t.strip() for t in a.tipos.split(',') if t.strip()] if a.tipos else []
    qs = construir_scopus(bloques, a.desde, a.hasta, tipos, a.acceso_abierto, a.excluir)
    qw = construir_wos(bloques, a.desde, a.hasta, tipos, a.excluir, a.anio_actual)
    if a.id:
        print(f'Ecuación {a.id}: {len(bloques)} bloque(s) AND')
    es, avs = valida_scopus(qs)
    ew, avw = valida_wos(qw)
    informe('Scopus, búsqueda avanzada', qs, es, avs)
    informe('Web of Science, Advanced Search', qw, ew, avw)
    print('\nRegistra en la hoja de trazabilidad: ID, base, ecuación exacta, fecha de ejecución y número de '
          'resultados. Una ecuación sin conteo registrado no existe. Si los resultados superan el umbral de depuración elegido en el panel de criterios, depura antes de cribar.')
    return 1 if es or ew else 0


def cmd_validar(a):
    q = a.ecuacion if a.ecuacion else open(a.archivo, encoding='utf-8').read().strip()
    e, av = (valida_scopus if a.base == 'scopus' else valida_wos)(q)
    informe(a.base, q, e, av)
    return 1 if e else 0


def cmd_traducir(a):
    q = a.ecuacion if a.ecuacion else open(a.archivo, encoding='utf-8').read().strip()
    nuc = nucleo_de(q, r'TITLE-ABS-KEY\s*\(')
    if nuc is None:
        sys.exit('No se encontró el bloque TITLE-ABS-KEY ( ... ) inicial.')
    m_d = re.search(r'PUBYEAR\s*>\s*(\d{4})', q)
    m_h = re.search(r'PUBYEAR\s*<\s*(\d{4})', q)
    desde = int(m_d.group(1)) + 1 if m_d else None
    hasta = int(m_h.group(1)) - 1 if m_h else None
    tipos = re.findall(r'\b([a-z]{2})\b', ' '.join(re.findall(r'DOCTYPE\s*\(([^)]*)\)', q)))
    excl = nucleo_de(q, r'AND NOT\s+TITLE-ABS-KEY\s*\(')
    w = 'TS=(' + re.sub(r'\s+', ' ', nuc) + ')'
    if desde or hasta:
        w += f' AND PY=({desde or 1900}-{hasta or a.anio_actual})'
    if tipos:
        w += ' AND DT=(' + ' OR '.join(TIPOS_WOS.get(t, t) for t in tipos) + ')'
    w = '(' + w + ')'
    if excl:
        w += ' NOT TS=(' + re.sub(r'\s+', ' ', excl) + ')'
    e, av = valida_wos(w)
    informe('Web of Science, traducida desde Scopus', w, e, av)
    print('\nTS busca en título, resumen, palabras clave del autor y Keywords Plus; TITLE-ABS-KEY incluye además '
          'las palabras clave indexadas. Los conteos de ambas bases no son comparables uno a uno.')
    return 1 if e else 0


def main():
    import datetime
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)
    q = s.add_parser('construir')
    q.add_argument('--id')
    q.add_argument('--nucleo', required=True, help='términos separados por |')
    q.add_argument('--acoplamiento')
    q.add_argument('--resultado')
    q.add_argument('--bloque-extra', action='append', help='bloque AND adicional (genera aviso si supera tres)')
    q.add_argument('--desde', type=int, help='primer año incluido')
    q.add_argument('--hasta', type=int, help='último año incluido')
    q.add_argument('--tipos', default='ar,re,cp', help='códigos de Scopus: ar, re, cp, ch, bk')
    q.add_argument('--acceso-abierto', action='store_true')
    q.add_argument('--excluir', help='términos de exclusión separados por |')
    q.add_argument('--anio-actual', type=int, default=datetime.date.today().year)
    q.set_defaults(fn=cmd_construir)
    q = s.add_parser('validar')
    q.add_argument('--base', choices=('scopus', 'wos'), required=True)
    q.add_argument('--ecuacion')
    q.add_argument('--archivo')
    q.set_defaults(fn=cmd_validar)
    q = s.add_parser('traducir')
    q.add_argument('--ecuacion')
    q.add_argument('--archivo')
    q.add_argument('--anio-actual', type=int, default=datetime.date.today().year)
    q.set_defaults(fn=cmd_traducir)
    a = p.parse_args()
    if a.cmd in ('validar', 'traducir') and not (a.ecuacion or a.archivo):
        sys.exit('Indica --ecuacion o --archivo.')
    sys.exit(a.fn(a))


if __name__ == '__main__':
    main()

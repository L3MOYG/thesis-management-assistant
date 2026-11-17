#!/usr/bin/env python3
"""Exporta el corpus a RIS y BibTeX para importarlo en un gestor de referencias (Zotero, Mendeley, EndNote).

Lee la hoja Corpus del libro creado por crear_corpus.py (encabezados en la fila 4) o un CSV con
las mismas columnas. Reconoce los encabezados por nombre, sin importar el orden.

Uso
  python3 corpus_a_ris.py --corpus 01_Literatura/Corpus_Fuentes.xlsx --ris corpus.ris --bib corpus.bib
  python3 corpus_a_ris.py --corpus Corpus_Fuentes.xlsx --hoja Obras_fundamentales --ris fundamentales.ris \
      --etiquetas obra_fundamental

Cada registro lleva como etiquetas (KW) las palabras clave, el pilar, la fase, el cuartil y las
etiquetas adicionales indicadas; la nota (N1) recoge el aporte a la obra propia y el estado de
verificación. Los autores se separan con punto y coma. Los registros sin título o sin autores
se omiten y se listan. Requiere openpyxl solo para leer .xlsx.
"""
import argparse
import csv
import re
import sys
import unicodedata

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

MAPA = {
    'autores': ('autores', 'autor', 'authors'), 'anio': ('año', 'anio', 'year'), 'titulo': ('título', 'titulo', 'title'),
    'revista': ('revista', 'fuente', 'journal', 'source title'), 'doi': ('doi',),
    'claves': ('palabras clave', 'keywords', 'author keywords'), 'pais': ('país', 'pais', 'country'),
    'aporte': ('aporte a la obra propia', 'aporte', 'papel teórico'), 'cuartil': ('cuartil',),
    'oa': ('acceso abierto',), 'tipo': ('tipo documental', 'tipo', 'document type'), 'pilar': ('pilar',),
    'fase': ('fase',), 'vacio': ('vacío que sustenta', 'vacio'), 'estado': ('estado de verificación',),
    'orden': ('orden de aporte',), 'id': ('id',),
}
TIPOS_RIS = {'artículo': 'JOUR', 'articulo': 'JOUR', 'article': 'JOUR', 'revisión': 'JOUR', 'review': 'JOUR',
             'ponencia': 'CPAPER', 'conference': 'CPAPER', 'proceedings': 'CPAPER', 'capítulo': 'CHAP', 'chapter': 'CHAP',
             'libro': 'BOOK', 'book': 'BOOK', 'tesis': 'THES', 'thesis': 'THES', 'norma': 'STAND', 'standard': 'STAND',
             'informe': 'RPRT', 'report': 'RPRT'}
TIPOS_BIB = {'JOUR': 'article', 'CPAPER': 'inproceedings', 'CHAP': 'incollection', 'BOOK': 'book', 'THES': 'thesis',
             'STAND': 'misc', 'RPRT': 'report'}


def sin_acentos(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def leer(ruta, hoja, fila_enc):
    if ruta.lower().endswith(('.xlsx', '.xlsm')):
        try:
            import openpyxl
        except ImportError:
            sys.exit('Para leer .xlsx instala openpyxl, o exporta la hoja a CSV.')
        wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
        if hoja not in wb.sheetnames:
            sys.exit(f'No existe la hoja {hoja}. Hojas: {", ".join(wb.sheetnames)}')
        filas = [[('' if c is None else str(c).strip()) for c in f] for f in wb[hoja].iter_rows(values_only=True)]
    else:
        with open(ruta, encoding='utf-8-sig', newline='') as fh:
            filas = [[c.strip() for c in f] for f in csv.reader(fh)]
    if fila_enc is None:  # primera fila que contenga DOI y título o autores
        for i, f in enumerate(filas[:30]):
            bajos = [c.lower() for c in f]
            if 'doi' in bajos and any(b in ('título', 'titulo', 'title', 'autores', 'authors') for b in bajos):
                fila_enc = i
                break
        else:
            sys.exit('No se encontró la fila de encabezados (debe contener DOI y Título o Autores). Usa --fila-encabezado.')
    else:
        fila_enc -= 1
    enc = [c.lower() for c in filas[fila_enc]]
    col = {}
    for clave, nombres in MAPA.items():
        for j, e in enumerate(enc):
            if any(e == n or e.startswith(n) for n in nombres):
                col[clave] = j
                break
    regs = []
    for f in filas[fila_enc + 1:]:
        r = {k: (f[j] if j < len(f) else '') for k, j in col.items()}
        if any(r.values()):
            regs.append(r)
    return regs


def autores(texto):
    partes = [a.strip() for a in re.split(r';|\n', texto) if a.strip()]
    if len(partes) == 1 and ' and ' in partes[0]:
        partes = [a.strip() for a in partes[0].split(' and ')]
    return partes


def apellido(autor):
    if ',' in autor:
        return autor.split(',')[0].strip()
    return autor.split()[-1] if autor.split() else autor


def limpiar_doi(d):
    d = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', d.strip(), flags=re.I)
    return '' if 'confirmar' in d.lower() else d


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--corpus', required=True)
    p.add_argument('--hoja', default='Corpus')
    p.add_argument('--fila-encabezado', type=int, help='número de fila de los encabezados (1 = primera)')
    p.add_argument('--ris')
    p.add_argument('--bib')
    p.add_argument('--etiquetas', default='', help='etiquetas adicionales para todos los registros, separadas por coma')
    a = p.parse_args()
    if not a.ris and not a.bib:
        sys.exit('Indica --ris, --bib o ambos.')

    regs = leer(a.corpus, a.hoja, a.fila_encabezado)
    extra = [e.strip() for e in a.etiquetas.split(',') if e.strip()]
    ris, bib, omitidos, claves_usadas, sin_doi = [], [], [], {}, []
    for r in regs:
        aus = autores(r.get('autores', ''))
        if not r.get('titulo') or not aus:
            omitidos.append(r.get('id') or r.get('titulo') or '(fila sin identificar)')
            continue
        tipo = 'JOUR'
        for k, v in TIPOS_RIS.items():
            if k in r.get('tipo', '').lower():
                tipo = v
                break
        m_anio = re.search(r'\d{4}', r.get('anio', '') or '')
        anio = m_anio.group(0) if m_anio else ''
        doi = limpiar_doi(r.get('doi', ''))
        if not doi:
            sin_doi.append(f'{apellido(aus[0])} {anio}')
        etiquetas = [k.strip() for k in re.split(r';|,', r.get('claves', '')) if k.strip()]
        for campo in ('pilar', 'fase', 'vacio'):
            if r.get(campo):
                etiquetas.append(re.sub(r'\s+', '_', r[campo].strip().lower()))
        q = re.search(r'Q[1-4]', r.get('cuartil', ''))
        if q:
            etiquetas.append(q.group(0))
        if r.get('oa', '').lower().startswith(('sí', 'si')):
            etiquetas.append('acceso_abierto')
        etiquetas += extra
        nota = '; '.join(x for x in (
            f"Aporte: {r['aporte']}" if r.get('aporte') else '', f"Cuartil: {r['cuartil']}" if r.get('cuartil') else '',
            f"País: {r['pais']}" if r.get('pais') else '', f"Pilar: {r['pilar']}" if r.get('pilar') else '',
            f"Orden de aporte: {r['orden']}" if r.get('orden') else '',
            f"Verificación: {r['estado']}" if r.get('estado') else '') if x)

        L = [f'TY  - {tipo}'] + [f'AU  - {x}' for x in aus]
        L += [f"TI  - {r['titulo']}"]
        if anio:
            L.append(f'PY  - {anio}')
        if r.get('revista'):
            L.append(f"{'JO' if tipo == 'JOUR' else 'T2'}  - {r['revista']}")
        if doi:
            L += [f'DO  - {doi}', f'UR  - https://doi.org/{doi}']
        L += [f'KW  - {e}' for e in dict.fromkeys(etiquetas)]
        if nota:
            L.append(f'N1  - {nota}')
        L.append('ER  - ')
        ris.append('\n'.join(L))

        base = re.sub(r'[^A-Za-z]', '', sin_acentos(apellido(aus[0]))) + anio
        n = claves_usadas.get(base, 0)
        claves_usadas[base] = n + 1
        clave = base + ('' if n == 0 else chr(ord('a') + n))
        campos = [('author', ' and '.join(aus)), ('title', '{' + r['titulo'] + '}'), ('year', anio),
                  ('journaltitle' if tipo == 'JOUR' else 'booktitle', r.get('revista', '')), ('doi', doi),
                  ('keywords', ', '.join(dict.fromkeys(etiquetas)))]
        bib.append('@' + TIPOS_BIB.get(tipo, 'misc') + '{' + clave + ',\n'
                   + ',\n'.join(f'  {k} = {{{v}}}' for k, v in campos if v) + '\n}')

    if a.ris:
        open(a.ris, 'w', encoding='utf-8').write('\n\n'.join(ris) + '\n')
    if a.bib:
        open(a.bib, 'w', encoding='utf-8').write('\n\n'.join(bib) + '\n')
    print(f'Registros exportados: {len(ris)}' + (f'; RIS: {a.ris}' if a.ris else '') + (f'; BibTeX: {a.bib}' if a.bib else ''))
    if omitidos:
        print(f'Omitidos por falta de título o autores ({len(omitidos)}): ' + '; '.join(map(str, omitidos)))
    if sin_doi:
        print(f'Sin DOI verificado ({len(sin_doi)}): ' + '; '.join(sin_doi) + '. El DOI es obligatorio en la referencia.')
    print('En Zotero: Archivo > Importar, con la opción de colocar los elementos en una colección nueva.')


if __name__ == '__main__':
    main()

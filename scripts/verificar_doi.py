#!/usr/bin/env python3
"""Verifica metadatos y acceso abierto de un conjunto de DOI contra OpenAlex, con Crossref de respaldo.

Regla del sistema: nada se afirma sin verificar. Lo que no pueda verificarse sale marcado
literalmente como "por confirmar", con el motivo y la consulta que lo resolvería. El script
nunca rellena un campo con una suposición.

Uso
  python3 verificar_doi.py --doi 10.1016/j.jobe.2023.108287 <otro DOI>
  python3 verificar_doi.py --archivo dois.txt --salida verificacion.csv
  python3 verificar_doi.py --corpus Corpus_Fuentes.xlsx --columna DOI --scimago scimagojr_2025.csv

  --scimago   archivo CSV descargado de SCImago Journal Rank (scimagojr.com > Journal Rankings >
              Download data). Con él se añade el cuartil por ISSN. Sin él, el cuartil queda
              "por confirmar". El valor es el mejor cuartil del año del archivo: declara el año.
  --mailto    correo de contacto para el grupo de cortesía de las API. Es opcional y no se envía
              salvo que lo indiques expresamente.
  --clave     clave de OpenAlex, si tu cuenta la requiere (o variable OPENALEX_API_KEY).

Si no hay red o la API limita la tasa (HTTP 429), el registro queda "por confirmar" y el
script lo informa; no reintenta en silencio. Solo usa la biblioteca estándar.
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

POR_CONFIRMAR = 'por confirmar'
CAMPOS = ['doi', 'estado', 'titulo', 'anio', 'revista', 'issn', 'primer_autor', 'n_autores', 'pais_primer_autor',
          'tipo', 'idioma', 'volumen', 'numero', 'paginas', 'acceso_abierto', 'estado_oa', 'enlace_oa', 'licencia', 'citas',
          'retractado', 'cuartil', 'fuente_verificacion', 'fecha_verificacion', 'nota']


def normaliza(doi):
    doi = doi.strip()
    doi = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', doi, flags=re.I)
    doi = re.sub(r'^doi:\s*', '', doi, flags=re.I)
    return doi.strip().rstrip('.').lower()


def obtener(url, espera=30):
    """Devuelve (objeto_json, None) o (None, motivo)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'verificador-bibliografico/1.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=espera) as r:
            return json.loads(r.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, 'no encontrado (404)'
        if e.code == 429:
            return None, 'límite de tasa (429): repetir más tarde'
        if e.code in (401, 403):
            return None, f'acceso denegado ({e.code}): la API puede requerir clave o la red la bloquea'
        return None, f'error HTTP {e.code}'
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, f'sin conexión con el servicio ({getattr(e, "reason", e)})'
    except json.JSONDecodeError:
        return None, 'respuesta no interpretable'


def desde_openalex(w):
    oa = w.get('open_access') or {}
    loc = w.get('primary_location') or {}
    src = loc.get('source') or {}
    mejor = w.get('best_oa_location') or {}
    bib = w.get('biblio') or {}
    autores = w.get('authorships') or []
    primero = autores[0] if autores else {}
    paises = primero.get('countries') or [i.get('country_code') for i in primero.get('institutions') or [] if i.get('country_code')]
    paginas = '-'.join(dict.fromkeys(x for x in (bib.get('first_page'), bib.get('last_page')) if x))
    enlace = oa.get('oa_url') or mejor.get('pdf_url') or mejor.get('landing_page_url')
    es_oa = oa.get('is_oa')
    if es_oa and not enlace:
        acceso, nota = POR_CONFIRMAR, 'OpenAlex lo marca abierto pero sin ubicación recuperable'
    else:
        acceso, nota = ('sí' if es_oa else 'no' if es_oa is False else POR_CONFIRMAR), ''
    return {
        'titulo': w.get('title') or w.get('display_name') or POR_CONFIRMAR,
        'anio': w.get('publication_year') or POR_CONFIRMAR,
        'revista': src.get('display_name') or POR_CONFIRMAR,
        'issn': ', '.join(src.get('issn') or ([src['issn_l']] if src.get('issn_l') else [])) or POR_CONFIRMAR,
        'primer_autor': (primero.get('author') or {}).get('display_name') or POR_CONFIRMAR,
        'n_autores': len(autores) or POR_CONFIRMAR,
        'pais_primer_autor': ', '.join(p for p in paises if p) or POR_CONFIRMAR,
        'tipo': w.get('type') or POR_CONFIRMAR, 'idioma': w.get('language') or POR_CONFIRMAR,
        'volumen': bib.get('volume') or '', 'numero': bib.get('issue') or '', 'paginas': paginas,
        'acceso_abierto': acceso, 'estado_oa': oa.get('oa_status') or POR_CONFIRMAR,
        'enlace_oa': enlace or '', 'licencia': mejor.get('license') or '',
        'citas': w.get('cited_by_count') if w.get('cited_by_count') is not None else POR_CONFIRMAR,
        'retractado': 'SÍ' if w.get('is_retracted') else 'no',
        'fuente_verificacion': 'OpenAlex', 'nota': nota,
    }


def desde_crossref(m):
    fecha = ((m.get('issued') or {}).get('date-parts') or [[None]])[0]
    autores = m.get('author') or []
    primero = autores[0] if autores else {}
    nombre = ' '.join(x for x in (primero.get('given'), primero.get('family')) if x) or primero.get('name')
    return {
        'titulo': (m.get('title') or [POR_CONFIRMAR])[0],
        'anio': fecha[0] if fecha and fecha[0] else POR_CONFIRMAR,
        'revista': (m.get('container-title') or [POR_CONFIRMAR])[0],
        'issn': ', '.join(m.get('ISSN') or []) or POR_CONFIRMAR,
        'primer_autor': nombre or POR_CONFIRMAR, 'n_autores': len(autores) or POR_CONFIRMAR,
        'pais_primer_autor': POR_CONFIRMAR, 'tipo': m.get('type') or POR_CONFIRMAR,
        'idioma': m.get('language') or POR_CONFIRMAR,
        'volumen': m.get('volume') or '', 'numero': m.get('issue') or '', 'paginas': m.get('page') or '',
        'acceso_abierto': POR_CONFIRMAR, 'estado_oa': POR_CONFIRMAR, 'enlace_oa': '',
        'licencia': ((m.get('license') or [{}])[0]).get('URL', ''),
        'citas': m.get('is-referenced-by-count', POR_CONFIRMAR), 'retractado': POR_CONFIRMAR,
        'fuente_verificacion': 'Crossref',
        'nota': 'Crossref no informa acceso abierto: verificar en OpenAlex o en la página del editor',
    }


def cargar_scimago(ruta):
    """Devuelve {issn_sin_guion: (cuartil, titulo)} a partir del CSV de SCImago (separado por ;)."""
    with open(ruta, encoding='utf-8-sig', newline='') as fh:
        muestra = fh.read(4096)
        fh.seek(0)
        sep = ';' if muestra.count(';') > muestra.count(',') else ','
        lector = csv.DictReader(fh, delimiter=sep)
        col_issn = next((c for c in lector.fieldnames if c and c.strip().lower() == 'issn'), None)
        col_q = next((c for c in lector.fieldnames if c and 'quartile' in c.lower()), None)
        col_t = next((c for c in lector.fieldnames if c and c.strip().lower() == 'title'), None)
        if not col_issn or not col_q:
            sys.exit(f'El archivo de SCImago no tiene columnas Issn y Quartile reconocibles: {lector.fieldnames}')
        tabla = {}
        for f in lector:
            for issn in re.split(r'[,\s]+', f.get(col_issn) or ''):
                issn = issn.replace('-', '').strip().upper()
                if issn:
                    tabla[issn] = (f.get(col_q) or '', f.get(col_t) or '')
    return tabla


def cuartil(reg, tabla, etiqueta):
    if not tabla:
        return POR_CONFIRMAR
    for issn in re.split(r'[,\s]+', str(reg.get('issn') or '')):
        clave = issn.replace('-', '').strip().upper()
        if clave in tabla and tabla[clave][0] and tabla[clave][0] != '-':
            return f'{tabla[clave][0]} ({etiqueta})'
    return f'{POR_CONFIRMAR}: ISSN no localizado en {etiqueta}'


def verificar(dois, mailto=None, clave=None, pausa=0.2, obtener_fn=obtener):
    hoy = datetime.date.today().isoformat()
    extra = ''
    if mailto:
        extra += '&mailto=' + urllib.parse.quote(mailto)
    if clave:
        extra += '&api_key=' + urllib.parse.quote(clave)
    resultados = {}
    pendientes = list(dict.fromkeys(dois))
    for i in range(0, len(pendientes), 40):
        lote = pendientes[i:i + 40]
        filtro = '|'.join(urllib.parse.quote(d, safe='/') for d in lote)
        url = f'https://api.openalex.org/works?filter=doi:{filtro}&per-page=50{extra}'
        datos, motivo = obtener_fn(url)
        if datos:
            for w in datos.get('results') or []:
                d = normaliza(w.get('doi') or '')
                if d:
                    resultados[d] = dict(desde_openalex(w), doi=d, estado='verificado', fecha_verificacion=hoy)
        for d in lote:
            if d in resultados:
                continue
            m_oa = motivo or 'no encontrado en OpenAlex'
            cr, motivo_cr = obtener_fn('https://api.crossref.org/works/' + urllib.parse.quote(d, safe='/')
                                       + ('?mailto=' + urllib.parse.quote(mailto) if mailto else ''))
            if cr and cr.get('message'):
                reg = dict(desde_crossref(cr['message']), doi=d, estado='verificado parcialmente', fecha_verificacion=hoy)
                reg['nota'] = f'OpenAlex: {m_oa}. ' + reg['nota']
                resultados[d] = reg
            else:
                resultados[d] = {c: (POR_CONFIRMAR if c not in ('volumen', 'numero', 'paginas', 'enlace_oa', 'licencia') else '')
                                 for c in CAMPOS}
                resultados[d].update(doi=d, estado=POR_CONFIRMAR, fuente_verificacion='ninguna', fecha_verificacion=hoy,
                                     nota=f'OpenAlex: {m_oa}. Crossref: {motivo_cr or "sin registro"}. '
                                          f'Lo resuelve: abrir https://doi.org/{d} y repetir la consulta con red disponible.')
            time.sleep(pausa)
        time.sleep(pausa)
    return [resultados[d] for d in pendientes]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--doi', nargs='*', default=[])
    p.add_argument('--archivo', help='texto con un DOI por línea')
    p.add_argument('--corpus', help='CSV o libro .xlsx del corpus con una columna de DOI')
    p.add_argument('--hoja', help='hoja del libro .xlsx (por defecto, todas las que tengan la columna)')
    p.add_argument('--columna', default='DOI')
    p.add_argument('--scimago')
    p.add_argument('--mailto')
    p.add_argument('--clave', default=os.environ.get('OPENALEX_API_KEY'))
    p.add_argument('--salida')
    a = p.parse_args()

    dois = list(a.doi)
    if a.archivo:
        dois += [l for l in open(a.archivo, encoding='utf-8').read().splitlines() if l.strip() and not l.startswith('#')]
    if a.corpus and a.corpus.lower().endswith(('.xlsx', '.xlsm')):
        # Libro del corpus: se leen todas las hojas que tengan la columna pedida (Corpus y Obras_fundamentales).
        try:
            import openpyxl
        except ImportError:
            sys.exit('Para leer el corpus en .xlsx instala openpyxl, o exporta la hoja a CSV.')
        wb = openpyxl.load_workbook(a.corpus, data_only=True, read_only=True)
        hojas = [a.hoja] if a.hoja else wb.sheetnames
        for h in hojas:
            if h not in wb.sheetnames:
                sys.exit(f'No existe la hoja {h}. Hojas: {", ".join(wb.sheetnames)}')
            j = None
            for fila in wb[h].iter_rows(values_only=True):
                celdas = ['' if c is None else str(c).strip() for c in fila]
                if j is None:
                    j = next((k for k, c in enumerate(celdas) if c.lower() == a.columna.lower()), None)
                elif j < len(celdas) and celdas[j] and POR_CONFIRMAR not in celdas[j].lower():
                    dois.append(celdas[j])
    elif a.corpus:
        with open(a.corpus, encoding='utf-8-sig') as fh:
            for f in csv.DictReader(l for l in fh if not l.startswith('#')):
                col = next((c for c in f if c and c.strip().lower() == a.columna.lower()), None)
                if col and f[col] and POR_CONFIRMAR not in f[col].lower():
                    dois.append(f[col])
    dois = [normaliza(d) for d in dois if normaliza(d)]
    invalidos = [d for d in dois if not re.match(r'^10\.\d{4,9}/\S+$', d)]
    dois = [d for d in dois if d not in invalidos]
    if not dois and not invalidos:
        sys.exit('No se recibió ningún DOI.')

    tabla = cargar_scimago(a.scimago) if a.scimago else None
    etiqueta = 'SCImago, archivo ' + os.path.basename(a.scimago) if a.scimago else ''
    registros = verificar(dois, a.mailto, a.clave)
    for r in registros:
        r['cuartil'] = cuartil(r, tabla, etiqueta)
    for d in invalidos:
        reg = {c: '' for c in CAMPOS}
        reg.update(doi=d, estado=POR_CONFIRMAR, nota='no tiene forma de DOI: revisar la transcripción')
        registros.append(reg)

    if a.salida:
        # El archivo se escribe antes de imprimir: un fallo de la consola no debe impedirlo.
        with open(a.salida, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=CAMPOS, extrasaction='ignore')
            w.writeheader()
            w.writerows(registros)
    ok = sum(r['estado'] == 'verificado' for r in registros)
    parcial = sum(r['estado'] == 'verificado parcialmente' for r in registros)
    print(f'DOI procesados: {len(registros)}; verificados: {ok}; parciales (solo Crossref): {parcial}; '
          f'por confirmar: {len(registros) - ok - parcial}')
    for r in registros:
        print(f"- {r['doi']}: {r['estado']}"
              + (f" | {r['primer_autor']} ({r['anio']}). {str(r['titulo'])[:70]} | {r['revista']} | "
                 f"OA: {r['acceso_abierto']} ({r['estado_oa']}) | cuartil: {r['cuartil']}" if r['estado'] != POR_CONFIRMAR else '')
              + (f" | NOTA: {r['nota']}" if r.get('nota') else '')
              + (' | RETRACTADO' if r.get('retractado') == 'SÍ' else ''))
    if a.salida:
        print(f'Archivo: {a.salida}')
    if not a.scimago:
        print('Cuartil sin verificar: aporta el CSV de SCImago con --scimago o consulta scimagojr.com por revista y año.')


if __name__ == '__main__':
    main()

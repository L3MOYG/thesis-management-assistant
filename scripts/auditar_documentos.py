#!/usr/bin/env python3
"""Auditoría mecánica de los documentos del proyecto. Detecta; no corrige.

Subcomandos
  cifras        Contrasta cada cifra canónica del Registro_Cifras contra todos los documentos y
                lista dónde aparece con un valor distinto.
  pendientes    Localiza todas las marcas "por confirmar" con su contexto.
  nomenclatura  Lista identificadores (A, B, Y1, Z9...) usados pero no declarados, y declarados
                pero no usados.
  citas         Cruza las citas autor-año del texto con el corpus: citadas que no están en el
                corpus y fuentes del corpus que nadie cita. Es heurístico: revisa los candidatos.

Uso
  python3 auditar_documentos.py cifras --registro 00_Gobierno/Registro_Cifras.csv --rutas 03_Metodologia 05_Capitulos
  python3 auditar_documentos.py pendientes --rutas .
  python3 auditar_documentos.py nomenclatura --declarados "A,B,C,Y1,Y2,Y3" --rutas 05_Capitulos
  python3 auditar_documentos.py citas --corpus 01_Literatura/Corpus_Fuentes.xlsx --rutas 05_Capitulos

Registro_Cifras.csv: columnas id, valor, unidad, descripcion, patron. El patrón es una expresión
regular con un único grupo de captura para el número, por ejemplo:  (\\d+)\\s+parcelas

Lee .docx, .md, .txt, .tex, .bib, .csv y, si openpyxl está instalado, .xlsx. Los .pdf no se leen:
audita el documento fuente. Solo usa la biblioteca estándar.
"""
import argparse
import csv
import html
import os
import re
import sys
import unicodedata
import zipfile

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

TEXTO = ('.md', '.txt', '.tex', '.bib', '.csv', '.rst')


def leer_docx(ruta):
    partes = []
    with zipfile.ZipFile(ruta) as z:
        for nombre in z.namelist():
            if re.match(r'word/(document|footnotes|endnotes|header\d*|footer\d*)\.xml$', nombre):
                xml = z.read(nombre).decode('utf-8', errors='replace')
                xml = re.sub(r'<w:tab[^>]*/>', '\t', xml)
                xml = re.sub(r'</w:p>|<w:br[^>]*/>|</w:tr>', '\n', xml)
                xml = re.sub(r'</w:tc>', ' | ', xml)
                partes.append(html.unescape(re.sub(r'<[^>]+>', '', xml)))
    return '\n'.join(partes)


def leer_xlsx(ruta):
    try:
        import openpyxl
    except ImportError:
        return None
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    lineas = []
    for ws in wb.worksheets:
        for fila in ws.iter_rows(values_only=True):
            celdas = [str(c) for c in fila if c is not None]
            if celdas:
                lineas.append(f'[{ws.title}] ' + ' | '.join(celdas))
    return '\n'.join(lineas)


def recorrer(rutas, extensiones=None):
    vistos, omitidos = [], []
    for ruta in rutas:
        if os.path.isfile(ruta):
            candidatos = [ruta]
        else:
            candidatos = []
            for raiz, dirs, archivos in os.walk(ruta):
                dirs[:] = [d for d in dirs if not d.startswith(('.', '~', '__'))]
                candidatos += [os.path.join(raiz, f) for f in sorted(archivos) if not f.startswith(('~$', '.'))]
        for c in candidatos:
            ext = os.path.splitext(c)[1].lower()
            if extensiones and ext not in extensiones:
                continue
            try:
                if ext == '.docx':
                    vistos.append((c, leer_docx(c)))
                elif ext == '.xlsx':
                    t = leer_xlsx(c)
                    if t is None:
                        omitidos.append((c, 'openpyxl no instalado'))
                    else:
                        vistos.append((c, t))
                elif ext in TEXTO:
                    vistos.append((c, open(c, encoding='utf-8', errors='replace').read()))
                elif ext == '.pdf':
                    omitidos.append((c, 'PDF: audita el documento fuente'))
            except (zipfile.BadZipFile, OSError, KeyError) as e:
                omitidos.append((c, f'no se pudo leer ({e})'))
    return vistos, omitidos


def contexto(texto, ini, fin, margen=70):
    a, b = max(0, ini - margen), min(len(texto), fin + margen)
    return ' '.join(texto[a:b].split())


def a_numero(s):
    s = s.strip().replace(' ', '').replace(' ', '').rstrip('.,;:')  # puntuación de fin de frase capturada por el patrón
    if re.match(r'^-?\d{1,3}(\.\d{3})+,\d+$', s):
        s = s.replace('.', '').replace(',', '.')
    else:
        s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def cmd_cifras(a):
    with open(a.registro, encoding='utf-8-sig', newline='') as fh:
        registro = [r for r in csv.DictReader(l for l in fh if not l.startswith('#')) if (r.get('patron') or '').strip()]
    if not registro:
        sys.exit('El registro no tiene cifras con patrón. Añade al menos una fila con id, valor y patron.')
    docs, omitidos = recorrer(a.rutas)
    docs = [(r, t) for r, t in docs if os.path.abspath(r) != os.path.abspath(a.registro)]
    discrepancias = total = 0
    for reg in registro:
        try:
            patron = re.compile(reg['patron'], re.I)
        except re.error as e:
            print(f"[{reg['id']}] patrón inválido: {e}")
            continue
        if patron.groups != 1:
            print(f"[{reg['id']}] el patrón debe tener exactamente un grupo de captura.")
            continue
        canon = a_numero(reg['valor'])
        hallazgos, malos = 0, []
        for ruta, texto in docs:
            for m in patron.finditer(texto):
                hallazgos += 1
                encontrado = a_numero(m.group(1))
                igual = (encontrado == canon) if canon is not None and encontrado is not None else m.group(1).strip() == reg['valor'].strip()
                if not igual:
                    malos.append((ruta, m.group(1), contexto(texto, m.start(), m.end())))
        total += hallazgos
        estado = 'coherente' if not malos else f'{len(malos)} DISCREPANCIA(S)'
        if hallazgos == 0:
            estado = 'sin apariciones (revisa el patrón o la cifra no se usa todavía)'
        print(f"[{reg['id']}] {reg.get('descripcion', '')} = {reg['valor']} {reg.get('unidad', '')}: "
              f"{hallazgos} aparición(es); {estado}")
        for ruta, valor, ctx in malos:
            discrepancias += 1
            print(f'    {ruta}: dice {valor}  ...{ctx}...')
    print(f'\nDocumentos leídos: {len(docs)}; cifras auditadas: {len(registro)}; apariciones: {total}; '
          f'discrepancias: {discrepancias}')
    for ruta, motivo in omitidos:
        print(f'  omitido {ruta}: {motivo}')
    if discrepancias:
        print('Una cifra canónica solo cambia en el registro y se propaga a todos los archivos en la misma sesión.')
    return 1 if discrepancias else 0


def cmd_pendientes(a):
    docs, omitidos = recorrer(a.rutas)
    patron = re.compile(r'por\s+confirmar', re.I)
    total = 0
    for ruta, texto in docs:
        ms = list(patron.finditer(texto))
        if not ms:
            continue
        total += len(ms)
        print(f'{ruta}: {len(ms)}')
        for m in ms[:a.max]:
            print(f'    ...{contexto(texto, m.start(), m.end())}...')
        if len(ms) > a.max:
            print(f'    (y {len(ms) - a.max} más)')
    print(f'\nDocumentos leídos: {len(docs)}; marcas "por confirmar": {total}')
    for ruta, motivo in omitidos:
        print(f'  omitido {ruta}: {motivo}')
    return 0


def cmd_nomenclatura(a):
    declarados = {d.strip() for d in a.declarados.split(',') if d.strip()}
    ignorar = {d.strip() for d in a.ignorar.split(',') if d.strip()}
    docs, _ = recorrer(a.rutas)
    patron = re.compile(a.patron)
    # Las letras sueltas (A, B, C) solo cuentan cuando siguen a una palabra que las designa como
    # identificador; de otro modo cualquier mayúscula aislada sería un falso positivo.
    letra = re.compile(r'\b(?:[Ff]actor(?:es)?|[Vv]ariable|[Cc]ovariable|[Rr]espuesta|[Bb]loque|[Tt]ratamiento)\s+([A-Z])\b')
    usados = {}
    for ruta, texto in docs:
        for m in patron.finditer(texto):
            usados.setdefault(m.group(0), {}).setdefault(ruta, 0)
            usados[m.group(0)][ruta] += 1
        for m in letra.finditer(texto):
            usados.setdefault(m.group(1), {}).setdefault(ruta, 0)
            usados[m.group(1)][ruta] += 1
    no_decl = {k: v for k, v in usados.items() if k not in declarados and k not in ignorar}
    print(f'Documentos leídos: {len(docs)}; identificadores declarados: {len(declarados)}')
    print(f'Usados y no declarados ({len(no_decl)}):')
    for k in sorted(no_decl):
        print(f'    {k}: ' + '; '.join(f'{os.path.basename(r)} ({n})' for r, n in no_decl[k].items()))
    sin_uso = sorted(d for d in declarados if d not in usados and (patron.fullmatch(d) or re.fullmatch(r'[A-Z]', d)))
    print(f'Declarados y no usados ({len(sin_uso)}): ' + (', '.join(sin_uso) or 'ninguno'))
    print('Un identificador no declarado puede ser un renombrado accidental o una sigla ajena: decide caso por caso.')
    return 0


def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s.lower())


def claves_corpus(ruta, hoja):
    filas = []
    if ruta.lower().endswith('.xlsx'):
        try:
            import openpyxl
        except ImportError:
            sys.exit('Para leer el corpus en .xlsx instala openpyxl o expórtalo a CSV.')
        wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
        hojas = [hoja] if hoja else [h for h in wb.sheetnames if h in ('Corpus', 'Obras_fundamentales')] or wb.sheetnames[:1]
        for h in hojas:
            filas += [[('' if c is None else str(c)) for c in f] for f in wb[h].iter_rows(values_only=True)] + [[]]
    else:
        with open(ruta, encoding='utf-8-sig', newline='') as fh:
            filas = list(csv.reader(fh))
    claves, ia, iy = {}, None, None
    for f in filas:
        bajos = [c.strip().lower() for c in f]
        if 'doi' in bajos and any(b in ('autores', 'authors') for b in bajos):
            ia = next(i for i, b in enumerate(bajos) if b in ('autores', 'authors'))
            iy = next((i for i, b in enumerate(bajos) if b in ('año', 'anio', 'year')), None)
            continue
        if ia is None or iy is None or len(f) <= max(ia, iy) or not f[ia].strip():
            continue
        primero = re.split(r';|\n', f[ia])[0].strip()
        ap = primero.split(',')[0].strip() if ',' in primero else (primero.split()[-1] if primero.split() else '')
        m = re.search(r'\d{4}', f[iy])
        if ap and m:
            claves[(norm(ap), m.group(0))] = f'{ap} ({m.group(0)})'
    if not claves:
        sys.exit('No se pudieron leer autores y años del corpus (se esperan columnas Autores, Año y DOI).')
    return claves


def cmd_citas(a):
    corpus = claves_corpus(a.corpus, a.hoja)
    docs, _ = recorrer(a.rutas, extensiones=('.docx', '.md', '.txt', '.tex'))
    ap = r"[A-ZÁÉÍÓÚÑÜ][\wáéíóúñüÁÉÍÓÚÑÜ'’-]+"
    narrativa = re.compile(rf"({ap})(?:\s+(?:et al\.|y colaboradores|y cols\.|(?:y|and|&)\s+{ap}))?\s+\((\d{{4}})[a-z]?\)")
    parentesis = re.compile(r'\(([^()]{3,300}?\d{4}[a-z]?[^()]{0,40}?)\)')
    dentro = re.compile(rf"({ap})[^;()]*?,?\s+(\d{{4}})[a-z]?")
    citadas = {}
    for ruta, texto in docs:
        for m in narrativa.finditer(texto):
            citadas.setdefault((norm(m.group(1)), m.group(2)), [f'{m.group(1)} ({m.group(2)})', set()])[1].add(os.path.basename(ruta))
        for m in parentesis.finditer(texto):
            for trozo in m.group(1).split(';'):
                d = dentro.search(trozo.strip())
                if d:
                    citadas.setdefault((norm(d.group(1)), d.group(2)), [f'{d.group(1)} ({d.group(2)})', set()])[1].add(os.path.basename(ruta))
    ruido = {'tabla', 'figura', 'ecuacion', 'capitulo', 'seccion', 'anexo', 'apendice', 'table', 'figure', 'en', 'de', 'desde', 'hasta'}
    fuera = {k: v for k, v in citadas.items() if k not in corpus and k[0] not in ruido}
    sin_citar = {k: v for k, v in corpus.items() if k not in citadas}
    print(f'Documentos leídos: {len(docs)}; fuentes en el corpus: {len(corpus)}; citas distintas detectadas: {len(citadas)}')
    print(f'\nCitadas en el texto y ausentes del corpus ({len(fuera)}): candidatas a revisar')
    for k in sorted(fuera):
        print(f'    {fuera[k][0]}: ' + ', '.join(sorted(fuera[k][1])))
    print(f'\nEn el corpus y sin cita detectada ({len(sin_citar)}):')
    for k in sorted(sin_citar):
        print(f'    {sin_citar[k]}')
    print('\nDetección heurística por apellido y año: una cita puede faltar por una grafía distinta, y normas o '
          'manuales citados fuera del corpus aparecerán como ausentes. La decisión es del autor.')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)
    q = s.add_parser('cifras')
    q.add_argument('--registro', required=True)
    q.add_argument('--rutas', nargs='+', required=True)
    q.set_defaults(fn=cmd_cifras)
    q = s.add_parser('pendientes')
    q.add_argument('--rutas', nargs='+', required=True)
    q.add_argument('--max', type=int, default=5, help='contextos mostrados por archivo')
    q.set_defaults(fn=cmd_pendientes)
    q = s.add_parser('nomenclatura')
    q.add_argument('--declarados', required=True)
    q.add_argument('--rutas', nargs='+', required=True)
    q.add_argument('--patron', default=r'\b[A-Z]{1,2}\d{1,2}\b')
    q.add_argument('--ignorar', default='Q1,Q2,Q3,Q4,A3,A4,A5,B5')
    q.set_defaults(fn=cmd_nomenclatura)
    q = s.add_parser('citas')
    q.add_argument('--corpus', required=True)
    q.add_argument('--hoja')
    q.add_argument('--rutas', nargs='+', required=True)
    q.set_defaults(fn=cmd_citas)
    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == '__main__':
    main()

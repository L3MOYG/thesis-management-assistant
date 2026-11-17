#!/usr/bin/env python3
"""Pruebas de regresión de las utilidades de Thesis Management Assistant.

Ejecuta cada utilidad con una entrada conocida y compara la salida con el valor esperado.
No necesita red. La prueba de la red de coocurrencia es opcional y requiere un archivo de
palabras clave con su tesauro y sus valores esperados. Sin las dependencias de
scripts/requirements.txt, los bloques que las usan se omiten y se informan como OMITIDA.

Uso
  python3 tests/pruebas_regresion.py
  python3 tests/pruebas_regresion.py --red-datos palabras_clave.csv --red-tesauro tesauro.csv \
      --red-esperado "17,42,3,0.353"
  python3 tests/pruebas_regresion.py --doi-en-vivo        (requiere red; consulta un DOI real)

Código de salida: 0 si todas pasan, 1 si alguna falla.
"""
import argparse
import csv
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Salida en UTF-8, como las utilidades: en Windows, la consola no siempre admite todos los caracteres.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(RAIZ, 'scripts')
RESULTADOS = []
OMITIDAS = []


def correr(script, *args):
    # Las utilidades escriben en UTF-8; se decodifica igual en todo sistema (en Windows la codificación local fallaba).
    r = subprocess.run([sys.executable, os.path.join(S, script), *map(str, args)], capture_output=True,
                       encoding='utf-8', errors='replace')
    return r.returncode, r.stdout + r.stderr


def prueba(nombre, condicion, detalle=''):
    RESULTADOS.append((nombre, bool(condicion)))
    print(('PASA   ' if condicion else 'FALLA  ') + nombre + (f'  [{detalle}]' if detalle else ''))


def faltan(*modulos):
    # Las utilidades se ejecutan con este mismo intérprete: lo que falta aquí, les falta a ellas.
    return [m for m in modulos if importlib.util.find_spec(m) is None]


def omitir(bloque, modulos):
    # Sin la dependencia, la utilidad sale antes de calcular: la prueba no diría nada de su lógica.
    OMITIDAS.append(bloque)
    print(f'OMITIDA  {bloque} (falta {", ".join(modulos)})')


def num(patron, texto):
    m = re.search(patron, texto)
    return float(m.group(1)) if m else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--red-datos')
    p.add_argument('--red-tesauro')
    p.add_argument('--red-esperado', help='nodos,enlaces,clústeres,modularidad')
    p.add_argument('--doi-en-vivo', action='store_true')
    a = p.parse_args()
    tmp = tempfile.mkdtemp(prefix='tesis_pruebas_')

    # 1. Potencia y grados de libertad
    falta = faltan('scipy')
    if falta:
        omitir('pruebas de potencia y grados de libertad', falta)
    else:
        _, o = correr('potencia.py', 'factorial', '--niveles', '2,3,3', '--replicas', 5, '--bloques', 5, '--f', 0.30)
        prueba('factorial 2x3x3, 5 réplicas en 5 bloques: gl error = 68', 'gl error = 68' in o)
        pot = num(r'\nA\s+1\s+([\d.]+)', o)
        prueba('potencia 0.80 para f = 0.30 con 1 gl', pot is not None and abs(pot - 0.80) < 0.005, f'{pot}')
        _, o = correr('potencia.py', 'anova', '--gl-num', 2, '--gl-error', 68, '--n-total', 90, '--f', 0.35)
        pot = num(r'Potencia = ([\d.]+)', o)
        prueba('potencia 0.84 para f = 0.35 con 2 gl', pot is not None and abs(pot - 0.84) < 0.005, f'{pot}')
        _, o = correr('potencia.py', 'factorial', '--niveles', '2,2', '--replicas', 5, '--bloques', 5, '--f', 0.70)
        prueba('factorial 2x2, 5 réplicas en 5 bloques: gl error = 12', 'gl error = 12' in o)
        for n, r in ((90, 0.207), (24, 0.404), (20, 0.444)):
            _, o = correr('potencia.py', 'correlacion', '--n', n)
            v = num(r'r crítico \([^)]*\) = ([\d.]+)', o)
            prueba(f'r crítico = {r} para n = {n}', v is not None and abs(v - r) < 0.0006, f'{v}')

    # 2. Matriz de corridas: reproducible con la semilla y con los gl esperados
    m1, m2 = os.path.join(tmp, 'm1.csv'), os.path.join(tmp, 'm2.csv')
    fact = 'G:g1,g2;D:d1,d2;E:e1,e2,e3;F:f1,f2'
    _, o = correr('matriz_corridas.py', '--factores', fact, '--replicas', 1, '--bloques', 0, '--semilla', 7, '--salida', m1)
    correr('matriz_corridas.py', '--factores', fact, '--replicas', 1, '--bloques', 0, '--semilla', 7, '--salida', m2)
    filas = [l for l in open(m1, encoding='utf-8-sig') if l.strip() and not l.startswith('#')]
    prueba('matriz 2x2x3x2 sin réplica: 24 corridas', len(filas) - 1 == 24, f'{len(filas) - 1}')
    prueba('matriz regenerable con la misma semilla', open(m1, 'rb').read() == open(m2, 'rb').read())

    # 3. Lenth sobre el factorial 2^4 sin réplica de la tasa de filtración (Montgomery, Design and
    #    Analysis of Experiments). Efectos de referencia: A 21.625, AC -18.125, AD 16.625.
    falta = faltan('numpy', 'scipy')
    if falta:
        omitir('pruebas de Lenth', falta)
    else:
        y = [45, 71, 48, 65, 68, 60, 80, 65, 43, 100, 45, 104, 75, 86, 70, 96]
        mont = os.path.join(tmp, 'mont.csv')
        with open(mont, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['A', 'B', 'C', 'D', 'y'])
            for i, v in enumerate(y):
                w.writerow([1 if i >> k & 1 else -1 for k in range(4)] + [v])
        _, o = correr('lenth.py', '--datos', mont, '--factores', 'A,B,C,D', '--respuesta', 'y')
        pse, me, sme = num(r'PSE = ([\d.]+)', o), num(r'[^S]ME = ([\d.]+)', o), num(r'SME = ([\d.]+)', o)
        ok = None not in (pse, me, sme) and abs(pse / 2 - 2.625) < 0.001 and abs(me / 2 - 6.75) < 0.01 and abs(sme / 2 - 13.70) < 0.01
        prueba('Lenth: PSE 2.625, ME 6.75 y SME 13.70 en unidades de efecto', ok, f'contrastes ortonormales: {pse}, {me}, {sme}')
        prueba('Lenth: 15 contrastes en un 2^4', 'contrastes: 15' in o)
        lin = [l for l in o.splitlines() if re.match(r'^A\s', l)]
        prueba('Lenth: efecto de A = 21.625', bool(lin) and '21.625' in lin[0], lin[0].strip() if lin else 'sin fila A')
        d24 = os.path.join(tmp, 'd24.csv')
        with open(m1, encoding='utf-8-sig') as f, open(d24, 'w', newline='') as g:
            filas = list(csv.DictReader(l for l in f if not l.startswith('#')))
            w = csv.writer(g)
            w.writerow(['G', 'D', 'E', 'F', 'Z1'])
            for i, r in enumerate(filas):
                w.writerow([r['G'], r['D'], r['E'], r['F'], 10 + (i * 37 % 11) + (3 if r['G'] == 'g2' else 0)])
        _, o = correr('lenth.py', '--datos', d24, '--factores', 'G,D,E,F', '--respuesta', 'Z1')
        prueba('Lenth: 23 contrastes ortogonales en un 2x2x3x2', 'contrastes: 23' in o)

    # 4. AHP. Sin numpy la utilidad sale con código 1 antes de leer la matriz: las pruebas de rechazo
    #    pasarían sin probar nada, por eso el bloque entero se omite.
    falta = faltan('numpy')
    if falta:
        omitir('pruebas de AHP', falta)
    else:
        _, o = correr('ahp.py', '--matriz', '1,3,5;1/3,1,2;1/5,1/2,1', '--nombres', 'a,b,c')
        pesos = [float(x) for x in re.findall(r'^\s+\w+\s+(0\.\d+)\s*$', o, re.M)]
        cr = num(r'CR = ([\d.]+)', o)
        ok = len(pesos) == 3 and all(abs(x - e) < 0.001 for x, e in zip(pesos, (0.648, 0.230, 0.122))) and cr is not None and abs(cr - 0.003) < 0.0006
        prueba('AHP: pesos 0.648, 0.230 y 0.122 con CR = 0.003', ok, f'{pesos}, CR {cr}')
        rc, _ = correr('ahp.py', '--matriz', '0,3,5;1/3,0,2;1/5,1/2,0', '--nombres', 'a,b,c')
        prueba('AHP rechaza una diagonal distinta de 1', rc != 0, f'código {rc}')
        rc, _ = correr('ahp.py', '--matriz', '1,3,5;1/2,1,2;1/5,1/2,1', '--nombres', 'a,b,c')
        prueba('AHP rechaza un par no recíproco', rc != 0, f'código {rc}')
        rc, o = correr('ahp.py', '--matriz', '1,9,1/9;1/9,1,9;9,1/9,1', '--nombres', 'a,b,c')
        prueba('AHP rechaza una matriz inconsistente (CR >= 0.10)', rc != 0, f'código {rc}')

    # 5. Validador de ecuaciones
    def errores(q):
        rc, o = correr('validar_ecuacion.py', 'validar', '--base', 'scopus', '--ecuacion', q)
        return rc, o
    rc, o = errores('TITLE-ABS-KEY ( "cover crop" AND maize ) AND OPENACCESS(1)')
    prueba('validador rechaza OPENACCESS(1)', rc != 0 and 'OPENACCESS' in o)
    rc, o = errores('TITLE-ABS-KEY ( "cover crop" and maize ) AND NOT TITLE-ABS-KEY ( greenhouse )')
    prueba('validador rechaza operadores en minúsculas', rc != 0 and 'mayúsculas' in o)
    rc, o = errores('TITLE-ABS-KEY ( “cover crop” AND maize ) AND NOT TITLE-ABS-KEY ( greenhouse )')
    prueba('validador rechaza comillas tipográficas', rc != 0 and 'omillas' in o)
    rc, o = errores('TITLE-ABS-KEY ( co* AND maize ) AND NOT TITLE-ABS-KEY ( greenhouse )')
    prueba('validador rechaza truncamiento de menos de tres letras', rc != 0 and 'runca' in o)
    rc, o = errores('TITLE-ABS-KEY ( ( a1 OR a2 ) AND ( bbb ) AND ( ccc ) AND ( ddd ) ) AND PUBYEAR > 2018 AND NOT TITLE-ABS-KEY ( greenhouse )')
    prueba('validador avisa con más de tres bloques AND', 'bloque' in o.lower() and ('viso' in o))
    rc, o = correr('validar_ecuacion.py', 'construir', '--id', 'E1', '--nucleo', 'cover crop*|green manure',
                   '--acoplamiento', 'maize|corn', '--resultado', 'yield', '--desde', 2019, '--tipos', 'ar,re',
                   '--acceso-abierto', '--excluir', 'greenhouse')
    prueba('constructor: Scopus con ACCESSTYPE ( oa ) y traducción a Web of Science', rc == 0 and 'ACCESSTYPE ( oa )' in o and 'TS=' in o)

    # 6. Deseabilidad: sin límites no hay cálculo
    falta = faltan('numpy', 'scipy')
    if falta:
        omitir('prueba de deseabilidad', falta)
    else:
        alt = os.path.join(tmp, 'alt.csv')
        open(alt, 'w').write('alternativa,RESPUESTA_1,RESPUESTA_2,RESPUESTA_3,RESPUESTA_4\nx,1,2,3,4\ny,2,3,4,5\n')
        rc, o = correr('deseabilidad.py', '--datos', alt, '--config', os.path.join(RAIZ, 'templates', 'config_deseabilidad.json'))
        prueba('deseabilidad se detiene si faltan límites o pesos', rc != 0 and 'no los inventa' in o)

    # 7. Verificador de DOI
    if a.doi_en_vivo:
        rc, o = correr('verificar_doi.py', '--doi', '10.1016/j.jobe.2023.108287')
        prueba('verificador de DOI en vivo: 1 verificado', 'verificados: 1' in o, o.strip().splitlines()[0] if o.strip() else '')
    rc, o = correr('verificar_doi.py', '--doi', 'no-es-un-doi')
    prueba('verificador de DOI: una cadena sin forma de DOI queda por confirmar', 'por confirmar' in o)

    # 7b. Panel de criterios de literatura
    crit = os.path.join(tmp, 'criterios.json')
    shutil.copy(os.path.join(RAIZ, 'templates', 'criterios_literatura.json'), crit)
    ver = os.path.join(tmp, 'verificacion.csv')
    cab = ('doi,estado,titulo,anio,revista,issn,primer_autor,n_autores,pais_primer_autor,tipo,idioma,volumen,numero,'
           'paginas,acceso_abierto,estado_oa,enlace_oa,licencia,citas,retractado,cuartil,fuente_verificacion,'
           'fecha_verificacion,nota')
    pc = 'por confirmar'
    filas = [
        ['10.1000/a1', 'verificado', 'A', '2022', 'R1', '1111-1111', 'Ana Pérez', '3', 'MX', 'article', 'en', '', '', '',
         'sí', 'gold', 'https://ejemplo.org/a1', '', '12', 'no', 'Q1 (índice)', 'OpenAlex', '2026-01-01', ''],
        ['10.1000/a2', 'verificado', 'B', '2012', 'R2', '2222-2222', 'Luis Okafor', '2', 'NG', 'article', 'en', '', '', '',
         'sí', 'gold', 'https://ejemplo.org/a2', '', '40', 'no', 'Q3 (índice)', 'OpenAlex', '2026-01-01', ''],
        ['10.1000/a3', 'verificado', 'C', '2023', 'R1', '1111-1111', 'A. Perez', '4', 'MX', 'review', 'en', '', '', '',
         'no', 'closed', '', '', '3', 'no', 'Q1 (índice)', 'OpenAlex', '2026-01-01', ''],
        ['10.1000/a4', 'verificado', 'D', '2024', 'Actas', pc, 'Mei Tanaka', '2', 'JP', 'proceedings-article', pc, '', '', '',
         pc, pc, '', '', pc, pc, pc, 'Crossref', '2026-01-01', ''],
        ['10.1000/a5', 'verificado', 'E', '2021', 'R3', '3333-3333', 'Joan Smith', '5', 'GB', 'article', 'en', '', '', '',
         'sí', 'gold', 'https://ejemplo.org/a5', '', '7', 'SÍ', 'Q2 (índice)', 'OpenAlex', '2026-01-01', ''],
        [f'10.1000/a6'] + [pc] * 10 + ['', '', '', pc, pc, '', '', pc, pc, pc, 'ninguna', '2026-01-01', 'sin conexión'],
    ]
    with open(ver, 'w', newline='', encoding='utf-8') as fh:
        fh.write(cab + '\n')
        csv.writer(fh).writerows(filas)
    rc, o = correr('criterios.py', 'aplicar', '--criterios', crit, '--verificacion', ver)
    prueba('criterios: sin filtros elegidos no aplica nada', rc == 2 and 'no supone criterios' in o, f'código {rc}')
    rc, o = correr('criterios.py', 'fijar', '--criterios', crit, '--cuartil', 'Q7')
    prueba('criterios: rechaza un valor fuera del panel', rc == 2, f'código {rc}')
    rc, o = correr('criterios.py', 'fijar', '--criterios', crit, '--codigos', 'A1 C2 V7 T1,2,3 I0 P1 R1 M0 U300')
    sel = json.load(open(crit, encoding='utf-8'))['filtros'] if rc == 0 else {}
    prueba('criterios: los códigos del panel guardan la selección',
           sel.get('acceso') == 'abierto' and sel.get('cuartil') == 'Q2' and sel.get('ventana') == 7
           and sel.get('tipos') == ['articulo', 'revision', 'ponencia'] and sel.get('idiomas') == 'sin_filtro'
           and sel.get('max_por_primer_autor') == 1 and sel.get('umbral_depuracion') == 300, f'código {rc}, {sel}')
    rc, o = correr('criterios.py', 'aplicar', '--criterios', crit, '--verificacion', ver, '--anio-referencia', 2026)
    prueba('criterios: selección estricta, 0 pasan, 4 casos abiertos y 2 por confirmar',
           rc == 0 and 'pasan: 0; casos abiertos: 4; por confirmar: 2' in o, o.strip().splitlines()[0] if o.strip() else '')
    rc, o = correr('criterios.py', 'fijar', '--criterios', crit, '--perfil', 'amplio')
    rc, o = correr('criterios.py', 'aplicar', '--criterios', crit, '--verificacion', ver, '--anio-referencia', 2026,
                   '--exentas-de-ventana')
    prueba('criterios: perfil amplio sin ventana, 2 pasan, 1 caso abierto y 3 por confirmar',
           rc == 0 and 'pasan: 2; casos abiertos: 1; por confirmar: 3' in o, o.strip().splitlines()[0] if o.strip() else '')

    # 7c. Tipo de ponencia de OpenAlex y salida en Windows con caracteres fuera de cp1252
    ver2 = os.path.join(tmp, 'verificacion_ponencia.csv')
    with open(ver2, 'w', newline='', encoding='utf-8') as fh:
        fh.write(cab + '\n')
        csv.writer(fh).writerow(['10.1000/p1', 'verificado', 'P', '2024', 'Actas', pc, 'Łukasz Nowak', '2', 'PL',
                                 'conference-paper', 'en', '', '', '', 'sí', 'gold', 'https://ejemplo.org/p1', '',
                                 '4', 'no', pc, 'OpenAlex', '2026-01-01', ''])
    crit2 = os.path.join(tmp, 'criterios_ponencia.json')
    shutil.copy(os.path.join(RAIZ, 'templates', 'criterios_literatura.json'), crit2)
    correr('criterios.py', 'fijar', '--criterios', crit2, '--codigos', 'A1 C0 V0 T1,3 I0 P0 R1 M0 U300')
    rc, o = correr('criterios.py', 'aplicar', '--criterios', crit2, '--verificacion', ver2)
    prueba('criterios: "conference-paper" de OpenAlex cuenta como ponencia', rc == 0 and 'pasan: 1;' in o,
           o.strip().splitlines()[0] if o.strip() else '')
    with open(ver2, newline='', encoding='utf-8') as fh:
        texto = fh.read().replace('conference-paper', 'conference-abstract')
    with open(ver2, 'w', newline='', encoding='utf-8') as fh:
        fh.write(texto)
    rc, o = correr('criterios.py', 'aplicar', '--criterios', crit2, '--verificacion', ver2)
    prueba('criterios: "conference-abstract" de OpenAlex cuenta como ponencia', rc == 0 and 'pasan: 1;' in o,
           o.strip().splitlines()[0] if o.strip() else '')
    salida_doi = os.path.join(tmp, 'doi_cp1252.csv')
    simulacion = (
        "import sys; sys.path.insert(0, sys.argv[1]); import verificar_doi as v\n"
        "w = {'doi': 'https://doi.org/10.1000/p1', 'title': 'Estudio con autor Łukasz', 'publication_year': 2024,\n"
        "     'type': 'article', 'language': 'pl', 'authorships': [{'author': {'display_name': 'Łukasz Nowak'}}],\n"
        "     'open_access': {'is_oa': False}, 'primary_location': {'source': {'display_name': 'Revista'}}}\n"
        "falso = lambda url, espera=30: ({'results': [w]}, None)\n"
        "original = v.verificar\n"
        "v.verificar = lambda d, m=None, c=None: original(d, m, c, pausa=0, obtener_fn=falso)\n"
        "sys.argv = ['verificar_doi.py', '--doi', '10.1000/p1', '--salida', sys.argv[2]]\n"
        "v.main()\n")
    entorno = dict(os.environ, PYTHONIOENCODING='cp1252')
    r = subprocess.run([sys.executable, '-c', simulacion, S, salida_doi], capture_output=True, env=entorno)
    escrito = os.path.exists(salida_doi) and 'Łukasz' in open(salida_doi, encoding='utf-8').read()
    prueba('verificador de DOI: un autor fuera de cp1252 no detiene la salida y el CSV se escribe',
           r.returncode == 0 and escrito, f'código {r.returncode}')

    # 8. Estructura, corpus, exportación y auditoría
    kit = os.path.join(tmp, 'kit')
    # Sin openpyxl no hay libro del corpus: el kit se crea con --sin-corpus y el libro se informa como omitido.
    sin_libro = ['--sin-corpus'] if faltan('openpyxl') else []
    rc, o = correr('crear_estructura.py', '--destino', kit, *sin_libro)
    esperado = ['00_Gobierno/Ficha_Proyecto.md', '00_Gobierno/Instrucciones_Project.md', '00_Gobierno/Manual_Usuario.md',
                '01_Literatura/Corpus_Fuentes.xlsx', '01_Literatura/criterios_literatura.json', '02_Planteamiento/Mapa_Vacios.md', '03_Metodologia/Plan_Analisis.md']
    if sin_libro:
        esperado.remove('01_Literatura/Corpus_Fuentes.xlsx')
    prueba('crear_estructura: kit completo' + (' salvo el libro del corpus' if sin_libro else ''),
           rc == 0 and all(os.path.exists(os.path.join(kit, e)) for e in esperado), f'código {rc}')
    ficha = os.path.join(kit, '00_Gobierno', 'Ficha_Proyecto.md')
    open(ficha, 'a', encoding='utf-8').write('\nMARCA DEL AUTOR\n')
    correr('crear_estructura.py', '--destino', kit, *sin_libro)
    prueba('crear_estructura no sobrescribe archivos existentes', 'MARCA DEL AUTOR' in open(ficha, encoding='utf-8').read())
    try:
        import openpyxl
        libro = os.path.join(kit, '01_Literatura', 'Corpus_Fuentes.xlsx')
        wb = openpyxl.load_workbook(libro)
        prueba('libro del corpus con sus cuatro hojas',
               wb.sheetnames == ['Corpus', 'Trazabilidad_busqueda', 'Obras_fundamentales', 'Casos_abiertos'], str(wb.sheetnames))
        ws = wb['Corpus']
        enc = [c.value for c in ws[4]]
        for j, v in (('ID', 'F01'), ('Autores', 'García, M.; López, R.'), ('Año', 2021), ('Título', 'Título de prueba'),
                     ('Revista', 'Revista A'), ('DOI', 'por confirmar'), ('Pilar', 'pilar 1')):
            ws.cell(5, enc.index(j) + 1, v)
        wb.save(libro)
        ris = os.path.join(tmp, 'c.ris')
        rc, o = correr('corpus_a_ris.py', '--corpus', libro, '--ris', ris)
        t = open(ris, encoding='utf-8').read() if os.path.exists(ris) else ''
        prueba('exportación a RIS sin inventar el DOI pendiente', 'AU  - García, M.' in t and 'DO  -' not in t and 'Sin DOI verificado' in o)
    except ImportError:
        omitir('pruebas del libro del corpus', ['openpyxl'])
    cap = os.path.join(kit, '05_Capitulos')
    open(os.path.join(cap, 'Cap3.md'), 'w', encoding='utf-8').write(
        'Se usaron 48 parcelas. El factor A y el factor C. Y1 y Y3. García y López (2021); Smith (2020). DOI por confirmar.\n')
    open(os.path.join(cap, 'Cap4.md'), 'w', encoding='utf-8').write('Se cosecharon 45 parcelas.\n')
    reg = os.path.join(tmp, 'cifras.csv')
    open(reg, 'w', encoding='utf-8').write('id,valor,unidad,descripcion,patron\nN,48,parcelas,Unidades,(\\d+)\\s+parcelas\n')
    rc, o = correr('auditar_documentos.py', 'cifras', '--registro', reg, '--rutas', cap)
    prueba('auditoría de cifras detecta la discrepancia', rc == 1 and 'dice 45' in o)
    rc, o = correr('auditar_documentos.py', 'nomenclatura', '--declarados', 'A,B,Y1', '--rutas', cap)
    prueba('auditoría de nomenclatura detecta C e Y3 sin declarar', re.search(r'\bC:', o) and 'Y3:' in o)
    rc, o = correr('auditar_documentos.py', 'pendientes', '--rutas', cap)
    prueba('auditoría de pendientes cuenta la marca', 'marcas "por confirmar": 1' in o)
    corp = os.path.join(tmp, 'corpus.csv')
    open(corp, 'w', encoding='utf-8').write('ID,Autores,Año,Título,DOI\nF01,"García, M.; López, R.",2021,T,10.1000/a\nF02,"Okafor, C.",2018,T,10.1000/b\n')
    rc, o = correr('auditar_documentos.py', 'citas', '--corpus', corp, '--rutas', cap)
    prueba('auditoría de citas: Smith fuera del corpus y Okafor sin citar', 'Smith (2020)' in o and 'Okafor (2018)' in o)

    # 9. Red de coocurrencia (opcional)
    if a.red_datos and a.red_esperado:
        n, e, c, q = a.red_esperado.split(',')
        args = ['--datos', a.red_datos, '--carpeta', os.path.join(tmp, 'red')] + (['--tesauro', a.red_tesauro] if a.red_tesauro else [])
        rc, o = correr('red_coocurrencia.py', *args)
        ok = f'ocurrencias): {n}\n' in o and f'Enlaces: {e}\n' in o and f'Clústeres: {c}\n' in o and f'Modularidad: {q}' in o
        prueba(f'red de coocurrencia: {n} nodos, {e} enlaces, {c} clústeres, modularidad {q}', ok)

    fallas = [n for n, ok in RESULTADOS if not ok]
    print(f'\n{len(RESULTADOS) - len(fallas)} de {len(RESULTADOS)} pruebas pasan.')
    if OMITIDAS:
        print(f'Bloques omitidos por dependencias: {len(OMITIDAS)}. Para la suite completa: '
              'pip install -r scripts/requirements.txt')
    return 1 if fallas else 0


if __name__ == '__main__':
    sys.exit(main())

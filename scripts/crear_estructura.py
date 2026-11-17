#!/usr/bin/env python3
"""Crea la estructura de carpetas del proyecto de tesis y coloca las plantillas del kit.

No sobrescribe nada: un archivo que ya existe se conserva y se informa. Puede ejecutarse
varias veces sin riesgo, por ejemplo para añadir una carpeta que faltaba.

Uso
  python3 crear_estructura.py --destino /ruta/Mi_Tesis
  python3 crear_estructura.py --destino /ruta/Mi_Tesis --titulo "Corpus de la tesis" --sin-corpus
  python3 crear_estructura.py --destino /ruta/Mi_Tesis --simular

  --destino     carpeta raíz del proyecto (se crea si no existe)
  --plantillas  carpeta de plantillas (por defecto, ../templates respecto de este script)
  --manual      ruta del manual de usuario (por defecto, ../docs/Manual_Usuario.md)
  --titulo      título del libro del corpus
  --sin-corpus  no crea 01_Literatura/Corpus_Fuentes.xlsx (requiere openpyxl)
  --simular     muestra lo que haría sin escribir nada

Solo usa la biblioteca estándar; el libro del corpus lo crea crear_corpus.py, que requiere openpyxl.
"""
import argparse
import os
import shutil
import subprocess
import sys

# Salida en UTF-8: en Windows, con la salida redirigida, un nombre como «Łukasz» detenía la utilidad.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))

CARPETAS = [
    ('00_Gobierno', 'Estado del proyecto: ficha, registro de decisiones, registro de cifras, plan de hilos, '
                    'instrucciones del Project y manual. Es lo primero que lee cada hilo.'),
    ('01_Literatura', 'Protocolo de búsqueda, libro del corpus, exportaciones de las bases y archivos para el '
                      'gestor de referencias.'),
    ('01_Literatura/PDF', 'Textos completos. Antecedentes: NN_PrimerAutor_Año.pdf, con NN igual al orden de aporte. '
                          'Obras fundamentales: F_PrimerAutor_Año.pdf.'),
    ('01_Literatura/exportaciones', 'Archivos exportados de las bases bibliográficas (CSV, RIS, BibTeX), sin editar.'),
    ('02_Planteamiento', 'Mapa de vacíos con su evidencia y cadena lógica: vacío, pregunta, hipótesis y objetivos.'),
    ('03_Metodologia', 'Diseño por población, plan de análisis, diccionario de variables y matrices de corridas.'),
    ('04_Datos', 'Datos del estudio.'),
    ('04_Datos/crudos', 'Datos tal como salieron del instrumento. No se editan nunca.'),
    ('04_Datos/procesados', 'Datos depurados, cada uno con el procedimiento que lo generó.'),
    ('04_Datos/resultados', 'Tablas, figuras y salidas de los análisis, regenerables desde los datos procesados.'),
    ('05_Capitulos', 'Capítulos de la tesis en el formato institucional. Un archivo canónico por capítulo.'),
    ('06_Productos_Derivados', 'Artículo de revisión y otros productos que nacen del corpus de la tesis.'),
    ('07_Defensa', 'Banco de preguntas del sínodo, puntos débiles y presentación.'),
]

# plantilla -> carpeta de destino
PLANTILLAS = {
    'Ficha_Proyecto.md': '00_Gobierno',
    'Registro_Decisiones.md': '00_Gobierno',
    'Registro_Cifras.csv': '00_Gobierno',
    'Plan_Hilos.md': '00_Gobierno',
    'Instrucciones_Project.md': '00_Gobierno',
    'Protocolo_Busqueda.md': '01_Literatura',
    'criterios_literatura.json': '01_Literatura',
    'Mapa_Vacios.md': '02_Planteamiento',
    'Cadena_Logica.md': '02_Planteamiento',
    'Plan_Analisis.md': '03_Metodologia',
    'Diccionario_Variables.csv': '03_Metodologia',
    'config_deseabilidad.json': '03_Metodologia',
}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--destino', required=True)
    p.add_argument('--plantillas', default=os.path.join(AQUI, '..', 'templates'))
    p.add_argument('--manual', default=os.path.join(AQUI, '..', 'docs', 'Manual_Usuario.md'))
    p.add_argument('--titulo', default='Corpus de fuentes de la tesis')
    p.add_argument('--sin-corpus', action='store_true')
    p.add_argument('--simular', action='store_true')
    a = p.parse_args()

    creados, conservados, faltantes = [], [], []
    raiz = os.path.abspath(a.destino)

    def hacer_carpeta(rel, descripcion):
        ruta = os.path.join(raiz, rel)
        if not os.path.isdir(ruta):
            creados.append(rel + '/')
            if not a.simular:
                os.makedirs(ruta, exist_ok=True)
        leeme = os.path.join(ruta, 'LEEME.md')
        if os.path.exists(leeme):
            conservados.append(os.path.join(rel, 'LEEME.md'))
        else:
            creados.append(os.path.join(rel, 'LEEME.md'))
            if not a.simular:
                with open(leeme, 'w', encoding='utf-8') as f:
                    f.write(f'# {rel}\n\n{descripcion}\n')

    def copiar(origen, rel_destino):
        destino = os.path.join(raiz, rel_destino)
        if not os.path.exists(origen):
            faltantes.append(origen)
        elif os.path.exists(destino):
            conservados.append(rel_destino)
        else:
            creados.append(rel_destino)
            if not a.simular:
                shutil.copyfile(origen, destino)

    for rel, descripcion in CARPETAS:
        hacer_carpeta(rel, descripcion)
    for nombre, carpeta in PLANTILLAS.items():
        copiar(os.path.join(a.plantillas, nombre), os.path.join(carpeta, nombre))
    copiar(a.manual, os.path.join('00_Gobierno', 'Manual_Usuario.md'))

    corpus_rel = os.path.join('01_Literatura', 'Corpus_Fuentes.xlsx')
    aviso_corpus = ''
    if not a.sin_corpus:
        if os.path.exists(os.path.join(raiz, corpus_rel)):
            conservados.append(corpus_rel)
        elif a.simular:
            creados.append(corpus_rel)
        else:
            r = subprocess.run([sys.executable, os.path.join(AQUI, 'crear_corpus.py'), '--salida',
                                os.path.join(raiz, corpus_rel), '--titulo', a.titulo], capture_output=True, text=True)
            if r.returncode == 0:
                creados.append(corpus_rel)
            else:
                aviso_corpus = (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else 'error sin mensaje'

    print(('SIMULACIÓN. ' if a.simular else '') + f'Raíz del proyecto: {raiz}')
    print(f'Creados ({len(creados)}):')
    for c in creados:
        print(f'    {c}')
    if conservados:
        print(f'Ya existían y se conservaron sin cambios ({len(conservados)}):')
        for c in conservados:
            print(f'    {c}')
    if faltantes:
        print(f'Plantillas no encontradas ({len(faltantes)}): el kit está incompleto.')
        for c in faltantes:
            print(f'    {c}')
    if aviso_corpus:
        print(f'No se creó el libro del corpus: {aviso_corpus}')
    return 1 if (faltantes or aviso_corpus) else 0


if __name__ == '__main__':
    sys.exit(main())

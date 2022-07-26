from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('edp.py', base=base, icon='icons/logo.ico')]

files = ['COD_EDP/','icons/','logo/', 'bancodedados.py', 'bancodedadosCAB.py', 'file_version_indo.txt']
excludes = ['tkinter', 'xml', 'html', 'future', 'email', 'json', 'http']
packs = ['wx',
         're',
         'sys',
         'time',
         'sqlite3',
         'datetime',
         'threading',
         'unicodecsv',
         'csv',
         'pubsub',
         'pandas',
         'numpy',
         'matplotlib',
         'drawnow',
         'serial',
         'shutil',
         'reportlab',
         'PyPDF2',
         'math']

setup(
    name = 'edp',
    version = '1.0.0',
    description = 'Ensaios Dinamicos para Pavimentacao',
    options = {'build_exe':{'include_files':files, "excludes":excludes, 'packages':packs}},
    executables = executables
)
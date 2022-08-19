from cx_Freeze import setup, Executable
import sys

base = None

executables = [Executable('edp.py', base=base, icon='icons/logo.ico')]

files = ['back/', 'banco/', 'COD_EDP/', 'front/', 'icons/','logo/', 'file_version_info.txt']
inc = ['os','wx','re','sys','time','sqlite3','datetime','threading','unicodecsv','csv','pubsub','pandas','numpy','matplotlib','drawnow','serial','shutil','reportlab','PyPDF2','math']
exc = ['tkinter']

setup(
    name = 'edp',
    version = '1.0.0',
    description = 'Ensaios Dinamicos para Pavimentacao',
    options = {'build_exe':{'include_files':files, 'packages': inc, 'excludes': exc}},
    executables = executables
)
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onedir',
    '--nowindow',
    '--name=edp',
    '--noconsole',
    '--version-file=file_version_info.txt',
    '--icon=icons/logo.ico',
    '--add-data= //back;.',
    '--add-data= //COD_EDP;.',
    '--add-data= //front;.',
    '--add-data= //icons;.',
    '--add-data= //logo;.',
    '--add-data= //bancodedados.py;.',
    '--add-data= //bancodedadosCAB.py;.',
    'edp.py'
])
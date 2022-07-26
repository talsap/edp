import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onedir',
    '--nowindow',
    '--name=edp',
    '--noconsole',
    '--version-file=file_version_info.txt',
    '--icon=logo.ico',
    '--add-data=back;back',
    '--add-data=COD_EDP;COD_EDP',
    '--add-data=front;front',
    '--add-data=icons;icons',
    '--add-data=logo;logo',
    '--add-data=bancodedados.py;.',
    '--add-data=bancodedadosCAB.py;.',
    'edp.py'
])
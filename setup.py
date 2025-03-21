from cx_Freeze import setup, Executable

build_options = {'packages': ['cv2'],
                #  'includes': ['pywinauto', 'pyuac', 'win32com', 'win32api'],
                 'build_exe': r'build\screenshot-video',
                 'include_files': [],
                 'include_msvcr': True}

base = 'console'

executables = [
    Executable('main.py', base=base, target_name='screenshot-video', copyright='Adan Einstein'),
]

setup(name='screenshot-video',
      version='1.0',
      description='Programa que tira uma quantidade pré-definida de prints de um video',
      options={'build_exe': build_options},
      executables=executables)
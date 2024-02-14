"""Модуль для изготовления скомпилированных .exe файлов"""
import subprocess
import shutil
import os


if os.path.exists('./exe_files'):
    shutil.rmtree('./exe_files')
os.makedirs('./exe_files')

for file in (
    'bot.exe',
    'restart.exe',
):
    subprocess.run(f'pyinstaller --onefile {file}', shell=True, check=True)

    FILE_EXE = file.replace('.py', '.exe')
    FILE_SPEC = file.replace('.py', '.spec')
    shutil.move(f'./dist/{FILE_EXE}', f'./{FILE_EXE}')
    os.remove(FILE_SPEC)

shutil.rmtree('build')
shutil.rmtree('dist')

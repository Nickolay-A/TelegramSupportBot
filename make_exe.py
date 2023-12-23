import subprocess
import shutil
import os


command = 'pyinstaller --onefile bot.py'
subprocess.run(command, shell=True)

shutil.move('./dist/bot.exe', 'bot.exe')
shutil.rmtree('build')
shutil.rmtree('dist')
os.remove('bot.spec')

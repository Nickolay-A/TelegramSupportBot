import subprocess
import shutil
import os


command = 'pyinstaller --onefile bot.py'
subprocess.run(command, shell=True)

command = 'pyinstaller --onefile restart.py'
subprocess.run(command, shell=True)

shutil.move('./dist/bot.exe', 'bot.exe')
os.remove('bot.spec')

shutil.move('./dist/restart.exe', 'restart.exe')
os.remove('restart.spec')

shutil.rmtree('build')
shutil.rmtree('dist')

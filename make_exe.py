import subprocess
import shutil
import os


command = 'pyinstaller --onefile bot.py'
subprocess.run(command, shell=True)

command = 'pyinstaller --onefile restart.py'
subprocess.run(command, shell=True)

shutil.move('./dist/bot.exe', 'bot.exe')
shutil.move('./dist/restart.exe', 'restart.exe')
shutil.rmtree('build')
shutil.rmtree('dist')
os.remove('bot.spec')
os.remove('restart.spec')

import os
import time
import subprocess
import psutil

def check_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def restart_process(process_path):
    subprocess.Popen(['cmd', '/c', 'start', '', process_path], shell=True)

process_name = 'bot.exe'
process_path = os.path.join(os.getcwd(), 'bot.exe')

while True:
    if not check_process_running(process_name):
        print(f"Процесс {process_name} завершился. Перезапуск...")
        restart_process(process_path)
    time.sleep(30)

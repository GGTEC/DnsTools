import eel
import webview
import threading
import sys,platform
import psutil
import time
import subprocess
from elevate import elevate
import ctypes

@eel.expose
def get_adapter_py():
    addrs = psutil.net_if_addrs()
    adapter = list(addrs.keys())[0]

    return adapter


def is_root():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

@eel.expose
def flush_dns():
    
    command = f'ipconfig /flushdns'
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
    if result.returncode == 0:
        eel.toast_notifc(F'O cache DNS foi limpo')
    else:
        eel.toast_notifc(f"Erro ao limpar o cache DNS")
    
    
@eel.expose
def change_dns(interface_name, dns):
    
    if dns == 'google': 
        
        dns_address_0 = '8.8.8.8'
        dns_address_1 = '8.4.4.8'
        
    elif dns == 'cloudflare':
        
        dns_address_0 = '1.1.1.1'
        dns_address_1 = '1.0.0.1'
        
    command = f'netsh interface ipv4 set dns name="{interface_name}" source=static addr={dns_address_0} validate=yes'
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
    if result.returncode == 0:
        eel.toast_notifc(F'As configurações de DNS para a conexão {interface_name} foram alteradas com sucesso')
    else:
        eel.toast_notifc(f"Erro ao alterar as configurações de DNS para a conexão {interface_name}: {result.stderr.decode()}")
    
    time.sleep(2)
    command_2 = f'netsh interface ipv4 add dns name="{interface_name}" addr={dns_address_1} index=2 validate=yes'
    result_2 = subprocess.run(command_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
    if result_2.returncode == 0:
        eel.toast_notifc(F'As configurações de DNS secundária para a conexão {interface_name} foram alteradas com sucesso')
    else:
        eel.toast_notifc(f"Erro ao alterar as configurações de DNS secundária para a conexão {interface_name}: {result.stderr.decode()}")
        

def start_eel():
    eel.init('web')
    
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start("index.html", size=(1200, 680), port=8000, mode=None, shutdown_delay=0.0)

def start_webview():

    
    window = webview.create_window("DNSTools", "http://localhost:8000/index.html", width=800, height=800, min_size=(800, 800))
    webview.start(debug=False)


def start_app():
    
    if is_root():
        eel_thread = threading.Thread(target=start_eel, args=(), daemon=True)
        eel_thread.start()
        
        start_webview()
    else:
        elevate()
        sys.exit(0)
    

    

start_app()
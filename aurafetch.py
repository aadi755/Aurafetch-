#!/usr/bin/env python3

import os
import platform
import socket
import subprocess
import time
import getpass
import shutil
import sys

# Auto-install/import required modules
def import_or_install(package, import_name=None):
    import importlib
    try:
        return importlib.import_module(import_name or package)
    except ImportError:
        subprocess.check_call([shutil.which("python3") or "python3", "-m", "pip", "install", "--quiet", package])
        return importlib.import_module(import_name or package)

psutil = import_or_install("psutil")
netifaces = import_or_install("netifaces")
requests = import_or_install("requests")
distro = import_or_install("distro")

# Handle --update
def handle_update():
    print("📦 Reinstalling AuraFetch...")
    try:
        subprocess.check_call("bash <(curl -s https://raw.githubusercontent.com/aadi755/Aurafetch-/main/install.sh)", shell=True, executable="/bin/bash")
        print("✅ Update complete!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Update failed: {e}")
    sys.exit(0)

def get_logo():
    os_id = distro.id().lower()
    logos = {
        "ubuntu": '''\033[1;35m
            .-/+oossssoo+/-.              
        `:+ssssssssssssssssss+:`          
      -+ssssssssssssssssssyyssss+-        
    .ossssssssssssssssssdMMMNysssso.      
   /ssssssssssshdmmNNmmyNMMMMhssssss/     
  +ssssssssshmydMMMMMMMNddddyssssssss+    
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/   
.ssssssssdMMMNhsssssssssshNMMMdssssssss.  
+sssshhhyNMMNyssssssssssssyNMMMysssssss+  
ossyNMMMNyMMhsssssssssssssshmmmhssssssso  
+sssshhhyNMMNyssssssssssssyNMMMysssssss+  
.ssssssssdMMMNhsssssssssshNMMMdssssssss.  
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/   
  +sssssssssdmydMMMMMMMMddddyssssssss+    
   /ssssssssssshdmNNNNmyNMMMMhssssss/     
    .ossssssssssssssssssdMMMNysssso.      
      -+sssssssssssssssssyyyssss+-        
        `:+ssssssssssssssssss+:`          
            .-/+oossssoo+/-               
\033[0m''',
        "debian": '''\033[1;31m
       _,met$$$$$gg.       
    ,g$$$$$$$$$$$$$$$P.    
  ,g$$P"     """Y$$.".      
,$$P'              `$$$.    
',$$P       ,ggs.     `$$b:  
`d$$'     ,$P"'   .    $$$   
 $$P      d$'     ,    $$P   
 $$:      $$.   -    ,d$$'   
 $$;      Y$b._   _,d$P'     
 Y$$.    `.`"Y$$$$P"'        
 `$$b      "-.__             
  `Y$$                          
   `Y$$.                        
     `$$b.                     
       `Y$$b.                  
          `"Y$b._             
              `"""
\033[0m''',
        "arch": '''\033[1;34m
                 -`                 
                .o+`                
               `ooo/                
              `+oooo:               
             `+oooooo:              
             -+oooooo+:             
           `/:-:++oooo+:            
          `/++++/+++++++:           
         `/++++++++++++++:          
        `/+++ooooooooooooo/`        
       ./ooosssso++osssssso+`       
      .oossssso-````/ossssss+`      
     -osssssso.      :ssssssso.     
    :osssssss/        osssso+++.    
   /ossssssss/        +ssssooo/-    
  `/ossssso+/:-        -:/+osssso+-  
 `+sso+:-`                 `.-/+oso: 
`++:.                           `-/+/
.`                                 `/
\033[0m''',
        "kali": '''\033[1;36m
     ____                      
    /\\  _`\\                     
    \\ \\ \\/\\_\\  ___     ___     
     \\ \\ \\/_/_ / __`\\ /' _ `\\   
      \\ \\ \\L\\ \\\\ \\L\\ \\\\ \\ \\/\\ \\  
       \\ \\____/ \\____/ \\_\\ \\_\\  
        \\/___/ \\/___/ \\/_/\\/_/ 
\033[0m'''
    }
    return logos.get(os_id, "\033[1;32mAuraFetch\033[0m")

def get_hostname():
    return socket.gethostname()

def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def get_shell():
    return os.environ.get("SHELL", "N/A")

def get_terminal():
    return os.environ.get("TERM", "N/A")

def get_cpu():
    cpu = platform.processor()
    if not cpu:
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.strip().split(":")[1].strip()
        except:
            return "Unknown CPU"
    return cpu

def get_cpu_temp():
    path = "/sys/class/thermal/thermal_zone0/temp"
    if os.path.exists(path):
        try:
            with open(path) as f:
                return f"{int(f.read()) / 1000:.1f}°C"
        except:
            pass
    return "N/A"

def get_gpu():
    if shutil.which("lspci"):
        try:
            output = subprocess.check_output("lspci | grep -i 'vga\\|3d'", shell=True).decode()
            return output.strip().split(":")[-1].strip()
        except:
            return "Error reading GPU"
    return "lspci not installed"

def get_ram():
    mem = psutil.virtual_memory()
    used = round(mem.used / 1e9, 2)
    total = round(mem.total / 1e9, 2)
    return f"{used} / {total} GB"

def get_disk():
    disk = psutil.disk_usage('/')
    used = disk.used // 2**30
    total = disk.total // 2**30
    return f"{used} / {total} GB"

def get_ip():
    local, public = "N/A", "N/A"
    try:
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        local = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    except:
        pass
    try:
        public = requests.get("https://api.ipify.org", timeout=3).text
    except:
        pass
    return local, public

def get_resolution():
    if os.environ.get("DISPLAY") and shutil.which("xdpyinfo"):
        try:
            res = subprocess.check_output("xdpyinfo | grep dimensions", shell=True).decode()
            return res.strip().split()[1]
        except:
            return "Unknown"
    return "No X / Headless"

def get_package_count():
    try:
        if shutil.which("dpkg"):
            output = subprocess.check_output("dpkg -l | grep '^ii' | wc -l", shell=True).decode()
        elif shutil.which("pacman"):
            output = subprocess.check_output("pacman -Q | wc -l", shell=True).decode()
        elif shutil.which("rpm"):
            output = subprocess.check_output("rpm -qa | wc -l", shell=True).decode()
        else:
            return "N/A"
        return output.strip()
    except:
        return "N/A"

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        handle_update()

    print(get_logo())
    print("🌌 \033[1m[ AuraFetch - System Info ]\033[0m 🌌\n")
    print(f"👤 User       : {getpass.getuser()}")
    print(f"💻 Hostname   : {get_hostname()}")
    print(f"🖥️ OS         : {distro.name()} {distro.version()}")
    print(f"🧬 Kernel     : {platform.release()}")
    print(f"⏱️ Uptime     : {get_uptime()}")
    print(f"🐚 Shell      : {get_shell()}")
    print(f"🪟 Terminal   : {get_terminal()}")
    print(f"🧠 CPU        : {get_cpu()}")
    print(f"🌡️ CPU Temp   : {get_cpu_temp()}")
    print(f"🎮 GPU        : {get_gpu()}")
    print(f"💾 RAM        : {get_ram()}")
    print(f"🗃️ Disk       : {get_disk()}")
    print(f"🖼️ Resolution : {get_resolution()}")
    print(f"📦 Packages   : {get_package_count()}")
    local, public = get_ip()
    print(f"🌐 Local IP   : {local}")
    print(f"🛰️ Public IP  : {public}")
    print("\n✅ Run again anytime with: \033[1maurafetch\033[0m")
    print("🔄 Update with: \033[1maurafetch --update\033[0m")

if __name__ == "__main__":
    main()

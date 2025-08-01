#!/usr/bin/env python3
import os, platform, psutil, socket, subprocess
import requests, netifaces, distro, time

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
    return platform.processor() or "Unknown CPU"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return f"{int(f.read()) / 1000:.1f}°C"
    except:
        return "N/A"

def get_gpu():
    try:
        output = subprocess.check_output("lspci | grep -i 'vga\\|3d'", shell=True).decode()
        return output.strip().split(":")[-1].strip()
    except:
        return "N/A"

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
    try:
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        local = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        public = requests.get("https://api.ipify.org").text
        return local, public
    except:
        return "N/A", "N/A"

def get_resolution():
    try:
        res = subprocess.check_output("xdpyinfo | grep dimensions", shell=True).decode()
        return res.strip().split()[1]
    except:
        return "N/A"

def get_package_count():
    try:
        if os.path.exists("/usr/bin/dpkg"):
            output = subprocess.check_output("dpkg -l | wc -l", shell=True).decode()
        elif os.path.exists("/usr/bin/pacman"):
            output = subprocess.check_output("pacman -Q | wc -l", shell=True).decode()
        elif os.path.exists("/usr/bin/rpm"):
            output = subprocess.check_output("rpm -qa | wc -l", shell=True).decode()
        else:
            return "N/A"
        return output.strip()
    except:
        return "N/A"

def main():
    print("🌌 [ AuraFetch - Ultimate System Info ] 🌌\n")
    print(f"User       : {os.getlogin()}")
    print(f"Hostname   : {get_hostname()}")
    print(f"OS         : {distro.name()} {distro.version()}")
    print(f"Kernel     : {platform.release()}")
    print(f"Uptime     : {get_uptime()}")
    print(f"Shell      : {get_shell()}")
    print(f"Terminal   : {get_terminal()}")
    print(f"CPU        : {get_cpu()}")
    print(f"CPU Temp   : {get_cpu_temp()}")
    print(f"GPU        : {get_gpu()}")
    print(f"RAM        : {get_ram()}")
    print(f"Disk       : {get_disk()}")
    print(f"Resolution : {get_resolution()}")
    print(f"Packages   : {get_package_count()}")
    local, public = get_ip()
    print(f"Local IP   : {local}")
    print(f"Public IP  : {public}")

if __name__ == "__main__":
    main()

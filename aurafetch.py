#!/usr/bin/env python3

import os, platform, socket, subprocess, time
import getpass
from datetime import datetime

# Optional imports with fallback
try:
    import psutil
except ImportError:
    psutil = None

try:
    import netifaces
except ImportError:
    netifaces = None

try:
    import requests
except ImportError:
    requests = None

try:
    import distro
except ImportError:
    distro = None

def get_hostname():
    return socket.gethostname()

def get_uptime

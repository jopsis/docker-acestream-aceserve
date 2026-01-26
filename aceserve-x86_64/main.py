import os
import sys
import threading
import traceback
import re
import platform
from datetime import datetime
from functools import wraps

# -----------------------------
# Configuración inicial
# -----------------------------
OUTPUT_CONSOLE = True
DEBUG_MODULE = True
GOT_RCP_HOST = True

# -----------------------------
# Simulación de app_bridge.Android
# -----------------------------
class Android:
    def getAceStreamHome(self, *args, **kwargs):
        return "/dev/shm"

    def makeToast(self, msg, *args, **kwargs):
        print(msg)

    def getDisplayLanguage(self, *args, **kwargs):
        return 'en'

    def getRAMSize(self, *args, **kwargs):
        return 1024 * 1024 * 1024

    def getMaxMemory(self, *args, **kwargs):
        return 1024 * 1024 * 1024

    def getDeviceId(self, *args, **kwargs):
        return 'd3efefe5-4ce4-345b-adb6-adfa3ba92eab'

    def getAppId(self, *args, **kwargs):
        return 'd3efefe5-4ce4-345b-adb6-adfa3ba92eab'

    def getDeviceManufacturer(self, *args, **kwargs):
        return 'Samsung'

    def getDeviceModel(self, *args, **kwargs):
        return 'Galaxy S3'

    def onSettingsUpdated(self, *args, **kwargs):
        return

    def onEvent(self, *args, **kwargs):
        return

    def getAppVersionCode(self, *args, **kwargs):
        return "6.6"

    # -----------------------------
    # Detectar arquitectura real
    # -----------------------------
    def getArch(self, *args, **kwargs):
        arch = platform.machine()
        if arch == 'aarch64':
            return 'arm64-v8a'
        elif arch.startswith('arm'):
            return 'armv7h'
        else:
            return arch

    def getLocale(self, *args, **kwargs):
        return "en-US"

    def isAndroidTv(self, *args, **kwargs):
        return False

    def hasBrowser(self, *args, **kwargs):
        return False

    def hasWebView(self, *args, **kwargs):
        return False

    def getMemoryClass(self, *args, **kwargs):
        return 64

    def publishFileReceiverState(self, *args, **kwargs):
        return

    def _fake_rpc(self, method, *args):
        print(method, *args)
        if hasattr(Android, method):
            return getattr(Android, method)(self, *args)
        raise Exception("Unknown method: %s" % method)

# Instancia de droid simulada
droid = Android()

# -----------------------------
# Directorio home
# -----------------------------
home_dir = droid.getAceStreamHome()

if not OUTPUT_CONSOLE:
    try:
        sys.stderr = open(os.path.join(home_dir, "acestream_std.log"), 'w')
        sys.stdout = sys.stderr
    except:
        pass

# -----------------------------
# Función de log
# -----------------------------
def log(msg):
    try:
        line = '{}|{}|bootstrap|{}'.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            threading.currentThread().name,
            msg
        )
        with open(os.path.join(home_dir, 'acestream.log'), 'a') as f:
            f.write(line + '\n')
        print(line)
    except:
        pass

log('Starting AceStream Service on architecture: {}'.format(droid.getArch()))

# -----------------------------
# DNS override siempre activo.
# Si existe una línea "# ExtServers: [x.x.x.x ...]" en /etc/resolv.conf, la usa.
# Si no, hace fallback a los nameserver normales.
# Logea método usado.
# -----------------------------
import dns.resolver
from dnsproxyd import dns_daemon

nameservers = []
found_extservers = False
with open('/etc/resolv.conf', 'r') as f:
    for line in f:
        ext_match = re.search(r'# ExtServers: \[(.*?)\]', line)
        if ext_match:
            ns_list = ext_match.group(1).split()
            nameservers.extend(ns_list)
            found_extservers = True
if not nameservers:
    with open('/etc/resolv.conf', 'r') as f:
        for line in f:
            match = re.match(r'nameserver\s+(\S+)', line)
            if match:
                nameservers.append(match.group(1))

if found_extservers:
    log(f'Override DNS usando ExtServers del comentario: {nameservers}')
else:
    log(f'Override DNS usando los nameserver estándar: {nameservers}')

RESOLVER = dns.resolver.Resolver()
RESOLVER.nameservers = nameservers
dns.resolver.override_system_resolver(RESOLVER)
dns_daemon(RESOLVER)

import aceserve
aceserve.main()


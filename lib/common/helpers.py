"""
This file contains miscellaneous functions used by the framework
"""

import ipaddress
import os
import random
import re
import string
import sys
import importlib.util


# Try to find and import the settings.py config file
try:
    sys.path.append("/etc/veil/")
    import settings
except ImportError:
    print(f"\n [!] ERROR #1-3: Can't import /etc/veil/settings.py.   Run: {os.path.abspath('./config/update-config.py')}\n")
    sys.exit()

# See if ./config/setup.sh has been executed
if not os.path.exists(settings.GOLANG_PATH):
    print(f"\n [!] ERROR #2-3: Can't find Go ({settings.GOLANG_PATH}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.PYINSTALLER_PATH):
    print(f"\n [!] ERROR #2-3: Can't find PyInstaller ({settings.PYINSTALLER_PATH}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.METASPLOIT_PATH):
    print(f"\n [!] ERROR #2-3: Can't find the Metasploit Framework ({settings.METASPLOIT_PATH}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.WINEPREFIX):
    print(f"\n [!] ERROR #2-3: Can't find the WINE profile ({settings.WINEPREFIX}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.WINEPREFIX + "/drive_c/Python34/python.exe"):
    print(f"\n [!] ERROR #2-3: Can't find the WINE profile for Python v3.4 ({settings.WINEPREFIX + '/drive_c/Python34/python.exe'}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.WINEPREFIX + "/drive_c/Ruby187/bin/ruby.exe"):
    print(f"\n [!] ERROR #2-3: Can't find the WINE profile for Ruby v1.8.7 ({settings.WINEPREFIX + '/drive_c/Ruby187/bin/ruby.exe'}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()

if not os.path.exists(settings.WINEPREFIX + "/drive_c/Program Files/AutoIt3/Aut2Exe/Aut2exe.exe"):
    print(f"\n [!] ERROR #2-3: Can't find the WINE profile for AuotIT v3 ({settings.WINEPREFIX + '/drive_c/Program Files/AutoIt3/Aut2Exe/Aut2exe.exe'}).   Run: {os.path.abspath('./config/setup.sh')} --force --silent\n")
    sys.exit()


def clean_payloads():
    print(f"\n [*] Cleaning {settings.PAYLOAD_SOURCE_PATH}")
    os.system(f'rm -f {settings.PAYLOAD_SOURCE_PATH}/*.*')

    print(f" [*] Cleaning {settings.PAYLOAD_COMPILED_PATH}")
    os.system(f'rm -f {settings.PAYLOAD_COMPILED_PATH}/*.exe')

    print(f" [*] Cleaning {settings.HANDLER_PATH}")
    os.system(f'rm -f {settings.HANDLER_PATH}/*.rc')

    print(f" [*] Cleaning {settings.HASH_LIST}")
    os.system(f'rm -f {settings.HASH_LIST}')
    os.system(f'touch {settings.HASH_LIST}')

    print(" [*] Cleaning ./tools/vt-notify/results.log")
    os.system('rm -f ./tools/vt-notify/results.log')
    return


def color(string, status=True, warning=False, bold=True, yellow=False):
    """
    Change text color for the linux terminal, defaults to green.

    Set "warning=True" for red.
    """
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if yellow:
        attr.append('33')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def check_int(incoming_int):
    # This checks if the variable is an integer and returns a boolean
    try:
        int(incoming_int)
        return True
    except ValueError:
        return False

#################################################################
#
# Randomization/obfuscation methods.
#
#################################################################


def randomString(length=-1):
    """
    Returns a random string of "length" characters.
    If no length is specified, resulting string is in between 6 and 15 characters.
    """
    if length == -1:
        length = random.randrange(6, 16)
    random_string = ''.join(random.choice(string.ascii_letters) for x in range(length))
    return random_string.encode('utf-8')


def randomKey(b=32):
    """
    Returns a random string/key of "b" characters in length, defaults to 32
    """
    return ''.join(random.choice(string.ascii_letters + string.digits + "{}!@#$^&()*&[]|,./?") for x in range(b)).encode('utf-8')


def randomNumbers(b=7):
    """
    Returns a random string/key of "b" characters in length, defaults to 7
    """
    random_number = int(''.join(random.choice(string.digits) for x in range(b))) + 100000

    if random_number < 1000000:
        random_number = random_number + 1000000

    return random_number


def validate_hostname(hostname):
    """
    Try to validate the passed host name, return True or False.
    """
    if len(hostname) > 255:
        return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def validate_ip(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def validate_port(port_number):
    try:
        if 0 < int(port_number) < 65535:
            return True
        else:
            return False
    except ValueError:
        return False


def load_module(module_path):
    """
    Takes module path, return module object
    """
    spec = importlib.util.spec_from_file_location(module_path, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

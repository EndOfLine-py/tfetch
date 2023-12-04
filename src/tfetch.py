import os
import distro
import wmctrl
import platform
import re
import subprocess
import json
import time

def termRun(command, arguments):
    output = subprocess.run([command, arguments],text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.stdout

def getOS(architecture=False, removeLinux=False):
    os = distro.linux_distribution()[0]
    if removeLinux:
        os = re.sub('linux', '', os, flags=re.IGNORECASE)
    os = os.rstrip()
    if architecture:
        os += ' ' + platform.machine()
    os = os.lower()
    return os

def getWM():
    try:
        return wmctrl.os.environ.get('DESKTOP_SESSION').split("/")[-1].lower()
    except:
        pass
    try:
        return wmctrl.os.environ.get('XDG_SESSION_DESKTOP')
    except:
        return None

def getKernel(fullName=True):
    kernel = platform.release()
    if not fullName:
        kernel = kernel.split('-')[0]
    return kernel

def getPackages(displayPackageManager=False):
    try:
        packages = termRun('pacman', '-Qq')
        string = str(len(packages.split('\n')))
        if displayPackageManager:
            string += ' (pacman)'
        return string
    except:
        return None


def checkColors(num: int):
    if num < 7:
        return True
    if num > 7 :
        return False

def transColor(num : int):
    if num == 0:
        return '\033[30m'
    elif num == 1:
        return '\033[31m'
    elif num == 2:
        return '\033[32m'
    elif num == 3:
        return '\033[33m'
    elif num == 4:
        return '\033[34m'
    elif num == 5:
        return '\033[35m'
    elif num == 6:
        return '\033[36m'
    elif num == 7:
        return '\033[37m'
    else:
        return ''



def main(color1:str, color2:str):
    bold = "\u001b[1m"
    reset = "\033[0m"
    linuxos = getOS(removeLinux=True)
    wm = getWM()
    de = subprocess.Popen(['wmctrl -m | grep "Name"'], stdout=subprocess.PIPE,shell=True).communicate()[0]
    de = str(de, "utf-8").strip("\n").strip("Name:").replace(" ","").lower()
    kernel = getKernel(fullName=False)
    pkgs = getPackages(displayPackageManager=False)
    shell = wmctrl.getoutput("echo $SHELL").replace("/","").replace("bin","")

    base = f""".
{reset}├─ {bold}{color1}distro{reset}
{reset}│  ├─ {color2}{linuxos}{reset}
{reset}│  └─ {color2}{kernel}{reset}
{reset}├─ {bold}{color1}pacman{reset}
{reset}│  └─ {bold}{color2}packages{reset}
{reset}│     └─ {color2}{pkgs}{reset}
{reset}├─ {bold}{color1}env{reset}
{reset}│  ├─ {bold}{color2}de{reset}
{reset}│  │  └─ {color2}{de}{reset}
{reset}│  └─ {bold}{color2}wm{reset}
{reset}│     └─ {color2}{wm}{reset}
{reset}└─ {bold}{color1}shell{reset}
{reset}   └─ {color2}{shell}{reset}"""

    print(base)



if __name__ == '__main__':
    default = None
    try:
        with open('./config.json') as f:
            data = json.load(f)
    except:
        input("Missing Config File")
        exit()

    # Check the data
    
    color1check = checkColors(data['color1'])
    color2check = checkColors(data['color2'])

    if color1check == True:
        color1 = transColor(data['color1'])
    else:
        color1 = ""

    if color2check == True:
        color2 = transColor(data['color2'])
    else:
        color2 = ""

    if color1check == True and color2check == True:
        main(color1, color2)
    else:
        print(" -> Using Default Config.")
        time.sleep(1)
        os.system("clear")
        main("\033[31m","\033[33m")

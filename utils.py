#/usr/bin/python3

import colorama
import math
import shutil
import subprocess
import time

DEBUG = False

if not shutil.which('espeak'):
    raise RuntimeError("espeak is not installed. Please install espeak to continue")

colorama.init()

#fix annotation?
def speak(text : str , wait = True) -> None:
    if text is None: return
    f = subprocess.call if wait else subprocess.Popen
    f('espeak -v en-gb \"' + text + '\"', shell=True, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def sqrt_floor(i : int) -> int:
    return math.floor(math.sqrt(i))

def countdown(n : int, incremental = None) -> None:
    if n <= 1: return
    start = n
    if incremental is None: incremental = n>30
    print(colorama.Fore.RED, end="")
    while n > 0:
        print(str(n) + "...", end="", flush=True)
        if n < 4: speak(str(n), wait=False)
        elif incremental:
            if n != start and not n % 15:
                speak(str(n) + " seconds remaining", wait=False)
        if not DEBUG: time.sleep(1)
        n -= 1
    print("0" + colorama.Fore.RESET)

def prettyTime(time : int) -> str:
    """takes a time, in seconds, and formats it for display"""
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    s = round(s, 2)
    if h: return "%s hour(s), %s minute(s), %s second(s)" % (int(h),int(m),s)
    else: return "%s minute(s), %s second(s)" % (int(m),s)

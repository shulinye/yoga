#/usr/bin/python3

import math
import shutil
import subprocess
import time

DEBUG = False

if not shutil.which('espeak'):
    raise RuntimeError("espeak is not installed. Please install espeak to continue")

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

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
    print(color.RED, end="")
    while n > 0:
        print(str(n) + "...", end="", flush=True)
        if n < 4: speak(str(n), wait=False)
        elif incremental:
            if n != start and not n % 15:
                speak(str(n) + " seconds remaining", wait=False)
        if not DEBUG: time.sleep(1)
        n -= 1
    print("0" + color.END)

def prettyTime(time : int) -> str:
    """takes a time, in seconds, and formats it for display"""
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    s = round(s, 2)
    if h: return "%s hour(s), %s minute(s), %s second(s)" % (h,m,s)
    else: return "%s minute(s), %s second(s)" % (m,s)

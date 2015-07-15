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


def speak(text : str ):
    subprocess.call('espeak -v en-gb \"' + text + '\"', shell=True)

def sqrt_floor(i : int) -> int:
    return math.floor(math.sqrt(i))

def countdown(n : int) -> None:
    if n <= 1: return None
    incremental = n>30
    print(color.RED, end="")
    while n > 0:
        print(str(n) + "...", end="", flush=True)
        if n < 4:
            speak(str(n))
        elif incremental:
            if n == 30:
                speak("30 seconds remaining")
            if n == 15:
                speak("15 seconds remaining")
        if not DEBUG: time.sleep(1)
        n -= 1
    print("0" + color.END)

def prettyTime(time : int) -> str:
    """takes a time, in seconds, and formats it for display"""
    h = time//3600
    m = time//60 % 60
    s = round(time % 60,2)
    if h: return "%s hour(s), %s minute(s), %s second(s)" % (h,m,s)
    else: return "%s minute(s), %s second(s)" % (m,s)

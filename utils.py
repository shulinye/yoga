#!/usr/bin/env python3

import colorama
import math
import shutil
import subprocess
import textwrap
import time

DEBUG = False

if not shutil.which('espeak'):
    raise RuntimeError("espeak is not installed. Please install espeak to continue")

colorama.init()
wrapper = textwrap.TextWrapper(width=120)

#fix annotation?
def speak(text : str , wait = True) -> None:
    if text is None: return
    f = subprocess.call if wait else subprocess.Popen
    return f('espeak -v en-gb \"' + text + '\"', shell=True, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def tee(text : str, f, say=None):
    """Sends a string to stdout, a file (f) and speak"""
    print(text)
    if say is None: speak(text)
    else: speak(say)
    if f: f.write(text + '\n\n')

def sqrt_floor(i : int) -> int:
    return math.floor(math.sqrt(i))

def countdown(n : int, incremental = None, step = 15) -> None:
    if n <= 1: return
    try:
        start = n
        position = 0
        if incremental is None: incremental = n>30
        print(colorama.Fore.RED, end="")
        while n > 0:
            print(str(n) + "...", end="", flush=True)
            position += len(str(n)) + 3
            if position > 120:
                print()
                position = 0
            if n < 4:
                speak(str(n), wait=False)
            elif incremental:
                if n != start and not n % step:
                    speak(str(n) + " seconds remaining", wait=False)
            if not DEBUG: time.sleep(1)
            n -= 1
    finally:
        print("0" + colorama.Style.RESET_ALL)

def prettyTime(time : int) -> str:
    """takes a time, in seconds, and formats it for display"""
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    s = round(s, 2)
    if h: return "%s hour(s), %s minute(s), %s second(s)" % (int(h),int(m),s)
    else: return "%s minute(s), %s second(s)" % (int(m),s)

if __name__ == "__main__":
    import sys
    countdown(int(sys.argv[1]))

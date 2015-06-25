#/usr/bin/python3

import subprocess
import sys
import time

DEBUG = False

def speak(text):
    subprocess.call('espeak -v en-gb \"' + text + '\"', shell=True)

def countdown(n, *args, **kwargs):
    incremental = n>30
    while n > 0:
        sys.stdout.write(str(n) + "...")
        sys.stdout.flush()
        if n < 4:
            speak(str(n))
        elif incremental:
            if n == 30:
                speak("30 seconds remaining")
            if n == 15:
                speak("15 seconds remaining")
        if not DEBUG: time.sleep(1)
        n -= 1
    sys.stdout.write("0\n")
    sys.stdout.flush()


def prettyTime(time):
    """takes a time, in seconds, and formats it for display"""
    h = time//3600
    m = time//60 % 60
    s = time % 60
    if h: return "%s hour(s), %s minute(s), %s second(s)" % (h,m,s)
    else: return "%s minute(s), %s second(s)" % (m,s)
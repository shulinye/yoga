#!/usr/bin/python3

"""An attempt to make a command-line based yoga program. NOTE: uses espeak for audio"""

import subprocess
import time
import sys

def speak(text):
    subprocess.call('espeak -v en-gb \"' + text +'\"', shell=True)

def countdown(n, *args):
    while n > 0:
        sys.stdout.write(str(n) + "...")
        sys.stdout.flush()
        if n <4: speak(str(n))
        time.sleep(1)
        n -= 1
    sys.stdout.write("0\n")
    sys.stdout.flush()

class Move(object):
    def __init__(self, title, side, audio, time, *args, **kwargs):
        self.title=title
        self.side=side
        self.audio=audio
        self.time=time
        self.nextMove = set(args)
        self.kwargs = kwargs
    def update(self, **kwargs):
        self.kwargs.update(kwargs)
    def addOtherSide(self, otherside):
        self.otherside = otherside
    def addMove(self, *args):
        self.nextMove.update(args)
    def play(self, **kwargs):
        print(self.title)
        if "verbose" in kwargs and kwargs["verbose"] and "verbose" in self.kwargs:
            speak(self.kwargs["verbose"])
        else:
            speak(self.audio)
        countdown(self.time)

def twoSides(title, audio, time, *args, **kwargs):
    """Hey, you have two legs."""
    R = Move(title+ ", Right", "Right", audio + ", Right Side", time, *args, **kwargs)
    L = Move(title+ ", Left", "Left", audio + ", Left Side", time, *args, **kwargs)
    R.addOtherSide(L)
    L.addOtherSide(R)
    return (R,L)

vinyasa = Move("Vinayasa", None, "Vinyasa", 5)
threeleggeddog = twoSides("Three Legged Dog", "Three Legged Dog", 10)
warrior1 = twoSides("Warrior 1", "Warrior One", 10)

if __name__== "__main__":
    for i in warrior1:
        i.play()

#!/usr/bin/python3

"""An attempt to make a command-line based yoga program. NOTE: uses espeak for audio"""

import subprocess
import time
import sys
import datetime
import random

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
        if "nextMove" in kwargs:
            nextMove = kwargs["nextMove"]
        else:
            nextMove = random.choice(tuple(self.nextMove))
        print("Next Move: " + nextMove.title)
        speak(self.audio)
        countdown(self.time)
        return nextMove
    def __repr__(self):
        return "Move(%s)" % self.title
    def __str__(self):
        return self.title
    def __hash__(self):
        return hash(self.title)

def twoSides(title, audio, time, *args, **kwargs):
    """Hey, you have two legs."""
    R = Move(title+ ", Right", "Right", audio % "Right Side", time, *args, **kwargs)
    L = Move(title+ ", Left", "Left", audio % "Left Side", time, *args, **kwargs)
    R.addOtherSide(L)
    L.addOtherSide(R)
    return (R,L)

#Begin list of moves

catCow = Move("Cat Cow", None, "Cat Cow", 10)
table = Move("Table Pose", None, "Table Pose", 5, catCow)
vinyasa = Move("Vinayasa", None, "Vinyasa", 5)
child = Move("Child's Pose", None, "Child's Pose", 5, table)
threeleggeddog = twoSides("Three Legged Dog", "Three Legged Dog, %s", 10)
downwardsDog = Move("Downwards Dog", None, "Downwards Dog", 5, *threeleggeddog)
warrior1 = twoSides("Warrior 1", "Warrior One, %s", 10, vinyasa)
warrior2 = twoSides("Warrior 2", "Warrior Two, %s", 10, vinyasa)
warrior3 = twoSides("Warrior 3", "Warrior Three, %s", 10, vinyasa)
chairTwist = twoSides("Chair Twist", "Twist to the %s", 15)
chair = Move("Chair Pose", None, "Chair Pose", 15, *chairTwist)

#Begin linking moves to each other
vinyasa.addMove(downwardsDog)

if __name__== "__main__":
    start = datetime.datetime.now()
    speak("Beginning in")
    countdown(3)
    nextPose = child.play()
    nextPose.play()


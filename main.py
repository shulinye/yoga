#!/usr/bin/python3

"""An attempt to make a command-line based yoga program. NOTE: uses espeak for audio"""

import subprocess
import time
import sys
import datetime
import random

debug=True

def speak(text):
    subprocess.call('espeak -v en-gb \"' + text +'\"', shell=True)

def countdown(n, *args, **kwargs):
    while n > 0:
        sys.stdout.write(str(n) + "...")
        sys.stdout.flush()
        if n <4:
            speak(str(n))
            if not debug:time.sleep(1)
        else:
            if not debug:time.sleep(1)
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
        """Tells me which pose I'm supposed to do and how I'm supposed to do it. Also figures out next pose."""
        print("")
        print(self.title)
        if "nextMove" in kwargs:
            nextMove = kwargs["nextMove"]
        else:
            nextMove = random.choice(tuple(self.nextMove))
        print("Next Move: " + nextMove.title)
        speak(self.audio + ". " + str(self.time) + " seconds")
        if "bind" in self.kwargs and self.kwargs["bind"]: speak("Bind if you want to")
        countdown(self.time)
        if "bind" in self.kwargs and self.kwargs["bind"]: speak("Release bind")
        return nextMove
    def __repr__(self):
        return "Move(%s)" % self.title
    def __str__(self):
        return self.title
    def __hash__(self):
        return hash(self.title)

def twoSides(title, audio, time, *args, **kwargs):
    """Hey, you have two legs."""
    if "%s" in audio:
        R = Move(title+ ", Right", "Right", audio % "Right", time, *args, **kwargs)
        L = Move(title+ ", Left", "Left", audio % "Left", time, *args, **kwargs)
    else:
        R = Move(title+ ", Right", "Right", audio, time, *args, **kwargs)
        L = Move(title+ ", Left", "Left", audio, time, *args, **kwargs)
    R.addOtherSide(L)
    L.addOtherSide(R)
    return (R,L)

def doubleAdd(move, *args, inverted=False):
    if inverted:
        for i in args:
            move[0].addMove(i[1])
            move[1].addMove(i[0])
    else:
        for i in args:
            move[0].addMove(i[0])
            move[1].addMove(i[1])
#Begin list of moves

balancingTable = twoSides("Balancing Table", "When you are ready, extend the opposite arm", 10)
balancingTableLegOnly = twoSides("Balancing Table, Leg Only", "Extend %s leg behind you", 5)
catCow = Move("Cat Cow", None, "Cat Cow", 10, *balancingTableLegOnly)
table = Move("Table Pose", None, "Table Pose", 5, catCow, *balancingTableLegOnly)
vinyasa = Move("Vinayasa", None, "Vinyasa", 5)
staff = Move("Staff Pose", None, "Staff Pose",10, vinyasa)
child = Move("Child's Pose", None, "Child's Pose", 5, table)
lowLunge = twoSides("Low Lunge", "Bring your %s foot down and set it between your hands. Low Lunge", 8)
threeLeggedDog = twoSides("Three Legged Dog", "Raise your %s foot up. Three Legged Dog", 10)
kneeToElbow = twoSides("Knee To Elbow", "Take your %s knee and bring it to your elbow. Hold", 15)
standingLegLift1 = twoSides("Standing Leg Lift", "Raise your %s foot up and grab it. Standing Leg Lift. Hold", 20)
standingLegLift2 = twoSides("Standing Leg Lift, Leg to Side", "Now take your %s foot and move it out to the side. Hold", 20)
standingLegLift3 = twoSides("Standing Leg Lift, Both Hands", "Return %s foot to center. Grab with both hands, head to knee or chin to shin. Hold.", 20)
standingLegLift4 = twoSides("Standing Leg Lift, No Hands", "Release %s foot. Hold.", 25)
backBend = Move("Back Bend", None, "Bend Backwards", 10)
mountainPose = Move("Mountain Pose", None, "Mountain Pose", 5, backBend, *standingLegLift1)
forwardFold = Move("Forward Fold", None, "Forward Fold", 5, mountainPose)
downwardsDog = Move("Downwards Dog", None, "Downwards Dog", 5, forwardFold, staff, *threeLeggedDog)
humbleWarrior = twoSides("Humble Warrior", "Intertwine your hands behind you. Lean forward. Humble Warrior", 5)
warrior1 = twoSides("Warrior 1", "Warrior One, %s Side", 10, vinyasa)
warrior2 = twoSides("Warrior 2", "Warrior Two, %s Side", 10, vinyasa)
warrior3 = twoSides("Warrior 3", "Warrior Three, %s Side", 10, vinyasa)
standingSplits = twoSides("Standing Splits", "Raise your %s foot up towards the ceiling",20, vinyasa)
cresent = twoSides("Cresent Lunge", "Cresent Lunge, %s foot forward", 10, early="Feel free to lower your other knee down to the ground")
cresentTwist = twoSides("Cresent Twist", "Twist to the %s side. Crest Twist", 15, bind=True)
chairTwist = twoSides("Chair Twist", "Twist to the %s", 15, bind=True)
chair = Move("Chair Pose", None, "Chair Pose", 15, vinyasa, *chairTwist, extended_time=[40])
crow = Move("Crow Pose", None, "Crow Pose", 30, vinyasa)
sideCrow = twoSides("Side Crow", "Side Crow, %s Side", 30, vinyasa)
boat = Move("Boat Pose", None, "Boat Pose", 30, staff)
revolvedHalfMoon = twoSides("Revolved Half Moon", "Revolved Half Moon, %s Side", 20)
halfMoon = twoSides("Half Moon", "Half Moon, %s Side", 20, *revolvedHalfMoon)
sideAngle = twoSides("Side Angle", "Lower your %s hand to the ground and raise the other hand up towards the ceiling. Side Angle", 10, vinyasa, *halfMoon)
triangle = twoSides("Triangle Pose", "Triangle Pose, %s side", 15, vinyasa, *halfMoon)
revolvedTriangle = twoSides("Revolved Triangle", "Revolved Triangle Pose, %s side", 15)
reverseWarrior = twoSides("Reverse Warrior", "Take your %s hand and raise it towards the back of the room. Reverse Warrior", 5)
bridge = Move("Bridge Pose", None, "Bridge Pose", 20)
wheel = Move("Wheel Pose", None, "Wheel Pose", 30)
lieOnBack = Move("LieOnBack", None, "Lie on Your Back", 5)

#Begin linking moves to each other
vinyasa.addMove(downwardsDog)
table.addMove(downwardsDog)
catCow.addMove(downwardsDog)
mountainPose.addMove(forwardFold, chair)
backBend.addMove(mountainPose)
staff.addMove(lieOnBack)
for i in balancingTable: i.addMove(table)
for i in standingLegLift4: i.addMove(mountainPose, forwardFold)
for i in chairTwist: i.addMove(chair, forwardFold)
for i in halfMoon: i.addMove(forwardFold)
for i in revolvedHalfMoon: i.addMove(forwardFold)

doubleAdd(warrior1, warrior2, warrior3, humbleWarrior)
doubleAdd(humbleWarrior, warrior1)
doubleAdd(warrior2, sideAngle)
doubleAdd(threeLeggedDog, lowLunge, kneeToElbow)
doubleAdd(kneeToElbow, lowLunge)
doubleAdd(lowLunge, warrior1, warrior2, warrior3, cresent)
doubleAdd(warrior3, standingLegLift1, standingSplits, inverted=True)
doubleAdd(cresent, warrior1, cresentTwist)
doubleAdd(cresentTwist, cresent, chairTwist)
doubleAdd(balancingTableLegOnly, balancingTable)
doubleAdd(sideAngle, reverseWarrior)
doubleAdd(reverseWarrior, sideAngle)
doubleAdd(standingLegLift1, standingLegLift2)
doubleAdd(standingLegLift1, warrior3, inverted=True)
doubleAdd(standingLegLift2, standingLegLift3)
doubleAdd(standingLegLift3, standingLegLift4)
doubleAdd(standingLegLift4, warrior3, inverted=True)
doubleAdd(standingLegLift4, standingSplits)
doubleAdd(triangle, revolvedTriangle)
doubleAdd(chairTwist, sideCrow)

def later():
    """These moves are reserved for later in a practice."""
    pass

def cooldown():
    """These are cooldown-moves added for very late in a practice"""
    pass

if __name__== "__main__":
    start = datetime.datetime.now()
    speak("Beginning in")
    print("Beginning in:")
    countdown(3)
    pose = child.play()
    try:
        while True:
            nextPose = pose.play()
            pose = nextPose
    except KeyboardInterrupt:
        print("\nTotal Time: " +str(datetime.datetime.now()-start))

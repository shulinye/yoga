#!/usr/bin/python3

"""An attempt to make a command-line based yoga program. NOTE: uses espeak for audio"""

import subprocess
import time
import sys
import datetime
import random

debug=False

aerobics = True

imbalance = []

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
    def addLateMove(self, *args):
        if "lateMove" not in self.kwargs:
            self.kwargs["lateMove"] = set()
        self.kwargs["lateMove"].update(args)
    def play(self, **kwargs):
        """Tells me which pose I'm supposed to do and how I'm supposed to do it. Also figures out next pose."""
        print("")
        print(self.title)
        #What is my next move?
        if "nextMove" in kwargs:
            nextMove = kwargs["nextMove"]
        elif imbalance:
            for i in imbalance:
                if i in self.nextMove:
                    nextMove = i
                    break
            else:
                print("no match found")
                nextMove = random.choice(tuple(self.nextMove))
        else:
            nextMove = random.choice(tuple(self.nextMove))
        if nextMove is not None:
            print("Next Move: " + nextMove.title)
        #Tell me what to do
        speak(self.audio)
        #How long am I supposed to do it?
        if "time" in kwargs:
            t = kwargs["time"]
        elif "extended" in kwargs and kwargs["extended"] and "extended_time" in self.kwargs:
            t = random.choice(self.kwargs["extended_time"])
        else:
            t = self.time
        if "bind" in self.kwargs and self.kwargs["bind"]: speak("Bind if you want to")
        speak(str(t) + "seconds")
        countdown(t)
        if "bind" in self.kwargs and self.kwargs["bind"]: speak("Release bind")
        #Deal with imbalances
        if self.side:
            if self in imbalance:
                imbalance.remove(self)
                print(imbalance)
            else:
                imbalance.append(self.otherside)
                print(imbalance)
        return nextMove
    def __repr__(self):
        return "Move(%s)" % self.title
    def __str__(self):
        return self.title
    def __hash__(self):
        return hash(self.title)
    def __eq__(self, other):
        return self.title == other.title
    def __ne__(self, other):
        return self.title != other.title
    def __le__(self, other):
        return self.title < other.title

def twoSides(title, audio, time, *args, **kwargs):
    """Hey, you have two legs."""
    dicR = {"same": "Right", "other": "Left"}
    dicL = {"same": "Left", "other": "Right"}
    if "%" in audio:
        R = Move(title+ ", Right", "Right", audio % dicR, time, *args, **kwargs)
        L = Move(title+ ", Left", "Left", audio % dicL, time, *args, **kwargs)
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

plank = Move("Plank", None, "Plank. Hold",30, extended_time=[60], harder="Throw in a few pushups!")
balancingTable = twoSides("Balancing Table", "When you are ready, extend the opposite arm", 10)
balancingTableLegOnly = twoSides("Balancing Table, Leg Only", "Extend %(same)s leg behind you", 5)
catCow = Move("Cat Cow", None, "Cat Cow", 10, plank, *balancingTableLegOnly)
table = Move("Table Pose", None, "Table Pose", 5, catCow, *balancingTableLegOnly)
threadTheNeedle = twoSides("Thread The Needle", "Take your %(same)s hand and reach it towards the ceiling. On an exhale, slide it under your other shoulder.", 20, table)
oneHandedTiger = twoSides("One-Handed Tiger", "Reach back and catch your %(same)s foot with your %(other)s hand. Lean into your hand",15, table)
vinyasa = Move("Vinayasa", None, "Vinyasa", 5)
seatedForwardFold = Move("Seated Forward Fold", None, "Seated Forward Fold", 15)
staff = Move("Staff Pose", None, "Staff Pose",10, vinyasa, seatedForwardFold)
butterflyStretch = Move("Butterfly Stretch", None, "Butterfly Stretch", 30, vinyasa, staff)
child = Move("Child's Pose", None, "Child's Pose", 5, table, extended_time=[20])
seatedTwist = twoSides("Seated Twist", "Twist to the %(same)s side", 10)
seatedMeditation = Move("Seated Meditation", None, "Seated Meditation", 5, child, butterflyStretch, *seatedTwist ,extended_time=[20,30,40])
childsPoseSideStretch = twoSides("Child's Pose, Side Stretch", "Reach your fingers over to your %(same)s side. You should feel a stretch across your %(other)s side body", 10, child)
lowLunge = twoSides("Low Lunge", "Bring your %(same)s foot down and set it between your hands. Low Lunge", 5)
threeLeggedDog = twoSides("Three Legged Dog", "Raise your %(same)s foot up. Three Legged Dog", 10)
kneeToElbow = twoSides("Knee To Elbow", "Take your %(same)s knee and bring it to your %(same)s elbow. Hold", 15, harder="Try to bring your knee up to your forearm!")
kneeToOtherElbow = twoSides("Knee To Other Elbow", "Take your %(same)s knee and bring it across your body to your %(other)s elbow", 15, extended_time=[20,30])
standingLegLift1 = twoSides("Standing Leg Lift", "Raise your %(same)s foot up and grab it with your %(same) hand. Standing Leg Lift. Hold", 20)
standingLegLift2 = twoSides("Standing Leg Lift, Leg to Side", "Now take your %(same)s foot and move it out to the side. Hold", 20)
standingLegLift3 = twoSides("Standing Leg Lift, Both Hands", "Return %(same)s foot to center. Grab with both hands, head to knee or chin to shin. Hold.", 20)
standingLegLift4 = twoSides("Standing Leg Lift, No Hands", "Release %(same)s foot. Hold.", 25)
eagle = twoSides("Eagle Pose", "Take your %(same)s foot and twist it over your %(other)s leg. Twine your arms, %(same) arm lower. Eagle Pose", 25, extended_time=[40],\
        harder="Bring your elbows to your knees, and then straighten. Repeat")
treePose = twoSides("Tree Pose", "Tree Pose, %(same)s side", 25)
dancer = twoSides("Dancer Pose", "Dancer Pose, %(same)s side", 25, vinyasa)
backBend = Move("Back Bend", None, "Bend Backwards", 10)
mountainPose = Move("Mountain Pose", None, "Mountain Pose", 5, backBend, *standingLegLift1)
standingTwist = twoSides("Standing Twist", "Bring your arms up to shoulder level and twist to the %(same)s", 15, mountainPose)
forwardFold = Move("Forward Fold", None, "Forward Fold", 5, mountainPose)
forearmBalance = Move("Forearm Balance", None, "Forearm Balance", 45, child)
dolphin = Move("Dolphin Pose", None, "Dolphin Pose", 30, vinyasa, lateMove = set(forearmBalance))
downwardDog = Move("Downwards Dog", None, "Downwards Dog", 5, forwardFold, staff, plank, dolphin, *threeLeggedDog)
humbleWarrior = twoSides("Humble Warrior", "Intertwine your hands behind you. Lean forward. Humble Warrior", 5)
warrior1 = twoSides("Warrior 1", "Warrior One, %(same)s Side", 10, vinyasa)
warrior2 = twoSides("Warrior 2", "Warrior Two, %(same)s Side", 10, vinyasa)
warrior3 = twoSides("Warrior 3", "Warrior Three, %(same)s Side", 10, vinyasa, harder="Bring your elbows to your knee, and then extend! Repeat")
standingSplits = twoSides("Standing Splits", "Raise your %(same)s foot up towards the ceiling",20, vinyasa)
lizard = twoSides("Lizard Pose", "Lizard Pose, %(same)s side", 30, vinyasa, bind=True, harder="Lower yourself onto your forearms")
runningMan = twoSides("Running Man", "Running Man, %(same)s side", 30, vinyasa)
cresent = twoSides("Cresent Lunge", "Cresent Lunge, %(same)s foot forward", 10, early="Feel free to lower your other knee down to the ground")
cresentTwist = twoSides("Cresent Twist", "Twist to the %(same)s side. Crest Twist", 15, bind=True)
chairTwist = twoSides("Chair Twist", "Twist to the %(same)s", 15, bind=True)
chair = Move("Chair Pose", None, "Chair Pose", 15, vinyasa, *chairTwist, extended_time=[40, 60])
oneLeggedChair = twoSides("OneLeggedChair", "Shift all your weight to your %(other)s foot. Grab your %(same)s foot with your %(same)s hand. Raise %(same)s foot", 15, chair, extended_time=[20,30])
crow = Move("Crow Pose", None, "Crow Pose", 30, vinyasa)
sideCrow = twoSides("Side Crow", "Side Crow, %(same)s Side", 30, vinyasa)
boat = Move("Boat Pose", None, "Boat Pose", 30, staff)
lowBoat = Move("Low Boat Pose", None, "Lower down into Low Boat Pose", 15, boat, vinyasa, extended_time=[20,30])
revolvedHalfMoon = twoSides("Revolved Half Moon", "Revolved Half Moon, %(same)s Side", 20)
halfMoon = twoSides("Half Moon", "Half Moon, %(same)s Side", 20)
sideAngle = twoSides("Side Angle", "Lower your %(same)s hand to the ground and raise the other hand up towards the ceiling. Side Angle", 10, vinyasa, *halfMoon)
sidePlank = twoSides("Side Plank", "Side Plank, %(same)s side", 15, plank, vinyasa, extended_time=[30,40])
triangle = twoSides("Triangle Pose", "Triangle Pose, %(same)s side", 15, vinyasa, *halfMoon)
pyramid = Move("Pyramid Pose", None, "Pyramid Pose", 15, vinyasa, *triangle)
revolvedTriangle = twoSides("Revolved Triangle", "Revolved Triangle Pose, %(same)s side", vinyasa, pyramid, 15)
reverseWarrior = twoSides("Reverse Warrior", "Take your %(same)s hand and raise it towards the back of the room. Reverse Warrior", 5)
bridge = Move("Bridge Pose", None, "Bridge Pose", 20)
bridgeWithRaisedLeg = twoSides("Bridge, with Raised Leg", "Raise your %(same)s leg into the air", 15, bridge, extended_time =[20,30])
wheel = Move("Wheel Pose", None, "Wheel Pose", 30, vinyasa, extended_time=[45,60], harder="Try to straighten your legs")
lieOnBack = Move("Lie On Back", None, "Lie on Your Back", 5)
spinalTwist = twoSides("Spinal Twist","Bring your knees up to your chest, and then let them fall to the %(same)s. Look towards your %(other)s hand. Spinal Twist", 20, lieOnBack)
lieOnFront = Move("Lie On Front", None, "Lie on Your Stomach", 5)
yogaBicycles = Move("Bicycles", None, "Bicycles", 30, lieOnBack, vinyasa, extended_time=[45, 60])
savasana = Move("Savasana", None, "Savahsana", 30, None)
starPose = Move('Star Pose', None, "Star Pose", 10, mountainPose, *warrior1)
goddessSquat = Move('Goddess Squat', None, "Goddess Squat", 5, starPose)
supportedHeadstand = Move('Supported Headstand', None, "Supported Headstand", 30, child)

#Begin linking moves to each other
vinyasa.addMove(downwardDog)
table.addMove(downwardDog, *threadTheNeedle)
catCow.addMove(downwardDog)
mountainPose.addMove(forwardFold, chair, *standingTwist)
mountainPose.addMove(*dancer)
backBend.addMove(mountainPose, forwardFold)
staff.addMove(lieOnBack, butterflyStretch)
downwardDog.addMove(plank)
lieOnBack.addMove(yogaBicycles, staff, seatedMeditation, lieOnFront, *spinalTwist)
plank.addMove(vinyasa)
child.addMove(downwardDog, seatedMeditation, *childsPoseSideStretch)
boat.addMove(lowBoat)
lowBoat.addMove(yogaBicycles)
chair.addMove(*oneLeggedChair)
starPose.addMove(goddessSquat)
pyramid.addMove(*revolvedTriangle)
bridge.addMove(lieOnBack)
seatedForwardFold.addMove(seatedMeditation)
for i in brigeWithRaiseLeg: i.addMove(lieOnBack)
for i in eagle: i.addMove(forwardFold)
for i in balancingTable: i.addMove(table)
for i in standingLegLift4: i.addMove(mountainPose, forwardFold)
for i in chairTwist: i.addMove(chair, forwardFold)
for i in halfMoon: i.addMove(forwardFold)
for i in revolvedHalfMoon: i.addMove(forwardFold)
for i in warrior1: i.addMove(starPose)
for i in seatedTwist: i.addMove(seatedMeditation)
for i in triangle: i.addMove(pyramid)
for i in dancer: i.addMove(forwardFold)

doubleAdd(oneLeggedChair, standingLegLift1)
doubleAdd(sidePlank, sideAngle, cresentTwist)
doubleAdd(warrior1, warrior2, warrior3, humbleWarrior)
doubleAdd(humbleWarrior, warrior1)
doubleAdd(warrior2, sideAngle)
doubleAdd(threeLeggedDog, lowLunge, kneeToElbow)
doubleAdd(kneeToElbow, kneeToOtherElbow, threeLeggedDog, lowLunge, runningMan)
doubleAdd(kneeToOtherElbow, threeLeggedDog)
doubleAdd(lowLunge, warrior1, warrior2, warrior3, cresent, lizard)
doubleAdd(warrior3, standingLegLift1, standingSplits, inverted=True)
doubleAdd(cresent, warrior1, cresentTwist)
doubleAdd(cresentTwist, cresent, chairTwist, sidePlank)
doubleAdd(balancingTableLegOnly, balancingTable)
doubleAdd(sideAngle, reverseWarrior, sidePlank, warrior2)
doubleAdd(reverseWarrior, sideAngle, warrior2)
doubleAdd(standingLegLift1, standingLegLift2, eagle, treePose)
doubleAdd(standingLegLift1, warrior3, inverted=True)
doubleAdd(standingLegLift2, standingLegLift3)
doubleAdd(standingLegLift3, standingLegLift4)
doubleAdd(standingLegLift4, warrior3, inverted=True)
doubleAdd(standingLegLift4, standingSplits, eagle, treePose)
doubleAdd(triangle, revolvedTriangle)
doubleAdd(chairTwist, sideCrow)
doubleAdd(lizard, runningMan)
doubleAdd(halfMoon, revolvedHalfMoon, warrior3)
doubleAdd(revolvedHalfMoon, halfMoon, warrior3)
doubleAdd(revolvedTriangle, revolvedHalfMoon)
doubleAdd(dancer, standingLegLift1, standingSplits)

if aerobics:
    jumpingJacks = Move("Jumping Jacks", None, "Jumping Jacks!", 60, mountainPose)
    runInPlace = Move("Running In Place", None, "Run In Place", 60, mountainPose, jumpingJacks)
    mountainPose.addMove(jumpingJacks, runInPlace)
    jumpingJacks.addMove(runInPlace)

def routine(li):
    li_copy = li.copy()
    for i in range(len(li)-1):
        current_pose, next_pose = li_copy[i], li_copy[i+1]
        current_pose.play(nextMove=next_pose)
    return li_copy[-1]

if __name__== "__main__":
    speak("Beginning in")
    print("Beginning in:")
    countdown(3)
    total_time = 60*int(sys.argv[-1])
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=total_time)
    pose = child.play(extended=True)
    try:
        #warmup
        print("warmup")
        while datetime.datetime.now() - start < datetime.timedelta(seconds=total_time//10):
            nextPose = pose.play()
            pose = nextPose
        #get me to table:
        if imbalance:
            pose = routine(imbalance)
        print("transition")
        while not pose == table or pose == downwardDog:
            if pose == child:
                if imbalance:
                    print(imbalance)
                nextPose = pose.play(nextMove = downwardDog)
            elif pose == forwardFold:
                nextPose = pose.play(nextMove = vinyasa)
            else:
                nextPose = pose.play()
            pose = nextPose
        pose = pose.play(nextMove=plank)
        pose = pose.play(extended = True)
        while datetime.datetime.now() -start < datetime.timedelta(seconds=total_time//2):
            nextPose = pose.play()
            pose = nextPose
        #deal with imbalances, somehow
    except KeyboardInterrupt:
        print(imbalance)
        savasana.play()
        print("\nTotal Time: " +str(datetime.datetime.now()-start))

#!/usr/bin/python3

"""An attempt to make a command-line based yoga program.
call with python3 main.py [length of routine wanted, in minutes]
NOTE: uses espeak for audio"""

import time
import sys
import random

import dijkstras
import utils

debug = False
aerobics = True
DEFAULT_TIME = 15 #minutes

imbalance = []

class Move(object):
    def __init__(self, title : str , side : int , audio : str , time : int , *args, **kwargs):
        """Creates a Move. Arguments are: title, side (-1 for left, 0 for None, 1 for Right)
        audio (for espeak), and time (in seconds)
        
        *args = moves for moveset
        **kwargs = options"""
        self.title = title
        self.side = side
        self.audio = audio
        self.time = time
        self.last = None
        self.nextMove = set(args)
        self.kwargs = kwargs
    def updateKwargs(self, **kwargs):
        self.kwargs.update(kwargs)
    def addOtherSide(self, otherside):
        self.otherside = otherside
    def addMove(self, *args):
        self.nextMove.update(args)
    def removeMove(self, *args):
        self.nextMove.difference_update(args)
    def addLateMove(self, *args):
        if "lateMove" not in self.kwargs:
            self.kwargs["lateMove"] = set()
        self.kwargs["lateMove"].update(args)
    def notLast(self):
        if self.last and len(self.nextMove)>1:
            movesCopy = self.nextMove.copy()
            movesCopy.remove(self.last)
            return random.choice(tuple(movesCopy))
        else:
            return random.choice(tuple(self.nextMove))
    def promoteLate(self):
         if "lateMove" in self.kwargs:
            try:
                move = self.kwargs["lateMove"].pop()
                self.addMove(move)
            except KeyError:
                pass
    def play(self, **kwargs) -> "Move" :
        """Tells me which pose I'm supposed to do and how I'm supposed to do it.
        Also figures out next pose and deals with adding late moves"""
        print("")
        print(self.title)
        #Deal with imbalances
        if self.side:
            if self in imbalance:
                imbalance.remove(self)
            else:
                imbalance.append(self.otherside)
        #What is my next move?
        if "nextMove" in kwargs:
            # Assume the caller knows what they're doing right now.
            # Should possibly assert that nextMove is a plausible nextMove
            nextMove = kwargs["nextMove"]
        elif imbalance:
            for i in imbalance:
                if i in self.nextMove:
                    nextMove = i
                    break
            else:
                nextMove = self.notLast()
        else:
            nextMove = self.notLast()
        if nextMove is not None:
            print("Next Move: " + nextMove.title)
            print("My options were: " + "; ".join(str(i) for i in self.nextMove))
            self.last = nextMove
        #Tell me what to do
        utils.speak(self.audio)
        if "early" in kwargs and kwargs["early"] and "early" in self.kwargs:
            utils.speak(self.kwargs["early"])
        elif "harder" in kwargs and kwargs["harder"] and "harder" in self.kwargs:
            utils.speak(self.kwargs["harder"])
        #How long am I supposed to do it?
        if "time" in kwargs:
            t = kwargs["time"]
        elif "extended" in kwargs and kwargs["extended"] and "extended_time" in self.kwargs:
            t = random.choice(self.kwargs["extended_time"])
        else:
            t = self.time
        if "bind" in self.kwargs and self.kwargs["bind"]: utils.speak("Bind if you want to")
        if t > 5: utils.speak(str(t) + "seconds")
        utils.countdown(t)
        if "bind" in self.kwargs and self.kwargs["bind"]: utils.speak("Release bind")
        self.promoteLate() #Add in options for harder followup moves next time
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
    def __lt__(self, other):
        return self.title < other.title


def twoSides(title : str , audio : str , time : int , *args, **kwargs):
    """Hey, you have two legs. Convenience method to generate both left and right sides for a move"""
    dicR = {"same": "Right", "other": "Left"}
    dicL = {"same": "Left", "other": "Right"}
    if "%" in audio:
        R = Move(title + ", Right", 1, audio % dicR, time, *args, **kwargs)
        L = Move(title + ", Left", -1, audio % dicL, time, *args, **kwargs)
    else:
        R = Move(title + ", Right", 1, audio, time, *args, **kwargs)
        L = Move(title + ", Left", -1, audio, time, *args, **kwargs)
    R.addOtherSide(L)
    L.addOtherSide(R)
    return (R,L)


def doubleAdd(move, *args, inverted=False, late=False):
    """Convenience method to help link moves that have sides
    inverted: if True, causes L to be linked to R and R to be linked to L
    late: if True, causes move to be linked as a late move"""
    f = Move.addLateMove if late else Move.addMove
    if inverted:
        f(move[0], *[i[1] for i in args])
        f(move[1], *[i[0] for i in args])
    else:
        f(move[0], *[i[0] for i in args])
        f(move[1], *[i[1] for i in args])

#Begin list of moves
lowPlank = Move("Low Plank", 0, "Lower down into Low Plank. Hold", 10, extended_time=[15,20])
plank = Move("Plank", 0, "Plank. Hold", 30, lowPlank, extended_time=[45,60], harder="Throw in a few pushups!")
balancingTable = twoSides("Balancing Table", "When you are ready, extend the opposite arm", \
        10, harder="Want a challenge? Extend the same arm.")
balancingTableLegOnly = twoSides("Balancing Table, Leg Only", "Extend %(same)s leg behind you", 4)
catCow = Move("Cat Cow", 0, "Cat Cow", 10, plank, *balancingTableLegOnly)
table = Move("Table Pose", 0, "Table Pose", 4, catCow, *balancingTableLegOnly)
threadTheNeedle = twoSides("Thread The Needle", "Take your %(same)s hand and reach it towards the ceiling. On an exhale, slide it under your other shoulder.", 20, table)
oneHandedTiger = twoSides("One-Handed Tiger", "Reach back and catch your %(same)s foot with your %(other)s hand. Lean into your hand", 15, table, catCow)
vinyasa = Move("Vinyasa", 0, "Vinyasa", 4, harder="Add in a push up!")
seatedForwardFold = Move("Seated Forward Fold", 0, "Seated Forward Fold", 15, vinyasa)
flyingStaff = Move("Flying Staff Pose", 0, "Press down on the ground. Try to lift your body off the ground", 20, vinyasa)
staff = Move("Staff Pose", 0, "Staff Pose", 10, vinyasa, seatedForwardFold, lateMove=set([flyingStaff]))
archer = twoSides("Archer Pose", "Grab each foot with hand. Try to straighten the %(same)s leg and bend the %(other)s leg, lifting both legs off the ground. Archer Pose.", 30, staff, vinyasa)
butterflyStretch = Move("Butterfly Stretch", 0, "Butterfly Stretch", 15, vinyasa, staff,lateMove=set(archer))
headToKnee = twoSides("Head To Knee", "With your %(same)s knee straight and your %(other)s knee bent, reach toward the toes of your %(same)s foot.", 15, staff, butterflyStretch)
child = Move("Child's Pose", 0, "Child's Pose", 4, table, extended_time=[10,15], lateMove=set([catCow]))
seatedTwist = twoSides("Seated Twist", "Twist to the %(same)s side", 10, vinyasa)
scale = Move("Scale Pose", 0, "Push upwards with your hands. Try to get your entire body off the ground. Scale Pose", 15, vinyasa)
seatedMeditation = Move("Seated Meditation", 0, "Seated Meditation", 4, \
        child, table, catCow, butterflyStretch, staff, *seatedTwist, \
        extended_time=[20,30,40], lateMove=set([scale, vinyasa]))
childsPoseSideStretch = twoSides("Child's Pose, Side Stretch", \
        "Reach your fingers over to your %(same)s side. You should feel a stretch across your %(other)s side body", \
        8, child, table, seatedMeditation)
lowLunge = twoSides("Low Lunge", "Bring your %(same)s foot down and set it between your hands. Low Lunge", 4)
threeLeggedDog = twoSides("Three Legged Dog", "Raise your %(same)s foot up. Three Legged Dog", \
        4, extended_time=[15,30])
kneeToNose = twoSides("Knee To Nose", "Take your %(same)s knee and bring it towards your nose. Hold.", \
        15, extended_time=[20,30])
kneeToElbow = twoSides("Knee To Elbow", "Take your %(same)s knee and bring it to your %(same)s elbow. Hold", \
        15, harder="Try to bring your knee up to your forearm!", extended_time=[20,30])
kneeToOtherElbow = twoSides("Knee To Other Elbow", "Take your %(same)s knee and bring it across your body to your %(other)s elbow", 15, vinyasa, extended_time=[20,30])
standingLegLift1 = twoSides("Standing Leg Lift", "Raise your %(same)s foot up and grab it with your %(same) hand. Standing Leg Lift. Hold", \
        20, extended_time=[30,45,60])
standingLegLift2 = twoSides("Standing Leg Lift, Leg to Side", "Now take your %(same)s foot and move it out to the side. Hold", \
        20, extended_time=[30,45,60])
standingLegLift3 = twoSides("Standing Leg Lift, Both Hands", "Return %(same)s foot to center. \
        Grab with both hands, head to knee or chin to shin. Hold.", 20, extended_time=[30,45,60])
standingLegLift4 = twoSides("Standing Leg Lift, No Hands", "Release %(same)s foot. Hold foot up towards ceiling.", \
        25, extended_time=[30,45,60])
eagle = twoSides("Eagle Pose", "Take your %(same)s foot and twist it over your %(other)s leg. Twine your arms, %(same) arm lower. Eagle Pose", 25, extended_time=[40],\
        harder="Bring your elbows to your knees, and then straighten. Repeat")
treePose = twoSides("Tree Pose", "Tree Pose, %(same)s side", 25, vinyasa, extended_time=[45,60])
halfBoundStandingLotus = twoSides("Half-Bound Standing Lotus", "Take your %(same)s foot and put it at the top of your %(other)s thigh. With your %(same)s hand, reach behind you and grab your %(same)s foot", 15, \
        vinyasa, harder="Lean forwards and touch the ground with your free hand.", extended_time=[30,45])
standingLotusSquat = twoSides("Standing Lotus Squat", "Bend your %(other)s thigh and squat down", 15, vinyasa, extended_time=[20,30])
toestand = twoSides("Toestand", "Continue bending down, rise up onto the toes of your %(other)s foot", 15, vinyasa, harder="Try to get your hands to your heart!", extended_time=[20,30])
flyingPigeon = twoSides("Flying Pigeon", "Plant your hands on the ground and lift your %(same)s foot. Flying Pigeon", 30, vinyasa)
dancer = twoSides("Dancer Pose", "Dancer Pose, %(same)s side", 25, vinyasa, extended_time=[25,45])
backBend = Move("Back Bend", 0, "Raise your hands towards the ceiling and bend backwards", 10, vinyasa)
wideLegStance = Move("Wide Leg Stance", 0, "Wide Leg Stance", 4)
wideLegForwardFold = Move("Wide Leg Forward Fold", 0, "Wide Leg Forward Fold",15, wideLegStance)
armPressurePose = Move("Arm Pressure Pose", 0, "Wrap legs around shoulders. Attempt to balance on arms.", \
        30, wideLegForwardFold)
standingLegStretch = twoSides("Standing Leg Stretch", "Reach for your %(same)s foot", \
        10, wideLegStance, wideLegForwardFold)
mountainPose = Move("Mountain Pose", 0, "Mountain Pose", 4, backBend, wideLegStance, \
        *standingLegLift1, extended_time=[10])
standingSideStretch = twoSides("Standing Side Stretch", "Lean to the %(same)s side", \
        10, backBend, mountainPose)
standingTwist = twoSides("Standing Twist", "Bring your arms up to shoulder level and twist to the %(same)s", \
        15, mountainPose)
forwardFoldShoulderStretch = Move("Forward Fold, Shoulder Stretch", 0, \
        "Clasp your hands together behind your head and allow gravity to drag your pinkies towards the floor", \
        10, mountainPose, extended_time=[15,20])
forwardFold = Move("Forward Fold", 0, "Forward Fold", 3, mountainPose, \
        forwardFoldShoulderStretch)
flatBack = Move("Flat Back", 0, "Flat Back", 3, forwardFold, vinyasa)
forearmBalance = Move("Forearm Balance", 0, "Forearm Balance", 30, child, extended_time=[45])
dolphin = Move("Dolphin Pose", 0, "Dolphin Pose", 30, vinyasa, lateMove = set([forearmBalance]), extended_time=[45])
downwardDog = Move("Downwards Dog", 0, "Downwards Dog", 4, forwardFold, staff, plank, dolphin, \
        *threeLeggedDog, extended_time=[10])
upwardDog = Move("Upward Dog", 0, "Upward Dog", 4, downwardDog, extended_time=[10,20])
humbleWarrior = twoSides("Humble Warrior", "Intertwine your hands behind you. Lean forward. Humble Warrior", \
        4, vinyasa)
warrior1 = twoSides("Warrior 1", "Warrior One, %(same)s Side", 10, vinyasa, extended_time=[20,30])
warrior2 = twoSides("Warrior 2", "Warrior Two, %(same)s Side", 10, vinyasa, extended_time=[20,30])
warrior3 = twoSides("Warrior 3", "Warrior Three, %(same)s Side", 10, vinyasa, \
        harder="Bring your elbows to your knee, and then extend! Repeat", extended_time=[20,30,45])
standingSplits = twoSides("Standing Splits", "Raise your %(same)s foot up towards the ceiling. Standing Splits", \
        20, vinyasa, extended_time=[30])
lizard = twoSides("Lizard Pose", "Lizard Pose, %(same)s side", 30, vinyasa, \
        bind=True, harder="Lower yourself onto your forearms", extended_time=[45,60])
chinStand = twoSides("Chin Stand", "Chin Stand, %(same)s side", 30, vinyasa)
runningMan = twoSides("Running Man", "Running Man, %(same)s side", 30, vinyasa)
revolvedRunningMan = twoSides("Revolved Running Man", "Revolved Running Man, %(same)s side", 30, vinyasa)
cresent = twoSides("Cresent Lunge", "Cresent Lunge, %(same)s foot forward", 10, \
        early="Feel free to lower your other knee down to the ground", extended_time=[20,30])
cresentTwist = twoSides("Cresent Twist", "Cresent Twist. Twist to the %(same)s side.", 15, bind=True)
chairTwist = twoSides("Chair Twist", "Chair Twist. Twist to the %(same)s side", 15, bind=True)
chair = Move("Chair Pose", 0, "Chair Pose", 15, vinyasa, *chairTwist, extended_time=[30, 40, 60])
oneLeggedChair = twoSides("One Legged Chair", "Shift all your weight to your %(other)s foot. Grab your %(same)s \
        foot with your %(same)s hand. Raise %(same)s foot", 15, chair, extended_time=[20,30])
crow = Move("Crow Pose", 0, "Crow Pose", 30, vinyasa, harder="Try to straigten your arms")
sideCrow = twoSides("Side Crow", "Side Crow, %(same)s Side", 30, vinyasa)
boat = Move("Boat Pose", 0, "Boat Pose", 30, staff, extended_time=[45,60])
boatLift = Move("Boat Lift", 0, "Cross one ankle over the other, plant your hands and lift", 10, boat)
boatTwist = Move("Boat Twist", 0, "Point your fingers towards the right and your ankles towards the left. Now reverse. Repeat", \
        20, boat, extended_time=[30,40])
lowBoat = Move("Low Boat Pose", 0, "Lower down into Low Boat Pose", \
        15, boat, vinyasa, extended_time=[20,30])
revolvedHalfMoon = twoSides("Revolved Half Moon", "Revolved Half Moon, %(same)s Side", \
        20, extended_time=[30])
halfMoon = twoSides("Half Moon", "Half Moon, %(same)s Side", 20, \
        harder="Try to take your hand off the ground!", extended_time=[30])
sideAngle = twoSides("Side Angle", "Side Angle", 10, vinyasa, extended_time=[20])
sidePlank = twoSides("Side Plank", "Side Plank, %(same)s side", 15, \
        plank, vinyasa, extended_time=[30,40])
sidePlankLegUp = twoSides("Side Plank, Leg Up", "Now raise your %(same)s leg up and hold", \
        15, extended_time=[20,25,30])
triangle = twoSides("Triangle Pose", "Triangle Pose, %(same)s side", 15, vinyasa,bind=True)
pyramid = twoSides("Pyramid Pose", "Pyramid Pose, %(same)s side", 15, vinyasa)
revolvedTriangle = twoSides("Revolved Triangle", "Revolved Triangle Pose, %(same)s side", 15, vinyasa)
reverseWarrior = twoSides("Reverse Warrior", "Take your %(same)s hand and raise it towards the back of the room. Reverse Warrior", \
        4, extended_time=[10])
bridge = Move("Bridge Pose", 0, "Bridge Pose", 20)
bridgeWithRaisedLeg = twoSides("Bridge, with Raised Leg", "Raise your %(same)s leg into the air", \
        15, bridge, extended_time =[20,30])
wheelWithRaisedLeg = twoSides("Wheel, with Raised Leg", "Raise your %(same)s leg into the air", 15)
wheel = Move("Wheel Pose", 0, "Wheel Pose", 30, vinyasa, \
        extended_time=[45,60], harder="Try to straighten your legs", lateMove=set(wheelWithRaisedLeg))
camel = Move("Camel Pose", 0, "Camel Pose", 30, vinyasa)
superMan = Move("Super Man", 0, "Raise both your hands and your feet off the ground at the same time. Hold", \
        15, vinyasa)
bow = Move("Bow Pose", 0, "Grab your feet with both hands and raise upwards", \
        15, vinyasa, extended_time=[20,30,40])
fish = Move("Fish Pose", 0, "Fish Pose", 20, vinyasa)
supportedShoulderStand = Move("Supported Shoulder Stand", 0, "Supported Shoulder Stand", 30, fish)
plow = Move("Plow Pose", 0, "Plow Pose", 30, supportedShoulderStand)
upwardPlank = Move("Upward Plank", 0, "Upward Plank", 30, vinyasa)
upwardPlankLiftedLeg = twoSides("Upward Plank, Lifted Leg", "Lift your %(same)s leg. Upward Plank, %(same)s leg lifted", \
        15, upwardPlank, vinyasa)
lieOnBack = Move("Lie On Back", 0, "Lie on Your Back", 4, supportedShoulderStand, upwardPlank, vinyasa)
spinalTwist = twoSides("Spinal Twist","Bring your knees up to your chest, and then let them fall to the %(same)s. \
        Look towards your %(other)s hand. Spinal Twist", 20, lieOnBack)
lieOnFront = Move("Lie On Front", 0, "Lie on Your Stomach", 4, superMan, bow, lieOnBack, vinyasa, lateMove=set([plank]))
yogaBicycles = Move("Bicycles", 0, "Bicycles", 30, lieOnBack, vinyasa, extended_time=[45, 60])
savasana = Move("Savasana", 0, "Sahvahsahnah", 30, None)
starPose = Move('Star Pose', 0, "Star Pose", 10, mountainPose, *warrior1)
goddessSquat = Move('Goddess Squat', 0, "Goddess Squat", 5, starPose)
supportedHeadstand = Move('Supported Headstand', 0, "Supported Headstand", 30, child)
pigeon = twoSides('Pigeon Pose', "Pigeon Pose, %(same)s side", 30, vinyasa)
kingPigeon = twoSides('King Pigeon', "King Pigeon, %(same)s side", 15, vinyasa)
birdOfParadise = twoSides('Bird of Paradise', 'Bird of Paradise', 30)
boundHalfMoon = twoSides('Bound Half Moon', 'Bound Half Moon', 30)
handstandHops = Move('Handstand Hops', 0, "Handstand Hops", 30, vinyasa)
twoLeggedDog = twoSides('Two Legged Dog', "Now raise your %(other)s hand. Hold", 20, lateMove=set([vinyasa]))
flippedDog = twoSides('Flipped Dog', "Flipped Dog, %(same)s side", 20)
feetUpAWall = Move("Feet Up A Wall", 0, "Feet Up A Wall", 4, lowBoat, boat, extended_time=[15,30])
hero = Move("Hero Pose", 0, "Tuck both feet under your glutes. Lean back as far as possible. Hero Pose", 20, seatedMeditation)
deepSquat = Move("Deep Squat", 0, "Squat as deeply as you can", 30, vinyasa, chair, lateMove=set([crow]))
frog = Move("Frog Pose", 0, "Frog Pose", 30, seatedMeditation, vinyasa)
cowFace = twoSides('Cow-Facing Pose', 'Cow-Facing Pose', 30, seatedMeditation, child) #TODO: more useful instructions

#Begin linking moves to each other
wideLegStance.addMove(mountainPose, starPose, wideLegForwardFold, *warrior2)
wideLegStance.addLateMove(armPressurePose, *cresent)
vinyasa.addMove(downwardDog)
table.addMove(*threadTheNeedle)
catCow.addMove(table)
mountainPose.addMove(forwardFold, chair, *standingTwist)
mountainPose.addMove(*standingSideStretch)
mountainPose.addLateMove(*dancer)
backBend.addMove(mountainPose, forwardFold, *standingSideStretch)
staff.addMove(lieOnBack, butterflyStretch, camel, boat)
staff.addLateMove(yogaBicycles, mountainPose)
downwardDog.addMove(plank)
flatBack.addMove(forwardFold)
flatBack.addLateMove(chair, deepSquat)
lieOnBack.addMove(yogaBicycles, bridge, staff, seatedMeditation, lieOnFront, feetUpAWall,*spinalTwist)
lieOnBack.addLateMove(wheel)
plow.addMove(fish)
upwardPlank.addMove(lieOnBack)
upwardPlank.addLateMove(*upwardPlankLiftedLeg)
supportedShoulderStand.addMove(plow)
plank.addMove(vinyasa, *sidePlank)
lowPlank.addMove(upwardDog, vinyasa)
lowPlank.addLateMove(plank)
child.addMove(*childsPoseSideStretch)
child.addLateMove(seatedMeditation)
boat.addMove(lowBoat, boatLift, boatTwist)
lowBoat.addMove(yogaBicycles)
chair.addMove(deepSquat, *oneLeggedChair)
starPose.addMove(goddessSquat, deepSquat)
bridge.addMove(lieOnBack, *bridgeWithRaisedLeg)
fish.addMove(lieOnBack)
seatedMeditation.addLateMove(mountainPose,boat,yogaBicycles)
seatedForwardFold.addMove(seatedMeditation, *headToKnee)
forwardFoldShoulderStretch.addMove(forwardFold, chair)
butterflyStretch.addMove(*headToKnee)
superMan.addMove(lieOnFront)
bow.addMove(lieOnFront)
scale.addMove(seatedMeditation)

def moveReverse(*args, late=False):
    f = Move.addLateMove if late else Move.addMove
    for i in args:
        f(i[0],i[1])
        f(i[1],i[0])

moveReverse(seatedTwist, childsPoseSideStretch, threadTheNeedle)
moveReverse(headToKnee)
moveReverse(cowFace)

wideLegForwardFold.addMove(*standingLegStretch)
forwardFold.addMove(flatBack)
forwardFold.addLateMove(chair)
for i in halfBoundStandingLotus: i.addMove(forwardFold)
for i in bridgeWithRaisedLeg: i.addMove(lieOnBack)
for i in wheelWithRaisedLeg: i.addMove(lieOnBack, wheel)
for i in eagle: i.addMove(forwardFold)
for i in balancingTable: i.addMove(table, child)
for i in standingLegLift4: i.addMove(mountainPose, forwardFold)
for i in chairTwist: i.addMove(chair, forwardFold)
for i in halfMoon: i.addMove(forwardFold)
for i in revolvedHalfMoon: i.addMove(forwardFold)
for i in warrior1: i.addMove(starPose)
for i in warrior2: i.addMove(starPose)
for i in seatedTwist: i.addMove(seatedMeditation)
for i in dancer: i.addMove(forwardFold)
for i in warrior3: i.addMove(forwardFold)
for i in headToKnee: i.addLateMove(hero)
for i in standingSplits: i.addLateMove(handstandHops)
for i in threadTheNeedle: i.addLateMove(child)

doubleAdd(oneLeggedChair, standingLegLift1)
doubleAdd(sidePlank, sideAngle, sidePlankLegUp)
doubleAdd(sidePlank, cresentTwist, late=True)
doubleAdd(sidePlankLegUp, sidePlank, cresentTwist)
doubleAdd(warrior1, warrior2, warrior3, humbleWarrior, cresent)
doubleAdd(humbleWarrior, warrior1)
doubleAdd(humbleWarrior, warrior3, late=True)
doubleAdd(warrior2, sideAngle, triangle, reverseWarrior, cresent)
doubleAdd(threeLeggedDog, lowLunge, kneeToElbow, kneeToNose, warrior1, warrior2, twoLeggedDog, flippedDog)
doubleAdd(twoLeggedDog, threeLeggedDog)
doubleAdd(threeLeggedDog, runningMan, revolvedRunningMan, late=True)
doubleAdd(flippedDog, threeLeggedDog)
doubleAdd(pigeon, threeLeggedDog, kingPigeon)
doubleAdd(kingPigeon, threeLeggedDog)
doubleAdd(kneeToNose, threeLeggedDog)
doubleAdd(kneeToElbow, kneeToOtherElbow, threeLeggedDog, lowLunge, runningMan)
doubleAdd(kneeToOtherElbow, threeLeggedDog)
doubleAdd(kneeToOtherElbow, revolvedRunningMan, late=True)
doubleAdd(lowLunge, warrior1, warrior2, cresent, lizard, standingSplits)
doubleAdd(lowLunge, warrior3, late=True)
doubleAdd(eagle, standingSplits)
doubleAdd(eagle, warrior3, late=True, inverted=True)
doubleAdd(warrior3, standingLegLift1, standingSplits, treePose, eagle, inverted=True)
doubleAdd(warrior3, warrior2)
doubleAdd(cresent, warrior1, cresentTwist, warrior3)
doubleAdd(cresentTwist, cresent, chairTwist, sidePlank)
doubleAdd(balancingTableLegOnly, balancingTable)
doubleAdd(sideAngle, reverseWarrior, sidePlank, warrior2, birdOfParadise, halfMoon)
doubleAdd(boundHalfMoon, late=True)
doubleAdd(birdOfParadise, sideAngle)
doubleAdd(reverseWarrior, sideAngle, warrior2)
doubleAdd(reverseWarrior, sidePlank, late=True)
doubleAdd(standingLegLift1, standingLegLift2, eagle, treePose)
doubleAdd(treePose, halfBoundStandingLotus, eagle, standingLegLift1)
doubleAdd(treePose, warrior3, inverted=True)
doubleAdd(halfBoundStandingLotus, standingLegLift1, treePose)
doubleAdd(halfBoundStandingLotus, standingLotusSquat, late=True)
doubleAdd(standingLotusSquat, flyingPigeon, toestand)
doubleAdd(standingLegLift1, warrior3, inverted=True)
doubleAdd(standingLegLift2, standingLegLift3)
doubleAdd(standingLegLift3, standingLegLift4)
doubleAdd(standingLegLift4, warrior3, inverted=True)
doubleAdd(standingLegLift4, standingSplits, eagle, treePose)
doubleAdd(triangle, revolvedTriangle, pyramid, sideAngle)
doubleAdd(triangle, halfMoon, late=True)
doubleAdd(pyramid, revolvedTriangle)
doubleAdd(standingLegStretch, pyramid)
doubleAdd(chairTwist, sideCrow)
doubleAdd(lizard, runningMan)
doubleAdd(halfMoon, revolvedHalfMoon, warrior3, warrior2)
doubleAdd(revolvedHalfMoon, halfMoon, warrior3, warrior1, cresent)
doubleAdd(revolvedTriangle, revolvedHalfMoon, pyramid, cresentTwist)
doubleAdd(sideCrow, revolvedRunningMan, late=True)
doubleAdd(dancer, standingLegLift1, standingSplits, warrior3)
doubleAdd(dancer, eagle, late=True)


# Aerobics
jumpingJacks = Move("Jumping Jacks", 0, "Jumping Jacks!", 60, mountainPose)
runInPlace = Move("Running In Place", 0, "Run In Place", 60, mountainPose, jumpingJacks)
burpies = Move("Burpies!", 0, "Burpies", 45, vinyasa, forwardFold, plank, extended=[60,75,90])
jumpingSquats = Move("Jumping Squats", 0, "Jumping Squats", 30, chair, forwardFold)
situps = Move("Situps", 0, "Situps", 30, vinyasa, extended=[45,60], lateMove=set([boat]))

# Strength

def linkAerobics():
    chair.addLateMove(jumpingSquats)
    mountainPose.addLateMove(jumpingJacks, runInPlace, burpies)
    jumpingJacks.addLateMove(runInPlace)
    downwardDog.addLateMove(burpies)
    lieOnBack.addLateMove(situps)

def linkSavasana(*args):
    moves = [child, downwardDog, staff, seatedMeditation, mountainPose, table, \
            lieOnBack, lieOnFront] + list(args)
    for i in moves:
        i.addMove(savasana)

def unlinkWarmup():
    mountainPose.removeMove(*standingTwist)
    mountainPose.removeMove(*standingSideStretch)
    backBend.removeMove(*standingSideStretch)
    seatedMeditation.removeMove(table, catCow, *seatedTwist)
    child.removeMove(*childsPoseSideStretch)
    #Remove these impossible moves from imbalances
    moves = set(standingTwist+standingSideStretch+seatedTwist+childsPoseSideStretch)
    for i in range(len(imbalance),0,-1):
        if i in moves: imbalances.pop(i)
    #Also, add these harder moves
    downwardDog.addLateMove(handstandHops)

def linkHarder():
    seatedMeditation.addMove(frog)
    staff.addMove(frog)
    doubleAdd(runningMan,chinStand)
    doubleAdd(threeLeggedDog, pigeon)

def linkCooldown():
    moveReverse(runningMan, sideCrow, flyingPigeon, revolvedRunningMan) #Allow me to just go from one arm balance to the opposite side, to increase the chances I get balanced
    child.addMove(*childsPoseSideStretch)
    downwardDog.addMove(table, child, lieOnBack)
    vinyasa.addMove(child, lieOnBack, staff)
    staff.addMove(hero)
    seatedMeditation.addMove(*cowFace)
    for i in threeLeggedDog: i.addMove(plank)

def routine(li : list, playLast = True, **kwargs):
    """Plays a list of moves. if playLast = False, returns last move instead of playing it"""
    li_copy = li.copy()
    for i in range(len(li)-1):
        current_pose, next_pose = li_copy[i], li_copy[i+1]
        current_pose.play(nextMove=next_pose, **kwargs)
    if not playLast: return li_copy[-1]
    return li_copy[-1].play(**kwargs)

def fixImbalance(pose, imbalance, maxImbalance=1, maxTime = 60, **kwargs):
    """Might try to fix the imbalance. Might not. Depends on how big the imbalance is.
    (Set maxImbalance to 1 to ensure imbalance gets fixed)"""
    fixImbalanceChance = len(imbalance)/maxImbalance
    if random.random() < fixImbalanceChance:
        end = time.time() + maxTime
        while imbalance and time.time() < end:
            print("Current imbalance is:", imbalance)
            try:
                pose = routine(dijkstras.dijkstra(pose,*imbalance,imbalance=imbalance, **kwargs))
            except dijkstras.TimeExceededError:
                print("got TimeExceededError", imbalance)
                break
            except ValueError:
                print("probably impossible...", imbalance)
                break
        if imbalance: print("Timeout: imbalance remains:", imbalance)
    return pose

def main():
    utils.speak("Beginning in")
    print("Beginning in:")
    utils.countdown(3)
    try:
        total_time = 60*int(sys.argv[-1])
    except ValueError:
        print("No time gotten. Using %s minutes" % DEFAULT_TIME)
        total_time = DEFAULT_TIME*60
    start = time.time()
    end = start + total_time
    pose = child.play(time=15)
    try:
        #warmup
        while time.time() - start < max(45,total_time//12):
            nextPose = pose.play(extended=True, early=True) #start slower
            pose = nextPose
        #get me to table:
        child.addMove(downwardDog, plank)
        table.addMove(downwardDog, plank)
        catCow.addMove(downwardDog, plank)
        if aerobics: linkAerobics()
        pose = fixImbalance(pose,imbalance,maxTime=max(45,total_time//10))
        pose = routine(dijkstras.dijkstra(pose, downwardDog), playLast=False) #get me to downwards dog
        unlinkWarmup()
        pose = pose.play(nextMove=plank)
        utils.speak("Alright, warmup over.")
        pose = pose.play()
        #starting main part of workout
        while time.time() - start < total_time//2:
            pose = fixImbalance(pose,imbalance,maxImbalance=10,maxTime=max(60,total_time//12))
            nextPose = pose.play()
            pose = nextPose
        #add harder poses in here
        linkHarder()
        pose = fixImbalance(pose, imbalance, maxTime=max(60, total_time//10))
        utils.speak("We have reached the halfway point")
        #end adding harder poses
        while time.time() < (end - max(60, total_time//10)):
            extendedChance = (time.time() - start)/total_time
            extended = random.random() < extendedChance
            pose = fixImbalance(pose, imbalance, maxImbalance=8, maxTime=max(110,total_time//10))
            nextPose = pose.play(harder=True, extended=extended)
            pose = nextPose
        #add in more restorative poses here
        linkCooldown()
        #one more try to fix that damned imbalance
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(60, total_time//10))
        #move into more restorative poses....
        while time.time() < (end-30):
            nextPose = pose.play(extended=True)
            pose = nextPose
        #deal with imbalances, somehow
        linkSavasana()
        pose = routine(dijkstras.dijkstra(pose,savasana, imbalance=imbalance)) #Somehow, get seamlessly to savasana
    except KeyboardInterrupt:
        linkSavasana()
        pose = routine(dijkstras.dijkstra(pose,savasana))
    finally:
        print(imbalance)
        print("\nTotal Time: " + utils.prettyTime(time.time()-start))

if __name__== "__main__":
    main()

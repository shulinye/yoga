#!/usr/bin/python3

import random
import functools
import operator

import utils

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
    def promoteLate(self, move = None):
        """Promotes a late move up to the normal move pool, if possible.
        If no move given, promotes a random move"""
        if "lateMove" in self.kwargs:
            if move is None:
                try:
                    move = self.kwargs["lateMove"].pop()
                    self.addMove(move)
                except KeyError:
                    pass
            elif move in self.kwargs["lateMove"]:
                self.addMove(move)
                self.kwargs["lateMove"].discard(move)
    def __call__(self, imbalance=[], **kwargs) -> "Move" :
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
            self.promoteLate(nextMove)
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


def moveReverse(*args, late=False):
    f = Move.addLateMove if late else Move.addMove
    for i in args:
        f(i[0],i[1])
        f(i[1],i[0])


def generateMoves(difficulty = 1):
    #Begin list of moves
    movesGraph = {
            'lowPlank': Move("Low Plank", 0, "Lower down into Low Plank. Hold", 10, extended_time=[15,20]),
            'vinyasa': Move("Vinyasa", 0, "Vinyasa", 4, harder="Add in a push up!"),
            'balancingTable': twoSides("Balancing Table", "When you are ready, extend the opposite arm", \
                10, harder="Want a challenge? Extend the same arm."),
            'balancingTableLegOnly': twoSides("Balancing Table, Leg Only", "Extend %(same)s leg behind you", 4),
            'fallenStar': twoSides("Fallen Star","Fallen Star, %(same)s side", 15), #TODO better instructions
            'lowLunge': twoSides("Low Lunge", "Bring your %(same)s foot down and set it between your hands. Low Lunge", 4),
            'threeLeggedDog': twoSides("Three Legged Dog", "Raise your %(same)s foot up. Three Legged Dog", \
                4, extended_time=[15,30]),
            'kneeToNose': twoSides("Knee To Nose", "Take your %(same)s knee and bring it towards your nose. Hold.", \
                15, extended_time=[20,30]),
            'kneeToElbow': twoSides("Knee To Elbow", "Take your %(same)s knee and bring it to your %(same)s elbow. Hold", \
                15, harder="Try to bring your knee up to your forearm!", extended_time=[20,30]),
            }
    movesGraph['plank'] = Move("Plank", 0, "Plank. Hold", 30, movesGraph['lowPlank'], extended_time=[45,60], harder="Throw in a few pushups!")
    movesGraph['catCow'] = Move("Cat Cow", 0, "Cat Cow", 10, movesGraph['plank'], *movesGraph['balancingTableLegOnly'])
    movesGraph['table'] = Move("Table Pose", 0, "Table Pose", 4, movesGraph['catCow'], *movesGraph['balancingTableLegOnly'])
    movesGraph['threadTheNeedle'] = twoSides("Thread The Needle", "Take your %(same)s hand and reach it towards the ceiling. \
            On an exhale, slide it under your other shoulder.", 20, movesGraph['table'])
    movesGraph['oneHandedTiger'] = twoSides("One-Handed Tiger", "Reach back and catch your %(same)s foot with your %(other)s hand. Lean \
            into your hand", 15, movesGraph['table'], movesGraph['catCow'])
    movesGraph['seatedForwardFold'] = Move("Seated Forward Fold", 0, "Seated Forward Fold", 15, movesGraph['vinyasa'])
    movesGraph['flyingStaff'] = Move("Flying Staff Pose", 0, "Press down on the ground. Try to lift your body off the ground", \
            20, movesGraph['vinyasa'])
    movesGraph['staff'] = Move("Staff Pose", 0, "Staff Pose", 10, movesGraph['vinyasa'], movesGraph['seatedForwardFold'], \
            lateMove=set([movesGraph['flyingStaff']]))
    movesGraph['archer'] = twoSides("Archer Pose", "Grab each foot with hand. Try to straighten the %(same)s leg and bend \
            the %(other)s leg, lifting both legs off the ground. Archer Pose.", 30, movesGraph['staff'], movesGraph['vinyasa'])
    movesGraph['butterflyStretch'] = Move("Butterfly Stretch", 0, "Butterfly Stretch", 15, movesGraph['vinyasa'], \
            movesGraph['staff'],lateMove=set(movesGraph['archer']))
    movesGraph['headToKnee'] = twoSides("Head To Knee", "With your %(same)s knee straight and your %(other)s knee bent, \
            reach toward the toes of your %(same)s foot.", 15, movesGraph['staff'], movesGraph['butterflyStretch'])
    movesGraph['child'] = Move("Child's Pose", 0, "Child's Pose", 4, movesGraph['table'], extended_time=[10,15], \
            lateMove=set([movesGraph['catCow']]))
    movesGraph['seatedTwist'] = twoSides("Seated Twist", "Twist to the %(same)s side", 10, movesGraph['vinyasa'])
    movesGraph['scale'] = Move("Scale Pose", 0, "Push upwards with your hands. Try to get your entire body off the ground. Scale Pose", \
            15, movesGraph['vinyasa'])
    movesGraph['seatedMeditation'] = Move("Seated Meditation", 0, "Seated Meditation", 4, movesGraph['child'], movesGraph['table'], \
            movesGraph['catCow'], movesGraph['butterflyStretch'], movesGraph['staff'], *movesGraph['seatedTwist'], \
            extended_time=[20,30,40], lateMove=set([movesGraph['scale'], movesGraph['vinyasa']]))
    movesGraph['childsPoseSideStretch'] = twoSides("Child's Pose, Side Stretch", "Reach your fingers over to your %(same)s side. \
            You should feel a stretch across your %(other)s side body", 8, movesGraph['child'], movesGraph['table'], \
            movesGraph['seatedMeditation'])
    movesGraph['kneeToOtherElbow'] = twoSides("Knee To Other Elbow", "Take your %(same)s knee and bring it across your body to \
            your %(other)s elbow", 15, movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['standingLegLift1'] = twoSides("Standing Leg Lift", "Raise your %(same)s foot up and grab it with your %(same) hand. \
            Standing Leg Lift. Hold", 20, extended_time=[30,45,60])
    movesGraph['standingLegLift2'] = twoSides("Standing Leg Lift, Leg to Side", "Now take your %(same)s foot and move it out to the side. Hold", \
        20, extended_time=[30,45,60])
    movesGraph['standingLegLift3'] = twoSides("Standing Leg Lift, Both Hands", "Return %(same)s foot to center. \
        Grab with both hands, head to knee or chin to shin. Hold.", 20, extended_time=[30,45,60])
    movesGraph['standingLegLift4'] = twoSides("Standing Leg Lift, No Hands", "Release %(same)s foot. Hold foot up towards ceiling.", \
        25, extended_time=[30,45,60])
    movesGraph['eagle'] = twoSides("Eagle Pose", "Take your %(same)s foot and twist it over your %(other)s leg. Twine your arms, %(same) arm lower. Eagle Pose", 25, extended_time=[40],\
        harder="Bring your elbows to your knees, and then straighten. Repeat")
    movesGraph['tree'] = twoSides("Tree Pose", "Tree Pose, %(same)s side", 25, movesGraph['vinyasa'], extended_time=[45,60])
    movesGraph['halfBoundStandingLotus'] = twoSides("Half-Bound Standing Lotus", "Take your %(same)s foot and put it at the top of your %(other)s thigh. \
            With your %(same)s hand, reach behind you and grab your %(same)s foot", 15, movesGraph['vinyasa'], \
            harder="Lean forwards and touch the ground with your free hand.", extended_time=[30,45])
    movesGraph['standingLotusSquat'] = twoSides("Standing Lotus Squat", "Bend your %(other)s thigh and squat down", 15, movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['toestand'] = twoSides("Toestand", "Continue bending down, rise up onto the toes of your %(other)s foot", \
            15, movesGraph['vinyasa'], harder="Try to get your hands to your heart!", extended_time=[20,30])
    movesGraph['flyingPigeon'] = twoSides("Flying Pigeon", "Plant your hands on the ground and lift your %(same)s foot. Flying Pigeon", \
            30, movesGraph['vinyasa'])
    movesGraph['dancer'] = twoSides("Dancer Pose", "Dancer Pose, %(same)s side", 25, movesGraph['vinyasa'], extended_time=[25,45])
    movesGraph['backBend'] = Move("Back Bend", 0, "Raise your hands towards the ceiling and bend backwards", 10, movesGraph['vinyasa'])
    movesGraph['wideLegStance'] = Move("Wide Leg Stance", 0, "Wide Leg Stance", 4)
    movesGraph['wideLegForwardFold'] = Move("Wide Leg Forward Fold", 0, "Wide Leg Forward Fold",15, movesGraph['wideLegStance'])
    movesGraph['armPressurePose'] = Move("Arm Pressure Pose", 0, "Wrap legs around shoulders. Attempt to balance on arms.", \
            30, movesGraph['wideLegForwardFold'])
    movesGraph['standingLegStretch'] = twoSides("Standing Leg Stretch", "Reach for your %(same)s foot", \
            10, movesGraph['wideLegStance'], movesGraph['wideLegForwardFold'])
    movesGraph['mountain'] = Move("Mountain Pose", 0, "Mountain Pose", 4, movesGraph['backBend'], movesGraph['wideLegStance'], \
            *movesGraph['standingLegLift1'], extended_time=[10])
    movesGraph['standingSideStretch'] = twoSides("Standing Side Stretch", "Lean to the %(same)s side", \
            10, movesGraph['backBend'], movesGraph['mountain'])
    movesGraph['standingTwist'] = twoSides("Standing Twist", "Bring your arms up to shoulder level and twist to the %(same)s", \
            15, movesGraph['mountain'])
    movesGraph['forwardFoldShoulderStretch'] = Move("Forward Fold, Shoulder Stretch", 0, \
            "Clasp your hands together behind your head and allow gravity to drag your pinkies towards the floor", \
            10, movesGraph['mountain'], extended_time=[15,20])
    movesGraph['forwardFold'] = Move("Forward Fold", 0, "Forward Fold", 3, movesGraph['mountain'], \
            movesGraph['forwardFoldShoulderStretch'])
    movesGraph['flatBack'] = Move("Flat Back", 0, "Flat Back", 3, movesGraph['forwardFold'], movesGraph['vinyasa'])
    movesGraph['forearmBalance'] = Move("Forearm Balance", 0, "Forearm Balance", 30, movesGraph['child'], extended_time=[45])
    movesGraph['dolphin'] = Move("Dolphin Pose", 0, "Dolphin Pose", 30, movesGraph['vinyasa'], \
            lateMove = set([movesGraph['forearmBalance']]), extended_time=[45])
    movesGraph['downwardDog'] = Move("Downwards Dog", 0, "Downwards Dog", 4, movesGraph['forwardFold'], movesGraph['staff'], \
            movesGraph['plank'], movesGraph['dolphin'], *movesGraph['threeLeggedDog'], extended_time=[10])
    movesGraph['upwardDog'] = Move("Upward Dog", 0, "Upward Dog", 4, movesGraph['downwardDog'], extended_time=[10,20])
    movesGraph['humbleWarrior'] = twoSides("Humble Warrior", "Intertwine your hands behind you. Lean forward. Humble Warrior", \
            4, movesGraph['vinyasa'])
    movesGraph['warrior1'] = twoSides("Warrior 1", "Warrior One, %(same)s Side", 10, movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['warrior2'] = twoSides("Warrior 2", "Warrior Two, %(same)s Side", 10, movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['warrior3'] = twoSides("Warrior 3", "Warrior Three, %(same)s Side", 10, movesGraph['vinyasa'], \
            harder="Bring your elbows to your knee, and then extend! Repeat", extended_time=[20,30,45])
    movesGraph['standingSplits'] = twoSides("Standing Splits", "Raise your %(same)s foot up towards the ceiling. Standing Splits", \
            20, movesGraph['vinyasa'], extended_time=[30])
    movesGraph['lizard'] = twoSides("Lizard Pose", "Lizard Pose, %(same)s side", 30, movesGraph['vinyasa'], \
            bind=True, harder="Lower yourself onto your forearms", extended_time=[45,60])
    movesGraph['chinStand'] = twoSides("Chin Stand", "Chin Stand, %(same)s side", 30, movesGraph['vinyasa'])
    movesGraph['runningMan'] = twoSides("Running Man", "Running Man, %(same)s side", 30, movesGraph['vinyasa'])
    movesGraph['revolvedRunningMan'] = twoSides("Revolved Running Man", "Revolved Running Man, %(same)s side", \
            30, movesGraph['vinyasa'])
    movesGraph['cresent'] = twoSides("Cresent Lunge", "Cresent Lunge, %(same)s foot forward", 10, \
            early="Feel free to lower your other knee down to the ground", extended_time=[20,30])
    movesGraph['cresentTwist'] = twoSides("Cresent Twist", "Cresent Twist. Twist to the %(same)s side.", 15, bind=True)
    movesGraph['chairTwist'] = twoSides("Chair Twist", "Chair Twist. Twist to the %(same)s side", 15, bind=True)
    movesGraph['chair'] = Move("Chair Pose", 0, "Chair Pose", 15, movesGraph['vinyasa'], *movesGraph['chairTwist'], extended_time=[30, 40, 60])
    movesGraph['oneLeggedChair'] = twoSides("One Legged Chair", "Shift all your weight to your %(other)s foot. Grab your %(same)s \
            foot with your %(same)s hand. Raise %(same)s foot", 15, movesGraph['chair'], extended_time=[20,30])
    movesGraph['crow'] = Move("Crow Pose", 0, "Crow Pose", 30, movesGraph['vinyasa'])
    movesGraph['crane'] = Move("Crane Pose", 0, "Crane Pose", 30, movesGraph['vinyasa'])
    movesGraph['sideCrow'] = twoSides("Side Crow", "Side Crow, %(same)s Side", 30, movesGraph['vinyasa'])
    movesGraph['boat'] = Move("Boat Pose", 0, "Boat Pose", 30, movesGraph['staff'], extended_time=[45,60])
    movesGraph['boatLift'] = Move("Boat Lift", 0, "Cross one ankle over the other, plant your hands and lift", 10, movesGraph['boat'])
    movesGraph['boatTwist'] = Move("Boat Twist", 0, "Point your fingers towards the right and your ankles towards the left. Now reverse. Repeat", \
            20, movesGraph['boat'], movesGraph['staff'], movesGraph['vinyasa'], extended_time=[30,40])
    movesGraph['lowBoat'] = Move("Low Boat Pose", 0, "Lower down into Low Boat Pose", \
            15, movesGraph['boat'], movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['revolvedHalfMoon'] = twoSides("Revolved Half Moon", "Revolved Half Moon, %(same)s Side", 20, extended_time=[30])
    movesGraph['halfMoon'] = twoSides("Half Moon", "Half Moon, %(same)s Side", 20, harder="Try to take your hand off the ground!", extended_time=[30])
    movesGraph['sideAngle'] = twoSides("Side Angle", "Side Angle", 10, movesGraph['vinyasa'], extended_time=[20])
    movesGraph['sidePlank'] = twoSides("Side Plank", "Side Plank, %(same)s side", 15, movesGraph['plank'], movesGraph['vinyasa'], \
            extended_time=[30,40])
    movesGraph['sidePlankLegUp'] = twoSides("Side Plank, Leg Up", "Now raise your %(same)s leg up and hold", 15, extended_time=[20,25,30])
    movesGraph['triangle'] = twoSides("Triangle Pose", "Triangle Pose, %(same)s side", 15, movesGraph['vinyasa'], bind=True)
    movesGraph['pyramid'] = twoSides("Pyramid Pose", "Pyramid Pose, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['revolvedTriangle'] = twoSides("Revolved Triangle", "Revolved Triangle Pose, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['reverseWarrior'] = twoSides("Reverse Warrior", "Take your %(same)s hand and raise it towards the back of the room. Reverse Warrior", \
            4, extended_time=[10])
    movesGraph['bridge'] = Move("Bridge Pose", 0, "Bridge Pose", 20)
    movesGraph['bridgeWithRaisedLeg'] = twoSides("Bridge, with Raised Leg", "Raise your %(same)s leg into the air", \
            15, movesGraph['bridge'], extended_time =[20,30])
    movesGraph['wheelWithRaisedLeg'] = twoSides("Wheel, with Raised Leg", "Raise your %(same)s leg into the air", 15)
    movesGraph['wheel'] = Move("Wheel Pose", 0, "Wheel Pose", 30, movesGraph['vinyasa'], \
            extended_time=[45,60], harder="Try to straighten your legs", lateMove=set(movesGraph['wheelWithRaisedLeg']))
    movesGraph['camel'] = Move("Camel Pose", 0, "Camel Pose", 30, movesGraph['vinyasa'])
    movesGraph['superMan'] = Move("Super Man", 0, "Raise both your hands and your feet off the ground at the same time. Hold", \
            15, movesGraph['vinyasa'])
    movesGraph['bow'] = Move("Bow Pose", 0, "Grab your feet with both hands and raise upwards", \
            15, movesGraph['vinyasa'], extended_time=[20,30,40])
    movesGraph['fish'] = Move("Fish Pose", 0, "Fish Pose", 20, movesGraph['vinyasa'])
    movesGraph['supportedShoulderStand'] = Move("Supported Shoulder Stand", 0, "Supported Shoulder Stand", 30, movesGraph['fish'])
    movesGraph['plow'] = Move("Plow Pose", 0, "Plow Pose", 30, movesGraph['supportedShoulderStand'])
    movesGraph['upwardPlank'] = Move("Upward Plank", 0, "Upward Plank", 30, movesGraph['vinyasa'])
    movesGraph['upwardPlankLiftedLeg'] = twoSides("Upward Plank, Lifted Leg", "Lift your %(same)s leg. Upward Plank, %(same)s leg lifted", \
        15, movesGraph['upwardPlank'], movesGraph['vinyasa'])
    movesGraph['lieOnBack'] = Move("Lie On Back", 0, "Lie on Your Back", 4, movesGraph['supportedShoulderStand'], movesGraph['upwardPlank'], \
            movesGraph['vinyasa'])
    movesGraph['spinalTwist'] = twoSides("Spinal Twist","Bring your knees up to your chest, and then let them fall to the %(same)s. \
            Look towards your %(other)s hand. Spinal Twist", 20, movesGraph['lieOnBack'])
    movesGraph['lieOnFront'] = Move("Lie On Front", 0, "Lie on Your Stomach", 4, movesGraph['superMan'], movesGraph['bow'], movesGraph['lieOnBack'], \
            movesGraph['vinyasa'], lateMove=set([movesGraph['plank']]))
    movesGraph['yogaBicycles'] = Move("Bicycles", 0, "Bicycles", 30, movesGraph['lieOnBack'], movesGraph['vinyasa'], extended_time=[45, 60])
    movesGraph['savasana'] = Move("Savasana", 0, "Sahvahsahnah", 30, None)
    movesGraph['star'] = Move('Star Pose', 0, "Star Pose", 10, movesGraph['mountain'], *movesGraph['warrior1'])
    movesGraph['goddessSquat'] = Move('Goddess Squat', 0, "Goddess Squat", 5, movesGraph['star'])
    movesGraph['supportedHeadstand'] = Move('Supported Headstand', 0, "Supported Headstand", 30, movesGraph['child'])
    movesGraph['pigeon'] = twoSides('Pigeon Pose', "Pigeon Pose, %(same)s side", 30, movesGraph['vinyasa'])
    movesGraph['kingPigeon'] = twoSides('King Pigeon', "King Pigeon, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['birdOfParadise'] = twoSides('Bird of Paradise', 'Bird of Paradise', 30)
    movesGraph['boundHalfMoon'] = twoSides('Bound Half Moon', 'Bound Half Moon', 30)
    movesGraph['handstandHops'] = Move('Handstand Hops', 0, "Handstand Hops", 30, movesGraph['vinyasa'])
    movesGraph['twoLeggedDog'] = twoSides('Two Legged Dog', "Now raise your %(other)s hand. Hold", 20, lateMove=set([movesGraph['vinyasa']]))
    movesGraph['flippedDog'] = twoSides('Flipped Dog', "Flipped Dog, %(same)s side", 20)
    movesGraph['feetUpAWall'] = Move("Feet Up A Wall", 0, "Feet Up A Wall", 4, movesGraph['lowBoat'], movesGraph['boat'], extended_time=[15,30])
    movesGraph['hero'] = Move("Hero Pose", 0, "Tuck both feet under your glutes. Lean back as far as possible. Hero Pose", 20, movesGraph['seatedMeditation'])
    movesGraph['deepSquat'] = Move("Deep Squat", 0, "Squat as deeply as you can", 30, movesGraph['vinyasa'], movesGraph['chair'], lateMove=set([movesGraph['crow']]))
    movesGraph['frog'] = Move("Frog Pose", 0, "Frog Pose", 30, movesGraph['seatedMeditation'], movesGraph['vinyasa'])
    movesGraph['cowFace'] = twoSides('Cow-Facing Pose', 'Cow-Facing Pose', 30, movesGraph['seatedMeditation'], movesGraph['child']) #TODO: more useful instructions

    #Begin linking moves to each other
    movesGraph['wideLegStance'].addMove(movesGraph['mountain'], movesGraph['star'], movesGraph['wideLegForwardFold'], *movesGraph['warrior2'])
    movesGraph['wideLegStance'].addLateMove(movesGraph['armPressurePose'], *movesGraph['cresent'])
    movesGraph['vinyasa'].addMove(movesGraph['downwardDog'])
    movesGraph['table'].addMove(*movesGraph['threadTheNeedle'])
    movesGraph['catCow'].addMove(movesGraph['table'])
    movesGraph['mountain'].addMove(movesGraph['forwardFold'], movesGraph['chair'], *movesGraph['standingTwist'])
    movesGraph['mountain'].addMove(*movesGraph['standingSideStretch'])
    movesGraph['mountain'].addLateMove(*movesGraph['dancer'])
    movesGraph['backBend'].addMove(movesGraph['mountain'], movesGraph['forwardFold'], *movesGraph['standingSideStretch'])
    movesGraph['staff'].addMove(movesGraph['lieOnBack'], movesGraph['butterflyStretch'], movesGraph['camel'], movesGraph['boat'])
    movesGraph['staff'].addLateMove(movesGraph['yogaBicycles'], movesGraph['mountain'])
    movesGraph['downwardDog'].addMove(movesGraph['plank'])
    movesGraph['flatBack'].addMove(movesGraph['forwardFold'])
    movesGraph['flatBack'].addLateMove(movesGraph['chair'], movesGraph['deepSquat'])
    movesGraph['lieOnBack'].addMove(movesGraph['yogaBicycles'], movesGraph['bridge'], movesGraph['staff'], movesGraph['seatedMeditation'], movesGraph['lieOnFront'], \
            movesGraph['feetUpAWall'],*movesGraph['spinalTwist'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['wheel'])
    movesGraph['plow'].addMove(movesGraph['fish'])
    movesGraph['upwardPlank'].addMove(movesGraph['lieOnBack'])
    movesGraph['upwardPlank'].addLateMove(*movesGraph['upwardPlankLiftedLeg'])
    movesGraph['supportedShoulderStand'].addMove(movesGraph['plow'])
    movesGraph['plank'].addMove(movesGraph['vinyasa'], *movesGraph['sidePlank'])
    movesGraph['lowPlank'].addMove(movesGraph['upwardDog'], movesGraph['vinyasa'])
    movesGraph['lowPlank'].addLateMove(movesGraph['plank'])
    movesGraph['child'].addMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['child'].addLateMove(movesGraph['seatedMeditation'])
    movesGraph['boat'].addMove(movesGraph['lowBoat'], movesGraph['boatLift'], movesGraph['boatTwist'])
    movesGraph['lowBoat'].addMove(movesGraph['yogaBicycles'])
    movesGraph['chair'].addMove(movesGraph['deepSquat'], *movesGraph['oneLeggedChair'])
    movesGraph['star'].addMove(movesGraph['goddessSquat'], movesGraph['deepSquat'])
    movesGraph['bridge'].addMove(movesGraph['lieOnBack'], *movesGraph['bridgeWithRaisedLeg'])
    movesGraph['fish'].addMove(movesGraph['lieOnBack'])
    movesGraph['seatedMeditation'].addLateMove(movesGraph['mountain'], movesGraph['boat'], movesGraph['yogaBicycles'])
    movesGraph['seatedForwardFold'].addMove(movesGraph['seatedMeditation'], *movesGraph['headToKnee'])
    movesGraph['forwardFoldShoulderStretch'].addMove(movesGraph['forwardFold'], movesGraph['chair'])
    movesGraph['butterflyStretch'].addMove(*movesGraph['headToKnee'])
    movesGraph['superMan'].addMove(movesGraph['lieOnFront'])
    movesGraph['bow'].addMove(movesGraph['lieOnFront'])
    movesGraph['scale'].addMove(movesGraph['seatedMeditation'])
    movesGraph['wideLegForwardFold'].addMove(*movesGraph['standingLegStretch'])
    movesGraph['forwardFold'].addMove(movesGraph['flatBack'])
    movesGraph['forwardFold'].addLateMove(movesGraph['chair'])
    for i in movesGraph['halfBoundStandingLotus']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['bridgeWithRaisedLeg']: i.addMove(movesGraph['lieOnBack'])
    for i in movesGraph['wheelWithRaisedLeg']: i.addMove(movesGraph['lieOnBack'], movesGraph['wheel'])
    for i in movesGraph['eagle']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['balancingTable']: i.addMove(movesGraph['table'], movesGraph['child'])
    for i in movesGraph['standingLegLift4']: i.addMove(movesGraph['mountain'], movesGraph['forwardFold'])
    for i in movesGraph['chairTwist']: i.addMove(movesGraph['chair'], movesGraph['forwardFold'])
    for i in movesGraph['halfMoon']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['revolvedHalfMoon']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['warrior1']: i.addMove(movesGraph['star'])
    for i in movesGraph['warrior2']: i.addMove(movesGraph['star'])
    for i in movesGraph['seatedTwist']: i.addMove(movesGraph['seatedMeditation'])
    for i in movesGraph['dancer']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['warrior3']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['headToKnee']: i.addLateMove(movesGraph['hero'])
    for i in movesGraph['standingSplits']: i.addLateMove(movesGraph['handstandHops'])
    for i in movesGraph['threadTheNeedle']: i.addLateMove(movesGraph['child'])
    for i in movesGraph['fallenStar']: i.addMove(movesGraph['table'])

    moveReverse(movesGraph['seatedTwist'], movesGraph['childsPoseSideStretch'], movesGraph['threadTheNeedle'])
    moveReverse(movesGraph['headToKnee'])
    moveReverse(movesGraph['cowFace'])

    doubleAdd(movesGraph['oneLeggedChair'], movesGraph['standingLegLift1'])
    doubleAdd(movesGraph['sidePlank'], movesGraph['sideAngle'], movesGraph['sidePlankLegUp'])
    doubleAdd(movesGraph['sidePlank'], movesGraph['cresentTwist'], late=True, inverted=True)
    doubleAdd(movesGraph['sidePlankLegUp'], movesGraph['sidePlank'])
    doubleAdd(movesGraph['sidePlankLegUp'], movesGraph['cresentTwist'], inverted=True)
    doubleAdd(movesGraph['threadTheNeedle'], movesGraph['fallenStar'])
    doubleAdd(movesGraph['warrior1'], movesGraph['warrior2'], movesGraph['warrior3'], movesGraph['humbleWarrior'], movesGraph['cresent'])
    doubleAdd(movesGraph['humbleWarrior'], movesGraph['warrior1'])
    doubleAdd(movesGraph['humbleWarrior'], movesGraph['warrior3'], late=True)
    doubleAdd(movesGraph['warrior2'], movesGraph['sideAngle'], movesGraph['triangle'], movesGraph['reverseWarrior'], movesGraph['cresent'])
    doubleAdd(movesGraph['threeLeggedDog'], movesGraph['lowLunge'], movesGraph['kneeToElbow'], movesGraph['kneeToNose'], movesGraph['warrior1'], \
            movesGraph['warrior2'], movesGraph['twoLeggedDog'], movesGraph['flippedDog'])
    doubleAdd(movesGraph['twoLeggedDog'], movesGraph['threeLeggedDog'])
    doubleAdd(movesGraph['threeLeggedDog'], movesGraph['runningMan'], movesGraph['revolvedRunningMan'], late=True)
    doubleAdd(movesGraph['flippedDog'], movesGraph['threeLeggedDog'])
    doubleAdd(movesGraph['pigeon'], movesGraph['threeLeggedDog'], movesGraph['kingPigeon'])
    doubleAdd(movesGraph['kingPigeon'], movesGraph['threeLeggedDog'])
    doubleAdd(movesGraph['kneeToNose'], movesGraph['threeLeggedDog'])
    doubleAdd(movesGraph['kneeToElbow'], movesGraph['kneeToOtherElbow'], movesGraph['threeLeggedDog'], movesGraph['lowLunge'], \
            movesGraph['runningMan'])
    doubleAdd(movesGraph['kneeToOtherElbow'], movesGraph['threeLeggedDog'])
    doubleAdd(movesGraph['kneeToOtherElbow'], movesGraph['revolvedRunningMan'], late=True)
    doubleAdd(movesGraph['lowLunge'], movesGraph['warrior1'], movesGraph['warrior2'], movesGraph['cresent'], movesGraph['lizard'])
    doubleAdd(movesGraph['lowLunge'], movesGraph['standingSplits'], inverted=True)
    doubleAdd(movesGraph['lowLunge'], movesGraph['warrior3'], late=True)
    doubleAdd(movesGraph['eagle'], movesGraph['standingSplits'])
    doubleAdd(movesGraph['eagle'], movesGraph['warrior3'], late=True, inverted=True)
    doubleAdd(movesGraph['warrior3'], movesGraph['standingLegLift1'], movesGraph['standingSplits'], movesGraph['tree'], movesGraph['eagle'], \
            inverted=True)
    doubleAdd(movesGraph['warrior3'], movesGraph['warrior2'])
    doubleAdd(movesGraph['cresent'], movesGraph['warrior1'], movesGraph['cresentTwist'], movesGraph['warrior3'])
    doubleAdd(movesGraph['cresentTwist'], movesGraph['cresent'], movesGraph['chairTwist'], movesGraph['sidePlank'])
    doubleAdd(movesGraph['balancingTableLegOnly'], movesGraph['balancingTable'])
    doubleAdd(movesGraph['sideAngle'], movesGraph['reverseWarrior'], movesGraph['sidePlank'], movesGraph['warrior2'], movesGraph['birdOfParadise'], \
            movesGraph['halfMoon'])
    doubleAdd(movesGraph['sideAngle'], movesGraph['boundHalfMoon'], late=True)
    doubleAdd(movesGraph['boundHalfMoon'], movesGraph['sideAngle'])
    doubleAdd(movesGraph['birdOfParadise'], movesGraph['sideAngle'])
    doubleAdd(movesGraph['reverseWarrior'], movesGraph['sideAngle'], movesGraph['warrior2'])
    doubleAdd(movesGraph['reverseWarrior'], movesGraph['sidePlank'], late=True)
    doubleAdd(movesGraph['standingLegLift1'], movesGraph['standingLegLift2'], movesGraph['eagle'], movesGraph['tree'])
    doubleAdd(movesGraph['tree'], movesGraph['halfBoundStandingLotus'], movesGraph['eagle'], movesGraph['standingLegLift1'])
    doubleAdd(movesGraph['tree'], movesGraph['warrior3'], inverted=True)
    doubleAdd(movesGraph['halfBoundStandingLotus'], movesGraph['standingLegLift1'], movesGraph['tree'])
    doubleAdd(movesGraph['halfBoundStandingLotus'], movesGraph['standingLotusSquat'], late=True)
    doubleAdd(movesGraph['standingLotusSquat'], movesGraph['flyingPigeon'], movesGraph['toestand'])
    doubleAdd(movesGraph['standingLegLift1'], movesGraph['warrior3'], inverted=True)
    doubleAdd(movesGraph['standingLegLift2'], movesGraph['standingLegLift3'])
    doubleAdd(movesGraph['standingLegLift3'], movesGraph['standingLegLift4'])
    doubleAdd(movesGraph['standingLegLift4'], movesGraph['warrior3'], inverted=True)
    doubleAdd(movesGraph['standingLegLift4'], movesGraph['standingSplits'], movesGraph['eagle'], movesGraph['tree'])
    doubleAdd(movesGraph['triangle'], movesGraph['revolvedTriangle'], movesGraph['pyramid'], movesGraph['sideAngle'])
    doubleAdd(movesGraph['triangle'], movesGraph['halfMoon'], late=True)
    doubleAdd(movesGraph['pyramid'], movesGraph['revolvedTriangle'])
    doubleAdd(movesGraph['standingLegStretch'], movesGraph['pyramid'])
    doubleAdd(movesGraph['chairTwist'], movesGraph['sideCrow'])
    doubleAdd(movesGraph['lizard'], movesGraph['runningMan'])
    doubleAdd(movesGraph['halfMoon'], movesGraph['revolvedHalfMoon'], movesGraph['warrior3'], movesGraph['warrior2'])
    doubleAdd(movesGraph['revolvedHalfMoon'], movesGraph['halfMoon'], movesGraph['warrior3'], movesGraph['warrior1'], movesGraph['cresent'])
    doubleAdd(movesGraph['revolvedTriangle'], movesGraph['revolvedHalfMoon'], movesGraph['pyramid'], movesGraph['cresentTwist'])
    doubleAdd(movesGraph['sideCrow'], movesGraph['revolvedRunningMan'], late=True)
    doubleAdd(movesGraph['dancer'], movesGraph['standingLegLift1'], movesGraph['standingSplits'], movesGraph['warrior3'])
    doubleAdd(movesGraph['dancer'], movesGraph['eagle'], late=True)
    return movesGraph

def linkAerobics(movesGraph):
    movesGraph['jumpingJacks'] = Move("Jumping Jacks", 0, "Jumping Jacks!", 60, movesGraph['mountain'])
    movesGraph['runInPlace'] = Move("Running In Place", 0, "Run In Place", 60, movesGraph['mountain'], movesGraph['jumpingJacks'])
    movesGraph['burpies'] = Move("Burpies!", 0, "Burpies", 45, movesGraph['vinyasa'], movesGraph['forwardFold'], movesGraph['plank'], extended=[60,75,90])
    movesGraph['jumpingSquats'] = Move("Jumping Squats", 0, "Jumping Squats", 30, movesGraph['chair'], movesGraph['forwardFold'])
    movesGraph['situps'] = Move("Situps", 0, "Situps", 30, movesGraph['vinyasa'], extended=[45,60], lateMove=set([movesGraph['boat']]))
    movesGraph['chair'].addLateMove(movesGraph['jumpingSquats'])
    movesGraph['mountain'].addLateMove(movesGraph['jumpingJacks'], movesGraph['runInPlace'], movesGraph['burpies'])
    movesGraph['jumpingJacks'].addLateMove(movesGraph['runInPlace'])
    movesGraph['downwardDog'].addLateMove(movesGraph['burpies'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['situps'])


def linkStrength(movesGraph):
    movesGraph['pushups'] = Move("Pushups", 0, "Pushups", 30, movesGraph['vinyasa'])

def linkSavasana(movesGraph, *args):
    moves = ['child', 'downwardDog', 'staff', 'seatedMeditation', 'mountain', 'table', \
            'lieOnBack', 'lieOnFront']
    for i in moves:
        movesGraph[i].addMove(movesGraph['savasana'])
    for i in args:
        i.addMove(movesGraph['savasana'])

def linkMain(movesGraph) -> None:
    for i in ['child', 'table', 'catCow']:
        movesGraph[i].addMove(movesGraph['downwardDog'], movesGraph['plank'])

def unlinkWarmup(movesGraph, imbalance=[]):
    movesGraph['mountain'].removeMove(*movesGraph['standingTwist'])
    movesGraph['mountain'].removeMove(*movesGraph['standingSideStretch'])
    movesGraph['backBend'].removeMove(*movesGraph['standingSideStretch'])
    movesGraph['seatedMeditation'].removeMove(movesGraph['table'], movesGraph['catCow'], *movesGraph['seatedTwist'])
    movesGraph['child'].removeMove(*movesGraph['childsPoseSideStretch'])
    #Remove these impossible moves from imbalances
    moves = set(functools.reduce(operator.add,[movesGraph[i] for i in ('standingTwist','standingSideStretch','seatedTwist','childsPoseSideStretch')]))
    for i in range(len(imbalance),0,-1):
        if i in moves: imbalances.pop(i)
    return imbalance

def linkHarder(movesGraph) -> None:
    """Links some harder moves."""
    movesGraph['seatedMeditation'].addMove(movesGraph['frog'])
    movesGraph['staff'].addMove(movesGraph['frog'])
    doubleAdd(movesGraph['runningMan'], movesGraph['chinStand'])
    doubleAdd(movesGraph['threeLeggedDog'], movesGraph['pigeon'])
    movesGraph['downwardDog'].addLateMove(movesGraph['handstandHops'])

def linkCooldown(movesGraph) -> None:
    #Allow me to just go from one arm balance to the opposite side, to increase the chances I get balanced
    moveReverse(movesGraph['runningMan'], movesGraph['sideCrow'], movesGraph['flyingPigeon'], \
            movesGraph['revolvedRunningMan'], movesGraph['chinStand'])
    movesGraph['child'].addMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['downwardDog'].addMove(movesGraph['table'], movesGraph['child'], movesGraph['lieOnBack'])
    movesGraph['vinyasa'].addMove(movesGraph['child'], movesGraph['lieOnBack'], movesGraph['staff'])
    movesGraph['staff'].addMove(movesGraph['hero'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['cowFace'])
    for i in movesGraph['threeLeggedDog']: i.addMove(movesGraph['plank'])


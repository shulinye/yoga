#!/usr/bin/python3

from models import Move

def generateMoves(difficulty = 1):
    # Begin list of moves
    movesGraph = {
            'lowPlank': Move("Low Plank", 0, "Lower down into Low Plank. Hold", 10 + 2*difficulty, \
                    extended_time=Move.reDifficultyTimes([20,30],3,difficulty)),
            'vinyasa': Move("Vinyasa", 0, "Vinyasa", 5 - difficulty, harder="Add in a push up!"),
            'balancingTable': Move.twoSides("Balancing Table", "When you are ready, extend the opposite arm", \
                10, harder="Want a challenge? Extend the same arm."),
            'balancingTableLegOnly': Move.twoSides("Balancing Table, Leg Only", "Extend %(same)s leg behind you", 5 - difficulty),
            'fallenStar': Move.twoSides("Fallen Star","Fallen Star, %(same)s side", 15), #TODO better instructions
            'lowLunge': Move.twoSides("Low Lunge", "Bring your %(same)s foot down and set it between your hands. Low Lunge", max(4 - 2*difficulty,0)),
            'threeLeggedDog': Move.twoSides("Three Legged Dog", "Raise your %(same)s foot up. Three Legged Dog", \
                max(5 - 2*difficulty,0), extended_time=Move.reDifficultyTimes([15,30],3,difficulty)),
            'kneeToNose': Move.twoSides("Knee To Nose", "Take your %(same)s knee and bring it towards your nose. Hold.", \
                15 + 2*difficulty, extended_time=Move.reDifficultyTimes([20,30], 3, difficulty)),
            'kneeToElbow': Move.twoSides("Knee To Elbow", "Take your %(same)s knee and bring it to your %(same)s elbow. Hold", \
                15 + 2*difficulty, harder="Try to bring your knee up to your forearm!", extended_time=Move.reDifficultyTimes([20,30],3,difficulty)),
            }
    movesGraph['plank'] = Move("Plank", 0, "Plank. Hold", 25 + 5*difficulty, movesGraph['lowPlank'], \
            extended_time=Move.reDifficultyTimes([40,60],5, difficulty), harder="Throw in a few pushups!", countdown=True)
    movesGraph['oneLeggedPlank'] = Move.twoSides("One Legged Plank", "Raise your %(same)s foot", 10 + difficulty, movesGraph['vinyasa'])
    movesGraph['twoPointPlank'] = Move.twoSides("Two Point Plank", "Now raise your %(other)s hand", 10 + difficulty, movesGraph['vinyasa'])
    movesGraph['catCow'] = Move("Cat Cow", 0, "Cat Cow", 10, movesGraph['plank'], *movesGraph['balancingTableLegOnly'], extended_time=[15])
    movesGraph['table'] = Move("Table Pose", 0, "Table Pose", 5-difficulty, movesGraph['catCow'], *movesGraph['balancingTableLegOnly'], \
            extended_time=[10-2*difficulty])
    movesGraph['threadTheNeedle'] = Move.twoSides("Thread The Needle", "Take your %(same)s hand and reach it towards the ceiling. \
            On an exhale, slide it under your other shoulder.", 20-4*difficulty, movesGraph['table'], lateMove=set([movesGraph['catCow']]))
    movesGraph['oneHandedTiger'] = Move.twoSides("One-Handed Tiger", "Reach back and catch your %(same)s foot with your %(other)s hand. Lean \
            into your hand", 15, movesGraph['table'], movesGraph['catCow'])
    movesGraph['seatedForwardFold'] = Move("Seated Forward Fold", 0, "Seated Forward Fold", 15, movesGraph['vinyasa'])
    movesGraph['flyingStaff'] = Move("Flying Staff Pose", 0, "Press down on the ground. Try to lift your body off the ground", \
            20, movesGraph['vinyasa'])
    movesGraph['staff'] = Move("Staff Pose", 0, "Staff Pose", 10, movesGraph['vinyasa'], movesGraph['seatedForwardFold'])
    if difficulty >= 1: movesGraph['staff'].addLateMove(movesGraph['flyingStaff'])
    movesGraph['archer'] = Move.twoSides("Archer Pose", "Grab each foot with hand. Try to straighten the %(same)s leg and bend \
            the %(other)s leg, lifting both legs off the ground. Archer Pose.", 30, movesGraph['staff'], movesGraph['vinyasa'])
    movesGraph['butterflyStretch'] = Move("Butterfly Stretch", 0, "Butterfly Stretch", 15, movesGraph['vinyasa'], \
            movesGraph['staff'])
    if difficulty >= 1: movesGraph['butterflyStretch'].addLateMove(*movesGraph['archer'])
    movesGraph['headToKnee'] = Move.twoSides("Head To Knee", "With your %(same)s knee straight and your %(other)s knee bent, \
            reach toward the toes of your %(same)s foot.", 15, movesGraph['staff'], movesGraph['butterflyStretch'])
    movesGraph['child'] = Move("Child's Pose", 0, "Child's Pose", 5 - difficulty, movesGraph['table'], extended_time=[10,15], \
            lateMove=set([movesGraph['catCow']]))
    movesGraph['seatedTwist'] = Move.twoSides("Seated Twist", "Twist to the %(same)s side", 10, movesGraph['vinyasa'])
    movesGraph['scale'] = Move("Scale Pose", 0, "Push upwards with your hands. Try to get your entire body off the ground. Scale Pose", \
            15 + 4*difficulty, movesGraph['vinyasa'])
    movesGraph['seatedMeditation'] = Move("Seated Meditation", 0, "Seated Meditation", 5 - difficulty, movesGraph['child'], movesGraph['table'], \
            movesGraph['catCow'], movesGraph['butterflyStretch'], movesGraph['staff'], *movesGraph['seatedTwist'], \
            extended_time=Move.reDifficultyTimes([20,30], -3, difficulty))
    if difficulty >= 1: movesGraph['seatedMeditation'].addLateMove(movesGraph['scale'], movesGraph['vinyasa'])
    movesGraph['childsPoseSideStretch'] = Move.twoSides("Child's Pose, Side Stretch", "Reach your fingers over to your %(same)s side. \
            You should feel a stretch across your %(other)s side body", 8, movesGraph['child'], movesGraph['table'], \
            movesGraph['seatedMeditation'], lateMove=set([movesGraph['staff']]))
    movesGraph['kneeToOtherElbow'] = Move.twoSides("Knee To Other Elbow", "Take your %(same)s knee and bring it across your body to \
            your %(other)s elbow", 15 + 2*difficulty, movesGraph['vinyasa'], extended_time=Move.reDifficultyTimes([20,30], 3, difficulty))
    movesGraph['standingLegLift1'] = Move.twoSides("Standing Leg Lift", "Raise your %(same)s foot up and grab it with your %(same) hand. \
            Standing Leg Lift. Hold", 15 + 3*difficulty, extended_time=Move.reDifficultyTimes([30,45,60], 5, difficulty))
    movesGraph['standingLegLift2'] = Move.twoSides("Standing Leg Lift, Leg to Side", "Now take your %(same)s foot and move it out to the side. Hold", \
            20 + 5*difficulty, extended_time=Move.reDifficultyTimes([30,45,60], 5, difficulty))
    movesGraph['twistedStandingLegLift'] = Move.twoSides("Standing Leg Lift, Twisted", "Take your %(same)s foot with your %(other)s hand and twist to the %(other)s side.", \
            20+5*difficulty, extended_time = Move.reDifficultyTimes([30,45,60],5, difficulty))
    movesGraph['standingLegLift3'] = Move.twoSides("Standing Leg Lift, Both Hands", "Return %(same)s foot to center. \
            Grab with both hands, head to knee or chin to shin. Hold.", 20, extended_time=Move.reDifficultyTimes([30,45,60], 5, difficulty))
    movesGraph['standingLegLift4'] = Move.twoSides("Standing Leg Lift, No Hands", "Release %(same)s foot. Hold foot up towards ceiling.", \
            25 + 5*difficulty, extended_time=Move.reDifficultyTimes([30,45,60], 5, difficulty))
    movesGraph['eagle'] = Move.twoSides("Eagle Pose", "Take your %(same)s foot and twist it over your %(other)s leg. Twine your arms, %(same) arm lower. \
            Eagle Pose", 20 + 3*difficulty, extended_time=Move.reDifficultyTimes([35,40], 5, difficulty), \
            harder="Bring your elbows to your knees, and then straighten. Repeat")
    movesGraph['tree'] = Move.twoSides("Tree Pose", "Tree Pose, %(same)s side", 20 + 3*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([45,60], 5, difficulty))
    movesGraph['halfBoundStandingLotus'] = Move.twoSides("Half-Bound Standing Lotus", "Take your %(same)s foot and put it at the top of your %(other)s thigh. \
            With your %(same)s hand, reach behind you and grab your %(same)s foot", 10 + 2*difficulty, movesGraph['vinyasa'], \
            harder="Lean forwards and touch the ground with your free hand.", extended_time=Move.reDifficultyTimes([30,45],3,difficulty))
    movesGraph['standingLotusSquat'] = Move.twoSides("Standing Lotus Squat", "Bend your %(other)s thigh and squat down", 15+3*difficulty, \
            movesGraph['vinyasa'], extended_time=Move.reDifficultyTimes([20,30],4,difficulty))
    movesGraph['toestand'] = Move.twoSides("Toestand", "Continue bending down, rise up onto the toes of your %(other)s foot", \
            15+3*difficulty, movesGraph['vinyasa'], harder="Try to get your hands to your heart!", \
            extended_time=Move.reDifficultyTimes([20,30],4,difficulty))
    movesGraph['flyingPigeon'] = Move.twoSides("Flying Pigeon", "Plant your hands on the ground and lift your %(same)s foot. Flying Pigeon", \
            30, movesGraph['vinyasa'])
    movesGraph['dancer'] = Move.twoSides("Dancer Pose", "Dancer Pose, %(same)s side", 20 + 5*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([25,45],5,difficulty))
    movesGraph['backBend'] = Move("Back Bend", 0, "Raise your hands towards the ceiling and bend backwards", 10-difficulty, movesGraph['vinyasa'])
    movesGraph['wideLegStance'] = Move("Wide Leg Stance", 0, "Wide Leg Stance", 5 - difficulty)
    movesGraph['wideLegForwardFold'] = Move("Wide Leg Forward Fold", 0, "Wide Leg Forward Fold", 15, movesGraph['wideLegStance'])
    movesGraph['armPressurePose'] = Move("Arm Pressure Pose", 0, "Wrap legs around shoulders. Attempt to balance on arms.", \
            30, movesGraph['wideLegForwardFold'])
    movesGraph['standingLegStretch'] = Move.twoSides("Standing Leg Stretch", "Reach for your %(same)s foot", \
            10, movesGraph['wideLegStance'], movesGraph['wideLegForwardFold'])
    movesGraph['mountain'] = Move("Mountain Pose", 0, "Mountain Pose", 5 - difficulty, movesGraph['backBend'], movesGraph['wideLegStance'], \
            *movesGraph['standingLegLift1'], extended_time=[10])
    movesGraph['standingSideStretch'] = Move.twoSides("Standing Side Stretch", "Lean to the %(same)s side", \
            10, movesGraph['backBend'], movesGraph['mountain'])
    movesGraph['standingTwist'] = Move.twoSides("Standing Twist", "Bring your arms up to shoulder level and twist to the %(same)s", \
            15, movesGraph['mountain'])
    movesGraph['forwardFoldShoulderStretch'] = Move("Forward Fold, Shoulder Stretch", 0, \
            "Clasp your hands together behind your head and allow gravity to drag your pinkies towards the floor", \
            10, movesGraph['mountain'], extended_time=[15,20])
    movesGraph['forwardFold'] = Move("Forward Fold", 0, "Forward Fold", 4 - difficulty, movesGraph['mountain'], \
            movesGraph['forwardFoldShoulderStretch'])
    movesGraph['flatBack'] = Move("Flat Back", 0, "Flat Back", 4 - difficulty, movesGraph['forwardFold'], movesGraph['vinyasa'])
    movesGraph['forearmBalance'] = Move("Forearm Balance", 0, "Forearm Balance", 30, movesGraph['child'], extended_time=[45])
    movesGraph['dolphin'] = Move("Dolphin Pose", 0, "Dolphin Pose", 25 + 5*difficulty, movesGraph['vinyasa'], \
            extended_time=[40 + 5*difficulty])
    if difficulty >= 1: movesGraph['dolphin'].addLateMove(movesGraph['forearmBalance'])
    movesGraph['downwardDog'] = Move("Downwards Dog", 0, "Downwards Dog", 4 - 2*difficulty, movesGraph['forwardFold'], \
            movesGraph['staff'], movesGraph['plank'], movesGraph['dolphin'], *movesGraph['threeLeggedDog'], extended_time=[10])
    movesGraph['upwardDog'] = Move("Upward Dog", 0, "Upward Dog", 3-difficulty, movesGraph['downwardDog'], extended_time=[10,20])
    movesGraph['humbleWarrior'] = Move.twoSides("Humble Warrior", "Intertwine your hands behind you. Lean forward. Humble Warrior", \
            5 - difficulty, movesGraph['vinyasa'])
    movesGraph['warrior1'] = Move.twoSides("Warrior 1", "Warrior One, %(same)s Side", 10 - 2*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([20,30],3,difficulty))
    movesGraph['warrior2'] = Move.twoSides("Warrior 2", "Warrior Two, %(same)s Side", 10 - 2*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([20,30],3,difficulty))
    movesGraph['warrior3'] = Move.twoSides("Warrior 3", "Warrior Three, %(same)s Side", 10 - 2*difficulty, movesGraph['vinyasa'], \
            harder="Bring your elbows to your knee, and then extend! Repeat", extended_time=Move.reDifficultyTimes([20,30,45],5,difficulty))
    movesGraph['standingSplits'] = Move.twoSides("Standing Splits", "Raise your %(same)s foot up towards the ceiling. Standing Splits", \
            20 + 2*difficulty, movesGraph['vinyasa'], extended_time=Move.reDifficultyTimes([30],2,difficulty))
    movesGraph['lizard'] = Move.twoSides("Lizard Pose", "Lizard Pose, %(same)s side", 25 + 5*difficulty, movesGraph['vinyasa'], \
            bind=True, harder="Lower yourself onto your forearms", extended_time=Move.reDifficultyTimes([45,60],5,difficulty))
    movesGraph['chinStand'] = Move.twoSides("Chin Stand", "Chin Stand, %(same)s side", 30, movesGraph['vinyasa'])
    movesGraph['runningMan'] = Move.twoSides("Running Man", "Running Man, %(same)s side", 30, movesGraph['vinyasa'], countdown=True)
    movesGraph['revolvedRunningMan'] = Move.twoSides("Revolved Running Man", "Revolved Running Man, %(same)s side", \
            30, movesGraph['vinyasa'], countdown=True)
    movesGraph['cresent'] = Move.twoSides("Cresent Lunge", "Cresent Lunge, %(same)s foot forward", 10-difficulty, \
            early="Feel free to lower your other knee down to the ground", extended_time=Move.reDifficultyTimes([20,30],2,difficulty),\
            lateMove=set([movesGraph['vinyasa']]))
    movesGraph['cresentTwist'] = Move.twoSides("Cresent Twist", "Cresent Twist. Twist to the %(same)s side.", 15, bind=True,\
            lateMove=set([movesGraph['vinyasa']]))
    movesGraph['chairTwist'] = Move.twoSides("Chair Twist", "Chair Twist. Twist to the %(same)s side", 15, bind=True)
    movesGraph['chair'] = Move("Chair Pose", 0, "Chair Pose", 15+2*difficulty, movesGraph['vinyasa'], *movesGraph['chairTwist'], \
            extended_time=Move.reDifficultyTimes([30, 40, 60],5,difficulty))
    movesGraph['oneLeggedChair'] = Move.twoSides("One Legged Chair", "Shift all your weight to your %(other)s foot. Grab your %(same)s \
            foot with your %(same)s hand. Raise %(same)s foot", 15 + 2*difficulty, movesGraph['chair'], \
            extended_time=Move.reDifficultyTimes([20,30],4,difficulty))
    movesGraph['revolvedOneLeggedChair'] = Move.twoSides("Revolved One Legged Chair", "Shift all your weight to your %(other)s foot. Grab your %(same)s foot with \
            your %(other)s hand. Raise %(same)s foot", 15 + 2*difficulty, movesGraph['vinyasa'], movesGraph['chair'], \
            extended_time=Move.reDifficultyTimes([20,30],4,difficulty))
    movesGraph['crow'] = Move("Crow Pose", 0, "Crow Pose", 30, movesGraph['vinyasa'])
    movesGraph['crane'] = Move("Crane Pose", 0, "Crane Pose", 30, movesGraph['vinyasa'])
    movesGraph['sideCrow'] = Move.twoSides("Side Crow", "Side Crow, %(same)s Side", 30, movesGraph['vinyasa'])
    movesGraph['boat'] = Move("Boat Pose", 0, "Boat Pose", 30, movesGraph['staff'], extended_time=[45,60])
    movesGraph['boatLift'] = Move("Boat Lift", 0, "Cross one ankle over the other, plant your hands and lift", 10, movesGraph['boat'])
    movesGraph['boatTwist'] = Move("Boat Twist", 0, "Point your fingers towards the right and your ankles towards the left. Now reverse. Repeat", \
            20, movesGraph['boat'], movesGraph['staff'], movesGraph['vinyasa'], extended_time=[30,40])
    movesGraph['lowBoat'] = Move("Low Boat Pose", 0, "Lower down into Low Boat Pose", \
            15, movesGraph['boat'], movesGraph['vinyasa'], extended_time=[20,30])
    movesGraph['revolvedHalfMoon'] = Move.twoSides("Revolved Half Moon", "Revolved Half Moon, %(same)s Side", 16 + 4*difficulty, \
            extended_time=Move.reDifficultyTimes([30,40],5,difficulty))
    movesGraph['halfMoon'] = Move.twoSides("Half Moon", "Half Moon, %(same)s Side", 16 + 4*difficulty, \
            harder="Try to take your hand off the ground!", extended_time=Move.reDifficultyTimes([30,40],5,difficulty))
    movesGraph['sideAngle'] = Move.twoSides("Side Angle", "Side Angle", 10 + 3*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([20,25],4,difficulty))
    movesGraph['sidePlank'] = Move.twoSides("Side Plank", "Side Plank, %(same)s side", 11 + 4*difficulty, movesGraph['plank'], movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([30,40],4,difficulty))
    movesGraph['sidePlankLegUp'] = Move.twoSides("Side Plank, Leg Up", "Now raise your %(other)s leg up and hold", 10 + 4*difficulty, \
            extended_time=Move.reDifficultyTimes([20,25,30],4,difficulty), lateMove=set([movesGraph['vinyasa']]))
    movesGraph['triangle'] = Move.twoSides("Triangle Pose", "Triangle Pose, %(same)s side", 15, movesGraph['vinyasa'], bind=True)
    movesGraph['pyramid'] = Move.twoSides("Pyramid Pose", "Pyramid Pose, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['revolvedTriangle'] = Move.twoSides("Revolved Triangle", "Revolved Triangle Pose, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['reverseWarrior'] = Move.twoSides("Reverse Warrior", "Take your %(same)s hand and raise it towards the back of the room. Reverse Warrior", \
            5 - difficulty, extended_time=[10])
    movesGraph['bridge'] = Move("Bridge Pose", 0, "Bridge Pose", 20 + 4*difficulty)
    movesGraph['bridgeWithRaisedLeg'] = Move.twoSides("Bridge, with Raised Leg", "Raise your %(same)s leg into the air", \
            15 + 4*difficulty, movesGraph['bridge'], extended_time =Move.reDifficultyTimes([20,30],4,difficulty))
    movesGraph['wheelWithRaisedLeg'] = Move.twoSides("Wheel, with Raised Leg", "Raise your %(same)s leg into the air", 15, countdown = True)
    movesGraph['wheel'] = Move("Wheel Pose", 0, "Wheel Pose", 25 + 5*difficulty, movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([40,55],5,difficulty), harder="Try to straighten your legs", countdown = True)
    movesGraph['wheelPushup'] = Move("Wheel Pushup", 0, "Wheel Pushup", 15)
    if difficulty >= 1:
        movesGraph['wheel'].addLateMove(*movesGraph['wheelWithRaisedLeg'])
    if difficulty >= 2:
        movesGraph['wheel'].addLateMove(movesGraph['mountain'])
    movesGraph['camel'] = Move("Camel Pose", 0, "Camel Pose", 30, movesGraph['vinyasa'])
    movesGraph['superMan'] = Move("Super Man", 0, "Raise both your hands and your feet off the ground at the same time. Hold", \
            13+2*difficulty, movesGraph['vinyasa'], extended_time=[26 + 4*difficulty])
    movesGraph['bow'] = Move("Bow Pose", 0, "Grab your feet with both hands and raise upwards", \
            13+2*difficulty, movesGraph['vinyasa'], extended_time=Move.reDifficultyTimes([20,30,40],4,difficulty))
    movesGraph['fish'] = Move("Fish Pose", 0, "Fish Pose", 20, movesGraph['vinyasa'])
    movesGraph['supportedShoulderStand'] = Move("Supported Shoulder Stand", 0, "Supported Shoulder Stand", 30, movesGraph['fish'])
    movesGraph['plow'] = Move("Plow Pose", 0, "Plow Pose", 30, movesGraph['supportedShoulderStand'])
    movesGraph['upwardPlank'] = Move("Upward Plank", 0, "Upward Plank", 30, movesGraph['vinyasa'])
    movesGraph['upwardPlankLiftedLeg'] = Move.twoSides("Upward Plank, Lifted Leg", "Lift your %(same)s leg. Upward Plank, %(same)s leg lifted", \
            15, movesGraph['upwardPlank'], movesGraph['vinyasa'])
    movesGraph['lieOnBack'] = Move("Lie On Back", 0, "Lie on Your Back", 5 - difficulty)
    movesGraph['spinalTwist'] = Move.twoSides("Spinal Twist","Bring your knees up to your chest, and then let them fall to the %(same)s. \
            Look towards your %(other)s hand. Spinal Twist", 20, movesGraph['lieOnBack'])
    movesGraph['lieOnFront'] = Move("Lie On Front", 0, "Lie on Your Stomach", 4 - difficulty, movesGraph['superMan'], movesGraph['bow'], \
            movesGraph['lieOnBack'], movesGraph['vinyasa'], lateMove=set([movesGraph['plank']]))
    movesGraph['yogaBicycles'] = Move("Bicycles", 0, "Bicycles", 20 + 10*difficulty, movesGraph['lieOnBack'], movesGraph['vinyasa'], \
            extended_time=Move.reDifficultyTimes([35, 50], 10, difficulty))
    movesGraph['savasana'] = Move("Savasana", 0, "Sahvahsahnah", 30, None)
    movesGraph['star'] = Move('Star Pose', 0, "Star Pose", 8, movesGraph['mountain'], *movesGraph['warrior1'])
    movesGraph['goddessSquat'] = Move('Goddess Squat', 0, "Goddess Squat", 5, movesGraph['star'])
    movesGraph['supportedHeadstand'] = Move('Supported Headstand', 0, "Supported Headstand", 30, movesGraph['child'])
    movesGraph['pigeon'] = Move.twoSides('Pigeon Pose', "Pigeon Pose, %(same)s side", 30, movesGraph['vinyasa'])
    movesGraph['kingPigeon'] = Move.twoSides('King Pigeon', "King Pigeon, %(same)s side", 15, movesGraph['vinyasa'])
    movesGraph['birdOfParadise'] = Move.twoSides('Bird of Paradise', 'Bird of Paradise', 30)
    movesGraph['boundHalfMoon'] = Move.twoSides('Bound Half Moon', 'Bound Half Moon', 30, lateMove=set([movesGraph['vinyasa']]))
    movesGraph['boundRevolvedHalfMoon'] = Move.twoSides('Bound Revolved Half Moon', 'Bound Revolved Half Moon', 30, lateMove=set([movesGraph['vinyasa']]))
    movesGraph['handstandHops'] = Move('Handstand Hops', 0, "Handstand Hops", 30, movesGraph['vinyasa'])
    movesGraph['twoLeggedDog'] = Move.twoSides('Two Legged Dog', "Now raise your %(other)s hand. Hold", 20, lateMove=set([movesGraph['vinyasa']]))
    movesGraph['flippedDog'] = Move.twoSides('Flipped Dog', "Flipped Dog, %(same)s side", 20, lateMove=set([movesGraph['downwardDog']]))
    movesGraph['feetUpAWall'] = Move("Feet Up A Wall", 0, "Feet Up A Wall", 4, movesGraph['lowBoat'], movesGraph['boat'], movesGraph['staff'], movesGraph['lieOnBack'], extended_time=[15,30])
    movesGraph['hero'] = Move("Hero Pose", 0, "Tuck both feet under your glutes. Lean back as far as possible. Hero Pose", 20, movesGraph['seatedMeditation'])
    movesGraph['deepSquat'] = Move("Deep Squat", 0, "Squat as deeply as you can", 30, movesGraph['vinyasa'], movesGraph['chair'], lateMove=set([movesGraph['crow']]))
    movesGraph['frog'] = Move("Frog Pose", 0, "Frog Pose", 30, movesGraph['seatedMeditation'], movesGraph['vinyasa'])
    movesGraph['cowFace'] = Move.twoSides('Cow-Facing Pose', 'Cow-Facing Pose', 30, movesGraph['seatedMeditation'], movesGraph['child']) #TODO: more useful instructions

    #Begin linking moves to each other
    movesGraph['wideLegStance'].addMove(movesGraph['mountain'], movesGraph['star'], movesGraph['wideLegForwardFold'], *movesGraph['warrior2'])
    if difficulty >= 0:
        movesGraph['wideLegStance'].addLateMove(movesGraph['armPressurePose'], *movesGraph['cresent'])
    if difficulty >= 1:
        movesGraph['wheelPushup'].addMove(movesGraph['lieOnBack'])
        movesGraph['wheel'].addLateMove(movesGraph['wheelPushup'])
    movesGraph['vinyasa'].addMove(movesGraph['downwardDog'])
    movesGraph['table'].addMove(*movesGraph['threadTheNeedle'])
    movesGraph['catCow'].addMove(movesGraph['table'])
    movesGraph['mountain'].addMove(movesGraph['forwardFold'], movesGraph['chair'], *movesGraph['standingTwist'])
    movesGraph['mountain'].addMove(*movesGraph['standingSideStretch'])
    movesGraph['mountain'].addMove(*movesGraph['standingTwist'])
    if difficulty >= 0:
        movesGraph['mountain'].last = movesGraph['chair']
        movesGraph['mountain'].addLateMove(*movesGraph['dancer'])
    movesGraph['backBend'].addMove(movesGraph['mountain'], movesGraph['forwardFold'], *movesGraph['standingSideStretch'])
    movesGraph['staff'].addMove(movesGraph['lieOnBack'], movesGraph['butterflyStretch'], movesGraph['camel'], movesGraph['seatedMeditation'])
    if difficulty >= 0:
        movesGraph['staff'].addMove(movesGraph['boat'])
        movesGraph['staff'].addLateMove(movesGraph['yogaBicycles'], movesGraph['mountain'])
    movesGraph['downwardDog'].addMove(movesGraph['plank'])
    if difficulty >= 1:
        movesGraph['downwardDog'].addLateMove(movesGraph['lowPlank'])
    movesGraph['flatBack'].addMove(movesGraph['forwardFold'])
    movesGraph['flatBack'].addLateMove(movesGraph['chair'], movesGraph['deepSquat'])
    if difficulty >= 2:
        movesGraph['flatBack'].addLateMove(movesGraph['handstandHops'])
    movesGraph['lieOnBack'].addMove(movesGraph['seatedMeditation'], movesGraph['feetUpAWall'],*movesGraph['spinalTwist'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['lieOnFront'])
    if difficulty >= 0:
        movesGraph['lieOnBack'].addLateMove(movesGraph['wheel'])
    movesGraph['plow'].addMove(movesGraph['fish'])
    if difficulty >= 0:
        movesGraph['fish'].addMove(movesGraph['upwardPlank'])
    movesGraph['upwardPlank'].addMove(movesGraph['lieOnBack'])
    if difficulty >= 1:
        movesGraph['upwardPlank'].addLateMove(*movesGraph['upwardPlankLiftedLeg'])
    movesGraph['supportedShoulderStand'].addMove(movesGraph['plow'])
    movesGraph['plank'].addMove(movesGraph['vinyasa'], *movesGraph['sidePlank'])
    Move.doubleAdd(movesGraph['oneLeggedPlank'], movesGraph['twoPointPlank'])
    if difficulty >= 1:
        movesGraph['plank'].addMove(*movesGraph['oneLeggedPlank'])
        Move.doubleAdd(movesGraph['oneLeggedPlank'], movesGraph['threeLeggedDog'], late = True)
        Move.doubleAdd(movesGraph['twoPointPlank'], movesGraph['twoLeggedDog'], late=True)
    movesGraph['lowPlank'].addMove(movesGraph['upwardDog'], movesGraph['vinyasa'])
    movesGraph['lowPlank'].addLateMove(movesGraph['plank'])
    movesGraph['child'].addMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['child'].addLateMove(movesGraph['seatedMeditation'])
    if difficulty >= 1:
        movesGraph['boat'].addMove(movesGraph['lowBoat'], movesGraph['boatLift'], movesGraph['boatTwist'])
        movesGraph['boatLift'].addMove(movesGraph['staff'])
        movesGraph['boatLift'].addLateMove(movesGraph['yogaBicycles'])
    movesGraph['lowBoat'].addMove(movesGraph['yogaBicycles'])
    movesGraph['chair'].addMove(movesGraph['deepSquat'], *movesGraph['oneLeggedChair'])
    if difficulty >= 1:
        movesGraph['chair'].addLateMove(*movesGraph['revolvedOneLeggedChair'])
    movesGraph['star'].addMove(movesGraph['goddessSquat'], movesGraph['deepSquat'])
    movesGraph['bridge'].addMove(movesGraph['lieOnBack'], *movesGraph['bridgeWithRaisedLeg'])
    if difficulty >= 0:
        movesGraph['bridge'].addLateMove(movesGraph['upwardPlank'])
    movesGraph['fish'].addMove(movesGraph['lieOnBack'])
    if difficulty >= 1:
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
    movesGraph['vinyasa'].addMove(movesGraph['upwardDog'])
    for i in movesGraph['halfBoundStandingLotus']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['bridgeWithRaisedLeg']: i.addMove(movesGraph['lieOnBack'])
    for i in movesGraph['wheelWithRaisedLeg']: i.addMove(movesGraph['lieOnBack'], movesGraph['wheel'])
    if difficulty < 1:
        for i in movesGraph['eagle']: i.addMove(movesGraph['forwardFold'])
    else:
        for i in movesGraph['eagle']:
            i.addMove(movesGraph['vinyasa'])
            i.addLateMove(movesGraph['mountain'])
    for i in movesGraph['balancingTable']: i.addMove(movesGraph['table'], movesGraph['child'], movesGraph['catCow'])
    for i in movesGraph['standingLegLift4']: i.addMove(movesGraph['mountain'], movesGraph['forwardFold'])
    for i in movesGraph['chairTwist']: i.addMove(movesGraph['chair'], movesGraph['forwardFold'])
    for i in movesGraph['halfMoon']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['revolvedHalfMoon']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['warrior1']: i.addMove(movesGraph['star'])
    for i in movesGraph['warrior2']: i.addMove(movesGraph['star'])
    for i in movesGraph['seatedTwist']: i.addMove(movesGraph['seatedMeditation'])
    for i in movesGraph['standingTwist']: i.addLateMove(movesGraph['forwardFold'])
    for i in movesGraph['dancer']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['warrior3']: i.addMove(movesGraph['forwardFold'])
    for i in movesGraph['headToKnee']: i.addLateMove(movesGraph['hero'])
    for i in movesGraph['standingSplits']: i.addLateMove(movesGraph['handstandHops'])
    for i in movesGraph['threadTheNeedle']: i.addLateMove(movesGraph['child'])
    for i in movesGraph['fallenStar']: i.addMove(movesGraph['table'])
    for i in movesGraph['sidePlankLegUp']: i.addMove(movesGraph['plank'])
    if difficulty < 2:
        for i in movesGraph['sidePlankLegUp']: i.addLateMove(movesGraph['lieOnFront'])
    if difficulty < 0:
        for j in range(1,4):
            for i in movesGraph['standingLegLift' + str(j)]: i.addLateMove(movesGraph['mountain'])

    Move.moveReverse(movesGraph['seatedTwist'], movesGraph['childsPoseSideStretch'], movesGraph['threadTheNeedle'])
    Move.moveReverse(movesGraph['standingSideStretch'], movesGraph['standingTwist'])
    Move.moveReverse(movesGraph['headToKnee'], movesGraph['cowFace'])

    Move.doubleAdd(movesGraph['standingSideStretch'], movesGraph['standingTwist'])
    Move.doubleAdd(movesGraph['standingTwist'], movesGraph['standingSideStretch'])
    Move.doubleAdd(movesGraph['standingTwist'], movesGraph['standingLegLift1'], late=True)
    Move.doubleAdd(movesGraph['oneLeggedChair'], movesGraph['standingLegLift1'])
    Move.doubleAdd(movesGraph['sidePlank'], movesGraph['sideAngle'], movesGraph['sidePlankLegUp'])
    Move.doubleAdd(movesGraph['sidePlank'], movesGraph['cresentTwist'], late=True, inverted=True)
    Move.doubleAdd(movesGraph['sidePlankLegUp'], movesGraph['cresentTwist'], inverted=True)
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['threadTheNeedle'], movesGraph['fallenStar'])
    Move.doubleAdd(movesGraph['warrior1'], movesGraph['warrior2'], movesGraph['warrior3'], movesGraph['humbleWarrior'], movesGraph['cresent'])
    Move.doubleAdd(movesGraph['humbleWarrior'], movesGraph['warrior1'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['humbleWarrior'], movesGraph['warrior3'], late=True)
    Move.doubleAdd(movesGraph['warrior2'], movesGraph['sideAngle'], movesGraph['triangle'], movesGraph['reverseWarrior'], movesGraph['cresent'])
    Move.doubleAdd(movesGraph['threeLeggedDog'], movesGraph['lowLunge'], movesGraph['kneeToElbow'], movesGraph['kneeToNose'], movesGraph['warrior1'], \
            movesGraph['warrior2'], movesGraph['twoLeggedDog'], movesGraph['flippedDog'], movesGraph['kneeToOtherElbow'])
    Move.doubleAdd(movesGraph['twoLeggedDog'], movesGraph['threeLeggedDog'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['threeLeggedDog'], movesGraph['runningMan'], movesGraph['revolvedRunningMan'], late=True)
    Move.doubleAdd(movesGraph['flippedDog'], movesGraph['threeLeggedDog'])
    Move.doubleAdd(movesGraph['pigeon'], movesGraph['threeLeggedDog'], movesGraph['kingPigeon'])
    Move.doubleAdd(movesGraph['kingPigeon'], movesGraph['threeLeggedDog'])
    Move.doubleAdd(movesGraph['kneeToNose'], movesGraph['threeLeggedDog'])
    if difficulty <= 0:
        Move.doubleAdd(movesGraph['kneeToNose'], movesGraph['lowLunge'], late=True)
    Move.doubleAdd(movesGraph['kneeToElbow'], movesGraph['kneeToOtherElbow'], movesGraph['threeLeggedDog'], movesGraph['lowLunge'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['kneeToElbow'], movesGraph['runningMan'], late=True)
    Move.doubleAdd(movesGraph['kneeToOtherElbow'], movesGraph['threeLeggedDog'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['kneeToOtherElbow'], movesGraph['revolvedRunningMan'], late=True)
    Move.doubleAdd(movesGraph['lowLunge'], movesGraph['warrior1'], movesGraph['warrior2'], movesGraph['cresent'], movesGraph['lizard'])
    Move.doubleAdd(movesGraph['lowLunge'], movesGraph['standingSplits'], inverted=True)
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['lowLunge'], movesGraph['warrior3'], late=True)
        Move.doubleAdd(movesGraph['eagle'], movesGraph['warrior3'], late=True, inverted=True)
        Move.doubleAdd(movesGraph['eagle'], movesGraph['standingLegLift4'])
        Move.doubleAdd(movesGraph['lizard'], movesGraph['cresent'], late = True)
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['eagle'], movesGraph['standingSplits'])
    Move.doubleAdd(movesGraph['warrior3'], movesGraph['standingLegLift1'], movesGraph['standingSplits'], movesGraph['tree'], movesGraph['eagle'], \
            inverted=True)
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['warrior3'], movesGraph['halfMoon'])
    Move.doubleAdd(movesGraph['warrior3'], movesGraph['warrior2'])
    Move.doubleAdd(movesGraph['cresent'], movesGraph['warrior1'], movesGraph['cresentTwist'], movesGraph['warrior3'])
    Move.doubleAdd(movesGraph['cresentTwist'], movesGraph['cresent'], movesGraph['chairTwist'])
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['cresentTwist'], movesGraph['sidePlank'], inverted=True)
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['cresentTwist'], movesGraph['sidePlankLegUp'], inverted=True, late=True)
    if difficulty >= 2:
        Move.doubleAdd(movesGraph['cresentTwist'], movesGraph['boundRevolvedHalfMoon'], late=True)
    Move.doubleAdd(movesGraph['balancingTableLegOnly'], movesGraph['balancingTable'])
    Move.doubleAdd(movesGraph['balancingTable'], movesGraph['oneHandedTiger'])
    Move.doubleAdd(movesGraph['sideAngle'], movesGraph['reverseWarrior'], movesGraph['warrior2'])
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['sideAngle'], movesGraph['sidePlank'], movesGraph['birdOfParadise'], movesGraph['halfMoon'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['sideAngle'], movesGraph['boundHalfMoon'], late=True)
    Move.doubleAdd(movesGraph['boundHalfMoon'], movesGraph['sideAngle'], movesGraph['halfMoon'])
    Move.doubleAdd(movesGraph['boundRevolvedHalfMoon'], movesGraph['cresentTwist'], movesGraph['revolvedHalfMoon'])
    Move.doubleAdd(movesGraph['birdOfParadise'], movesGraph['sideAngle'])
    Move.doubleAdd(movesGraph['reverseWarrior'], movesGraph['sideAngle'], movesGraph['warrior2'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['reverseWarrior'], movesGraph['sidePlank'], late=True)
    Move.doubleAdd(movesGraph['standingLegLift1'], movesGraph['standingLegLift2'], movesGraph['eagle'], movesGraph['tree'])
    Move.doubleAdd(movesGraph['tree'], movesGraph['halfBoundStandingLotus'], movesGraph['eagle'], movesGraph['standingLegLift1'])
    Move.doubleAdd(movesGraph['tree'], movesGraph['warrior3'], inverted=True)
    Move.doubleAdd(movesGraph['halfBoundStandingLotus'], movesGraph['standingLegLift1'], movesGraph['tree'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['halfBoundStandingLotus'], movesGraph['standingLotusSquat'], late=True)
        Move.doubleAdd(movesGraph['standingLotusSquat'], movesGraph['toestand'])
    if difficulty >= 2:
        Move.doubleAdd(movesGraph['standingLotusSquat'], movesGraph['flyingPigeon'])
    Move.doubleAdd(movesGraph['standingLegLift1'], movesGraph['warrior3'], inverted=True)
    Move.doubleAdd(movesGraph['standingLegLift2'], movesGraph['standingLegLift3'])
    if difficulty < 1:
        Move.doubleAdd(movesGraph['standingLegLift2'], movesGraph['tree'], late = True)
    Move.doubleAdd(movesGraph['standingLegLift3'], movesGraph['standingLegLift4'])
    Move.doubleAdd(movesGraph['standingLegLift4'], movesGraph['warrior3'], inverted=True)
    Move.doubleAdd(movesGraph['standingLegLift4'], movesGraph['standingSplits'], movesGraph['eagle'], movesGraph['tree'])
    Move.doubleAdd(movesGraph['triangle'], movesGraph['revolvedTriangle'], movesGraph['pyramid'], movesGraph['sideAngle'])
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['triangle'], movesGraph['halfMoon'], late=True)
    Move.doubleAdd(movesGraph['pyramid'], movesGraph['revolvedTriangle'])
    Move.doubleAdd(movesGraph['standingLegStretch'], movesGraph['pyramid'])
    Move.doubleAdd(movesGraph['chairTwist'], movesGraph['sideCrow'], late = True)
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['lizard'], movesGraph['runningMan'], late=True)
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['lizard'], movesGraph['sideAngle'], late=True)
    Move.doubleAdd(movesGraph['halfMoon'], movesGraph['revolvedHalfMoon'], movesGraph['warrior3'], movesGraph['warrior2'])
    Move.doubleAdd(movesGraph['revolvedHalfMoon'], movesGraph['halfMoon'], movesGraph['warrior3'], movesGraph['warrior1'], movesGraph['cresent'])
    Move.doubleAdd(movesGraph['revolvedTriangle'], movesGraph['revolvedHalfMoon'], movesGraph['pyramid'], movesGraph['cresentTwist'])
    Move.doubleAdd(movesGraph['sideCrow'], movesGraph['revolvedRunningMan'], late=True)
    Move.doubleAdd(movesGraph['dancer'], movesGraph['standingLegLift1'], movesGraph['standingSplits'], movesGraph['warrior3'])
    if difficulty >= 0:
        Move.doubleAdd(movesGraph['dancer'], movesGraph['eagle'], late=True)
    return movesGraph

def linkSavasana(movesGraph, *args, difficulty=1) -> None:
    moves = ['child', 'downwardDog', 'staff', 'seatedMeditation', 'mountain', 'table', \
            'lieOnBack', 'lieOnFront', 'fish', 'wheel']
    for i in moves:
        movesGraph[i].addMove(movesGraph['savasana'])
    for i in args:
        i.addMove(movesGraph['savasana'])

def linkMain(movesGraph, difficulty=1) -> None:
    for i in ['child', 'table', 'catCow']:
        movesGraph[i].addMove(movesGraph['downwardDog'], movesGraph['plank'])
        movesGraph[i].promoteLate()
    movesGraph['lieOnBack'].addMove(movesGraph['supportedShoulderStand'], movesGraph['upwardPlank'], movesGraph['vinyasa'], \
            movesGraph['yogaBicycles'], movesGraph['bridge'], movesGraph['staff'] )
    if difficulty >= 1:
        movesGraph['table'].addLateMove(movesGraph['lowPlank'])
        movesGraph['catCow'].addLateMove(movesGraph['lowPlank'])
        movesGraph['lieOnFront'].addLateMove(movesGraph['lowPlank'])

def unlinkWarmup(movesGraph, imbalance=[], difficulty=1) -> list:
    movesGraph['mountain'].removeMove(*movesGraph['standingTwist'])
    movesGraph['lieOnBack'].removeMove(movesGraph['seatedMeditation'])
    movesGraph['mountain'].removeMove(movesGraph['backBend'], *movesGraph['standingSideStretch'])
    movesGraph['backBend'].removeMove(*movesGraph['standingSideStretch'])
    movesGraph['seatedMeditation'].removeMove(movesGraph['table'], movesGraph['catCow'], *movesGraph['seatedTwist'])
    movesGraph['child'].removeMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['feetUpAWall'].removeMove(movesGraph['staff'], movesGraph['lieOnBack'])
    movesGraph['table'].removeMove(*movesGraph['balancingTable'])
    movesGraph['table'].removeMove(*movesGraph['threadTheNeedle'])
    movesGraph['catCow'].removeMove(*movesGraph['balancingTable'])
    if difficulty >= 1:
        movesGraph['vinyasa'].removeMove(movesGraph['upwardDog'])
        for i in movesGraph['threeLeggedDog']: i.time = max(0, i.time - 1)
        for i in movesGraph['lowLunge']: i.time = max(0, i.time - max(0, difficulty))
    #Remove these impossible moves from imbalances
    moves = set(sum([movesGraph[i] for i in ('standingTwist','standingSideStretch','seatedTwist', \
            'childsPoseSideStretch', 'threadTheNeedle', 'balancingTable')],()))
    return [i for i in imbalance if i not in moves]

def linkHarder(movesGraph, difficulty=1) -> None:
    """Links some harder moves."""
    if difficulty >= 2:
        movesGraph['downwardDog'].addLateMove(movesGraph['handstandHops'])
        movesGraph['vinyasa'].addMove(movesGraph['forwardFold'])
        Move.doubleAdd(movesGraph['runningMan'], movesGraph['chinStand'])
        Move.doubleAdd(movesGraph['triangle'], movesGraph['boundHalfMoon'], late=True)
        for i in movesGraph['cresent']: i.addLateMove(movesGraph['handstandHops'])
        movesGraph['crow'].addLateMove(movesGraph['crane'])
    if difficulty >= 1:
        movesGraph['vinyasa'].time = max(0, movesGraph['vinyasa'].time - 1)
        movesGraph['forwardFold'].addMove(movesGraph['crow'])
        movesGraph['seatedMeditation'].addMove(movesGraph['frog'])
        movesGraph['staff'].addMove(movesGraph['frog'])
        movesGraph['child'].addMove(movesGraph['supportedHeadstand'])
        movesGraph['downwardDog'].addLateMove(movesGraph['supportedHeadstand'])
        Move.doubleAdd(movesGraph['threeLeggedDog'], movesGraph['pigeon'])
        for i in movesGraph['twoLeggedDog']: i.addLateMove(movesGraph['plank'])
    for i in ['warrior1', 'warrior2', 'standingLegLift4', 'threeLeggedDog']:
        for j in movesGraph[i]: j.promoteLate()
    for i in ['star', 'mountain', 'downwardDog']:
        movesGraph[i].promoteLate()
    movesGraph['mountain'].promoteLate(n=max(1, difficulty+1))


def linkEnding(movesGraph) -> None:
    #Allow me to just go from one arm balance to the opposite side, to increase the chances I get balanced
    Move.moveReverse(movesGraph['runningMan'], movesGraph['sideCrow'], movesGraph['flyingPigeon'], \
            movesGraph['revolvedRunningMan'], movesGraph['chinStand'], movesGraph['twoLeggedDog'])
    for i in movesGraph['runningMan']: i.addMove(movesGraph['child'])
    for i in movesGraph['revolvedRunningMan']: i.addMove(movesGraph['child'])
    for i in movesGraph['sideCrow']: i.addMove(movesGraph['child'])
    for i in movesGraph['flyingPigeon']: i.addMove(movesGraph['child'])
    for i in movesGraph['twoLeggedDog']: i.addMove(movesGraph['child'], movesGraph['downwardDog'])
    for i in movesGraph['threeLeggedDog']:
        i.addMove(movesGraph['plank'])
        i.time += 1

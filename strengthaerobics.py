#/usr/bin/python3

from moves import Move, doubleAdd, twoSides, moveReverse, reDifficultyTimes

def linkAerobics(movesGraph, difficulty=1):
    movesGraph['jumpingJacks'] = Move("Jumping Jacks", 0, "Jumping Jacks!", 40 + 20*difficulty, movesGraph['mountain'], countReps=True)
    movesGraph['runInPlace'] = Move("Running In Place", 0, "Run In Place", 40 + 20*difficulty, movesGraph['mountain'], movesGraph['jumpingJacks'])
    movesGraph['burpies'] = Move("Burpies!", 0, "Burpies", 30+10*difficulty, movesGraph['vinyasa'], movesGraph['forwardFold'], movesGraph['plank'], \
            extended=reDifficultyTimes([60,75,90], 10, difficulty), countReps=True)
    movesGraph['situps'] = Move("Situps", 0, "Situps", 30 + 10*difficulty, movesGraph['vinyasa'], extended=reDifficultyTimes([40,50],10,difficulty), \
            lateMove=set([movesGraph['boat']]), countReps=True)
    movesGraph['mountain'].addLateMove(movesGraph['jumpingJacks'], movesGraph['runInPlace'], movesGraph['burpies'])
    movesGraph['jumpingJacks'].addLateMove(movesGraph['runInPlace'])
    movesGraph['downwardDog'].addLateMove(movesGraph['burpies'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['situps'])
    movesGraph['staff'].addLateMove(movesGraph['situps'])
    if difficulty >= 1:
        movesGraph['seatedMeditation'].addLateMove(movesGraph['situps'])

def linkAerobicsCooldown(movesGraph, difficulty=1) -> None:
    movesGraph['runInPlace'].addMove(movesGraph['lieOnBack'])
    movesGraph['burpies'].addMove(movesGraph['lieOnFront'])

def linkStrength(movesGraph, difficulty=1) -> None:
    #New moves
    movesGraph['pushups'] = Move("Pushups", 0, "Pushups", 15 + 5*difficulty, movesGraph['vinyasa'], extended=reDifficultyTimes([20,30],5,difficulty), \
            lateMove=set((movesGraph['plank'],) + movesGraph['sidePlank']), countReps=True)
    movesGraph['pistolSquats'] = twoSides("Pistol Squats", "Pistol Squats, %(same)s foot up", 15+5*difficulty, movesGraph['mountain'], countReps=True) #//TODO: better description
    movesGraph['jumpingSquats'] = Move("Jumping Squats", 0, "Jumping Squats", 30, movesGraph['chair'], \
            movesGraph['forwardFold'], lateMove=set([movesGraph['mountain']]), countReps=True)
    movesGraph['sideLunges'] = Move("Side Lunges", 0, "Side Lunges", 20 + 10*difficulty, movesGraph['wideLegStance'], countReps=True)
    movesGraph['aroundTheWorld'] = twoSides("Around The World", "Around The World, %(same)s side", 20 + 10*difficulty, movesGraph['mountain'], \
            lateMove=set([movesGraph['vinyasa']]), countReps=True)

    #link moves
    movesGraph['downwardDog'].addLateMove(movesGraph['pushups'])
    if difficulty >= 1:
        for i in movesGraph['sidePlank']: i.addLateMove(movesGraph['pushups'])
        movesGraph['mountain'].addLateMove(*movesGraph['aroundTheWorld'])
        movesGraph['chair'].addLateMove(movesGraph['jumpingSquats'], *movesGraph['pistolSquats'])
    if difficulty >= 2:
        for i in movesGraph['sidePlankLegUp']: i.addLateMove(movesGraph['pushups'])
        movesGraph['pushups'].addLateMove(*movesGraph['sidePlankLegUp'])
    movesGraph['mountain'].addLateMove(movesGraph['jumpingSquats'])
    movesGraph['wideLegStance'].addLateMove(movesGraph['jumpingSquats'])
    movesGraph['star'].addLateMove(movesGraph['sideLunges'])
    doubleAdd(movesGraph['oneLeggedChair'], movesGraph['pistolSquats'])
    movesGraph['lieOnFront'].addLateMove(movesGraph['pushups'])
    if difficulty >= 1:
        doubleAdd(movesGraph['standingLegLift4'], movesGraph['pistolSquats'], late=True)
        doubleAdd(movesGraph['standingLegLift1'], movesGraph['pistolSquats'], late=True)

def linkStrengthCooldown(movesGraph, difficulty=1) -> None:
    movesGraph['pushups'].addMove(movesGraph['lieOnFront'])
    for i in movesGraph['pistolSquats']: i.addMove(movesGraph['lieOnBack'])

def linkStrengthAerobics(movesGraph, difficulty=1) -> None:
    movesGraph['runInPlace'].addMove(movesGraph['jumpingSquats'])
    movesGraph['jumpingSquats'].addMove(movesGraph['runInPlace'])



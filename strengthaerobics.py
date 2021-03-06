#/usr/bin/python3

from models import Move

def linkAerobics(movesGraph, difficulty = 1, aerobics = 0):
    """Adds in aerobics moves"""
    movesGraph['jumpingJacks'] = Move("Jumping Jacks", 0, "Jumping Jacks!", 40 + 20*difficulty, movesGraph['mountain'], countReps=True, countdown=True)
    movesGraph['runInPlace'] = Move("Running In Place", 0, "Run In Place", 40 + 20*difficulty, movesGraph['mountain'], movesGraph['jumpingJacks'], countdown=True)
    movesGraph['burpies'] = Move("Burpies!", 0, "Burpies", 30+10*difficulty, movesGraph['vinyasa'], movesGraph['forwardFold'], movesGraph['plank'], \
            extended=Move.reDifficultyTimes([60,75,90], 10, difficulty+aerobics), countReps=True, countdown=True)
    movesGraph['situps'] = Move("Situps", 0, "Situps", 30 + 10*difficulty, movesGraph['vinyasa'], extended=Move.reDifficultyTimes([40,50],10,difficulty + aerobics//2), \
            lateMove=set([movesGraph['boat']]), countReps=True)
    movesGraph['shuffle'] = Move("Shuffle", 0, "Shuffle", 30+10*difficulty, movesGraph['vinyasa']) #//TODO: better description
    movesGraph['highKnees'] = Move("High Knees", 0, "High Knees", 30+10*difficulty, movesGraph['vinyasa'])
    #linking here
    movesGraph['mountain'].addLateMove(movesGraph['jumpingJacks'], movesGraph['runInPlace'], movesGraph['burpies'])
    movesGraph['jumpingJacks'].addLateMove(movesGraph['runInPlace'])
    movesGraph['downwardDog'].addLateMove(movesGraph['burpies'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['situps'])
    movesGraph['staff'].addLateMove(movesGraph['situps'])
    if aerobics >= 2:
        movesGraph['star'].addLateMove(movesGraph['jumpingJacks'])
        for i in movesGraph['eagle']: i.addLateMove(movesGraph['runInPlace'])
    if difficulty >= 1:
        movesGraph['seatedMeditation'].addLateMove(movesGraph['situps'])
        movesGraph['runInPlace'].addMove(movesGraph['vinyasa'])
    else:
        movesGraph['burpies'].addMove(movesGraph['mountain'])
    if aerobics + difficulty >= 3:
        movesGraph['mountain'].addLateMove(movesGraph['highKnees'])
        movesGraph['boat'].addLateMove(movesGraph['situps'])
        movesGraph['flatBack'].addLateMove(movesGraph['plank'])
        movesGraph['wideLegStance'].addLateMove(movesGraph['jumpingJacks'])
        movesGraph['jumpingJacks'].addMove(movesGraph['vinyasa'])

def linkAerobicsCooldown(movesGraph, difficulty=1, aerobics = 0) -> None:
    movesGraph['runInPlace'].addMove(movesGraph['lieOnBack'])
    movesGraph['burpies'].addMove(movesGraph['lieOnFront'])
    movesGraph['situps'].addMove(movesGraph['lieOnBack'])

def linkStrength(movesGraph, difficulty=1, strength = 0) -> None:
    #New moves
    movesGraph['pushups'] = Move("Pushups", 0, "Pushups", 15 + 5*difficulty, movesGraph['vinyasa'], extended=Move.reDifficultyTimes([20,30],5,difficulty), \
            lateMove=set((movesGraph['plank'],) + movesGraph['sidePlank']), countReps=True)
    movesGraph['pistolSquats'] = Move.twoSides("Pistol Squats", "Pistol Squats, %(same)s foot up", 15+5*difficulty, movesGraph['mountain'], countReps=True, \
            countdown=True, lateMove=set([movesGraph['vinyasa']])) #//TODO: better description
    movesGraph['jumpingSquats'] = Move("Jumping Squats", 0, "Jumping Squats", 30, movesGraph['chair'], \
            movesGraph['forwardFold'], lateMove=set([movesGraph['mountain']]), countReps=True)
    movesGraph['jumpingLunges'] = Move("Jumping Lunges", 0, "Jumping Lunges", 20 + 10*difficulty + 10*strength, movesGraph['vinyasa'], countReps=True)
    movesGraph['sideLunges'] = Move("Side Lunges", 0, "Side Lunges", 20 + 10*difficulty, movesGraph['wideLegStance'], countReps=True)
    movesGraph['aroundTheWorld'] = Move.twoSides("Around The World", "Around The World, %(same)s side", 20 + 10*difficulty, movesGraph['mountain'], \
            lateMove=set([movesGraph['vinyasa']]), countReps=True)
    movesGraph['alternatingLunges'] = Move("Alternating Lunges", 0, "Alternating Lunges", 20+10*difficulty, movesGraph['mountain'], \
            movesGraph['vinyasa'], *movesGraph['warrior1'], countdown = True, countReps = True)
    movesGraph['dips'] = Move("Dips", 0, "Dips", 15 + 5*difficulty, movesGraph['vinyasa']) #//TODO: better description
    movesGraph['obliqueCrunch'] = Move.twoSides("Oblique Crunch", "Oblique Crunch, %(same)s side", 20 + 10*difficulty, movesGraph['lieOnBack'], countReps=True)
    movesGraph['balletSquat'] = Move("Ballet Squats", 0, "Ballet Squats", 15 + 5*difficulty, movesGraph['mountain'], movesGraph['star'], countReps=True)
    movesGraph['crunch'] = Move("Crunch", 0, "Crunch", 15+5*difficulty, movesGraph['lieOnBack'], countReps=True, countdown=True)
    movesGraph['jackknife'] = Move("Jack Knife", 0, "Jack Knife", 15+5*difficulty, movesGraph['lieOnBack'], countReps=True, countdown=True)

    #link moves
    movesGraph['downwardDog'].addLateMove(movesGraph['pushups'])
    if difficulty >= 1:
        for i in movesGraph['sidePlank']: i.addLateMove(movesGraph['pushups'])
        movesGraph['mountain'].addLateMove(*movesGraph['aroundTheWorld'])
        movesGraph['chair'].addLateMove(movesGraph['jumpingSquats'], *movesGraph['pistolSquats'])
    if difficulty >= 2 and strength >=2:
        for i in movesGraph['sidePlankLegUp']: i.addLateMove(movesGraph['pushups'])
        movesGraph['pushups'].addLateMove(*movesGraph['sidePlankLegUp'])
        Move.doubleAdd(movesGraph['warrior3'], movesGraph['pistolSquats'], inverted = True, late=True)
        movesGraph['boat'].addMove(movesGraph['jackknife'], *movesGraph['obliqueCrunch'])
    movesGraph['mountain'].addLateMove(movesGraph['jumpingSquats'])
    movesGraph['wideLegStance'].addLateMove(movesGraph['jumpingSquats'], movesGraph['balletSquat'])
    movesGraph['star'].addLateMove(movesGraph['sideLunges'])
    Move.doubleAdd(movesGraph['oneLeggedChair'], movesGraph['pistolSquats'])
    Move.doubleAdd(movesGraph['cresent'], movesGraph['aroundTheWorld'], late = True)
    movesGraph['lieOnFront'].addLateMove(movesGraph['pushups'])
    movesGraph['upwardPlank'].addLateMove(movesGraph['dips'])
    movesGraph['lieOnBack'].addLateMove(movesGraph['crunch'], movesGraph['jackknife'], *movesGraph['obliqueCrunch'])
    movesGraph['lieOnBack'].promoteLate(n=max(1, strength+difficulty))
    if strength >= 2:
        for i in movesGraph['warrior1']: i.addLateMove(movesGraph['alternatingLunges'])
    if strength + difficulty >= 3:
        movesGraph['mountain'].addLateMove(movesGraph['shuffle'])
        Move.doubleAdd(movesGraph['eagle'], movesGraph['pistolSquats'], late=True)
        movesGraph['star'].addLateMove(movesGraph['jumpingSquats'])
        Move.doubleAdd(movesGraph['balancingTableLegOnly'], movesGraph['oneLeggedPlank'], late=True)
        Move.doubleAdd(movesGraph['oneLeggedChair'], movesGraph['pistolSquats'])
        movesGraph['chair'].promoteLate(n=(strength + difficulty)//2)
        for i in movesGraph['warrior1']: i.addLateMove(movesGraph['jumpingLunges'])
    if difficulty >= 1:
        Move.doubleAdd(movesGraph['standingLegLift4'], movesGraph['pistolSquats'], late=True)
        Move.doubleAdd(movesGraph['standingLegLift1'], movesGraph['pistolSquats'], late=True)
    movesGraph['plank'].time += difficulty

def linkStrengthHarder(movesGraph, difficulty=1, strength = 0) -> None:
    Move.moveReverse(movesGraph['pistolSquats'])
    movesGraph['mountain'].promoteLate(n=max(1, difficulty+1))
    movesGraph['plank'].time += 5

def linkStrengthCooldown(movesGraph, difficulty=1, strength = 0) -> None:
    movesGraph['pushups'].addMove(movesGraph['lieOnFront'])
    for i in movesGraph['pistolSquats']: i.addMove(movesGraph['lieOnBack'])

def linkStrengthAerobics(movesGraph, difficulty=1, strength = 0, aerobics = 0) -> None:
    movesGraph['runInPlace'].addMove(movesGraph['jumpingSquats'], movesGraph['plank'])
    movesGraph['jumpingSquats'].addMove(movesGraph['runInPlace'])
    movesGraph['pushups'].addLateMove(movesGraph['burpies'])

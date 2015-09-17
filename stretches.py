#!/usr/bin/python3

from models import Move

def defineStretches(movesGraph, difficulty = 1) -> None:
    """Add in a few stretches?"""
    movesGraph['upwardDogStretches'] = Move.twoSides('Upward Dog Stretch', 'Push your %(same)s shoulder forward', 10, movesGraph['upwardDog'])
    Move.moveReverse(movesGraph['upwardDogStretches'])
    if difficulty < 1:
        movesGraph['upwardDog'].addMove(*movesGraph['upwardDogStretches'])

def linkEasy(movesGraph, difficulty = -1) -> None:
    raise NotImplemented

def linkCooldown(movesGraph, difficulty = 1) -> None:
    """Links cooldown moves in."""
    movesGraph['twistedHeadToKnee'] = Move.twoSides("Twisted Head To Knee", "Take your %(same)s hand and grab the inside of your %(same)s foot.\
            Lean sideways over your %(same)s leg.", 30, movesGraph['seatedMeditation'], movesGraph['staff'], movesGraph['lieOnBack'])
    movesGraph['preztel'] = Move.twoSides("Preztel", "Take your %(same)s foot and put it in front of your %(other)s knee. Pull your %(other)s knee \
            towards you", 30, movesGraph['lieOnBack'])
    movesGraph['four'] = Move.twoSides("Four", "Four pose, %(same)s side", 30, movesGraph['supportedShoulderStand'])
    for i in movesGraph['four']: i.addLateMove(movesGraph['lieOnBack'])
    Move.moveReverse(movesGraph['four'], movesGraph['preztel'], movesGraph['twistedHeadToKnee'])

    movesGraph['child'].addMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['downwardDog'].addMove(movesGraph['table'], movesGraph['child'], movesGraph['lieOnBack'])
    movesGraph['vinyasa'].addMove(movesGraph['child'], movesGraph['lieOnBack'], movesGraph['staff'], movesGraph['upwardDog'])
    movesGraph['staff'].addMove(movesGraph['hero'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['cowFace'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['seatedTwist'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['twistedHeadToKnee'])
    movesGraph['mountain'].addMove(movesGraph['backBend'], *movesGraph['standingSideStretch'])
    movesGraph['mountain'].addMove(*movesGraph['standingTwist'])
    movesGraph['backBend'].removeMove(*movesGraph['standingSideStretch'])
    movesGraph['crow'].addMove(movesGraph['child'])
    movesGraph['lieOnBack'].addMove(*movesGraph['preztel'])
    movesGraph['supportedShoulderStand'].addMove(*movesGraph['four'])
    for i in movesGraph['birdOfParadise']: i.addMove(movesGraph['mountain'])
    for i in movesGraph['sidePlank']: i.addMove(movesGraph['lieOnFront'])
    for i in movesGraph['sidePlankLegUp']: i.addMove(movesGraph['lieOnFront'])
    for i in movesGraph['standingLegLift1']: i.addMove(movesGraph['mountain'])

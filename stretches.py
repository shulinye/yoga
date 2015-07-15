#!/usr/bin/python3

from moves import Move, doubleAdd, twoSides, moveReverse, reDifficultyTimes


def linkEasy(movesGraph, difficulty = -1) -> None:
    raise NotImplemented

def linkCooldown(movesGraph) -> None:
    """Links cooldown moves in."""
    movesGraph['twistedHeadToKnee'] = twoSides("Twisted Head To Knee", "Take your %(same)s hand and grab the inside of your %(same)s foot.\
            Lean sideways over your %(same)s leg.", 30, movesGraph['seatedMeditation'], movesGraph['staff'], movesGraph['lieOnBack'])

    movesGraph['child'].addMove(*movesGraph['childsPoseSideStretch'])
    movesGraph['downwardDog'].addMove(movesGraph['table'], movesGraph['child'], movesGraph['lieOnBack'])
    movesGraph['vinyasa'].addMove(movesGraph['child'], movesGraph['lieOnBack'], movesGraph['staff'], movesGraph['upwardDog'])
    movesGraph['staff'].addMove(movesGraph['hero'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['cowFace'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['seatedTwist'])
    movesGraph['seatedMeditation'].addMove(*movesGraph['twistedHeadToKnee'])
    movesGraph['mountain'].addMove(movesGraph['backBend'], *movesGraph['standingSideStretch'])
    movesGraph['backBend'].removeMove(*movesGraph['standingSideStretch'])
    movesGraph['crow'].addMove(movesGraph['child'])
    for i in movesGraph['sidePlank']: i.addMove(movesGraph['lieOnFront'])
    for i in movesGraph['sidePlankLegUp']: i.addMove(movesGraph['lieOnFront'])
    for i in movesGraph['standingLegLift1']: i.addMove(movesGraph['mountain'])

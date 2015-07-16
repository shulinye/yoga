#!/usr/bin/python3

import argparse
import os.path
import logging
LOG_FILENAME = '/tmp/yoga.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

import moves
import strengthaerobics
import stretches

def sloppyRun(func, *args, **kwargs):
    """Runs a function, catching all exceptions
    and writing them to a log file."""
    try:
        return func(*args, **kwargs)
    except:
        logging.exception(func.__name__ + str(args) + str(kwargs))

def log_isinstance(ob, t, context=None, logfunc = logging.error):
    if not isinstance(ob, t):
        logfunc(repr(ob) + " is not " + repr(t) + (" :" + str(context) if context is not None else ""))
        return False
    return True

def generateAllMoves(d = 1, a = 0, s = 0):
    movesGraph = moves.generateMoves(d)
    sloppyRun(moves.linkMain, movesGraph, difficulty=d)
    if a: sloppyRun(strengthaerobics.linkAerobics, movesGraph, d, a)
    if s: sloppyRun(strengthaerobics.linkStrength, movesGraph, d, s)
    if a*s: sloppyRun(strengthaerobics.linkStrengthAerobics, movesGraph, d, s, a)
    sloppyRun(moves.unlinkWarmup, movesGraph, [], d)
    sloppyRun(moves.linkHarder, movesGraph, d)
    if s: sloppyRun(strengthaerobics.linkStrengthHarder, movesGraph, d, s)
    sloppyRun(moves.linkEnding, movesGraph)
    sloppyRun(stretches.linkCooldown, movesGraph)
    if s: sloppyRun(strengthaerobics.linkStrengthCooldown, movesGraph, d, s)
    if a: sloppyRun(strengthaerobics.linkAerobicsCooldown, movesGraph, d, a)
    sloppyRun(moves.linkSavasana, movesGraph, difficulty = d)
    return movesGraph

def checkChildType(move):
    for m in move.nextMove:
        log_isinstance(m, moves.Move, context=move)
    if "lateMove" in move.kwargs:
        for m in move.kwargs["lateMove"]:
            log_isinstance(m, moves.Move, context=move)


def checkGraph(movesGraph):
    for i in movesGraph:
        if isinstance(movesGraph[i], tuple):
            for j in movesGraph[i]:
                if log_isinstance(j, moves.Move):
                   checkChildType(j)
        elif log_isinstance(movesGraph[i], moves.Move):
            checkChildType(movesGraph[i])
        
        
def checkLog(filename):
    if os.path.isfile(filename):
        print("Error file exists")

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--aerobics", dest="a", help="Insert aerobics moves", action='count', default=0)
    parser.add_argument("-s", "--strength", dest="s", help="Insert strength moves", action='count', default=0)
    parser.add_argument("-d", "--difficulty", dest="d", help="Difficulty: larger number=harder", default=1, type=int, choices=[-1,0,1,2])
    args = parser.parse_args()
    print("Generating moves graph")
    movesGraph = generateAllMoves(**vars(args))
    print("Checking graph")
    checkGraph(movesGraph)
    checkLog(LOG_FILENAME)

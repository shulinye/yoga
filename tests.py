#!/usr/bin/python3

"""Various utils to check the integrity of the movesGraph"""

import argparse
import datetime
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

def log_isinstance(ob, t, context=None, level = logging.ERROR):
    if not isinstance(ob, t):
        logging.log(level, repr(ob) + " is not " + repr(t) + (" :" + str(context) if context is not None else ""))
        return False
    return True

def generateAllMoves(d = 1, a = 0, s = 0):
    movesGraph = moves.generateMoves(d)
    sloppyRun(stretches.defineStretches, movesGraph, difficulty=d)
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
    print("%d moves discovered" % len(movesGraph))
    return movesGraph

def checkChildType(move):
    if len(move.nextMove) == 0:
        logging.error(str(move) + " has no children")
    for m in move:
        log_isinstance(m, moves.Move, context=move)

def checkGraph(movesGraph):
    for i in movesGraph.values():
        if isinstance(i, tuple):
            for j in i:
                if log_isinstance(j, moves.Move):
                   checkChildType(j)
        elif log_isinstance(i, moves.Move):
            checkChildType(i)
        
def checkConnected(movesGraph):
    allmoves = set()
    linkedmoves = set()
    for i in movesGraph.values():
        if isinstance(i, tuple):
            for j in i:
                allmoves.add(j)
                linkedmoves.update(j)
        else:
            allmoves.add(i)
            linkedmoves.update(i)
    return allmoves.difference(linkedmoves)
        
def checkLog(filename):
    if os.path.isfile(filename):
        print("Error file exists:", filename)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--aerobics", dest="a", help="Insert aerobics moves", action='count', default=0)
    parser.add_argument("-s", "--strength", dest="s", help="Insert strength moves", action='count', default=0)
    parser.add_argument("-d", "--difficulty", dest="d", help="Difficulty: larger number=harder", default=1, type=int, choices=[-1,0,1,2])
    args = parser.parse_args()
    logging.info("Running with settings: " + str(vars(args)))
    logging.info("Run time: " + datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'))
    print("Generating moves graph")
    movesGraph = generateAllMoves(**vars(args))
    print("Checking graph")
    checkGraph(movesGraph)
    m = checkConnected(movesGraph)
    if m: logging.debug("There is no way to get to the following moves:\n    " + "\n    ".join(repr(i) for i in sorted(m)))
    checkLog(LOG_FILENAME)

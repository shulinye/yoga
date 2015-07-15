#!/usr/bin/python3

import argparse
import logging
LOG_FILENAME = '/tmp/yoga.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

import moves
import strengthaerobics
import stretches

def generateAllMoves(d = 1, a = 0, s = 0):
    movesGraph = moves.generateMoves(d)
    try:
        moves.linkMain(movesGraph, difficulty=d)
    except:
        logging.exception('linkMain')
    try:
        if a: strengthaerobics.linkAerobics(movesGraph, d, a)
    except:
        logging.exception('linkAerobics')
    try:
        if s: strengthaerobics.linkStrength(movesGraph, d, s)
    except:
        logging.exception('linkStrength')
    try:
        if a*s: strengthaerobics.linkStrengthAerobics(movesGraph, d, s, a)
    except:
        logging.exception('linkStrengthAerobics')
    try:
        moves.unlinkWarmup(movesGraph)
    except:
        logging.exception('unlinkWarmup')
    try:
        moves.linkHarder(movesGraph, d)
    except:
        logging.exception('linkHarder')
    try:
        if s: strengthaerobics.linkStrengthHarder(movesGraph, d, s)
    except:
        logging.exception('linkStrengthHarder')
    try:
        moves.linkEnding(movesGraph)
    except:
        logging.exception('linkEnding')
    try:
        stretches.linkCooldown(movesGraph)
    except:
        logging.exception('linkCooldown')
    try:
        if s: strengthaerobics.linkStrengthCooldown(movesGraph, d, s)
    except:
        logging.exception('linkStrengthCooldown')
    try:
        if a: strengthaerobics.linkAerobicsCooldown(movesGraph, d, a)
    except:
        logging.exception('linkAerobicsCooldown')
    try:
        moves.linkSavasana(movesGraph, difficulty = d)
    except:
        logging.exception('linkSavasana')
    return movesGraph

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--aerobics", dest="a", help="Insert aerobics moves", action='count', default=0)
    parser.add_argument("-s", "--strength", dest="s", help="Insert strength moves", action='count', default=0)
    parser.add_argument("-d", "--difficulty", dest="d", help="Difficulty: larger number=harder", default=1, type=int, choices=[-1,0,1,2])
    args = parser.parse_args()
    movesGraph = generateAllMoves(**vars(args))

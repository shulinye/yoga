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
        moves.linkSavasana(movesGraph, d)
    except:
        logging.exception('linkSavasana')


if __name__== "__main__":
    generateAllMoves()

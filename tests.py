#!/usr/bin/python3

import logging

import moves
import strengthaerobics

def generateAllMoves(d = 1, a = 0, s = 0):
    movesGraph = moves.generateMoves(d)
    try:
        moves.unlinkWarmup(movesGraph)
    except:
        #deal with exceptions

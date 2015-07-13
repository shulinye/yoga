#!/usr/bin/python3

"""Takes a file of moves and plays it back for you"""

import fileinput
import moves


def main(**kwargs):
    movesGraph = moves.generateMoves(difficulty=2)
    moves.linkStrength(movesGraph, difficulty=2, strength=5)
    moves.linkAerobics(movesGraph, difficulty=2, aerobics=5)

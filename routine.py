#!/usr/bin/python3

"""Takes a file of moves and plays it back for you"""

import fileinput
import re

import moves
import strengthaerobics

re_move = re.compile(r'[a-zA-Z\s]+[0-9]{1,2}$')

def main(**kwargs):
    movesGraph = moves.generateMoves(difficulty=2)
    strengthaerobics.linkStrength(movesGraph, difficulty=2, strength=5)
    strengthaerobics.linkAerobics(movesGraph, difficulty=2, aerobics=5)

    m = {movesGraph[k].title: movesGraph[k] for k in movesGraph}

    for line in fileinput.input():
        if re_move.match(line.strip()):
            print(line)
    return m

if __name__ == "__main__":
    main()

#!/usr/bin/python3

"""Application that reads out yoga moves to you."""

__version__="0.01"
__author__="Shulin Ye"

import collections
import colorama
import datetime
import time
import sys
import random

import dijkstras
import utils
import moves
import stretches
import strengthaerobics

colorama.init()

def routine(li : list, imbalance : list, playLast=True, **kwargs) -> "Move":
    """Plays a list of moves. if playLast = False, returns last move instead of playing it
    If KeyboardInterrupt, tries to return the move it's currently on"""
    try:
        for i in range(len(li)-1):
            current_pose, next_pose = li[i], li[i+1]
            current_pose(imbalance=imbalance, nextMove=next_pose, **kwargs)
    except KeyboardInterrupt:
        sys.stdout.write(colorama.Style.RESET_ALL)
        return next_pose if "next_pose" in locals() else li[0]
    if not playLast: return li[-1]
    return li[-1](imbalance=imbalance,**kwargs)

def fixImbalance(pose : "Move", imbalance : list, maxImbalance=1, maxTime=60, **kwargs) -> "Move":
    """Might try to fix the imbalance. Might not. Depends on how big the imbalance is.
    (Set maxImbalance to 1 to ensure imbalance gets fixed)
    if KeyboardInterrupt: Immediately return whatever pose it was on."""
    fixImbalanceChance = len(imbalance)/maxImbalance
    if random.random() < fixImbalanceChance:
        end = time.time() + maxTime
        while imbalance and time.time() < end:
            try:
                pose = routine(dijkstras.dijkstra(pose,*imbalance,imbalance=imbalance), imbalance=imbalance, **kwargs)
            except (TimeoutError, ValueError):
                break
            except KeyboardInterrupt:
                sys.stdout.write(colorama.Style.RESET_ALL)
                return pose
    return pose

def main(**kwargs):
    defaults = {
            "time": 30,
            "difficulty": 1,
            "initial_move": "child",
            "warmup": True,
            "cooldown": True,
            "aerobics": 0,
            "strength": 0,
            "target": "plank",
            "verbose":1,
            "memory":5,
            "outfile": None,
            }
    defaults.update(kwargs)
    if defaults["outfile"]:
        f = open(defaults["outfile"], "a")
        f.write(str(datetime.datetime.now()) + "\n")
        f.write(str(defaults) + "\n")
    else:
        f = None
    utils.speak('Beginning in')
    utils.countdown(3)

    if defaults["verbose"] >= 2: print(defaults)
    elif defaults["verbose"] >= 1: print("Workout length:", defaults['time'], "minutes.", "Beginning in:")
    # setup
    total_time = defaults['time']*60
    movesGraph = moves.generateMoves(difficulty=defaults["difficulty"])
    start = time.time()
    end = start + total_time
    imbalance = []
    prev = collections.deque([],defaults["memory"])
    try:
        pose = movesGraph[defaults['initial_move']]
    except KeyError:
        pose = movesGraph['child']

    try:
        #warmup
        if defaults["warmup"]:
            pose = pose(time=min(30,max(15, total_time//120+7)), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"], f=f)
            while time.time() - start < min(max(45,total_time//15),300):
                pose = pose(imbalance=imbalance, extended=True, early=True, prev=prev, verbosity=defaults["verbose"], f=f) #start slower
        #get me to my target:
        moves.linkMain(movesGraph, defaults['difficulty'])
        if defaults['aerobics']:
            strengthaerobics.linkAerobics(movesGraph, defaults["difficulty"], defaults["aerobics"])
        if defaults['strength']:
            strengthaerobics.linkStrength(movesGraph, defaults["difficulty"], defaults["strength"])
            if defaults['aerobics']:
                strengthaerobics.linkStrengthAerobics(movesGraph, defaults["difficulty"], defaults["strength"], defaults["aerobics"])
        if defaults['warmup']:
            pose = fixImbalance(pose,imbalance,maxTime=max(45,total_time//12), prev=prev, verbosity=defaults['verbose'], f=f)
        imbalance = moves.unlinkWarmup(movesGraph, imbalance=imbalance, difficulty=defaults["difficulty"])
        try:
            target = movesGraph[defaults['target']]
        except KeyError:
            target = movesGraph['plank']
        try:
            pose = routine(dijkstras.dijkstra(pose, target, imbalance=imbalance), imbalance=imbalance, playLast=False, prev=prev, verbosity=defaults["verbose"], f=f)
        except (TimeoutError, ValueError):
            pass
        if defaults["warmup"]:
            print("Warmup Over: " + utils.prettyTime(time.time() - start))
            if f: f.write("Warmup Over: " + utils.prettyTime(time.time() - start) + '\n\n')
            utils.speak("Alright, warmup over.")
        pose = pose(imbalance=imbalance, prev=prev, verbosity=defaults["verbose"], f=f)
        #starting main part of workout
        while time.time() - start < total_time//2 - 30:
            pose = fixImbalance(pose, imbalance, maxImbalance=10 + total_time//600, maxTime=max(60,total_time//12), prev=prev, verbosity=defaults["verbose"], f=f)
            pose = pose(imbalance=imbalance, prev=prev, verbosity=defaults["verbose"], f=f)
        #add harder poses in here
        if defaults["difficulty"] >= 1:
            moves.linkHarder(movesGraph, defaults["difficulty"])
            if defaults["strength"]:
                strengthaerobics.linkStrengthHarder(movesGraph, defaults["difficulty"], defaults["strength"])
        pose = fixImbalance(pose, imbalance, maxTime=max(60, total_time//10), prev=prev, verbosity=defaults["verbose"], f=f)
        try:
            pose = routine(dijkstras.dijkstra(pose, movesGraph[defaults['target']], imbalance=imbalance), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"], f=f)
        except (TimeoutError, KeyError, ValueError):
            pass
        if defaults["verbose"] >= 1:
            print("Halfway point: " + utils.prettyTime(time.time()-start))
            if f: f.write("Halfway point: " + utils.prettyTime(time.time()-start) + '\n\n')
            utils.speak("We have reached the halfway point")
        #end adding harder poses
        while time.time() < (end - max(60, total_time//5)) if defaults['cooldown'] else end:
            extendedChance = (time.time() - start)/total_time
            extended = random.random() < extendedChance
            pose = fixImbalance(pose, imbalance, maxImbalance=8+total_time//800, maxTime=max(110,total_time//10), prev=prev, verbosity=defaults["verbose"], f=f)
            pose = pose(harder=True if defaults["difficulty"] >=1 else False, imbalance = imbalance, extended=extended, prev=prev, verbosity=defaults["verbose"], f=f)
        moves.linkEnding(movesGraph)
        while time.time() < (end - max(60, total_time//10)):
            pose = fixImbalance(pose, imbalance, maxImbalance=max(1,total_time//800), maxTime=max(120, total_time//10), prev=prev, verbosity=defaults["verbose"], f=f)
            pose = pose(imbalance = imbalance, prev=prev, verbosity=defaults["verbose"], f=f)
        if defaults["cooldown"]:
            pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(75, total_time//10+15), prev=prev, verbosity=defaults["verbose"], f=f)
            print("Cooldown begins: " + utils.prettyTime(time.time() - start))
            if f: f.write("Cooldown begins: " + utils.prettyTime(time.time() - start)+'\n\n')
            utils.speak("Cooldown begins")
            stretches.linkCooldown(movesGraph, difficulty=defaults["difficulty"])
            if defaults["strength"]: strengthaerobics.linkStrengthCooldown(movesGraph,difficulty=defaults["difficulty"], strength = defaults["strength"])
            if defaults["aerobics"]: strengthaerobics.linkAerobicsCooldown(movesGraph,difficulty=defaults["difficulty"], aerobics = defaults["aerobics"])
            try:
                pose = routine(dijkstras.dijkstra(pose, movesGraph['wheel'], imbalance=imbalance), imbalance=imbalance, prev=prev, verbosity=defaults['verbose'], f=f)
            except (TimeoutError, ValueError):
                pass
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(60, total_time//10), prev=prev, verbosity=defaults['verbose'], f=f)
        while time.time() < (end-max(30, total_time//15)) if defaults["cooldown"] else end:
            pose = pose(imbalance=imbalance, extended=True, prev=prev, verbosity=defaults['verbose'], f=f)
            pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(30, total_time//10), prev=prev, verbosity=defaults['verbose'], f=f)
        if defaults['cooldown']:
            moves.linkSavasana(movesGraph, difficulty=defaults['difficulty'])
            pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(30, total_time//10), prev=prev, verbosity=defaults['verbose'], f=f)
            pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance=imbalance), imbalance=imbalance, prev=prev, verbosity=defaults['verbose'], f=f)
    except (KeyboardInterrupt, BrokenPipeError):
        moves.linkSavasana(movesGraph, difficulty=defaults['difficulty'])
        pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance = imbalance), imbalance=imbalance, prev=prev, verbosity=defaults['verbose'], f=f)
        return imbalance
    finally:
        final_time = utils.prettyTime(time.time() - start)
        if f:
            f.write('Total Time: %s\n\n' % final_time)
            f.close()
        utils.speak('Done! Total time was %s' % final_time.replace('(','').replace(')',''))
        sys.stdout.write(colorama.Style.RESET_ALL)
        print('\nTotal Time: %s' % final_time)
        print(imbalance)
    return imbalance

if __name__== '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage = './main.py [options]')
    parser.add_argument('--version', action='version', version='yoga %s' % __version__)
    parser.add_argument('-t', '--time', help='time (in minutes)', default=30, type=int)
    parser.add_argument('-a', '--aerobics', help='Insert aerobics moves', action='count', default=0)
    parser.add_argument('-s', '--strength', help='Insert strength moves', action='count', default=0)
    parser.add_argument('-d', '--difficulty', help='Difficulty: larger number=harder', default=1, type=int, choices=[-1,0,1,2])
    parser.add_argument('-w', '--skip-warmup', action='store_false', dest='warmup', help='skips warmup period')
    parser.add_argument('-c', '--skip-cooldown', action='store_false', dest='cooldown', help='skips cooldown')
    parser.add_argument('-i', '--initial-move', default='child', choices=['child', 'seatedMeditation', 'lieOnBack', 'mountain'])
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--debug', action='store_true', help='Debug mode: all delays removed.')
    parser.add_argument('-m', '--memory', default=5, type=int, help='How many previous moves shall I remember? (default: 5)')
    parser.add_argument('--target', default='plank', choices=['plank', 'boat'])
    parser.add_argument('-o', '--outfile', help='File to write log to')
    args = parser.parse_args()
    utils.DEBUG = args.debug
    main(**vars(args))

#!/usr/bin/python3

__version__="0.01"
__author__="Shulin Ye"

"""An attempt to make a command-line based yoga program.
call with python3 main.py [length of routine wanted, in minutes]
NOTE: uses espeak for audio"""

import argparse
import time
import sys
import random

import dijkstras
import utils
import moves

debug = False


def routine(li : list, imbalance, playLast = True, **kwargs) -> "Move":
    """Plays a list of moves. if playLast = False, returns last move instead of playing it
    If KeyboardInterrupt, tries to return the move it's currently on"""
    li_copy = li.copy()
    try:
        for i in range(len(li)-1):
            current_pose, next_pose = li_copy[i], li_copy[i+1]
            current_pose(imbalance=imbalance, nextMove=next_pose, **kwargs)
    except KeyboardInterrupt:
        try:
            return next_pose
        except NameError:
            return li[0]
    if not playLast: return li_copy[-1]
    return li_copy[-1](imbalance=imbalance,**kwargs)

def fixImbalance(pose, imbalance, maxImbalance=1, maxTime = 60, **kwargs) -> "Move":
    """Might try to fix the imbalance. Might not. Depends on how big the imbalance is.
    (Set maxImbalance to 1 to ensure imbalance gets fixed)
    if KeyboardInterrupt: Immediately return whatever pose it was on."""
    fixImbalanceChance = len(imbalance)/maxImbalance
    if random.random() < fixImbalanceChance:
        end = time.time() + maxTime
        while imbalance and time.time() < end:
            try:
                pose = routine(dijkstras.dijkstra(pose,*imbalance,imbalance=imbalance, **kwargs), imbalance=imbalance)
            except dijkstras.TimeExceededError:
                break
            except ValueError:
                break
            except KeyboardInterrupt:
                return pose
    return pose

def main(**kwargs):
    defaults = {
            "time": DEFAULT_TIME,
            "difficulty": 1,
            "initial_move": "child",
            "warmup": True,
            "cooldown": True,
            "aerobics": False,
            "strength": False,
            "target": "plank",
            }
    defaults.update(kwargs)
    utils.speak("Beginning in")
    print("Workout length:", defaults['time'], "minutes")
    print("Beginning in:")
    utils.countdown(3)
    total_time = defaults['time']*60
    movesGraph = moves.generateMoves(difficulty=defaults["difficulty"])
    start = time.time()
    end = start + total_time
    imbalance = []
    try:
        pose = movesGraph[defaults['initial_move']]
    except KeyError:
        pose = movesGraph['child']
    try:
        #warmup
        if defaults["warmup"]:
            pose = pose(time=min(15, total_time//120+7), imbalance=imbalance)
            while time.time() - start < max(45,total_time//15):
                pose = pose(imbalance=imbalance, extended=True, early=True) #start slower
        #get me to table:
        moves.linkMain(movesGraph, d)
        if defaults["aerobics"]:
            moves.linkAerobics(movesGraph, d)
        pose = fixImbalance(pose,imbalance,maxTime=max(45,total_time//12))
        pose = routine(dijkstras.dijkstra(pose, movesGraph['downwardDog'], imbalance=imbalance), imbalance=imbalance, playLast=False) #get me to downwards dog
        imbalance = moves.unlinkWarmup(movesGraph, imbalance=imbalance)
        try:
            pose = routine(dijkstras.dijkstra(pose,movesGraph[defaults['target']], imbalance=imbalance), imbalance=imbalance)
        except KeyError:
            pass
        except ValueError:
            pass
        except dijkstras.TimeExceededError:
            pass
        pose = pose(nextMove=movesGraph['plank'])
        utils.speak("Alright, warmup over.")
        pose = pose(imbalance=imbalance)
        #starting main part of workout
        while time.time() - start < total_time//2 - 30:
            pose = fixImbalance(pose,imbalance,maxImbalance=10 + total_time//600,maxTime=max(60,total_time//12))
            pose = pose(imbalance=imbalance)
        #add harder poses in here
        if d >= 1: moves.linkHarder(movesGraph, d)
        pose = fixImbalance(pose, imbalance, maxTime=max(60, total_time//10))
        try:
            pose = routine(dijkstras.dijkstra(pose, movesGraph[defaults['target']], imbalance=imbalance), imbalance=imbalance)
        except KeyError:
            pass
        except ValueError:
            pass
        except dijkstras.TimeExceededError:
            pass
        utils.speak("We have reached the halfway point")
        #end adding harder poses
        while time.time() < (end - max(60, total_time//10)) if defaults["cooldown"] else end:
            extendedChance = (time.time() - start)/total_time
            extended = random.random() < extendedChance
            pose = fixImbalance(pose, imbalance, maxImbalance=8 + total_time//800, maxTime=max(110,total_time//10))
            pose = pose(harder=True, imbalance = imbalance, extended=extended)
        if defaults["cooldown"]:
            #add in more restorative poses here
            moves.linkCooldown(movesGraph)
        #one more try to fix that damned imbalance
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(60, total_time//10))
        #move into more restorative poses....
        while time.time() < (end-max(30, total_time//10)) if defaults["cooldown"] else end:
            pose = pose(imbalance=imbalance, extended=True)
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(30, total_time//10))
        if defaults["cooldown"]
            moves.linkSavasana(movesGraph, difficulty=d)
            pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance=imbalance), imbalance=imbalance) #Somehow, get seamlessly to savasana
    except KeyboardInterrupt:
        moves.linkSavasana(movesGraph, difficulty=d)
        pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance = imbalance), imbalance=imbalance)
    finally:
        print(imbalance)
        utils.speak("Done!")
        print("\nTotal Time: " + utils.prettyTime(time.time()-start))

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="time (in minutes)", default=30, type=int)
    parser.add_argument("-a", "--aerobics", help="Insert aerobics moves", action='store_true')
    parser.add_argument("-s", "--strength", help="Insert strength moves/NotImplemented", action='store_true')
    parser.add_argument("-d", "--difficulty", help="Difficulty/NotImplemented", default=1, type=int, choices=[-1,0,1,2])
    parser.add_argument("-w",  "--skip-warmup", action='store_false', dest="warmup", help="skips warmup period")
    parser.add_argument("-c", "--skip-cooldown", action='store_false', dest='cooldown', help='skips cooldown')
    parser.add_argument("-i", "--initial-move", default="child", choices=["child", "seatedMeditation", "lieOnBack"])
    parser.add_argument("--target", default="plank", choices=["plank", "boat"])
    parser.add_argument("--version", action="version", version="yoga " + __version__)
    args = parser.parse_args()
    #print(args)
    main(**vars(args))

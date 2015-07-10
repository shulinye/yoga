#!/usr/bin/python3

__version__="0.01"
__author__="Shulin Ye"

import argparse
import collections
import time
import sys
import random

import dijkstras
import utils
import moves

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
                pose = routine(dijkstras.dijkstra(pose,*imbalance,imbalance=imbalance), imbalance=imbalance, **kwargs)
            except dijkstras.TimeExceededError:
                break
            except ValueError:
                break
            except KeyboardInterrupt:
                return pose
    return pose

def main(**kwargs):
    defaults = {
            "time": 30,
            "difficulty": 1,
            "initial_move": "child",
            "warmup": True,
            "cooldown": True,
            "aerobics": False,
            "strength": False,
            "target": "plank",
            "verbose":1,
            "memory":5,
            }
    defaults.update(kwargs)
    print(defaults)
    utils.speak("Beginning in")
    if defaults["verbose"] >= 1:
        print("Workout length:", defaults['time'], "minutes")
        print("Beginning in:")
    utils.countdown(3)
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
            pose = pose(time=max(15, total_time//120+7), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"])
            while time.time() - start < max(45,total_time//15):
                pose = pose(imbalance=imbalance, extended=True, early=True, prev=prev, verbosity=defaults["verbose"]) #start slower
        #get me to table:
        moves.linkMain(movesGraph, defaults["difficulty"])
        if defaults["aerobics"]: moves.linkAerobics(movesGraph, defaults["difficulty"])
        if defaults["strength"]: moves.linkStrength(movesGraph, defaults["difficulty"])
        pose = fixImbalance(pose,imbalance,maxTime=max(45,total_time//12), prev=prev, verbosity=defaults["verbose"])
        pose = routine(dijkstras.dijkstra(pose, movesGraph['downwardDog'], imbalance=imbalance), imbalance=imbalance, playLast=False, prev=prev, verbosity=defaults["verbose"]) #get me to downwards dog
        imbalance = moves.unlinkWarmup(movesGraph, imbalance=imbalance)
        try:
            pose = routine(dijkstras.dijkstra(pose,movesGraph[defaults['target']], imbalance=imbalance), imbalance=imbalance, prev=prev,verbosity=defaults["verbose"])
        except KeyError:
            pass
        except ValueError:
            pass
        except dijkstras.TimeExceededError:
            pass
        pose = pose(nextMove=movesGraph['plank'], prev=prev, verbosity=defaults["verbose"])
        utils.speak("Alright, warmup over.")
        pose = pose(imbalance=imbalance, prev=prev, verbosity=defaults["verbose"])
        #starting main part of workout
        while time.time() - start < total_time//2 - 30:
            pose = fixImbalance(pose,imbalance,maxImbalance=10 + total_time//600,maxTime=max(60,total_time//12), prev=prev, verbosity=defaults["verbose"])
            pose = pose(imbalance=imbalance, prev=prev, verbosity=defaults["verbose"])
        #add harder poses in here
        if defaults["difficulty"] >= 1: moves.linkHarder(movesGraph, defaults["difficulty"])
        pose = fixImbalance(pose, imbalance, maxTime=max(60, total_time//10), prev=prev, verbosity=defaults["verbose"])
        try:
            pose = routine(dijkstras.dijkstra(pose, movesGraph[defaults['target']], imbalance=imbalance), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"])
        except KeyError:
            pass
        except ValueError:
            pass
        except dijkstras.TimeExceededError:
            pass
        if defaults["verbose"] >= 1: utils.speak("We have reached the halfway point")
        #end adding harder poses
        while time.time() < (end - max(60, total_time//10)) if defaults["cooldown"] else end:
            extendedChance = (time.time() - start)/total_time
            extended = random.random() < extendedChance
            pose = fixImbalance(pose, imbalance, maxImbalance=8 + total_time//800, maxTime=max(110,total_time//10), prev=prev, verbosity=defaults["verbose"])
            pose = pose(harder=True if defaults["difficulty"] >=1 else False, imbalance = imbalance, extended=extended, prev=prev, verbosity=defaults["verbose"])
        if defaults["cooldown"]:
            utils.speak("Cooldown begins")
            moves.linkCooldown(movesGraph)
        print("wtf")
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(60, total_time//10), prev=prev, verbosity=defaults["verbose"])
        while time.time() < (end-max(30, total_time//10)) if defaults["cooldown"] else end:
            pose = pose(imbalance=imbalance, extended=True, prev=prev, verbosity=defaults["verbose"])
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(30, total_time//10), prev=prev, verbosity=defaults["verbose"])
        if defaults["cooldown"]:
            print("reached cooldown")
            moves.linkSavasana(movesGraph, difficulty=defaults["difficulty"])
            pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance=imbalance), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"]) #Somehow, get seamlessly to savasana
    except KeyboardInterrupt:
        moves.linkSavasana(movesGraph, difficulty=defaults["difficulty"])
        pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance = imbalance), imbalance=imbalance, prev=prev, verbosity=defaults["verbose"])
    finally:
        utils.speak("Done!")
        print("\nTotal Time: " + utils.prettyTime(time.time()-start))
        print(imbalance)
        return imbalance

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="time (in minutes)", default=30, type=int)
    parser.add_argument("-a", "--aerobics", help="Insert aerobics moves", action='store_true')
    parser.add_argument("-s", "--strength", help="Insert strength moves/NotImplemented", action='store_true')
    parser.add_argument("-d", "--difficulty", help="Difficulty", default=1, type=int, choices=[-1,0,1,2])
    parser.add_argument("-w",  "--skip-warmup", action='store_false', dest="warmup", help="skips warmup period")
    parser.add_argument("-c", "--skip-cooldown", action='store_false', dest='cooldown', help='skips cooldown')
    parser.add_argument("-i", "--initial-move", default="child", choices=["child", "seatedMeditation", "lieOnBack"])
    parser.add_argument("-v", "--verbose", action='count', default=0)
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument("-m", "--memory", default=5, type=int, help="How many previous moves shall i remember?")
    parser.add_argument("--target", default="plank", choices=["plank", "boat"])
    parser.add_argument("--version", action="version", version="yoga " + __version__)
    args = parser.parse_args()
    utils.DEBUG = vars(args)["debug"]
    main(**vars(args))

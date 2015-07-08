#!/usr/bin/python3

__version__="incomplete"
__author__="Shulin Ye"

"""An attempt to make a command-line based yoga program.
call with python3 main.py [length of routine wanted, in minutes]
NOTE: uses espeak for audio"""

import time
import sys
import random

import dijkstras
import utils
import moves

debug = False
aerobics = True
strength = True
DEFAULT_TIME = 30 #minutes

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
                print("got TimeExceededError", imbalance)
                break
            except ValueError:
                print("probably impossible...", imbalance)
                break
            except KeyboardInterrupt:
                return pose
        if imbalance: print("Timeout: imbalance remains:", imbalance)
    return pose

def main():
    utils.speak("Beginning in")
    print("Beginning in:")
    utils.countdown(3)
    try:
        total_time = 60*int(sys.argv[-1])
    except ValueError:
        print("No time gotten. Using %s minutes" % DEFAULT_TIME)
        total_time = DEFAULT_TIME*60
    movesGraph = moves.generateMoves()
    start = time.time()
    end = start + total_time
    imbalance = []
    pose = movesGraph['child'](time=min(15, total_time//60), imbalance=imbalance)
    try:
        #warmup
        while time.time() - start < max(45,total_time//15):
            pose = pose(imbalance=imbalance, extended=True, early=True) #start slower
        #get me to table:
        moves.linkMain(movesGraph)
        if aerobics: moves.linkAerobics(movesGraph)
        pose = fixImbalance(pose,imbalance,maxTime=max(45,total_time//12))
        pose = routine(dijkstras.dijkstra(pose, movesGraph['downwardDog']), imbalance=imbalance, playLast=False) #get me to downwards dog
        imbalance = moves.unlinkWarmup(movesGraph, imbalance=imbalance)
        pose = pose(nextMove=movesGraph['plank'])
        utils.speak("Alright, warmup over.")
        pose = pose(imbalance=imbalance)
        #starting main part of workout
        while time.time() - start < total_time//2 - 30:
            pose = fixImbalance(pose,imbalance,maxImbalance=10 + total_time//600,maxTime=max(60,total_time//12))
            pose = pose(imbalance=imbalance)
        #add harder poses in here
        moves.linkHarder(movesGraph)
        pose = fixImbalance(pose, imbalance, maxTime=max(60, total_time//10))
        utils.speak("We have reached the halfway point")
        #end adding harder poses
        while time.time() < (end - max(60, total_time//10)):
            extendedChance = (time.time() - start)/total_time
            extended = random.random() < extendedChance
            pose = fixImbalance(pose, imbalance, maxImbalance=8 + total_time//800, maxTime=max(110,total_time//10))
            pose = pose(harder=True, imbalance = imbalance, extended=extended)
        #add in more restorative poses here
        moves.linkCooldown(movesGraph)
        #one more try to fix that damned imbalance
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(60, total_time//10))
        #move into more restorative poses....
        while time.time() < (end-max(30, total_time//10)):
            pose = pose(imbalance=imbalance, extended=True)
        #deal with imbalances, somehow
        moves.linkSavasana(movesGraph)
        pose = fixImbalance(pose, imbalance, maxImbalance=1, maxTime=max(30, total_time//10))
        pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana'], imbalance=imbalance), imbalance=imbalance) #Somehow, get seamlessly to savasana
    except KeyboardInterrupt:
        moves.linkSavasana(movesGraph)
        pose = routine(dijkstras.dijkstra(pose, movesGraph['savasana']))
    finally:
        print(imbalance)
        utils.speak("Done!")
        print("\nTotal Time: " + utils.prettyTime(time.time()-start))

if __name__== "__main__":
    main()

#!/usr/bin/python3

import random
import time
import utils


class Meta(type):
    def __repr__(cls):
        return cls.__name__

class Move(object):
    __metaclass__ = Meta
    def __init__(self, title: str, side: int, audio: str, time: int, *moves, **kwargs):
        """Creates a Move. Arguments are: title,
        side (-1 for left, 0 for None, 1 for Right)
        audio (for espeak), and time (in seconds)"""
        self.title = title
        self.side = side
        self.audio = audio
        self.time = max(time,0)
        self.last = None
        self.nextMove = set(moves)
        self.kwargs = kwargs

    def updateKwargs(self, **kwargs):
        self.kwargs.update(kwargs)

    def addExtendedTime(self, *times):
        if "exended_time" in self.kwargs:
            self.kwargs["extended_time"] += times
        else:
            self.kwargs["extended_time"] = times

    def addOtherSide(self, otherside):
        self.otherside = otherside

    def addMove(self, *moves):
        self.nextMove.update(moves)

    def removeMove(self, *moves):
        self.nextMove.difference_update(moves)
        if "lateMove" in self.kwargs:
            self.kwargs["lateMove"].difference_update(moves)

    def addLateMove(self, *moves):
        if "lateMove" not in self.kwargs:
            self.kwargs["lateMove"] = set()
        self.kwargs["lateMove"].update(moves)

    def notLast(self, prev=None) -> "Move":
        """Returns a move, trying to avoid
        both self.last and the N moves
        previously called."""
        if self.last and len(self.nextMove) > 1:
            movesCopy = self.nextMove.copy()
            try:
                movesCopy.remove(self.last)
            except KeyError:
                pass
            if prev is not None:
                movesCopy = movesCopy.difference(prev)
            if movesCopy:
                return random.choice(tuple(movesCopy))
        if self.nextMove:
            return random.choice(tuple(self.nextMove))
        else:
            if "lateMove" in self.kwargs and self.kwargs["lateMove"]:
                c = random.choice(tuple(self.kwargs["lateMove"]))
                self.promoteLate(c)
                return c
        raise ValueError("No possible move found")

    def promoteLate(self, move=None) -> None:
        """Promotes a late move up to the normal move pool, if possible.
        If no move given, promotes a random move"""
        if "lateMove" in self.kwargs:
            if move is None:
                try:
                    move = self.kwargs["lateMove"].pop()
                    self.addMove(move)
                except KeyError:
                    pass
            elif move in self.kwargs["lateMove"]:
                self.addMove(move)
                self.kwargs["lateMove"].discard(move)

    def repCount(self):
        if "countReps" in self.kwargs and self.kwargs["countReps"]:
            utils.speak("How many reps?")
            return input("How many reps? ")
        else:
            return None

    def __call__(self, imbalance=[], prev=None, verbosity=1, **kwargs) -> "Move":
        """Tells me which pose I'm supposed to do and how I'm supposed to do it.
        Also figures out next pose and deals with adding late moves"""
        print("\n" + utils.color.BOLD + self.title + utils.color.END)
        # Deal with imbalances
        if self.side:
            if self in imbalance:
                imbalance.remove(self)
            else:
                imbalance.append(self.otherside)
        if verbosity >= 2:
            print(utils.color.BLUE + "Prev:", "; ".join(str(i) for i in prev) + utils.color.END)
            print(utils.color.PURPLE + "Imbalances:", "; ".join(str(i) for i in imbalance) + utils.color.END)
        if prev is not None:
            prev.append(self)
        # What is my next move?
        if "nextMove" in kwargs:
            # Assume the caller knows what they're doing right now.
            # Should possibly assert that nextMove is a plausible nextMove
            nextMove = kwargs["nextMove"]
            self.promoteLate(nextMove)
        elif imbalance:
            for i in imbalance:
                if i in self.nextMove:
                    nextMove = i
                    break
            else:
                nextMove = self.notLast(prev)
        else:
            nextMove = self.notLast(prev)
        if nextMove is not None:
            print("Next Move: " + nextMove.title)
            if verbosity >= 1:
                print(utils.color.DARKCYAN + "My options were: " + "; ".join(str(i) for i in self.nextMove) + utils.color.END)
                if "lateMove" in self.kwargs and self.kwargs["lateMove"]:
                    print(utils.color.GREEN + "Latemoves: " + "; ".join(str(i) for i in self.kwargs["lateMove"]) + utils.color.END)
            self.last = nextMove
        # Tell me what to do
        utils.speak(self.audio)
        time.sleep(0.2)
        if "early" in kwargs and kwargs["early"] and "early" in self.kwargs:
            utils.speak(self.kwargs["early"])
        elif "harder" in kwargs and kwargs["harder"] and "harder" in self.kwargs:
            utils.speak(self.kwargs["harder"])
        # How long am I supposed to do it?
        if "time" in kwargs:
            t = kwargs["time"]
        elif "extended" in kwargs and kwargs["extended"] and "extended_time" in self.kwargs:
            t = random.choice(self.kwargs["extended_time"])
        else:
            t = self.time
        if "bind" in self.kwargs and self.kwargs["bind"]:
            utils.speak("Bind if you want to")
        if t > 5:
            utils.speak(str(t) + "seconds")
        utils.countdown(t)
        if "f" in kwargs and kwargs["f"]:
            kwargs["f"].write(self.title + " " + str(t)+"\n")
            s = self.repCount()
            if s: kwargs["f"].write(str(s) + " reps\n")
            kwargs["f"].write("\n")
            kwargs["f"].flush()
        if "bind" in self.kwargs and self.kwargs["bind"]:
            utils.speak("Release bind")
        self.promoteLate()  #Add in options for harder followup moves next time
        return nextMove

    def __repr__(self):
        return "Move(%s)" % self.title

    def __str__(self):
        return self.title

    def __hash__(self):
        return hash(self.title)

    def __eq__(self, other):
        if other is None: return False
        if type(other) == tuple:
            print(other)
            raise ValueError(str(other) + " is not a move")
        return self.title == other.title

    def __ne__(self, other):
        if other is None: return True
        return self.title != other.title

    def __lt__(self, other):
        return self.title < other.title

    @staticmethod
    def twoSides(title : str , audio : str , time : int , *args, **kwargs):
        """Hey, you have two legs. Convenience method to generate both left and right sides for a move"""
        dicR = {"same": "Right", "other": "Left"}
        dicL = {"same": "Left", "other": "Right"}
        if "%" in audio:
            R = Move(title + ", Right", 1, audio % dicR, time, *args, **kwargs)
            L = Move(title + ", Left", -1, audio % dicL, time, *args, **kwargs)
        else:
            R = Move(title + ", Right", 1, audio, time, *args, **kwargs)
            L = Move(title + ", Left", -1, audio, time, *args, **kwargs)
        R.addOtherSide(L)
        L.addOtherSide(R)
        return (R,L)

    @staticmethod
    def doubleAdd(move, *args, inverted=False, late=False):
        """Convenience method to help link moves that have sides
        inverted: if True, causes L to be linked to R and R to be linked to L
        late: if True, causes move to be linked as a late move"""
        f = Move.addLateMove if late else Move.addMove
        if inverted:
            f(move[0], *[i[1] for i in args])
            f(move[1], *[i[0] for i in args])
        else:
            f(move[0], *[i[0] for i in args])
            f(move[1], *[i[1] for i in args])

    
    @staticmethod
    def moveReverse(*moves, late=False):
        f = Move.addLateMove if late else Move.addMove
        for i in moves:
            f(i[0],i[1])
            f(i[1],i[0])

    @staticmethod
    def reDifficultyTimes(li, val, difficulty):
        return [max(i + val*difficulty,0) for i in li]


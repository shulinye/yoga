#!/usr/bin/python3

import colorama
import random
import time
import utils

colorama.init()

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
        self.time = max(time, 0)
        self.last = None
        self.nextMove = set(moves)
        for k, v in kwargs.items():
            setattr(self, k, v)
        if "lateMove" not in kwargs:
            self.lateMove = set()
        if "extended_time" not in kwargs:
            self.extended_time = []

    @property
    def times(self):
        return [self.time] + self.extended_time

    @times.setter
    def times(self, args):
        args = sorted(args)
        self.time = max(args[0], 0)
        self.extended_time = args[1:]

    def updateKwargs(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def addMove(self, *moves) -> None:
        self.nextMove.update(moves)

    def removeMove(self, *moves) -> None:
        self.nextMove.difference_update(moves)
        self.lateMove.difference_update(moves)

    def addLateMove(self, *moves) -> None:
        self.lateMove.update(moves)
        self.lateMove.difference_update(self.nextMove)

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
        if self.lateMove:
            c = random.choice(tuple(self.lateMove))
            self.promoteLate(c)
            return c
        raise ValueError("No possible move found")

    def promoteLate(self, *args, n=1) -> None:
        """Promotes a late move up to the normal move pool, if possible.
        If no move given, promotes a random move"""
        if args:
            self.nextMove.update(self.lateMove.intersection(args))
            self.lateMove.difference_update(args)
        elif self.lateMove:
            moves = random.sample(tuple(self.lateMove), min(n,len(self.lateMove)))
            self.lateMove.difference_update(moves)
            self.addMove(*moves)

    def repCount(self) -> None:
        if self.countReps:
            utils.speak("How many reps?")
            return input("How many reps? ")

    def __call__(self, imbalance=[], prev=None, verbose=1, **kwargs) -> "Move":
        """Tells me which pose I'm supposed to do and how I'm supposed to do it.
        Also figures out next pose and deals with adding late moves"""
        print("\n" + colorama.Style.BRIGHT + self.title + colorama.Style.NORMAL)
        # Deal with imbalances
        if self.side:
            if self in imbalance: imbalance.remove(self)
            else: imbalance.append(self.otherside)
        if verbose >= 2:
            print(colorama.Fore.BLUE + utils.wrapper.fill('Prev: ' + '; '.join(map(str, prev))))
            print(colorama.Fore.MAGENTA + utils.wrapper.fill('Imbalances: ' + '; '.join(map(str,imbalance))) + colorama.Fore.RESET)
        if prev is not None: prev.append(self)
        # What is my next move?
        if 'nextMove' in kwargs:
            # Assume the caller knows what they're doing right now.
            # Should possibly assert that nextMove is a plausible nextMove
            nextMove = kwargs['nextMove']
            self.promoteLate(nextMove)
        else:
            for i in imbalance:
                if i in self.nextMove:
                    nextMove = i
                    break
            else:
                nextMove = self.notLast(prev)
        if nextMove is not None:
            print('Next Move: ' + nextMove.title)
            self.last = nextMove
            if verbose >= 1:
                print(colorama.Fore.CYAN + utils.wrapper.fill('My options were: ' + '; '.join(str(i) for i in self.nextMove)))
                print(colorama.Fore.GREEN + utils.wrapper.fill('Latemoves: ' + '; '.join(str(i) for i in self.lateMove)) + colorama.Fore.RESET)
        # Tell me what to do
        utils.speak(self.audio)
        time.sleep(0.2)
        for i in ('early', 'harder'):
            if i in kwargs and kwargs[i]: utils.speak(getattr(self, i, None))
        # How long am I supposed to do it?
        if 'time' in kwargs: t = kwargs['time']
        elif 'extended' in kwargs and kwargs['extended'] and self.extended_time: t = random.choice(self.extended_time)
        else: t = self.time
        # Actually count down
        if getattr(self, 'bind', None): utils.speak("Bind if you want to")
        if t > 5: utils.speak(str(t) + " seconds")
        if getattr(self, 'countdown', None): utils.countdown(t, incremental = True)
        else: utils.countdown(t)
        #record to file, if we were given a file
        if 'f' in kwargs and kwargs['f']:
            kwargs['f'].write('%s: %d' % (self.title, t))
            s = self.repCount()
            if s: kwargs['f'].write(' - %s reps' % s)
            kwargs['f'].write('\n')
            kwargs['f'].flush()
        if getattr(self, 'bind', None): utils.speak('Release bind')
        self.promoteLate()  # Add in options for harder followup moves next time
        return nextMove

    def __repr__(self):
        return 'Move(%s)' % self.title

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def __hash__(self):
        return hash(self.title)

    def __eq__(self, other):
        if not isinstance(other, Move): return False
        return self.title == other.title

    def __ne__(self, other):
        if not isinstance(other, Move): return True
        return self.title != other.title

    def __lt__(self, other):
        if not isinstance(other, Move): raise TypeError("Unorderable types: Move() <= " + str(type(other)))
        return self.title < other.title

    def __contains__(self, other):
        if other in self.nextMove: return True
        if other in self.lateMove: return True
        return False

    def __len__(self):
        return len(self.nextMove.union(self.lateMove))
    
    def __iter__(self):
        yield from self.nextMove.union(self.lateMove)

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
        R.otherside = L
        L.otherside = R
        return (R,L)

    @staticmethod
    def doubleAdd(move, *moves, inverted=False, late=False):
        """Convenience method to help link moves that have sides
        inverted: if True, causes L to be linked to R and R to be linked to L
        late: if True, causes move to be linked as a late move"""
        f = Move.addLateMove if late else Move.addMove
        if inverted:
            f(move[0], *[i[1] for i in moves])
            f(move[1], *[i[0] for i in moves])
        else:
            f(move[0], *[i[0] for i in moves])
            f(move[1], *[i[1] for i in moves])

    
    @staticmethod
    def moveReverse(*moves, late=False):
        """Convenience method. Link a move to its .otherside, and also in reverse."""
        f = Move.addLateMove if late else Move.addMove
        for i in moves:
            f(i[0],i[1])
            f(i[1],i[0])

    @staticmethod
    def reDifficultyTimes(li, val, difficulty):
        return [max(i + val*difficulty,0) for i in li]


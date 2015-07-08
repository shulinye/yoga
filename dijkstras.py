#!/usr/bin/python3

import heapq
import time

LATEPENALTY = 40
IMBALANCE_BOUNTY = 3
LAST_MOVE_PENALTY = 10

class TimeExceededError(Exception):
    """Dijkstras Algorithm did not give path that would end
    in time limit given."""
    def __init__(self, value):
        self.value = value

def bounty(node : int, imbalance : list , cost : int ) -> int:
    """Awards a bounty to a node that's currently in the imbalanced list"""
    if node is None: return 1000 #Not a move, just set my value insanely high
    return cost - IMBALANCE_BOUNTY if node in imbalance else cost

def dijkstra(start : "node" , *goal, limit=None, imbalance=[]) -> list:
    """Uses dijkstra's algorithm to find the shortest path to a target move.
    If multiple targets are entered, use the first one found.
    raises: ValueError if frontier is ever empty or node becomes None
    raises: TimeExceededError if time exceeded"""
    if start in goal: return [start]
    node = start
    frontier = [(0, start)]
    seen = set()
    explored = set()
    prev = {}
    while True:
        if len(frontier) == 0:
            raise ValueError("frontier is empty")
        cost, node = heapq.heappop(frontier)
        if limit and cost > limit:
            raise TimeExceededError("Time exceeded. No match found")
        if node is None:
            raise ValueError("Node is None")
        new_cost = cost + node.time
        late_cost = cost + node.time + LATEPENALTY
        if node in goal:
            li = [node]
            n = node
            while n != start:
                li.append(prev[n])
                n = prev[n]
            return li[::-1]
        explored.add(node)
        not_seen = node.nextMove.difference(seen).difference(explored)
        has_late = "lateMove" in node.kwargs
        late_not_seen = node.kwargs["lateMove"].difference(seen).difference(explored) if has_late else set()
        frontier_copy = frontier.copy()
        for i,j in frontier_copy:
            if j not in explored:
                if j in node.nextMove:
                    my_cost = bounty(j, imbalance, new_cost)
                    if node.last and j == node.last: my_cost += LAST_MOVE_PENALTY
                    if i > my_cost:
                        frontier.remove((i,j))
                        frontier.append((new_cost, j))
                        prev[j] = node
                elif has_late and j in node.kwargs["lateMove"]:
                    my_cost = bounty(j, imbalance, late_cost)
                    if node.last and j == node.last: my_cost += LAST_MOVE_PENALTY
                    if i > late_cost:
                        frontier.remove((i,j))
                        frontier.append((late_cost,j))
                        prev[j] = node
        heapq.heapify(frontier)
        for i in not_seen:
            my_cost = bounty(i, imbalance, new_cost)
            if node.last and i == node.last: my_cost += LAST_MOVE_PENALTY
            heapq.heappush(frontier, (my_cost,i))
            seen.add(i)
            prev[i] = node
        for i in late_not_seen:
            if node.last and i == node.last: my_cost += LAST_MOVE_PENALTY
            my_cost = bounty(i, imbalance, late_cost)
            heapq.heappush(frontier, (my_cost,i))
            seen.add(i)
            prev[i] = node

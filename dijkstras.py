#!/usr/bin/python3

import heapq
import time

LATEPENALTY = 250
IMBALANCE_BOUNTY = 3

class TimeExceededError(Exception):
    def __init__(self, value):
        self.value = value

def bounty(node, imbalance, cost):
    return cost - IMBALANCE_BOUNTY if node in imbalance else cost

def dijkstra(start, *goal, limit=None, imbalance=[]):
    """Uses dijkstra's algorithm to find the shortest path to a target move.
    If multiple targets are entered, use the first one found."""
    node = start
    frontier = [(0, start)]
    seen = set()
    explored = set()
    prev = {}
    if start in goal: return [start]
    while True:
        if len(frontier) == 0:
            raise ValueError("frontier is empty")
        cost, node = heapq.heappop(frontier)
        if limit and cost > limit:
            raise TimeExceededError("Time exceeded. No match found")
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
                    if i > my_cost:
                        frontier.remove((i,j))
                        frontier.append((new_cost, j))
                        prev[j] = node
                elif has_late and j in node.kwargs["lateMove"]:
                    my_cost = bounty(j, imbalance, late_cost)
                    if i > late_cost:
                        frontier.remove((i,j))
                        frontier.append((late_cost,j))
                        prev[j] = node
        heapq.heapify(frontier)
        for i in not_seen:
            my_cost = bounty(i, imbalance, new_cost)
            heapq.heappush(frontier, (my_cost,i))
            seen.add(i)
            prev[i] = node
        for i in late_not_seen:
            my_cost = bounty(i, imbalance, late_cost)
            heapq.heappush(frontier, (my_cost,i))
            seen.add(i)
            prev[i] = node

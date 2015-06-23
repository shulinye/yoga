#!/usr/bin/python3

import heapq
import time

LATEPENALTY = 250


def dijkstra(start, *goal, limit=None):
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
            raise KeyError("Time exceeded. No match found")
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
                    if i > newcost:
                        frontier.remove((i,j))
                        frontier.append((newcost, j))
                        prev[j] = node
                elif has_late and j in node.kwargs["lateMove"]:
                    if i > late_cost:
                        frontier.remove((i,j))
                        frontier.append((late_cost,j))
                        prev[j] = node
        heapq.heapify(frontier)
        for i in not_seen:
            heapq.heappush(frontier, (newcost,i))
            seen.add(i)
            prev[i] = node
        for i in late_not_seen:
            heapq.heappush(frontier, (latecost,i))
            seen.add(i)
            prev[i] = node

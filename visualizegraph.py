#!/usr/bin/python3

import networkx as nx
import matplotlib.pyplot as plt
import tests


def addMove(move, graph):
    if move is not None and move not in graph:
        graph.add_node(move, name=move.title)
    for i in move.nextMove:
        if i is not None:
            if i not in graph: graph.add_node(i, name=i.title)
            graph.add_edge(move, i)
    if "lateMove" in move.kwargs:
        for i in move.kwargs["lateMove"]:
            if i not in graph: graph.add_node(i, name=i.title)
            graph.add_edge(move, i, color="green")

def main(d=1,a=0,s=0):
    G = nx.DiGraph()
    movesGraph = tests.generateAllMoves()
    for key in movesGraph:
        if isinstance(movesGraph[key], tuple):
            for i in movesGraph[key]:
                addMove(i,G)
        else:
            addMove(movesGraph[key],G)
    nx.draw_networkx(G, node_shape='8')
    plt.savefig("test.png")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import string
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

'''
    #############
    #ab.c.d.e.fg#
    ###h#i#j#k###
      #l#m#n#o#
      #########
'''
edgeweights = {
    ("a", "b"): 1,
    ("b", "h"): 2,
    ("b", "c"): 2,
    ("c", "h"): 2,
    ("c", "i"): 2,
    ("c", "d"): 2,
    ("d", "i"): 2,
    ("d", "j"): 2,
    ("d", "e"): 2,
    ("e", "j"): 2,
    ("e", "k"): 2,
    ("e", "f"): 2,
    ("f", "k"): 2,
    ("f", "g"): 1,
    ("h", "l"): 1,
    ("i", "m"): 1,
    ("j", "n"): 1,
    ("k", "o"): 1,
}
targets = {
    "A": ("h", "l"),
    "B": ("i", "m"),
    "C": ("j", "n"),
    "D": ("k", "o")
}
weights = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    orderedlets = []

    for line in input_fh:
        letters = re.findall("[A-Z]", line.strip("\n"))
        if len(letters) > 0:
            orderedlets.extend(letters)

    startingpos = []

    for letter in orderedlets:
        pod = letter + "1"
        if pod in startingpos:
            pod = letter[0] + "2"
        startingpos.append(pod)

    return startingpos


# Create grid
def buildGrid(setup, pods):
    G = nx.Graph()
    G.add_nodes_from(string.ascii_lowercase[0:15], occupied=False, occupant=None)
    updateEdges(G)

    attrs = {}

    for i, pod in enumerate(setup):
        node = chr(ord("h") + i)
        attrs[node] = {"occupied": True, "occupant": pod}
        pods[pod] = node

    nx.set_node_attributes(G, attrs)

    return G


def updateEdges(G):
    for edge in edgeweights:
        G.add_edge(*edge, weight=edgeweights[edge])


def findCheapestPath(G, pods):
    # Key = moves, Value = cost
    states = {stateTuple(pods): 0}

    # For each pod, calculate each initial move
    for _ in range(15):
        newstates = states.copy()
        for state in states:
            podpos = podDict(state)
            for pod in podpos:
                newpods = podpos.copy()
                allpaths = nx.single_source_dijkstra_path(G, pods[pod])
                for end in allpaths:
                    if validPath(allpaths[end], pods):
                        newpods[pod] = allpaths[end][-1]
                        cost = states[state] + \
                            nx.shortest_path_length(G, pods[pod], newpods[pod], weight="weight") * weights[pod[0]]
                        newstate = stateTuple(newpods)
                        if newstate not in newstates or cost < newstates[newstate]:
                            newstates[newstate] = cost

        states = newstates

    print(states)


def stateTuple(pods):
    state = []
    for pod in sorted(pods):
        state.extend([pod, pods[pod]])
    return tuple(state)


def podDict(pods):
    it = iter(pods)
    return dict(zip(it, it))


def validPath(points, pods):
    if len(points) == 1:
        return False
    for p in points[1:]:
        if p in pods.values():
            return False
    return True


def main():
    setup = parseInput(args.input)
    pods = {}
    G = buildGrid(setup, pods)

    findCheapestPath(G, pods)

    # print("Got this far, solved manually, come back to finish")
    # print("Save states, update if cheaper cost, don't need to track every path")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
from networkx import exception as nxex

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
alocs = []
vectors = [-1j, 1, 1j, -1]
start = 0j
end = 0j


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    global start
    global end
    row = 0

    for line in input_fh:
        for i, x in enumerate(list(line.strip("\n"))):
            if x == "S":
                grid[i + row * 1j] = "a"
                start = i + row * 1j
            elif x == "E":
                grid[i + row * 1j] = "z"
                end = i + row * 1j
            elif x == "a":
                grid[i + row * 1j] = x
                alocs.append(i + row * 1j)
            else:
                grid[i + row * 1j] = x
        row += 1


# Create networkx map from grid
def createMap():
    G = nx.DiGraph()

    # Create nodes
    for pos in grid.keys():
        G.add_node(pos)

    # For each node identify moveable edges
    for pos in grid.keys():
        for dest in getEdges(pos):
            G.add_edge(pos, dest)

    return G


# Calculate movable edges for a given node
def getEdges(pos):
    edges = []

    for dest in [pos + x for x in vectors]:
        if dest in grid:
            if ord(grid[dest]) <= ord(grid[pos]) + 1:
                edges.append(dest)

    return edges


# Find shortest path from start to end
def processData(G):
    print(f"Part 1: {len(nx.shortest_path(G, start, end)) - 1}")


# Process harder
def processMore(G):
    minroute = 500

    for begin in alocs:
        try:
            if len(nx.shortest_path(G, begin, end)) - 1 < minroute:
                minroute = len(nx.shortest_path(G, begin, end)) - 1
        except nxex.NetworkXNoPath:
            continue

    print(f"Part 2: {minroute}")


def main():
    parseInput(args.input)
    G = createMap()

    # Part 1
    processData(G)

    # Part 2
    processMore(G)


if __name__ == "__main__":
    main()

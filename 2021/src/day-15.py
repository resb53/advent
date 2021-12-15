#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
gridmax = []
FULL = 5


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    x = 0
    y = 0

    for line in input_fh:
        line = line.strip("\n")
        for val in line:
            grid[(x, y)] = int(val)
            x += 1
        x = 0
        y += 1

    # Create network of nodes between grid positions to use those as edges
    gridmax.append(max(grid.keys(), key=lambda k: k[0])[0] + 1)
    gridmax.append(max(grid.keys(), key=lambda k: k[1])[1] + 1)
    maxx = gridmax[0] * FULL - 1
    maxy = gridmax[1] * FULL - 1

    return (maxx, maxy)


# Build nx graph
def buildGraph(maxx, maxy):
    G = nx.DiGraph()

    for y in range(maxy + 1):
        for x in range(maxx + 1):
            node = (x, y)
            G.add_node(node)
            if x != maxx:
                noderight = (x + 1, y)
                weightout = getWeight(noderight)
                weightback = getWeight(node)
                G.add_edge(node, noderight, weight=weightout)
                G.add_edge(noderight, node, weight=weightback)
            if y != maxy:
                nodedown = (x, y + 1)
                weightout = getWeight(nodedown)
                weightback = getWeight(node)
                G.add_edge(node, nodedown, weight=weightout)
                G.add_edge(nodedown, node, weight=weightback)

    return G


# Get edge weight
def getWeight(loc):
    magx = loc[0] // gridmax[0]
    remx = loc[0] % gridmax[0]
    magy = loc[1] // gridmax[1]
    remy = loc[1] % gridmax[1]

    weight = (grid[(remx, remy)] + magx + magy)

    while weight > 9:
        weight -= 9

    return weight


# For each pass, identify its seat
def shortestPath(G, start, end):
    sp = nx.shortest_path(G, source=start, target=end, weight="weight")
    cost = 0
    for a, b in zip(sp, sp[1:]):
        cost += G[a][b]["weight"]
    return cost


# Process harder
def processMore():
    return False


def main():
    (maxx, maxy) = parseInput(args.input)
    Graph = buildGraph(maxx, maxy)

    # Part 1
    print(f"Solution to part 1: {shortestPath(Graph, (0, 0), (gridmax[0] - 1, gridmax[1] - 1))}")

    # Part 2
    print(f"Solution to part 2: {shortestPath(Graph, (0, 0), (maxx, maxy))}")


if __name__ == "__main__":
    main()

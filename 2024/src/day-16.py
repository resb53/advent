#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
from itertools import combinations

sys.setrecursionlimit(5000)

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
bounds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        line = line.rstrip()
        for x, val in enumerate(line):
            grid[x + 1j * y] = val
            if val == "S":
                start = x + 1j * y
                grid[x + 1j * y] = "."
            elif val == "E":
                end = x + 1j * y
                grid[x + 1j * y] = "."
        y += 1

    bounds.extend([x+1, y])

    return start, end


# Print the grid
def printGrid():
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            print(grid[x + 1j * y], end="")
        print()


# Build graph and find lowest cost way to reach the end.
def processData(start, end):
    G = nx.Graph()
    visited = set()
    exploreFromNode(G, start, visited)
    nodes = [start, end]
    for x in G.nodes:
        connections = len(list(G.neighbors(x)))
        if connections != 2:
            nodes.append(x)

    # Collapse to a simpler graph
    C = nx.Graph()
    C.add_nodes_from(nodes)
    for pair in combinations(nodes, 2):
        route = nx.shortest_path(G, pair[0], pair[1])
        if spanningRoute(route, nodes):
            continue
        C.add_edge(pair[0], pair[1], weight=routeWeight(route))

    print(nx.shortest_path(C, start, end, weight="weight"))

    return nx.shortest_path_length(C, start, end, weight="weight")


# Find connected nodes
def exploreFromNode(G: nx.Graph, pos, visited):
    if pos in visited:
        return
    visited.add(pos)
    for dir in [1, 1j, -1, -1j]:
        if grid[pos + dir] == ".":
            G.add_edge(pos, pos + dir)
            exploreFromNode(G, pos + dir, visited)


# Return true if this route>2 spans additional nodes
def spanningRoute(route, nodes):
    if len(route) == 2:
        return False
    else:
        for x in route[1:-2]:
            if x in nodes:
                return True
    return False


# Calculate the weight of a completed route
def routeWeight(route: list) -> int:
    weight = 0
    dir = 1
    lst = route[0]
    for nxt in route[1:]:
        if nxt - lst == dir:
            weight += 1
            lst = nxt
        else:
            weight += 1001
            dir = nxt - lst
            lst = nxt

    return weight


# Calculate number of neighbours that are .
def neighbours(p):
    n = 0
    for dir in [1, 1j, -1, -1j]:
        if grid[p + dir] == ".":
            n += 1
    return n


# Process harder
def processMore():
    return False


def main():
    s, e = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(s, e)}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

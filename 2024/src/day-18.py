#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
grid = {}
bounds = [70, 70]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        x, y = line.split(",")
        data.append(int(x) + 1j * int(y))

    # Build the grid too
    for y in range(0, bounds[1]+1):
        for x in range(0, bounds[0]+1):
            grid[x + 1j * y] = "."


# Print the grid
def printGrid():
    for y in range(0, bounds[1]+1):
        for x in range(0, bounds[0]+1):
            print(grid[x + 1j * y], end="")
        print()


# Simulate 1024 bytes, and find the shortest path
def processData():
    for pos in data[0:1024]:
        grid[pos] = "#"

    # Build graph
    G = nx.Graph()
    for pos in grid:
        if grid[pos] == '.':
            addEdges(G, pos)

    return len(nx.shortest_path(G, 0, bounds[0] + 1j * bounds[1])) - 1


# Find edges for the graph
def addEdges(G: nx.Graph, node):
    for dir in [1, 1j, -1, -1j]:
        if node + dir in grid and grid[node + dir] == ".":
            G.add_edge(node, node + dir)


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

G = nx.DiGraph()
grid = {}
FULL = 1


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
    maxx = (max(grid.keys(), key=lambda k: k[0])[0] + 1) * FULL - 1
    maxy = (max(grid.keys(), key=lambda k: k[1])[1] + 1) * FULL - 1

    print(maxx, maxy)

    # Set edges attributes right and down for each node unless node is right or bottom edge
    for node in G.nodes:
        if node[0] != maxx:
            noderight = (node[0] + 1, node[1])
            G.add_edge(node, noderight, weight=grid[noderight])
            G.add_edge(noderight, node, weight=grid[node])
        if node[1] != maxy:
            nodedown = (node[0], node[1] + 1)
            G.add_edge(node, nodedown, weight=grid[nodedown])
            G.add_edge(nodedown, node, weight=grid[node])

    for y in range(maxy + 1):
        for x in range(maxx + 1):
            node = (x, y)
            G.add_node(node)
            if x != maxx:
                noderight = (x + 1, y)
                G.add_edge(node, noderight, weight=grid[noderight])
                G.add_edge(noderight, node, weight=grid[node])
            if y != maxy:
                nodedown = (x, y + 1)
                G.add_edge(node, nodedown, weight=grid[nodedown])
                G.add_edge(nodedown, node, weight=grid[node])

    return (maxx, maxy)


# For each pass, identify its seat
def shortestPath(start, end):
    sp = nx.shortest_path(G, source=start, target=end, weight="weight")
    cost = 0
    for x in sp[1:]:
        cost += grid[x]
    print(cost)


# Process harder
def processMore():
    return False


def main():
    (maxx, maxy) = parseInput(args.input)

    # Part 1
    shortestPath((0, 0), (maxx, maxy))

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

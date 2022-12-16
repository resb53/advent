#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import re
import copy
from itertools import combinations, permutations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        match = re.match(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)\n$", line)

        if match is not None:
            data.append([match[1], int(match[2]), match[3].split(", ")])


# Build cave map - it's never worth stopping at or turning on a valve when the valve = 0
def caveMap():
    G = nx.Graph()
    zeroes = []

    for paths in data:
        G.add_node(paths[0], flow=paths[1])
        G.add_edges_from([(paths[0], x, {"weight": 1}) for x in paths[2]])

    for node in G.nodes():
        if node != "AA" and G.nodes[node]["flow"] == 0:
            zeroes.append(node)

    for node in zeroes:
        for connect in combinations(G.neighbors(node), 2):
            if connect not in G.edges():
                G.add_edge(connect[0], connect[1], weight=nx.shortest_path_length(G, connect[0], connect[1], "weight"))
            else:
                print(f"Check {connect}")
        G.remove_node(node)

    print(G.nodes())
    for edge in G.edges():
        print(f'{edge}: {G.edges[edge]["weight"]}')

    return G


# Find route that releases the most pressure in 30 minutes
def processData(caves: nx.Graph):
    print(list(nx.all_pairs_shortest_path(caves)))


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)
    caves = caveMap()

    # Part 1
    processData(caves)

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

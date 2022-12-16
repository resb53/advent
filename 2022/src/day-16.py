#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import re
import copy

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


# Build cave map
def caveMap():
    G = nx.Graph()

    for paths in data:
        G.add_node(paths[0], flow=paths[1])
        G.add_nodes_from(paths[2])
        G.add_edges_from([(paths[0], x) for x in paths[2]])

    return G


# For each pass, identify its seat
def processData(caves: nx.DiGraph):

    # List of actions, current released pressure, current exhaust rate, opened valves
    actions = [[["AA"], 0, 0, []]]

    # BFS through all routes until time passed == 30
    for _ in range(10):
        updated = []
        for route in actions:
            pos = route[0][-1]
            if pos == "open":
                pos = route[0][-2]

            # If valve closed, could open it
            if pos not in route[3]:
                nextstep = copy.deepcopy(route[0])
                nextstep.append("open")
                exhaust = route[1] + route[2]
                newflow = route[2] + caves.nodes[pos]["flow"]
                opened = copy.deepcopy(route[3])
                opened.append(pos)
                updated.append([nextstep, exhaust, newflow, opened])

            # Could move to any connected room
            for neighbour in caves[pos]:
                nextstep = copy.deepcopy(route[0])
                nextstep.append(neighbour)
                exhaust = route[1] + route[2]
                opened = copy.deepcopy(route[3])
                updated.append([nextstep, exhaust, route[2], route[3]])

            # Could do nothing
            nextstep = copy.deepcopy(route[0])
            nextstep.append(pos)
            exhaust = route[1] + route[2]
            opened = copy.deepcopy(route[3])
            updated.append([nextstep, exhaust, route[2], route[3]])

        actions = updated

    mostflow = 0

    for x in actions:
        if x[1] > mostflow:
            mostflow = x[1]

    print(f"Part 1: {mostflow}")


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

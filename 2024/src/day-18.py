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


# Simulate 1024 bytes, and find the shortest path
def processData():
    G = nx.Graph()
    for y in range(0, bounds[1]+1):
        for x in range(0, bounds[0]+1):
            pos = x + 1j * y
            for dir in [1, 1j, -1, -1j]:
                if inBounds(pos + dir):
                    G.add_edge(pos, pos + dir)

    for corrupt in data[0:1024]:
        G.remove_node(corrupt)

    print(f"Part 1: {len(nx.shortest_path(G, 0, bounds[0] + 1j * bounds[1])) - 1}")

    for corrupt in data[1024:]:
        G.remove_node(corrupt)
        try:
            nx.shortest_path(G, 0, bounds[0] + 1j * bounds[1])
        except nx.exception.NetworkXNoPath:
            answer = ",".join([str(int(corrupt.real)), str(int(corrupt.imag))])
            print(f"Part 2: {answer}")
            break


# Check if position is in bounds
def inBounds(p):
    x = int(p.real)
    y = int(p.imag)
    if x >= 0 and x <= bounds[0]:
        if y >= 0 and y <= bounds[1]:
            return True
    return False


def main():
    parseInput(args.input)
    processData()


if __name__ == "__main__":
    main()

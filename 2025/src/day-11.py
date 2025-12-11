#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()


# Parse the input file
def parseInput(inp):
    G = nx.DiGraph()

    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()

        src, dest = line.split(": ")
        dest = dest.split(" ")

        if src not in G.nodes:
            G.add_node(src)

        for n in dest:
            if n not in G.nodes:
                G.add_node(n)
            G.add_edge(src, n)

    return G


# Find number of paths to out
def processData(G):
    return len(list(nx.all_simple_paths(G, source="you", target="out")))


# Process harder
def processMore(G):
    return False


def main():
    G = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(G)}")

    # Part 2
    print(f"Part 2: {processMore(G)}")


if __name__ == "__main__":
    main()

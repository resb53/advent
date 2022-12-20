#!/usr/bin/env python3

import argparse
import sys

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
        data.append(tuple(int(x) for x in line.strip("\n").split(",")))


def getEdges(blob):
    (x, y, z) = blob
    edges = []

    edges.append(blob + (x + 1, y, z))
    edges.append((x - 1, y, z) + blob)
    edges.append(blob + (x, y + 1, z))
    edges.append((x, y - 1, z) + blob)
    edges.append(blob + (x, y, z + 1))
    edges.append((x, y, z - 1) + blob)

    return edges


# For each cube, store it's edges
def processData():
    outerEdges = set()

    for element in data:
        for edge in getEdges(element):
            if edge not in outerEdges:
                outerEdges.add(edge)
            else:
                outerEdges.remove(edge)

    print(len(outerEdges))


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

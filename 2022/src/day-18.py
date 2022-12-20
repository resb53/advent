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


def getAdjacent(seed, bounds):
    adj = []
    adj.append((seed[0] - 1, seed[1], seed[2]))
    adj.append((seed[0] + 1, seed[1], seed[2]))
    adj.append((seed[0], seed[1] - 1, seed[2]))
    adj.append((seed[0], seed[1] + 1, seed[2]))
    adj.append((seed[0], seed[1], seed[2] - 1))
    adj.append((seed[0], seed[1], seed[2] + 1))

    reduced = adj.copy()
    for x in adj:
        if (
            x[0] < bounds[0] or x[0] > bounds[1] or
            x[1] < bounds[2] or x[1] > bounds[3] or
            x[2] < bounds[4] or x[2] > bounds[5]
           ):
            reduced.remove(x)

    return reduced


def fillWater():
    minx = min([x[0] for x in data]) - 1
    maxx = max([x[0] for x in data]) + 1
    miny = min([y[1] for y in data]) - 1
    maxy = max([y[1] for y in data]) + 1
    minz = min([z[2] for z in data]) - 1
    maxz = max([z[2] for z in data]) + 1
    bounds = (minx, maxx, miny, maxy, minz, maxz)
    coolSurface = 0

    water = {(minx, miny, minz)}
    spread = {(minx, miny, minz)}

    while len(spread) > 0:
        oldspread = spread
        spread = set()
        for drop in oldspread:
            adj = getAdjacent(drop, bounds)
            # Check if there is anything in the way
            for x in adj:
                if x not in water:
                    if x in data:
                        # We have a face between edge and water
                        coolSurface += 1
                    else:
                        spread.add(x)
                        water.add(x)

    return coolSurface


# For each cube, store it's edges
def processData():
    outerEdges = set()

    for element in data:
        for edge in getEdges(element):
            if edge not in outerEdges:
                outerEdges.add(edge)
            else:
                outerEdges.remove(edge)

    print(f"Part 1: {len(outerEdges)}")


# Process harder
def processMore():
    print(f"Part 2: {fillWater()}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

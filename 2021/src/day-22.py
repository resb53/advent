#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

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
        box = {}
        (state, instr) = line.strip("\n").split(" ")
        if state == "on":
            state = 1
        else:
            state = 0
        instr = instr.split(",")
        for r in instr:
            (d, vals) = r.split("=")
            vals = vals.split("..")
            box[d] = (int(vals[0]), int(vals[1]))
        data.append([state, box])


# Run through reactor startup instructions
def startReactor():
    cores = set()

    for switch in data[0:20]:
        for z in range(switch[1]["z"][0], switch[1]["z"][1] + 1):
            for y in range(switch[1]["y"][0], switch[1]["y"][1] + 1):
                for x in range(switch[1]["x"][0], switch[1]["x"][1] + 1):
                    if switch[0] == "on":
                        cores.add((x, y, z))
                    else:
                        if (x, y, z) in cores:
                            cores.remove((x, y, z))

    return len(cores)


# New approach for part 2, track blocks and calculate any intersections
def cubeIntersects():
    # Ignore off regions
    cores = Counter()

    for switch in data:
        if switch[0]:
            minx = min(switch[1]["x"])
            maxx = max(switch[1]["x"])
            miny = min(switch[1]["y"])
            maxy = max(switch[1]["y"])
            minz = min(switch[1]["z"])
            maxz = max(switch[1]["z"])
            reg = (minx, maxx, miny, maxy, minz, maxz)
            cores[reg] += 1
        doIntersects(cores, reg)

    return cores


# Prevent double counting of intersects, delete for cubes already considered
def doIntersects(cores, reg):
    newregs = Counter()
    for region in cores:
        xbigmin = max(reg[0], region[0])
        xsmolmax = min(reg[1], region[1])
        ybigmin = max(reg[2], region[2])
        ysmolmax = min(reg[3], region[3])
        zbigmin = max(reg[4], region[4])
        zsmolmax = min(reg[5], region[5])

        if zbigmin <= zsmolmax:
            if ybigmin <= ysmolmax:
                if xbigmin <= xsmolmax:
                    newregs[(xbigmin, xsmolmax, ybigmin, ysmolmax, zbigmin, zsmolmax)] -= 1

    cores.update(newregs)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Solution to part 1: {startReactor()}")

    # Part 2
    print(f"Solution to part 2: {cubeIntersects()}")



if __name__ == "__main__":
    main()

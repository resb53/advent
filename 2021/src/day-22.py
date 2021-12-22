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


# New approach for part 2, track blocks and calculate any intersections
def cubeIntersects(n):
    # Lines to work through:
    if n == "all":
        n = len(data)

    # Ignore off regions
    cores = Counter()

    for switch in data[0:n]:
        doIntersects(cores, switch[1])
        if switch[0]:
            minx = min(switch[1]["x"])
            maxx = max(switch[1]["x"])
            miny = min(switch[1]["y"])
            maxy = max(switch[1]["y"])
            minz = min(switch[1]["z"])
            maxz = max(switch[1]["z"])
            cores[(minx, maxx, miny, maxy, minz, maxz)] += 1
            # print(f"on: {(minx, maxx, miny, maxy, minz, maxz)}")

    counton = 0

    for reg in cores:
        counton += (reg[1] - reg[0] + 1) * (reg[3] - reg[2] + 1) * (reg[5] - reg[4] + 1) * cores[reg]

    return counton


# Prevent double counting of intersects, delete for cubes already considered
def doIntersects(cores, switch):
    newregs = Counter()
    for region in cores:
        xbigmin = max(switch["x"][0], region[0])
        xsmolmax = min(switch["x"][1], region[1])
        ybigmin = max(switch["y"][0], region[2])
        ysmolmax = min(switch["y"][1], region[3])
        zbigmin = max(switch["z"][0], region[4])
        zsmolmax = min(switch["z"][1], region[5])

        if zbigmin <= zsmolmax:
            if ybigmin <= ysmolmax:
                if xbigmin <= xsmolmax:
                    # print(f"forget: {(xbigmin, xsmolmax, ybigmin, ysmolmax, zbigmin, zsmolmax)}")
                    newregs[(xbigmin, xsmolmax, ybigmin, ysmolmax, zbigmin, zsmolmax)] -= cores[region]

    cores.update(newregs)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Solution to part 1: {cubeIntersects(20)}")

    # Part 2
    solution = cubeIntersects("all")
    print(f"Solution to part 2: {solution}")


if __name__ == "__main__":
    main()

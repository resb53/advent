#!/usr/bin/env python3

import argparse
import sys
from itertools import cycle

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

instr = []
network = {}
lr = {
    76: 48,
    82: 49
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    instr.extend([int(x) for x in input_fh.readline().rstrip().translate(lr)])

    for line in input_fh:
        line = line.rstrip()
        if len(line) > 0:
            start, dest = line.split(" = ")
            dest = dest.strip("()")
            dest = dest.split(", ")
            network[start] = dest


# Finf how long it takes to traverse AAA to ZZZ following instructions
def processData():
    src = "AAA"
    steps = 0
    for dirn in cycle(instr):
        if src == "ZZZ":
            return steps
        src = network[src][dirn]
        steps += 1


# Find loops in maze
def getLoops():
    src = [x for x in network.keys() if x[-1] == "A"]
    loops = []
    for node in src:
        visits = set()
        state = []
        for dirn in cycle(enumerate(instr)):
            if (dirn[0], node) in visits:
                offset = state.index((dirn[0], node))
                loops.append([
                    offset,
                    len(visits) - offset,
                    [x - offset for x, n in enumerate(state) if n[1][-1] == "Z"]
                ])
                break
            state.append((dirn[0], node))
            if len(state) == 16344:
                print(state[-1][1])
            visits.add((dirn[0], node))
            node = network[node][dirn[1]]
    return loops


# Move like a ghost: find individual... loops?
def processMore():
    # Offset, Periodicity, Steps to Z within period
    # Testing on the full input there's only one Z for each path!
    # SO, when (offset + c*(periodicity) + stepsToZ) works for int(c) >= 0, we're all at Z
    loops = getLoops()
    steps = 0
    while True:
        steps += 1
        zeds = 0
        for (offset, period, stz) in loops:
            if (steps - offset - stz[-1]) % period == 0:
                zeds += 1
        if zeds == len(loops):
            return steps


def main():
    parseInput(args.input)

    # Part 1
    # print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

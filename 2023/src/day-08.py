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


# Move like a ghost
def processMore():
    src = [x for x in network.keys() if x[-1] == "A"]
    print(len(src))
    steps = 0
    for dirn in cycle(instr):
        if len([x for x in src if x[-1] == "Z"]) == len(src):
            return steps
        for i, x in enumerate(src):
            src[i] = network[x][dirn]
        steps += 1
    return steps


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

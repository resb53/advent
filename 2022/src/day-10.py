#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

instr = []
cycle = [1]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        instr.append(line.strip("\n").split(" "))


# For each pass, identify its seat
def processData():
    for call in instr:
        if call[0] == "noop":
            cycle.append(cycle[-1])
        elif call[0] == "addx":
            cycle.append(cycle[-1])
            cycle.append(cycle[-1] + int(call[1]))

    # During 20th cycle always = end of 19th cycle
    signal = 20 * cycle[19] \
        + 60 * cycle[59] \
        + 100 * cycle[99] \
        + 140 * cycle[139] \
        + 180 * cycle[179] \
        + 220 * cycle[219]

    print(f"Part 1: {signal}")


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

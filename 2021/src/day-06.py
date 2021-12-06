#!/usr/bin/env python3

import argparse
from os import spawnve
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

fish = defaultdict(int)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.strip("\n")
        for f in line.split(","):
            fish[int(f)] += 1


# For each pass, identify its seat
def reproduceFish(period):
    while period > 0:
        diff = min(fish) + 1
        period -= diff

        # Age fish
        for f in sorted(fish.keys()):
            fish[f - diff] = fish.pop(f)

        # Reset 0's and spawn new fish
        spawn = fish.pop(-1)
        fish[6] += spawn
        fish[8] += spawn

    print(f"Solution to part 1: {sum(fish.values())}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    reproduceFish(80)

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

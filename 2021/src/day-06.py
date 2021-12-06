#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = defaultdict(int)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.strip("\n")
        for f in line.split(","):
            data[int(f)] += 1


# For each pass, identify its seat
def reproduceFish(part, period):
    # Prepare fish
    fish = data.copy()
    # Calculate
    diff = min(fish) + 1
    while period - diff >= 0:
        period -= diff

        # Age fish
        for f in sorted(fish.keys()):
            fish[f - diff] = fish.pop(f)

        # Reset 0's and spawn new fish
        spawn = fish.pop(-1)
        fish[6] += spawn
        fish[8] += spawn

        diff = min(fish) + 1

    print(f"Solution to part {part}: {sum(fish.values())}")


def main():
    parseInput(args.input)

    # Part 1
    reproduceFish(1, 80)

    # Part 2
    reproduceFish(2, 256)


if __name__ == "__main__":
    main()

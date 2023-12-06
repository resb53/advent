#!/usr/bin/env python3

import argparse
import sys
from math import prod

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

time = []
dist = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        parts = line.split(":")
        if parts[0] == "Time":
            time.extend([int(x) for x in parts[1].strip().split()])
        else:
            dist.extend([int(x) for x in parts[1].strip().split()])


# For each race, identify range of winning criteria.
def processData():
    waysToWin = []
    # Symmetry 0,7 1,6 2,5 etc. Start in middle for success
    for race in range(len(time)):
        successes = 0
        change = 0
        spread = 0
        mid = time[race] // 2

        if (time[race] - mid) * mid > dist[race]:
            successes += 1

        while successes != change:
            change = successes
            spread += 1

            if (time[race] - (mid+spread)) * (mid+spread) > dist[race]:
                successes += 1

            if (time[race] - (mid-spread)) * (mid-spread) > dist[race]:
                successes += 1

        waysToWin.append(successes)

    return prod(waysToWin)


# Bad Kerning
def processMore():
    ktime = int("".join([str(x) for x in time]))
    kdist = int("".join([str(x) for x in dist]))

    successes = 0
    change = 0
    spread = 0
    mid = ktime // 2

    if (ktime - mid) * mid > kdist:
        successes += 1

    while successes != change:
        change = successes
        spread += 1

        if (ktime - (mid+spread)) * (mid+spread) > kdist:
            successes += 1

        if (ktime - (mid-spread)) * (mid-spread) > kdist:
            successes += 1

    return successes


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

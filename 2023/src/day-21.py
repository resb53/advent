#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

plots = set()
dirs = [1, 1j, -1, -1j]
bounds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    maxx = 0
    start = 0
    for line in input_fh:
        line = line.rstrip()
        if maxx == 0:
            maxx = len(line)
        for x, val in enumerate(line):
            if val == ".":
                plots.add(complex(x, y))
            elif val == "S":
                start = complex(x, y)
                plots.add(complex(x, y))
        y += 1
    bounds.extend([maxx, y])
    return start


# Plots reachable by 64 steps, track odd/even count, but only process leading edge
def processData(start, moves, inf=False):
    pos = set([start])
    prev = set()
    evens = 1
    odds = 0
    for n in range(moves):
        newpos = set()
        rem = set()
        for p in pos:
            for newp in [p + x for x in dirs]:
                check = newp
                if inf:
                    check = complex(int(newp.real) % bounds[0], int(newp.imag) % bounds[1])
                if check in plots:
                    if newp not in prev:
                        prev.add(p)
                        newpos.add(newp)
                    else:
                        rem.add(newp)
        for x in newpos:
            if (n + 1) % 2 == 1:
                odds += 1
            else:
                evens += 1
        pos = newpos
        if len(pos) == 0:
            break
        for x in rem:
            prev.remove(x)

    if moves % 2 == 1:
        return odds
    else:
        return evens


def main():
    start = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(start, 64)}")

    # Part 2
    print(f"Part 2: {processData(start, 5000, inf=True)}")


if __name__ == "__main__":
    main()

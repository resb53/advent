#!/usr/bin/env python3

import argparse
import sys
from collections import deque

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
        data.append(int(line.strip("\n")))


# Mix values in list
def processData():
    size = len(data)
    mixed = deque(data)
    indices = deque(range(size))

    for i in range(size):
        pos = indices.index(i)
        # Rotate to target 0th element
        mixed.rotate(-1 * pos)
        indices.rotate(-1 * pos)
        x = mixed.popleft()
        indices.popleft()
        # Rotate to relevent insert position
        mixed.rotate(-1 * x)
        indices.rotate(-1 * x)
        mixed.appendleft(x)
        indices.appendleft(i)

    zeropos = mixed.index(0)
    print(f"Part 1: {sum([mixed[(n + zeropos) % size] for n in (1000, 2000, 3000)])}")


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

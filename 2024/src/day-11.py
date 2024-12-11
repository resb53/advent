#!/usr/bin/env python3

import argparse
import sys

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
        data.extend([int(x) for x in line.rstrip().split()])


# For each blink, update the stones
def processData(n, stones):
    for i in range(1, n+1):
        stones = blink(stones)
    return len(stones)


# Carry out stone operations for a blink
def blink(stones):
    newstones = []
    for stone in stones:
        if stone == 0:
            newstones.append(1)
        elif len(str(stone)) % 2 == 0:
            hl = len(str(stone)) // 2
            a = int(str(stone)[0:hl])
            b = int(str(stone)[hl:])
            newstones.extend([a, b])
        else:
            newstones.append(stone * 2024)
    return newstones


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(25, data)}")

    # Part 2
    # print(f"Part 2: {processData(75, data)}")


if __name__ == "__main__":
    main()

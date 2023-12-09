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
        data.append([int(x) for x in line.rstrip().split()])


# Get set of gaps between values
def getGaps(seq):
    gaps = set()
    newseq = []
    for x in range(1, len(seq)):
        y = seq[x] - seq[x-1]
        gaps.add(y)
        newseq.append(y)

    return gaps, newseq


# For each sequence, find pattern
def processData():
    for seq in data:
        print(seq)
        depth = 0
        value = 0
        gaps, seq = getGaps(seq)
        while True:
            print(seq)
            depth += 1
            if len(gaps) == 1:
                value = gaps.pop()
                break
            gaps, seq = getGaps(seq)
        print(depth, value)

    return False


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

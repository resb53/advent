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

    ranges = []

    for line in input_fh:
        line = line.rstrip()
        if "-" in line:
            insert = -1
            r = tuple(int(x) for x in line.split("-"))
            for i, x in enumerate(ranges):
                if r[0] > x[0]:
                    continue
                elif r[0] == x[0]:
                    if r[1] > x[1]:
                        continue
                    else:
                        insert = i
                        break
                else:
                    insert = i
                    break
            if insert == -1:
                ranges.append(r)
            else:
                ranges.insert(insert, r)
        elif len(line) > 0:
            data.append(int(line))

    return ranges


# Collapse fresh ranges
def collapseRanges(ranges):
    rng = []
    a, b = ranges[0]

    for r in ranges[1:]:
        if r[0] > b + 1:
            rng.append((a, b))
            a, b = r
        else:
            b = max(b, r[1])

    rng.append((a, b))

    return rng


# Count fresh ingredients
def processData(ranges):
    count = 0
    rng = collapseRanges(ranges)

    for x in data:
        fresh = False
        for r in rng:
            if x >= r[0] and x <= r[1]:
                fresh = True

        if fresh:
            count += 1

    return count


# Process harder
def processMore(ranges):
    return False


def main():
    ranges = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(ranges)}")

    # Part 2
    print(f"Part 2: {processMore(ranges)}")


if __name__ == "__main__":
    main()

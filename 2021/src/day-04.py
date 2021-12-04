#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

rows = defaultdict(list)
cols = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    # Get call list
    call = []
    for i in input_fh.readline().strip("\n").split(','):
        call.append(int(i))

    # Generate rows per board
    count = -1

    for line in input_fh:
        line = line.strip("\n")
        if len(line) == 0:
            count += 1
        else:
            rows[count].append([])
            row = line.split()
            for n in row:
                rows[count][-1].append([int(n), 0])

    # Generate columns per board
    for board in rows:
        for i in range(5):
            cols[board].append([])
            for r in rows[board]:
                cols[board][-1].append([r[i][0], 0])

    return call


# For each pass, identify its seat
def processData(call, criteria):
    latestscore = -1

    for element in call:
        # Mark off elements
        for board in rows:
            for row in rows[board]:
                total = 0
                for item in row:
                    if item[0] == element:
                        item[1] = 1
                    total += item[1]
                if criteria == 'first':
                    if total == 5:
                        return element * sumZeroes(rows[board])
                if criteria == 'last':
                    latestscore = element * sumZeroes(rows[board])

        for board in cols:
            for col in cols[board]:
                total = 0
                for item in col:
                    if item[0] == element:
                        item[1] = 1
                    total += item[1]
                if criteria == 'first':
                    if total == 5:
                        return element * sumZeroes(cols[board])
                if criteria == 'last':
                    latestscore = element * sumZeroes(cols[board])

    return latestscore


# Sum zeroes on board
def sumZeroes(board):
    sum = 0
    for line in board:
        for val in line:
            if val[1] == 0:
                sum += val[0]
    return sum


def main():
    call = parseInput(args.input)

    # Part 1
    print(f"Solution 1: {processData(call, 'first')}")

    # Part 2
    print(f"Solution 2: {processData(call, 'last')}")


if __name__ == "__main__":
    main()

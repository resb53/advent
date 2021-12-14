#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

# Rather than recipe, give new pairings it produces
generate = {}
paircount = Counter()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    pattern = input_fh.readline().strip("\n")
    _ = input_fh.readline()

    for line in input_fh:
        (pair, result) = line.strip("\n").split(" -> ")
        generate[pair] = (pair[0] + result, result + pair[1])

    for i in range(len(pattern) - 1):
        paircount[pattern[i] + pattern[i+1]] += 1


# For each pass, identify its seat
def stepThrough(iters):
    for _ in range(iters):
        initcount = paircount.copy()

        for pair in initcount:
            paircount[pair] -= 1
            for gen in generate[pair]:
                paircount[gen] += initcount[pair]

        # Delete 0's
        delpair = []
        for check in paircount:
            if paircount[check] == 0:
                delpair.append(check)
        for x in delpair:
            paircount.pop(x)


def main():
    parseInput(args.input)

    # Part 1
    stepThrough(10)

    print(paircount)

    freq = paircount.most_common()
    print(f"Solution to part 1: {freq[0][1] - freq[-1][1]}")

    # Part 2
    return


if __name__ == "__main__":
    main()

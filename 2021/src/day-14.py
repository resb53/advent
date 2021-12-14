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

    # Return first character in chain
    return pattern[0]


# For each pass, identify its seat
def stepThrough(iters, paircount, first):
    # This makes a copy due to pass by object reference
    countpairs = paircount

    for _ in range(iters):
        newcount = Counter()

        for pair in countpairs:
            for new_pair in generate[pair]:
                newcount[new_pair] += countpairs[pair]

        countpairs = newcount

    # Count individuals
    indivs = Counter()
    indivs[first] += 1
    for x in countpairs:
        indivs[x[1]] += countpairs[x]

    # print(indivs)
    freq = indivs.most_common()

    return freq[0][1] - freq[-1][1]


def main():
    first = parseInput(args.input)

    # Part 1
    print(f"Solution to part 1: {stepThrough(10, paircount, first)}")

    # Part 2
    print(f"Solution to part 1: {stepThrough(40, paircount, first)}")


if __name__ == "__main__":
    main()

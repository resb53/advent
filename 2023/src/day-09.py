#!/usr/bin/env python3

import argparse
import sys
from sympy import symbols, Poly

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
coef = []


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


# Get polynomial for the sequence -- in the end this was NOT needed, but fun to learn sympy!
# https://stackoverflow.com/questions/56824622/finding-a-polynomial-formula-for-sequence-of-numbers
def lagrange(yseq):
    x = symbols("x")
    zeropoly = Poly(0, x)
    onepoly = Poly(1, x)
    xseq = list(range(1, len(yseq) + 1))

    result = Poly(zeropoly, x)
    for j, (xj, yj) in enumerate(zip(xseq, yseq)):
        # Build the j'th base polynomial
        polyj = onepoly
        for m, xm in enumerate(xseq):
            if m != j:
                polyj *= (x - xm) / (xj - xm)
        # Add in the j'th polynomial
        result += yj * polyj
    return result.all_coeffs()


# For each sequence, find pattern
def processData():
    sumnext = 0
    for n, seq in enumerate(data):
        coeffs = lagrange(seq)
        coef.append(coeffs)
        nextx = len(seq) + 1
        value = 0
        power = 0
        for i in range(len(coeffs)-1, -1, -1):
            value += coeffs[i] * nextx ** power
            power += 1
        print(f"Processed {n+1} / {len(data)}", end="\r")
        sumnext += value
    print()

    return sumnext


# Find for zero'th element
def processMore():
    sumzero = 0
    for coeffs in coef:
        sumzero += coeffs[-1]

    return sumzero


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

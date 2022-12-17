#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []

shapes = [
    [2, 3, 4, 5],  # -
    [3, 2+1j, 2+1j, 4+1j],  # +
    [2, 3, 4, 4+1j, 4+2j],  # ⅃
    [2, 2+1j, 2+2j, 2+3j],  # |
    [2, 3, 2+1j, 2+2j]  # □
]


# Wind generator
def generateWind():
    i = 0
    while True:
        yield data[i % len(data)]
        i += 1


# Shape generator
def generateShape():
    i = 0
    while True:
        yield shapes[i % len(shapes)]
        i += 1


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.extend(list(line.strip("\n")))


# For each pass, identify its seat
def processData():
    wind = generateWind()
    shape = generateShape()
    for _ in range(2):
        print(next(wind))
        print(next(shape))


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

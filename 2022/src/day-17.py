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
    [3, 2+1j, 3+1j, 4+1j, 3+2j],  # +
    [2, 3, 4, 4+1j, 4+2j],  # ⅃
    [2, 2+1j, 2+2j, 2+3j],  # |
    [2, 3, 2+1j, 3+1j]  # □
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


# Drop shape
def dropShape(floor, stack, wind, shape):
    base = max(floor) * 1j + 4j
    falling = [x + base for x in next(shape)]
    leftedge = min([int(x.real) for x in falling])
    rightedge = max([int(x.real) for x in falling])

    while True:
        # Wind blows
        blow = next(wind)
        if blow == "<":
            if leftedge > 0:
                test = [x - 1 for x in falling]
                collision = False
                for block in test:
                    if int(block.imag) in stack[int(block.real)]:
                        collision = True
                if not collision:
                    falling = test
                    leftedge = min([int(x.real) for x in falling])
                    rightedge = max([int(x.real) for x in falling])
        else:
            if rightedge < 6:
                test = [x + 1 for x in falling]
                collision = False
                for block in test:
                    if int(block.imag) in stack[int(block.real)]:
                        collision = True
                if not collision:
                    falling = test
                    leftedge = min([int(x.real) for x in falling])
                    rightedge = max([int(x.real) for x in falling])
        # Block falls
        stops = False
        for x in falling:
            if int(x.imag) - 1 in stack[int(x.real)]:
                stops = True
        if stops:
            break
        else:
            falling = [x - 1j for x in falling]
        for x in falling:
            if int(x.imag) < 0:
                sys.exit("Fallen through the floor.")

    # Update floor
    for x in range(len(floor)):
        newy = floor[x]
        for y in falling:
            if int(y.real) == x and int(y.imag) > newy:
                newy = int(y.imag)
        floor[x] = newy

    # Update stack
    for x, s in enumerate(stack):
        for y in falling:
            if int(y.real) == x:
                s.add(int(y.imag))


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
    floor = [0] * 7
    stack = [{0}, {0}, {0}, {0}, {0}, {0}, {0}]
    wind = generateWind()
    shape = generateShape()

    for count in range(2022):
        dropShape(floor, stack, wind, shape)

    print(max(floor))


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

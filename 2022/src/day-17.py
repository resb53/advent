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

state = []


# Wind generator
def generateWind():
    i = 0
    while True:
        yield (data[i % len(data)], i % len(data))
        i += 1


# Shape generator
def generateShape():
    i = 0
    while True:
        yield (shapes[i % len(shapes)], i % len(shapes))
        i += 1


# Check system state: LOOP: 100 - 1850
# Maths:
# Height after count 100 shapes: 152
# (Gap 2796)
# Height after count 1850 shapes: 2948
# (Gap 2796)
# Heigh after count 3600 shapes: 5744

# 1000000000000 - (100 + 571428571 * 1750) = 650
# => Height = 152 + 571428571 * 2796 + [count 750 - 152 = 1030] = 1597714285698

# 2500 - (100 + 1 * 1750) = 650
# => Height = 152 + 1 * 2796 + 1030 = 3978
# 4250 - (100 + 2 * 1750) = 650
# => Height = 152 + 2 * 2796 + 1030 = 6774
# 6000 - (100 + 3 * 1750) = 650
# => Height = 152 + 3 * 2796 + 1030 = 9570

def checkState(floor, shape, wind):
    minHeight = min(floor)
    normaliseFloor = [x - minHeight for x in floor]
    stuple = (shape, wind, normaliseFloor)
    if stuple not in state:
        state.append(stuple)
    else:
        old = state.index(stuple)
        print(f"LOOP: {old} - {len(state)}")
        state.append(stuple)


# Drop shape
def dropShape(floor, stack, wind, shape):
    base = max(floor) * 1j + 4j
    (nextshape, shapestate) = next(shape)
    (nextblow, windstate) = next(wind)
    # checkState(floor, shapestate, windstate)
    falling = [x + base for x in nextshape]
    leftedge = min([int(x.real) for x in falling])
    rightedge = max([int(x.real) for x in falling])

    while True:
        # Wind blows
        if nextblow is not None:
            blow = nextblow
            nextblow = None
        else:
            (blow, _) = next(wind)
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

    for count in range(750):
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

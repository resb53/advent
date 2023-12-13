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

    shape = set()
    y = 0
    for line in input_fh:
        line = line.rstrip()
        if line == "":
            data.append(shape)
            shape = set()
            y = 0
        else:
            for x, val in enumerate(line):
                if val == "#":
                    shape.add(complex(x, y))
            y += 1
    data.append(shape)


# See if this is a true reflection
def isReflection(shape, r, bounds):
    # Columns
    if r.imag == 0:
        for z in shape:
            check = complex(2*r - z.real - 1, z.imag)
            # If in bounds
            if check.real >= 0 and check.real <= bounds[0] and check.imag >= 0 and check.imag <= bounds[1]:
                if check not in shape:
                    return False

        return True

    # Rows
    else:
        for z in shape:
            check = complex(z.real, 2*r.imag - z.imag - 1)
            # If in bounds
            if check.real >= 0 and check.real <= bounds[0] and check.imag >= 0 and check.imag <= bounds[1]:
                if check not in shape:
                    return False
        return True


# Find the best true reflection of the shape
def reflectLine(shape, bounds, veto=None):
    # Columns
    for x in range(1, bounds[0] + 1):
        if veto is not None:
            if x != veto:
                if isReflection(shape, x, bounds):
                    return x
        else:
            if isReflection(shape, x, bounds):
                return x

    # Rows
    for y in [complex(0, z) for z in range(1, bounds[1] + 1)]:
        if veto is not None:
            if y != veto:
                if isReflection(shape, y, bounds):
                    return y
        else:
            if isReflection(shape, y, bounds):
                return y

    return False


# For each shape, find its reflection line (1 = between 0 and 1, etc.)
def processData():
    score = 0
    for shape in data:
        bounds = (int(max([z.real for z in shape])), int(max([z.imag for z in shape])))
        rp = reflectLine(shape, bounds)
        if rp.imag == 0:
            score += rp.real
        else:
            score += 100 * rp.imag

    return int(score)


def reflectSmudge(shape, bounds):
    old = reflectLine(shape, bounds)

    for y in range(bounds[1] + 1):
        for x in range(bounds[0] + 1):
            tempShape = set([x for x in shape])

            if complex(x, y) in tempShape:
                tempShape.remove(complex(x, y))
            else:
                tempShape.add(complex(x, y))

            rp = reflectLine(tempShape, bounds, veto=old)
            if rp is not False:
                return rp


# Find a (new?) reflection with a single smudge
def processMore():
    score = 0
    for shape in data:
        bounds = (int(max([z.real for z in shape])), int(max([z.imag for z in shape])))
        rp = reflectSmudge(shape, bounds)
        if rp.imag == 0:
            score += rp.real
        else:
            score += 100 * rp.imag

    return int(score)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

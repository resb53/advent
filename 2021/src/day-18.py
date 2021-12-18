#!/usr/bin/env python3

import argparse
import sys
import json

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
        data.append(json.loads(line.strip("\n")))


# Work through snail numbers and add them together
def doSums():
    result = data[0]
    for snumber in data[1:]:
        result = sadd(result, snumber)

    return result


# Add snail numbers
def sadd(left, right):
    return reduce([left, right])


# Reduce snail number
def reduce(snumber):
    depthlist = calcdepths(snumber, 0)
    reduced = False

    while not reduced:
        # Check for explodes
        needexplode = False
        needsplit = False
        oni = None

        for i, depthpair in enumerate(depthlist):
            if depthpair[0] >= 4:
                needexplode = True
                oni = i
                break
        if needexplode:
            depthlist = explode(depthlist, oni)
            continue

        for i, depthpair in enumerate(depthlist):
            if depthpair[1] >= 10:
                needsplit = True
                oni = i
                break
        if needsplit:
            depthlist = split(depthlist, oni)
            continue

        reduced = True

    # Rebuild for depthlist
    return rebuild(depthlist)


def calcdepths(snumber, depth):
    (left, right) = snumber

    if isinstance(left, int):
        left = [(depth, left)]
    else:
        left = calcdepths(left, depth + 1)

    if isinstance(right, int):
        right = [(depth, right)]
    else:
        right = calcdepths(right, depth + 1)

    return (left + right)


# Explode element boom of depthlist
def explode(depthlist, boom):
    if boom > 0:
        depthlist[boom - 1] = (depthlist[boom - 1][0], depthlist[boom - 1][1] + depthlist[boom][1])
    if boom < len(depthlist) - 2:
        depthlist[boom + 2] = (depthlist[boom + 2][0], depthlist[boom + 1][1] + depthlist[boom + 2][1])
    depthlist[boom] = (depthlist[boom][0] - 1, 0)
    depthlist.pop(boom + 1)
    return depthlist


def split(depthlist, spli):
    depth = depthlist[spli][0] + 1
    left = depthlist[spli][1] // 2
    right = depthlist[spli][1] - left
    depthlist[spli] = (depth, left)
    depthlist.insert(spli + 1, (depth, right))
    return depthlist


def rebuild(depthlist):
    while len(depthlist) > 1:
        for i in range(len(depthlist) - 1):
            if depthlist[i][0] == depthlist[i + 1][0]:
                stackeddepth = [(depthlist[i][0] - 1, [depthlist[i][1], depthlist[i + 1][1]])]
                depthlist = (depthlist[:i] + stackeddepth + depthlist[(i + 2):])
                break

    return depthlist[0][1]


def magnitude(snumber):
    (left, right) = snumber

    if isinstance(left, int):
        left *= 3
    else:
        left = magnitude(left) * 3

    if isinstance(right, int):
        right *= 2
    else:
        right = magnitude(right) * 2

    return left + right


def main():
    parseInput(args.input)

    # Part 1
    answer = doSums()
    print(f"Solution to part 1: {magnitude(answer)}")


if __name__ == "__main__":
    main()

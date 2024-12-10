#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
files = []  # (start, length) - id is pos in array
space = []  # (startpos, length)

# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        digits = [int(x) for x in line.rstrip()]
        free = False
        id = 0
        pos = 0
        for x in digits:
            if not free:
                data.extend([id] * x)
                files.append((pos, x))
                pos += x
                free = not free
                id += 1
            else:
                data.extend(["."] * x)
                space.append((pos, x))
                pos += x
                free = not free


# Move blocks to leftmost free space, and calculate resulting checksum
def processData():
    lastblock, firstspace = updateStatus()
    while lastblock > firstspace:
        data[firstspace] = data[lastblock]
        data[lastblock] = "."
        lastblock, firstspace = updateStatus()
    return checksum(data)


# Update current status
def updateStatus():
    for i in range(len(data)-1, -1, -1):
        if data[i] != ".":
            lastblock = i
            break
    firstspace = data.index(".")

    return lastblock, firstspace


# Get checksum of filesystem
def checksum(fs):
    total = 0
    for i, x in enumerate(fs):
        if x != ".":
            total += i * x
    return total


# Move full files, not just blocks
def processMore():
    for id in range(len(files)-1, -1, -1):
        start, size = files[id]
        # Find left-most space which could contain file
        for i, x in enumerate(space):
            if x[1] >= size and x[0] < start:
                # Move file into space
                if x[1] > size:
                    space[i] = (x[0] + size, x[1] - size)
                else:
                    space.remove(x)
                files[id] = (x[0], size)
                # Add space back in!
                space.append((start, size))
                cleanup(space)
                break
    return blockcheck(files)


# Cleanup available space records
def cleanup(records):
    # Arrange
    records.sort(key=lambda x: x[0])
    # Amalgamate
    for i in range(len(records)-2, -1, -1):
        left = records[i]
        right = records[i+1]
        if left[0] + left[1] == right[0]:
            update = (left[0], left[1] + right[1])
            records.pop(i + 1)
            records[i] = update


# Calculate checksum of blocked files
def blockcheck(fs):
    total = 0
    for id, file in enumerate(fs):
        loc, size = file
        for x in range(size):
            total += loc * id
            loc += 1
    return total


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

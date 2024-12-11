#!/usr/bin/env python3

# Before improvements to part 1:
# Part 1: Time taken: 27.102 seconds
# Part 2: Time taken: 4.523 seconds

# After improvements to part 1:
# Part 1: Time taken: 0.013 seconds
# Part 2: Time taken: 4.065 seconds

import argparse
import sys
import time

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
files = []  # (start, length) - id is pos in array
space = []  # (startpos, length)


# Time functions in script
def perf(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, *kwargs)
        end = time.perf_counter()
        print(f"Time taken: {end - start:.3f} seconds")
        return result
    return wrapper


# Parse the input file
@perf
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        free = False
        pos = 0
        for x in [int(x) for x in line.rstrip()]:
            if not free:
                files.append((pos, x))
            else:
                space.append((pos, x))
            pos += x
            free = not free


# Move blocks to leftmost free space, and calculate resulting checksum
@perf
def processData():
    shrink = []  # (id, length)
    fillers = files.copy()
    pos = 0
    i = 0
    blocks = sum([x[1] for x in files])
    while pos < blocks:
        gap = files[i][0] - pos
        if gap == 0:
            shrink.append((i, fillers[i][1]))
            pos += fillers[i][1]
            i += 1
        else:
            shrink.extend(fillgap(gap, fillers))
            pos += gap
    return checksum(shrink)


# Calculate blocks to fill the gap
def fillgap(size, fillers):
    newblocks = []
    i = len(fillers) - 1
    while size > 0:
        if fillers[i][1] <= size:
            newblocks.append((i, fillers[i][1]))
            size -= fillers[i][1]
            fillers.pop(i)
            i -= 1
        else:
            fillers[i] = (fillers[i][0], fillers[i][1] - size)
            newblocks.append((i, size))
            size = 0
    return newblocks


# Calculate checksm for compressed filesystem
def checksum(fs):
    total = 0
    loc = 0
    for x in fs:
        for _ in range(x[1]):
            total += loc * x[0]
            loc += 1
    return total


# Move full files, not just blocks
@perf
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
        for _ in range(size):
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

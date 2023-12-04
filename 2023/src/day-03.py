#!/usr/bin/env python3

import argparse
import sys
import re

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
        data.append(line.strip("\n"))


# Find the missing part
def processData():
    total = 0

    for y, line in enumerate(data):
        values = re.finditer(r'\d+', line)

        for value in values:
            minx = value.start() - 1
            if minx < 0:
                minx = 0
            maxx = value.end()
            if maxx >= len(line):
                maxx = len(line) - 1
            miny = y - 1
            if miny < 0:
                miny = 0
            maxy = y + 1
            if maxy >= len(data):
                maxy = y

            # Look for symbols
            borders = data[miny][minx:maxx+1] + line[minx] + line[maxx] + data[maxy][minx:maxx+1]
            if re.search(r'[^\d\.]', borders):
                total += int(value.group(0))

    return total


# Calculate the gear ratios
def processMore():
    total = 0

    # Find the gears
    for y, line in enumerate(data):
        values = re.finditer(r'\*', line)

        # No stars at edge of data, limits ok
        for value in values:
            minx = value.start() - 1
            maxx = value.end()
            miny = y - 1
            maxy = y + 1

            # Look for numbers tested data: no more than 2 by a star
            borders = [data[miny][minx:maxx+1], line[minx], line[maxx], data[maxy][minx:maxx+1]]
            count = 0
            nums = []
            if m := re.search(r'(\d)\D(\d)', borders[0]):
                count += 2
            elif m := re.search(r'(\d+)', borders[0]):
                count += 1
            if m := re.search(r'(\d)', borders[1]):
                count += 1
            if m := re.search(r'(\d)', borders[2]):
                count += 1
            if m := re.search(r'(\d)\D(\d)', borders[3]):
                count += 2
                nums.extend([m.group(1), m.group(2)])
            elif m := re.search(r'(\d)', borders[3]):
                count += 1
            print(nums)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

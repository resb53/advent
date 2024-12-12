#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
maxv = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        for x, val in enumerate(line.rstrip()):
            grid[x + 1j * y] = val
        y += 1
    maxv.extend([x + 1, y])


# Print the grid
def printGrid():
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            print(grid[x + 1j * y], end="")
        print()


# Calculate the cost of fencing each region
def processData():
    regions = separateRegions()
    total = 0
    # Calculate cost of fencing all regions
    for region in regions:
        total += region["perimeter"] * len(region["region"])
    return total


# Split up the distinct region in the grid
def separateRegions():
    regions = []  # List of dicts with perimeters and sets, each containing the grid locations for that region
    field = [x for x in grid.items()]
    while len(field) > 0:
        loc, target = field[0]
        region = {"perimeter": 0, "region": set()}
        expandRegion(region, loc, target)
        regions.append(region)
        for x in region["region"]:
            field.remove((x, target))
    return regions


# Expand current region from starting seed
def expandRegion(region, pos, type):
    if pos in region["region"]:
        return region
    region["region"].add(pos)
    for neighbour in [1, 1j, -1, -1j]:
        if pos + neighbour in grid and grid[pos + neighbour] == type:
            expandRegion(region, pos + neighbour, type)
        else:
            region["perimeter"] += 1
    return region


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

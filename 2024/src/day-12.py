#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

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
    # Calculate cost of fencing in all regions
    p1 = 0
    for region in regions:
        p1 += len(region["fencing"]) * len(region["region"])
    # Calculate cost of fencing in all regions with discounts applied
    p2 = 0
    for region in regions:
        p2 += calculateSides(region["fencing"]) * len(region["region"])
    return p1, p2


# Split up the distinct region in the grid
def separateRegions():
    regions = []  # List of dicts with perimeters and sets, each containing the grid locations for that region
    field = [x for x in grid.items()]
    while len(field) > 0:
        loc, target = field[0]
        region = {"fencing": set(), "region": set()}
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
            # Position fencing between tiles, but nearer to the inside of the field
            region["fencing"].add(pos + (neighbour / 4))
    return region


# Calculate how many sides of fencing are in a region
def calculateSides(fencing):
    sides = defaultdict(list)
    count = 0
    for pos in fencing:
        x = pos.real
        y = pos.imag
        if x == int(x):
            sides[y * 1j].append(int(x))
        else:
            sides[x].append(int(y))
    for row in sides:
        sides[row].sort()
        last = -2
        for pos in sides[row]:
            if pos != last + 1:
                count += 1
            last = pos
    return count


def main():
    parseInput(args.input)
    p1, p2 = processData()

    # Part 1
    print(f"Part 1: {p1}")

    # Part 2
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()

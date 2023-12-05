#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
seeds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        if len(line) > 0:
            parts = line.split(":")

            if len(parts) > 1:
                if len(parts[1]) != 0:
                    # Get the seeds, not the leading space
                    seeds.extend([int(x) for x in parts[1].split(" ")[1:]])
                else:
                    data.append([])

            else:
                data[-1].append([int(x) for x in line.split(" ")])


# Find corresponding next value
def corresponds(id, level):
    # print(f"Mapping {id} at level {level}...")
    for mapping in data[level]:
        dest, src, rng = mapping

        if id >= src and id < src+rng:
            id = id - src + dest
            break

    if (level+1) >= len(data):
        return id
    else:
        return corresponds(id, level+1)


# Find lowest location number for any seed
def processData():
    locations = []
    for seed in seeds:
        locations.append(corresponds(seed, 0))
    return min(locations)


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

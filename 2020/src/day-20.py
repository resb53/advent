#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Images.")
parser.add_argument('input', metavar='input', type=str,
                    help='Image list input.')
args = parser.parse_args()

tiles = {}
edges = {}

def main():
    parseInput(args.input)

    # Part 1
    findEdges()

    # Part 2

    # Debug
    printTiles()


# Parse the input file
def parseInput(inp):
    global tiles
    try:
        tiles_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    key = 0
    row = 0

    for line in tiles_fh:
        line = line.strip("\n")

        if len(line) > 0:
            if line[0] == 'T':
                key = int(line.split(" ")[1][0:-1])
                tiles[key] = {}
                row = -1
            else:
                for col, val in enumerate(line):
                    if val == '.':
                        tiles[key][row + col * 1j] = 0
                    else:
                        tiles[key][row + col * 1j] = 1
            row += 1


# For each pass, identify its seat
def findEdges():
    return True


def printTiles():
    for key in tiles:
        print(tiles[key])


if __name__ == "__main__":
    main()

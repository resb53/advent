#!/usr/bin/python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Tiles.")
parser.add_argument('input', metavar='input', type=str,
                    help='Tile list input.')
args = parser.parse_args()

tiles = defaultdict(bool)
instr = []
adjust = {
    "nw": -1 - 0.5j,
    "ne": -1 + 0.5j,
    "w": -1j,
    "e": 1j,
    "sw": 1 - 0.5j,
    "se": 1 + 0.5j
}


def main():
    parseInput(args.input)

    # Part 1
    flipTiles(instr)

    black = 0
    for tile in tiles:
        if tiles[tile]:
            black += 1

    print(black)

    # Part 2

    # Debug
    # printTiles()


# Parse the input file
def parseInput(inp):
    global instr
    try:
        tiles_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in tiles_fh:
        instr.append(line.strip("\n"))


# For each instruction, flip target tile
def flipTiles(flips):
    global tiles
    for move in flips:
        tar = complex()
        drn = ''

        for char in move:
            drn += char
            if char == 'e' or char == 'w':
                tar += adjust[drn]
                drn = ''

        tiles[tar] = not tiles[tar]


def printTiles():
    print(tiles)


if __name__ == "__main__":
    main()

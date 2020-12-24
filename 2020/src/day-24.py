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
    printBlack()

    # Part 2
    livingArt(100)
    printBlack()

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


def livingArt(count):
    global tiles

    # Actual day == day + 1
    for day in range(count):
        toflip = set()

        # State only changes if next to a black tile.
        blacktiles = [i for i in tiles if tiles[i]]

        for tile in blacktiles:
            # If black
            if tiles[tile]:
                # Check adjacents
                adj = 0
                for check in adjust.values():
                    if tiles[tile + check]:
                        adj += 1
                    else:
                        # If neighbour white, check its neighbours
                        blk = 0
                        for dblcheck in adjust.values():
                            if tiles[tile + check + dblcheck]:
                                blk += 1
                        # Flip if exactly 2
                        if blk == 2:
                            toflip.add(tile + check)
                # Flip if 0 or more than 2
                if adj == 0 or adj > 2:
                    toflip.add(tile)

        # Flip tiles
        for tile in toflip:
            tiles[tile] = not tiles[tile]


def printBlack():
    black = 0
    for tile in tiles:
        if tiles[tile]:
            black += 1

    print(black)


def printTiles():
    print(tiles)


if __name__ == "__main__":
    main()

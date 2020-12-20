#!/usr/bin/python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Images.")
parser.add_argument('input', metavar='input', type=str,
                    help='Image list input.')
args = parser.parse_args()

tiles = {}
edges = defaultdict(list)

top = [0, 0+1j, 0+2j, 0+3j, 0+4j, 0+5j, 0+6j, 0+7j, 0+8j, 0+9j]
right = [0+9j, 1+9j, 2+9j, 3+9j, 4+9j, 5+9j, 6+9j, 7+9j, 8+9j, 9+9j]
bottom = [9, 9+1j, 9+2j, 9+3j, 9+4j, 9+5j, 9+6j, 9+7j, 9+8j, 9+9j]
left = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def main():
    parseInput(args.input)

    # Part 1
    findEdges()

    # Any unique edges?
    uniq = defaultdict(int)

    for key in edges:
        if len(edges[key]) == 1:
            uniq[edges[key][0]] += 1

    # for sortkey in sorted(uniq, key=uniq.get, reverse=True):
    #    print(f"{sortkey}: {uniq[sortkey]}")

    answer = 1
    for corner in uniq:
        if uniq[corner] == 4:
            answer *= corner

    print(answer)

    # Part 2

    # Debug
    # printTiles()


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


# Calculate edge possibilities for tiles
def findEdges():
    global edges

    for key in tiles:
        values = [
            int("".join(str(tiles[key][i]) for i in top), 2),
            int("".join(str(tiles[key][i]) for i in reversed(top)), 2),
            int("".join(str(tiles[key][i]) for i in right), 2),
            int("".join(str(tiles[key][i]) for i in reversed(right)), 2),
            int("".join(str(tiles[key][i]) for i in bottom), 2),
            int("".join(str(tiles[key][i]) for i in reversed(bottom)), 2),
            int("".join(str(tiles[key][i]) for i in left), 2),
            int("".join(str(tiles[key][i]) for i in reversed(left)), 2)
        ]

        for val in values:
            edges[val].append(key)


def printTiles():
    for key in tiles:
        print(tiles[key])


if __name__ == "__main__":
    main()

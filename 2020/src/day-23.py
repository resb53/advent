#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Cups.")
parser.add_argument('input', metavar='input', type=str,
                    help='Crab Cup list input.')
args = parser.parse_args()

cups = []
current = 0


def main():
    parseInput(args.input)

    # Part 1
    for turn in range(100):
        # print("".join([str(i) for i in cups]))
        moveCups()

    print("".join([str(i) for i in cups]))
        
    # Part 2
    parseInput(args.input)
    embiggenCups(1000000)

    for turn in range(100):
        moveCups()

    one = cups.index(1)
    print((cups[one + 1], cups[one + 2]))

    # Debug
    # printCups()


# Parse the input file
def parseInput(inp):
    global cups, current
    try:
        cups_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = cups_fh.readline().strip("\n")
    cups = [int(i) for i in line]
    current = cups[0]


# For each pass, identify its seat
def moveCups():
    global cups, current

    curpos = cups.index(current)

    pickup = [
        (curpos + 1) % 9,
        (curpos + 2) % 9,
        (curpos + 3) % 9,
    ]

    heldcups = [cups[i] for i in pickup]
    # print(heldcups)

    dest = (current - 1) % 9
    if dest == 0:
        dest = 9

    while dest in heldcups:
        dest = (dest - 1) % 9
        if dest == 0:
            dest = 9

    # print(dest)

    for i in heldcups:
        cups.remove(i)

    destind = cups.index(dest)

    for i, v in enumerate(heldcups, start=1):
        cups.insert(destind + i, v)

    curpos = cups.index(current)
    nextpos = (curpos + 1) % 9
    current = cups[nextpos]


def embiggenCups(size):
    global cups

    biggest = max(cups)

    while biggest < size:
        biggest += 1
        cups.append(biggest)

    print(len(cups))


def printCups():
    print(cups)


if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import sys
from itertools import cycle

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Cups.")
parser.add_argument('input', metavar='input', type=str,
                    help='Crab Cup list input.')
args = parser.parse_args()

cups = []
current = 0
cupdict = {}
cupcount = 0


def main():
    global current, cupcount
    
    parseInput(args.input)

    # Part 1
    for turn in range(100):
        # print("".join([str(i) for i in cups]))
        moveCups()

    print("".join([str(i) for i in cups]))

    # Part 2
    parseInput(args.input)
    embiggenCups(1000000)
    cupcount = len(cups)
    prepCupDict()
    current = cups[0]
    for turn in range(10000000):
        moveCupDict()

    print(cupdict[1] * cupdict[cupdict[1]])

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


def prepCupDict():
    circle = cycle(cups)
    nextcup = next(circle)

    for _ in range(len(cups)):
        thiscup, nextcup = nextcup, next(circle)
        cupdict[thiscup] = nextcup


def moveCupDict():
    global current

    one = cupdict[current]
    two = cupdict[one]
    three = cupdict[two]
    four = cupdict[three]

    dest = (current - 1) % cupcount
    if dest == 0:
        dest = cupcount

    while dest in (one, two, three):
        dest = dest - 1 % cupcount
        if dest == 0:
            dest = cupcount

    newend = cupdict[dest]
    cupdict[dest] = one
    cupdict[three] = newend

    cupdict[current] = four
    current = four


def printCups():
    print(cups)


if __name__ == "__main__":
    main()

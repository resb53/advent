#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Memory.")
parser.add_argument('input', metavar='input', type=str,
                    help='Numbers game input.')
args = parser.parse_args()

turns = []  # Reverse turn order so to use list.index()
lastseen = {}  # memory conservation for part 2!
lastval = 0


def main():
    parseInput(args.input)

    # Part 1
    takeTurns(2020)
    print(turns[0])

    # Part 2
    print(findTurn(30000000))

    # Debug
    #printTurns()


# Parse the input file
def parseInput(inp):
    global turns, lastseen, curval, curturn
    try:
        nums_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = nums_fh.readline()
    seen = [int(i) for i in line.strip("\n").split(',')]
    turns = list(reversed(seen))

    i = 1
    for val in seen[:-1]:
        lastseen[val] = i
        i += 1
    curval = seen[-1]
    curturn = i


# For each pass, identify its seat
def takeTurns(limit):
    global turns

    while len(turns) < limit:
        try:
            val = turns.index(turns[0], 1)
        except ValueError:
            val = 0
        turns.insert(0, val)


def findTurn(target):
    global lastseen, curval, curturn

    while curturn < target:
        # print(f"Current turn: {curturn}, Value spoken: {curval}")

        if curval not in lastseen:
            lastseen[curval] = curturn
            curval = 0
        else:
            nextval = curturn - lastseen[curval]
            lastseen[curval] = curturn
            curval = nextval
        curturn += 1
        # print(lastseen)

    return curval


def printTurns():
    last = len(turns)  # Start at 1
    for turn, num in enumerate(turns):
        print(f", {last-turn}: {num}", end="")
    print("")


if __name__ == "__main__":
    main()

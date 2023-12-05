#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

cards = []
winners = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line.rstrip()
        data = line.split(": ")[1]
        winner, card = data.split(" | ")
        cards.append([int(x) for x in card.split()])
        winners.append([int(x) for x in winner.split()])


# For each pass, identify its seat
def processData():
    score = 0

    for id in range(len(cards)):
        count = 0

        for x in cards[id]:
            if x in winners[id]:
                count += 1

        if count > 0:
            score += 2 ** (count-1)

    return score


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

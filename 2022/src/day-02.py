#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
# A = Rock, B = Paper, C = Scissors
# X = Rock, Y = Paper, Z = Scissors
rock = 1
paper = 2
scissors = 3
lose = 0
draw = 3
win = 6

score = {
    "A": {
        "X": draw + rock,
        "Y": win + paper,
        "Z": lose + scissors,
    },
    "B": {
        "X": lose + rock,
        "Y": draw + paper,
        "Z": win + scissors
    },
    "C": {
        "X": win + rock,
        "Y": lose + paper,
        "Z": draw + scissors
    }
}

newscore = {
    "A": {
        "X": lose + scissors,
        "Y": draw + rock,
        "Z": win + paper
    },
    "B": {
        "X": lose + rock,
        "Y": draw + paper,
        "Z": win + scissors
    },
    "C": {
        "X": lose + paper,
        "Y": draw + scissors,
        "Z": win + rock
    }
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n").split(" "))


# For each pass, identify its seat
def processData():
    totalScore = 0

    for choices in data:
        totalScore += score[choices[0]][choices[1]]

    print(f"Part 1: {totalScore}")


# Process harder
def processMore():
    totalScore = 0

    for choices in data:
        totalScore += newscore[choices[0]][choices[1]]

    print(f"Part 2: {totalScore}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()

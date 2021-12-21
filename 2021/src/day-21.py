#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

# startingpos = [1, 10]
startingpos = [4, 8]


class DetDice:
    state = 0

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        rolled = self.state + 1
        self.state = rolled % self.sides
        return rolled


# For each pass, identify its seat
def playGame():
    dice = DetDice(6)

    for _ in range(8):
        print(dice.roll())


def main():
    # Part 1
    playGame()


if __name__ == "__main__":
    main()

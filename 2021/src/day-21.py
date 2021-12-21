#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

startingpos = [1, 10]
# startingpos = [4, 8]


class DetDice:
    state = 0

    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        rolled = self.state + 1
        self.state = rolled % self.sides
        return rolled


class Player:
    score = 0
    position = 0

    def __init__(self, start):
        self.position = start

    def move(self, newpos):
        self.position = newpos
        self.score += newpos
        return self.score

    def getpos(self):
        return self.position

    def getscore(self):
        return self.score


# For each pass, identify its seat
def playGame(start):
    # Init game
    dice = DetDice(100)
    players = []
    board = 10
    rolls = 0
    scores = [0, 0]
    turn = 0

    for pos in start:
        players.append(Player(pos))

    while max(scores) < 1000:
        pos = players[turn].getpos()
        rolls += 3
        roll = dice.roll() + dice.roll() + dice.roll()
        newpos = (((pos - 1) + roll) % board) + 1
        scores[turn] = players[turn].move(newpos)
        turn = (turn + 1) % len(players)

    return(rolls, scores)


def main():
    # Part 1
    (rolls, scores) = playGame(startingpos)

    print(f"Solution to part 1: {rolls * min(scores)}")


if __name__ == "__main__":
    main()

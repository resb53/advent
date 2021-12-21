#!/usr/bin/env python3

import argparse
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


# Play with deterministic dice
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

    return (rolls, scores)


# Play with Dirac dice

# For each player, and each board position, and each scorepair?
# Track how many universes they're in that state

def playDirac(start):
    # Init game
    board = 10
    turn = 0
    # (pos1, sco1, pos2, sco2)
    states = Counter()
    wins = Counter()

    states[(start[0], 0, start[1], 0)] += 1

    while sum(states.values()) > 0:
        newState = Counter()

        for state in states:
            changers = states[state]
            for outcome, n in rollDirac():
                if turn == 0:
                    newpos = (((state[0] - 1) + outcome) % board) + 1
                    newscore = state[1] + newpos
                    newtuple = (newpos, newscore, state[2], state[3])
                    newState[newtuple] += changers * n
                else:
                    newpos = (((state[2] - 1) + outcome) % board) + 1
                    newscore = state[3] + newpos
                    newtuple = (state[0], state[1], newpos, newscore)
                    newState[newtuple] += changers * n

        turn = (turn + 1) % 2
        states = newState

        # Remove and record wins
        for state in states:
            if state[1] >= 21:
                wins[1] += states[state]
                states[state] = 0
            if state[3] >= 21:
                wins[2] += states[state]
                states[state] = 0

    return wins


def rollDirac():
    # Each round, roll dice 3 times => 27 outcomes:
    # 1,1,1 1,1,2 1,1,3 1,2,1 1,2,2 1,2,3 1,3,1 1,3,2 1,3,3
    # 2,1,1 2,1,2 2,1,3 2,2,1 2,2,2 2,2,3 2,3,1 2,3,2 2,3,3
    # 3,1,1 3,1,2 3,1,3 3,2,1 3,2,2 3,2,3 3,3,1 3,3,2 3,3,3
    # Moves in each universe
    # 3 4 5 4 5 6 5 6 7
    # 4 5 6 5 6 7 6 7 8
    # 5 6 7 6 7 8 7 8 9
    outcomes = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1
    }

    return list(outcomes.items())


def main():
    # Part 1
    (rolls, scores) = playGame(startingpos)

    print(f"Solution to part 1: {rolls * min(scores)}")

    # Part 2
    mostwins = max(playDirac(startingpos).values())
    print(f"Solution to part 2: {mostwins}")


if __name__ == "__main__":
    main()

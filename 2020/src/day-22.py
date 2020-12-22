#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Cards.")
parser.add_argument('input', metavar='input', type=str,
                    help='Card list input.')
args = parser.parse_args()

cards = []


def main():
    parseInput(args.input)

    # Part 1
    playCombat()
    printScore()

    # Part 2

    # Debug
    # printCards()


# Parse the input file
def parseInput(inp):
    global cards
    try:
        cards_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    hand = []

    for line in cards_fh:
        line = line.strip("\n")

        if line != "":
            if line[0] == "P":
                cards.append(hand)
                hand = []
            else:
                hand.append(int(line))

    cards.append(hand)
    cards.pop(0)


# Play the game Combat
def playCombat():
    global cards

    while len(cards[0]) > 0 and len(cards[0]) > 0:
        p1card = cards[0].pop(0)
        p2card = cards[1].pop(0)

        if p1card > p2card:
            cards[0].extend([p1card, p2card])
        else:
            cards[1].extend([p2card, p1card])


def printScore():
    for i, hand in enumerate(cards):
        if len(hand) > 0:
            points = zip(hand, range(len(hand), 0, -1))
            score = 0

            for p in points:
                score += p[0] * p[1]

            print(f"Player {i} wins, with a score of {score}!")


def printCards():
    for i, hand in enumerate(cards):
        print(f"Player {i}:")
        print(hand)


if __name__ == "__main__":
    main()

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
    global cards
    parseInput(args.input)

    # Part 1
    playCombat()
    printScore()

    # Part 2
    cards = []
    parseInput(args.input)

    playRecursiveCombat(cards)
    printScore()

    # Debug
    # printCards(cards)


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


# Returns winner of the game
def playRecursiveCombat(hands) -> int:
    cache = set()

    while len(hands[0]) > 0 and len(hands[0]) > 0:
        state = updateCache(cache)
        if state in cache:
            return 0
        else:
            cache.add(updateCache(cache))

            p1card = hands[0].pop(0)
            p2card = hands[1].pop(0)

            if len(hands[0]) >= p1card and len(hands[1]) >= p2card:
                minihands = []
                minihands.append(hands[0][:p1card])
                minihands.append(hands[1][:p2card])
                winner = playRecursiveCombat(minihands)

                if winner == 0:
                    hands[0].extend([p1card, p2card])
                else:
                    hands[1].extend([p2card, p1card])

            else:
                if p1card > p2card:
                    return 0
                else:
                    return 1


def updateCache(cache):
    p1str = ",".join([str(i) for i in cards[0]])
    p2str = ",".join([str(i) for i in cards[1]])

    return p1str + "-" + p2str


def printScore():
    for i, hand in enumerate(cards):
        if len(hand) > 0:
            points = zip(hand, range(len(hand), 0, -1))
            score = 0

            for p in points:
                score += p[0] * p[1]

            print(f"Player {i+1} wins, with a score of {score}!")


def printCards(hands):
    for i, hand in enumerate(hands):
        print(f"Player {i+1}:")
        print(hand)


if __name__ == "__main__":
    main()

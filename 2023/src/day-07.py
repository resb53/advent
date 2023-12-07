#!/usr/bin/env python3

import argparse
import sys
from itertools import groupby

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

hands = []
jhands = []


class InvalidCardException(Exception):
    pass


class Card:
    order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    jorder = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def __new__(cls, value, joker=False):
        if value in Card.order:
            return super().__new__(cls)
        else:
            raise InvalidCardException(f"Card must have a value in {Card.order}.")

    def __init__(self, value, joker=False):
        self.value = value
        self.joker = joker
        if joker:
            self.order = self.jorder

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self.order.index(self.value) < self.order.index(other.value)

    def __le__(self, other):
        return self.order.index(self.value) <= self.order.index(other.value)

    def __gt__(self, other):
        return self.order.index(self.value) > self.order.index(other.value)

    def __ge__(self, other):
        return self.order.index(self.value) >= self.order.index(other.value)

    def __eq__(self, other):
        return self.value == other.value


class InvalidHandException(Exception):
    pass


class Hand:
    types = ["HC", "1P", "2P", "3oak", "FH", "4oak", "5oak"]

    def __new__(cls, value, joker=False):
        if type(value) is not list:
            raise InvalidHandException("Hand must be a list of 5 Cards.")
        else:
            if len(value) != 5:
                raise InvalidHandException("Hand must contain exactly 5 Cards.")
            for crd in value:
                if type(crd) is not Card:
                    raise InvalidHandException("Hand must only contain Cards.")
        if joker:
            for crd in value:
                if not crd.joker:
                    raise InvalidHandException("Joker Hands may only contain Joker Cards.")
        else:
            for crd in value:
                if crd.joker:
                    raise InvalidHandException("Normal Hands may not contain Joker Cards.")

        return super().__new__(cls)

    def __init__(self, value, joker=False):
        self.contents = value
        self.joker = joker

        # Determine type of hand
        sorthand = sorted(value)
        groups = []
        unique = []
        for k, g in groupby(sorthand):
            groups.append(list(g))
            unique.append(k)

        if self.joker:
            if Card("J", joker=True) in unique:
                jcount = len(groups[0])  # J is weakest Jcard
                # Make strongest type by adding J to any largest group
                if jcount != 5:
                    jgroup = groups.pop(0)
                    unique.pop(0)

                    largestcount = 0
                    largestindex = 0

                    for ix, grp in enumerate(groups):
                        if len(grp) >= largestcount:
                            largestcount = len(grp)
                            largestindex = ix

                    groups[largestindex].extend(jgroup)

        if len(groups) == 1:
            self.type = "5oak"

        elif len(groups) == 2:
            if len(groups[0]) == 4 or len(groups[1]) == 4:
                self.type = "4oak"
            else:
                self.type = "FH"

        elif len(groups) == 3:
            if len(groups[0]) == 3 or len(groups[1]) == 3 or len(groups[2]) == 3:
                self.type = "3oak"
            else:
                self.type = "2P"

        elif len(groups) == 4:
            self.type = "1P"

        else:
            self.type = "HC"

    def __str__(self):
        return str([str(x) for x in self.contents])

    def __lt__(self, other):
        if self.type != other.type:
            return Hand.types.index(self.type) < Hand.types.index(other.type)
        else:
            if self.contents[0] != other.contents[0]:
                return self.contents[0] < other.contents[0]
            elif self.contents[1] != other.contents[1]:
                return self.contents[1] < other.contents[1]
            elif self.contents[2] != other.contents[2]:
                return self.contents[2] < other.contents[2]
            elif self.contents[3] != other.contents[3]:
                return self.contents[3] < other.contents[3]
            elif self.contents[4] != other.contents[4]:
                return self.contents[4] < other.contents[4]
            else:
                return False

    def __le__(self, other):
        if self.type != other.type:
            return Hand.types.index(self.type) <= Hand.types.index(other.type)
        else:
            if self.contents[0] != other.contents[0]:
                return self.contents[0] <= other.contents[0]
            elif self.contents[1] != other.contents[1]:
                return self.contents[1] <= other.contents[1]
            elif self.contents[2] != other.contents[2]:
                return self.contents[2] <= other.contents[2]
            elif self.contents[3] != other.contents[3]:
                return self.contents[3] <= other.contents[3]
            elif self.contents[4] != other.contents[4]:
                return self.contents[4] <= other.contents[4]
            else:
                return False

    def __gt__(self, other):
        if self.type != other.type:
            return Hand.types.index(self.type) > Hand.types.index(other.type)
        else:
            if self.contents[0] != other.contents[0]:
                return self.contents[0] > other.contents[0]
            elif self.contents[1] != other.contents[1]:
                return self.contents[1] > other.contents[1]
            elif self.contents[2] != other.contents[2]:
                return self.contents[2] > other.contents[2]
            elif self.contents[3] != other.contents[3]:
                return self.contents[3] > other.contents[3]
            elif self.contents[4] != other.contents[4]:
                return self.contents[4] > other.contents[4]
            else:
                return False

    def __ge__(self, other):
        if self.type != other.type:
            return Hand.types.index(self.type) >= Hand.types.index(other.type)
        else:
            if self.contents[0] != other.contents[0]:
                return self.contents[0] >= other.contents[0]
            elif self.contents[1] != other.contents[1]:
                return self.contents[1] >= other.contents[1]
            elif self.contents[2] != other.contents[2]:
                return self.contents[2] >= other.contents[2]
            elif self.contents[3] != other.contents[3]:
                return self.contents[3] >= other.contents[3]
            elif self.contents[4] != other.contents[4]:
                return self.contents[4] >= other.contents[4]
            else:
                return False

    def __eq__(self, other):
        if self.contents[0] == other.contents[0] and \
           self.contents[1] == other.contents[1] and \
           self.contents[2] == other.contents[2] and \
           self.contents[3] == other.contents[3] and \
           self.contents[4] == other.contents[4]:
            return True
        else:
            return False


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        cards, bet = line.rstrip().split()
        hand = Hand([Card(x) for x in cards])
        hands.append([hand, int(bet)])
        jhand = Hand([Card(x, joker=True) for x in cards], joker=True)
        jhands.append([jhand, int(bet)])


# Find winnings for standard rules
def processData():
    winnings = 0
    sorthands = sorted(hands)
    for rank, hand in enumerate(sorthands):
        winnings += (rank+1) * hand[1]
    return winnings


# Find winnings for Joker J's
def processMore():
    winnings = 0
    sortjhands = sorted(jhands)
    for rank, hand in enumerate(sortjhands):
        winnings += (rank+1) * hand[1]
    return winnings


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

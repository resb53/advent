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


class InvalidCardException(Exception):
    pass


class Card:
    order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __new__(cls, value):
        if value in Card.order:
            return super().__new__(cls)
        else:
            raise InvalidCardException(f"Card must have a value in {Card.order}.")

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return Card.order.index(self.value) < Card.order.index(other.value)

    def __le__(self, other):
        return Card.order.index(self.value) <= Card.order.index(other.value)

    def __gt__(self, other):
        return Card.order.index(self.value) > Card.order.index(other.value)

    def __ge__(self, other):
        return Card.order.index(self.value) >= Card.order.index(other.value)

    def __eq__(self, other):
        return self.value == other.value


class InvalidHandException(Exception):
    pass


class Hand:
    types = ["HC", "1P", "2P", "3oak", "FH", "4oak", "5oak"]

    def __new__(cls, value):
        if type(value) is not list:
            raise InvalidHandException("Hand must be a list of 5 Cards.")
        else:
            if len(value) != 5:
                raise InvalidHandException("Hand must contain exactly 5 Cards.")
            for crd in value:
                if type(crd) is not Card:
                    raise InvalidHandException("Hand must only contain Cards.")
            return super().__new__(cls)

    def __init__(self, value):
        self.contents = value

        # Determine type of hand
        sorthand = sorted(value)
        groups = [list(g) for k, g in groupby(sorthand)]

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
        return [str(x) for x in self.contents]

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
        data.append(line.rstrip())


# For each pass, identify its seat
def processData():
    for element in data:
        print(f"{element}")
    return False


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

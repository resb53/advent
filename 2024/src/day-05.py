#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

befores = defaultdict(list)
afters = defaultdict(list)
books = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        if '|' in line:
            a, b = line.split('|')
            befores[int(a)].append(int(b))
            afters[int(b)].append(int(a))
        elif ',' in line:
            books.append([int(x) for x in line.split(',')])


# Check the page orders
def processData():
    summid = 0
    for book in books:
        if validate_book(book):
            mid = len(book) // 2
            summid += book[mid]

    return summid


# Validate if page order is correct
def validate_book(book):
    for page in book:
        if page in befores:
            for x in befores[page]:
                if x in book and book.index(x) < book.index(page):
                    return False
        if page in afters:
            for x in afters[page]:
                if x in book and book.index(x) > book.index(page):
                    return False

    return True


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

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
incorrect = []

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
        else:
            incorrect.append(book)

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


# Reorder the pages of the incorrect books
def processMore():
    summid = 0
    for book in incorrect:
        summid += reorder(book)

    return summid


# Reorder an incorrect books pages
def reorder(book):
    pages = [x for x in book]
    for page in pages:
        # If page must precede others, find leftest one it must precede
        if page in befores:
            for x in book:
                if x in befores[page]:
                    book.remove(page)
                    book.insert(book.index(x), page)
                    break
    # Mid or reordered book:
    mid = len(book) // 2
    return book[mid]


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()

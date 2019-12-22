#!/usr/bin/python3

import argparse
import sys
from collections import deque
from math import gcd

# Check correct usage
parser = argparse.ArgumentParser(description="Shuffle cards.")
parser.add_argument('inp', metavar='inp', type=str, help='Input shuffle instructions.')
parser.add_argument('-n', metavar='cards', type=int, default=10, help='Number of cards.')
parser.add_argument('-t', metavar='cards', type=int, default=10, help='Target card.')
args = parser.parse_args()

#cards = deque(range(args.n), maxlen=args.n) # Card array
instr = [] # Instructions

# Part 1: Run simple instructions
# Part 2: Many numbers. Shuffles aren't really mixing cards, but predictively reordering.
# Calculate the pattern for repetition n?

first = 0 # First card in the deck
nextgap = 1 # Gap till the next number

def main():
    global instr
    instr = getInstr(args.inp)
    for cmd in instr:
        print(cmd[0] + ' ' + str(cmd[1]))
        cmds[cmd[0]](cmd[1])
        print("First:" + str(first) + "; Gap:" + str(nextgap))
        printDeck()

def getInstr(inp):
    try:
        fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    instrs = []
    for line in fh:
        line = line.strip('\n')
        words = line.split(' ')
        val = ''
        if words[-1] != 'stack':
            val = int(words.pop())
        cmd = ' '.join(words)
        instrs.append([cmd, val])

    return instrs

def printDeck():
    deck = [None] * args.n
    deck[0] = first
    cards = list(range(first+1, args.n))
    cards.extend(list(range(0, first)))
    n = 1
    for i in cards:
        deck[(n * nextgap) % args.n] = i
        n += 1
    print(deck)

def shufNew(val):
    # Gapping gets inverted, and first card is now the last card...?
    # 0,1,2,3,4 -> 4,3,2,1,0 nextgap=1/-1
    # 0,3,1,4,2 -> 2,4,1,3,0 nextgap=2/3
    global first, nextgap
    first = (first + nextgap) % args.n
    nextgap = (nextgap * -1) % args.n

def shufCut(val):
    # Gapping stays the same, but first card changes
    # 0,1,2,3,4 -> 1,2,3,4,0 cut 1, gap 1
    # 2,3,4,0,1 -> 4,0,1,2,3 cut 2, gap 1
    # 0,3,1,4,2 -> 1,4,2,0,3 cut 2, gap 2
    # 0,3,1,4,2 -> 4,2,0,3,1 cut -2, gap 2
    # first card will be card in position val
    # 0,1,2,3,4 -> 3,4,0,1,2 cut 3, gap 1
    # 0,3,1,4,2 -> 4,2,0,3,1 cut 3, gap 2
    # cut -n = cut (-n % args.n)
    # first = first + LCM(val,nextgap) (keep looping around until we know a value, number of loops = number of increments?)
    global first
    val %= args.n
    print(str(lcm(nextgap, val)))
    first = (first + lcm(nextgap, val)//nextgap) % args.n

def shufInc(val):
    # First card stays the same, gapping changes
    # 0,1,2,3,4 -> 0,3,1,4,2 val 2
    # 0,1,2,3,4 -> 0,2,4,1,3 val 3
    global nextgap
    nextgap = (nextgap * val) % args.n

def lcm(x, y): # Calculate LCM of two values as per moons.py
    return int(x * y / (gcd(x, y)))

cmds = {    'cut': shufCut,
            'deal with increment': shufInc,
            'deal into new stack': shufNew}

if __name__ == "__main__":
    main()

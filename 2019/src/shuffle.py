#!/usr/bin/python3

import argparse
import sys
from collections import deque

# Check correct usage
parser = argparse.ArgumentParser(description="Shuffle cards.")
parser.add_argument('inp', metavar='inp', type=str, help='Input shuffle instructions.')
parser.add_argument('-n', metavar='cards', type=int, default=10, help='Number of cards.')
args = parser.parse_args()

cards = deque(range(args.n), maxlen=args.n) # Card array
instr = [] # Instructions

# Part 1: Run simple instructions
# Part 2: Many numbers. Look for patterns to shortcut / simplify / calculate card position after commands. Track one card?
# Observations over 20 cards:
# Reverse, card in position n moves to maxlen-n
# Wait... Need number on card in position 2020, can't follow single card around.
def main():
    global instr, cards
    instr = getInstr(args.inp)
    for cmd in instr:
        print(cmd[0] + ' ' + str(cmd[1]))
        cmds[cmd[0]](cmd[1])
        print(cards)
        print(cards.index(4))
    
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

def shufCut(val):
    global cards
    cards.rotate(-val)

def shufInc(val):
    global cards
    new = [None] * args.n
    for i in range(0,len(cards)):
        new[i * val % args.n] = cards[i]
    cards = deque(new, maxlen=args.n)

def shufNew(val):
    global cards
    cards.reverse()

cmds = {    'cut': shufCut,
            'deal with increment': shufInc,
            'deal into new stack': shufNew}

if __name__ == "__main__":
    main()

#!/usr/bin/python3

import intCode
import curses
import sys
import time
import tty
import termios
import signal
from random import randint

pos = [0,0] # x,y
prev = [0,0]
start = [0,0]
oxy = [0,0]
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 robot
around = {} # whats currently around the bot
io = {'input': [], 'output': []} # Dict holding next input / last output
move = {'w': 1, 's': 2, 'a': 3, 'd':4}
draw = {0: '█', 1: 'o', 2: '!', 3: '.', 4: 'x'} # in the new space draw a wall, or the new droid pos, or the oxysys
counter = 0

def main():
    global win, pos, start, curses
    # Read ch from stdin
    fh = sys.stdin.fileno()
    old = termios.tcgetattr(fh)
    tty.setraw(sys.stdin.fileno())
    # Prepare screen
    win = curses.initscr()
    win.clear()
    win.refresh()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    # Handle SIGINT gracefully
    signal.signal(signal.SIGINT, sigintClean)
    # Get starting point
    winy, winx = win.getmaxyx()
    # Start in the middle
    pos = [winx//2, winy//2]
    start = [winx//2, winy//2]
    if pos[1] not in grid:
        grid[pos[1]] = {}
    grid[pos[1]][pos[0]] = 1
    # Draw grid
    drawin()
    # Prepare intcode computer
    prog = intCode.Program('inputs/oxygen.txt')
    prog.run(i=instr_in,o=instr_out)
    # Cleanup
    termios.tcsetattr(fh, termios.TCSADRAIN, old)
    curses.endwin()

def sigintClean(sig, frame):
    curses.endwin()
    sys.exit(0)

def drawin():
    win.addstr(0, 0, str(counter))
    for y in grid:
        for x in grid[y]:
            win.addstr(y, x, draw[grid[y][x]])
    win.refresh()

def instr_in():
    global counter
    k = 'x'
    # Manual Play
    while k not in move:
        k = sys.stdin.read(1)
        if k == 'r':
            #Reset counter
            win.addstr(0, 0, '0                                                     ')
            win.refresh()
            counter = 0
    # Auto Play
    #k = generateMove()

    moveFocus(move[k])
    counter += 1
    return move[k]

def instr_out(p):
    global oxy
    grid[pos[1]][pos[0]] = p
    if p == 0:
        # If it was a wall, keep droid in pos, reset pos
        pos[0] = prev[0]
        pos[1] = prev[1]
    else:
        # If it was the tank, record this
        if p == 2:
            oxy[0] = pos[0]
            oxy[1] = pos[1]
        if prev[0] == oxy[0] and prev[1] == oxy[1]:
            grid[prev[1]][prev[0]] = 2
        # Else if it was the start use an x, else change previous space to a .
        elif prev[0] == start[0] and prev[1] == start[1]:
            grid[prev[1]][prev[0]] = 4
        else:
            grid[prev[1]][prev[0]] = 3

    updateSur()
    drawin()

def moveFocus(k):
    # Which tile will the next response be for? update pos
    global pos, prev, grid
    prev[0] = pos[0]
    prev[1] = pos[1]
    if k == 1:
        pos[1] -= 1
    elif k == 2:
        pos[1] += 1
    elif k == 3:
        pos[0] -= 1
    else:
        pos[0] += 1
    if pos[1] not in grid:
        grid[pos[1]] = {}
    grid[pos[1]][pos[0]] = ''

def generateMove():
    # Use around to pick next move
    for d in around:
        if around[d] == None:
            return d
    else:
        return list(move.keys())[randint(0,3)]

def updateSur():
    global around
    check = [0, 0]
    check[0] = pos[0]
    check[1] = pos[1]
    # w
    check[1] -= 1
    around['w'] = getTile(check)
    # s
    check[1] += 2
    around['s'] = getTile(check)
    # a
    check[1] -= 1
    check[0] -= 1
    around['a'] = getTile(check)
    # d
    check[0] += 2
    around['d'] = getTile(check)
    # print
    #global win
    #win.addstr(0, 0, '                                                      ')
    #win.addstr(0, 0, str(around))
    #win.refresh

def getTile(check):
    if check[1] in grid and check[0] in grid[check[1]]:
        return grid[check[1]][check[0]]
    else:
        return None


if __name__ == "__main__":
    main()

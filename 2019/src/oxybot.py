#!/usr/bin/python3

import intCodeClass
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
expl = [0,0] # Current exploration tile
hist = [] # List of history
rev = 0 # Reversing flag
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 robot
io = {'input': [], 'output': []} # Dict holding next input / last output
move = {'w': 1, 's': 2, 'a': 3, 'd':4}
draw = {0: '█', 1: 'o', 2: '!', 3: '.', 4: 'x'} # in the new space draw a wall, or the new droid pos, or the oxysys
#counter = 0

def main():
    global win, pos, start, expl, curses
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
    expl = [winx//2, winy//2] # explore this
    start = [winx//2, winy//2]
    if pos[1] not in grid:
        grid[pos[1]] = {}
    grid[pos[1]][pos[0]] = 1
    # Draw grid
    drawin()
    # Prepare intcode computer
    prog = intCodeClass.Program('inputs/oxygen.txt')
    prog.run(i=instr_in,o=instr_out)
    # Cleanup
    termios.tcsetattr(fh, termios.TCSADRAIN, old)
    curses.endwin()

def sigintClean(sig, frame):
    curses.endwin()
    print(grid, file=open('grid.txt', 'a'))
    sys.exit(0)

def drawin():
    #win.addstr(0, 0, str(counter))
    for y in grid:
        for x in grid[y]:
            win.addstr(y, x, draw[grid[y][x]])
    win.refresh()

def instr_in():
    global hist
    # Print old to new position
    #win.addstr(0, 0, '                                                     ')
    #win.addstr(0, 0, str(prev) + ' -> ' + str(pos))
    #win.refresh()
    # Make next move
    # Auto Play
    g = generateMove()
    # Manual Play
    k = 'x'
    while k not in move:
        k = sys.stdin.read(1)
        if k == 'q': #Semiauto
            k = g
        #if k == 'r':
            #Reset counter
            #win.addstr(0, 0, '0                                                     ')
            #win.refresh()
            #counter = 0

    moveFocus(move[k])
    if rev == 0:
        hist.append(k)
    if len(hist) > 100:
        hist.pop(0)
    win.addstr(4, 0, str(hist))
    #counter += 1
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
    global win, expl, ret, hist, rev
    nex = ''
    rev = 0 # Try a new path
    #win.addstr(1, 0, '                                                       ')
    #win.addstr(1, 0, str(getSur(pos)))
    #win.addstr(2, 0, '                                                       ')
    #win.addstr(2, 0, str(getSur(prev)))
    #win.addstr(3, 0, '                                                       ')

    # If moved since last time:
    if pos[0] != expl[0] or pos[1] != expl[1]:
        n = 0
        c = getSur(prev)
        for d in c:
            if c[d] == None:
                n += 1
        if n != 0:
            if pos[0] > expl[0]:
                nex = 'a'
            if pos[0] < expl[0]:
                nex = 'd'
            if pos[1] > expl[1]:
                nex = 'w'
            if pos[1] < expl[1]:
                nex = 's'
        else:
            expl[0] = pos[0]
            expl[1] = pos[1]
            return generateMove()
    else:
        f = 0
        c = getSur(pos)
        for d in c:
            if c[d] == None:
                f = 1
                nex = d
        if f == 0:
            # Find available route that isn't yet explored
            for d in c:
                if c[d] == 3:
                    x = {}
                    if d == 'w':
                        x = getSur([pos[0],pos[1]-1])
                    elif d == 's':
                        x = getSur([pos[0],pos[1]+1])
                    elif d == 'a':
                        x = getSur([pos[0]-1,pos[1]])
                    elif d == 'd':
                        x = getSur([pos[0]+1,pos[1]])
                    n = 0
                    for y in x:
                        if x[y] == None:
                            n += 1
                    if n != 0:
                        nex = d
            # If still nothing, retrace steps till there is
            if nex == '':
                if len(hist) > 0:
                    v = hist.pop()
                else:
                    return '?'
                w = ''
                if v == 'w':
                    w = 's'
                elif v == 's':
                    w = 'w'
                elif v == 'a':
                    w = 'd'
                elif v == 'd':
                    w = 'a'
                nex = w
                rev = 1 # still reversing
    win.addstr(3, 0, 'Press ' + nex)
    win.refresh()
    return nex

def getSur(p):
    around = {}
    check = [0, 0]
    check[0] = p[0]
    check[1] = p[1]
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
    return around

def getTile(check):
    if check[1] in grid and check[0] in grid[check[1]]:
        return grid[check[1]][check[0]]
    else:
        return None


if __name__ == "__main__":
    main()

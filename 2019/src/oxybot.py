#!/usr/bin/python3

import intCode
import curses
import sys
import time
import tty
import termios
import signal

pos = [0,0] # x,y
prev = [0,0]
start = [0,0]
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 robot
io = {'input': [], 'output': []} # Dict holding next input / last output
move = {'w': 1, 's': 2, 'a': 3, 'd':4}
draw = {0: '█', 1: 'o', 2: '!', 3: '.', 4: 'x'} # in the new space draw a wall, or the new droid pos, or the oxysys

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
    for y in grid:
        for x in grid[y]:
            win.addstr(y, x, draw[grid[y][x]])
    win.refresh()

def instr_in():
    k = 'x'
    while k not in move:
        k = sys.stdin.read(1)
    moveFocus(move[k])
    return move[k]

def instr_out(p):
    grid[pos[1]][pos[0]] = p
    if p == 0:
        # If it was a wall, keep droid in pos, reset pos
        pos[0] = prev[0]
        pos[1] = prev[1]
    else:
        # If it was the start use an x, else change previous space to a .
        #global win
        #win.addstr(0, 0, str(prev) + ' vs ' + str(start))
        if prev[0] == start[0] and prev[1] == start[1]:
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

if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import curses
import sys
import tty
import termios

# Check correct usage
parser = argparse.ArgumentParser(description="Watch oxygen fill the room.")
parser.add_argument('grid', metavar='grid', type=str, help='Grid object')
args = parser.parse_args()

grid = {} # grid[y][x] -> draw value
draw = {0: '█', 1: 'o', 2: '!', 3: '.', 4: 'x'} # in the new space draw a wall, or the new droid pos, or the oxysys
count = 0 # minutes passed
oxy = {} # oxy-filled points that can expand
dot = {} # oxy-starved points

def main():
    global grid, curses, win, count
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
    # Get standard grid
    grid = eval(getGrid(args.grid))
    # Initiate for oxyfill
    gridInit()
    # Draw grid
    drawin()
    while len(dot) > 0:
        # Act on keypress
        expand()
        count += 1
        # Draw grid
        drawin()
    # Cleanupi
    termios.tcsetattr(fh, termios.TCSADRAIN, old)
    curses.endwin()

def getGrid(loc):
    try:
        grid_fh = open(loc, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + loc)

    return grid_fh.readline().strip('\n') 

def gridInit():
    global oxy, dot, grid
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == 4:
                grid[y][x] = 3
                if y not in dot:
                    dot[y] = {}
                dot[y][x] = 1
            elif grid[y][x] == 3:
                if y not in dot:
                    dot[y] = {}
                dot[y][x] = 1
            elif grid[y][x] == 2:
                grid[y][x] = 1
                if y not in oxy:
                    oxy[y] = {}
                oxy[y][x] = 1

def drawin():
    win.addstr(0, 0, str(count))
    win.addstr(1, 0, str(oxy))
    #win.addstr(2, 0, str(dot))
    for y in grid:
        for x in grid[y]:
            win.addstr(y, x, draw[grid[y][x]])
    win.refresh()

def expand():
    global oxy, dot, grid
    newoxy = {}
    for y in oxy:
        for x in oxy[y]:
            if oxy[y][x] == 1:
                # Expand
                if grid[y-1][x] == 3:
                    grid[y-1][x] == 1
                    dot[y-1][x] = 0
                    if y-1 not in newoxy:
                        newoxy[y-1] = {}
                    newoxy[y-1][x] = 1
                if grid[y+1][x] == 3:
                    grid[y+1][x] == 1
                    dot[y+1][x] = 0
                    if y+1 not in newoxy:
                        newoxy[y+1] = {}
                    newoxy[y+1][x] = 1
                if grid[y][x-1] == 3:
                    grid[y][x-1] == 1
                    dot[y][x-1] = 0
                    if y not in newoxy:
                        newoxy[y] = {}
                    newoxy[y][x-1] = 1
                if grid[y][x+1] == 3:
                    grid[y][x+1] == 1
                    dot[y][x+1] = 0
                    if y not in newoxy:
                        newoxy[y] = {}
                    newoxy[y][x+1] = 1
                oxy[y][x] == 0
    # Update oxy
    for y in newoxy:
        for x in newoxy[y]:
            if y not in oxy:
                oxy[y] = {}
            oxy[y][x] = 1

if __name__ == "__main__":
    main()

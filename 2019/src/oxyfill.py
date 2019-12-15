#!/usr/bin/python3

import argparse
import curses
import sys
import tty
import termios
from time import sleep

# Check correct usage
parser = argparse.ArgumentParser(description="Watch oxygen fill the room.")
parser.add_argument('grid', metavar='grid', type=str, help='Grid object')
args = parser.parse_args()

grid = {} # grid[y][x] -> draw value
draw = {0: '█', 1: 'o', 2: '!', 3: '.', 4: 'x'} # in the new space draw a wall, or the new droid pos, or the oxysys
count = 0 # minutes passed
dots = 1

def main():
    global grid, curses, win, count, dots
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
    while dots > 0:
        expand()
        count += 1
        # Count dots
        dots = 0
        for y in grid:
            for x in grid[y]:
                if grid[y][x] == 3:
                    dots += 1
        # Display gradually
        sleep(0.05)
        # Draw grid
        drawin()
    # Cleanupi
    termios.tcsetattr(fh, termios.TCSADRAIN, old)
    curses.endwin()

    print("Room filled in " + str(count) + " minutes.")

def getGrid(loc):
    try:
        grid_fh = open(loc, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + loc)

    return grid_fh.readline().strip('\n') 

def gridInit():
    global oxy, dot, grid, maxy
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == 4:
                grid[y][x] = 3
            elif grid[y][x] == 2:
                grid[y][x] = 1

def drawin():
    global win, dots
    win.addstr(0, 0, '                                                       ')
    win.addstr(0, 0, str(count) + " minutes: " + str(dots) + " dots remain.")
    for y in grid:
        for x in grid[y]:
            win.addstr(y, x, draw[grid[y][x]])
    win.refresh()

def expand():
    global grid
    newo = []
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == 1:
                # Expand
                if grid[y-1][x] == 3:
                    newo.append([y-1, x])
                if grid[y+1][x] == 3:
                    newo.append([y+1, x])
                if grid[y][x-1] == 3:
                    newo.append([y, x-1])
                if grid[y][x+1] == 3:
                    newo.append([y, x+1])
    for c in newo:
        grid[c[0]][c[1]] = 1

if __name__ == "__main__":
    main()

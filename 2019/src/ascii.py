#!/usr/bin/python3

import intCode
import curses
import sys
import time

pos = [0,0] # x, y
grid = {} # grid[y][x]

def main():
    # Prepare intcode computer
    prog = intCode.Program('inputs/ascii.txt')
    prog.run(o=instr_out)
    cleanGrid()
    printGrid()
    # Do part 1: Find intersections and calculate alignment parameters
    intersect()

def instr_out(p):
    global pos, grid
    p = int(p)
    # Update pos
    if p == 10:
        pos[1] += 1
        pos[0] = 0
    else:
        # Add to grid
        y = pos[1]
        x = pos[0]
        if y not in grid:
            grid[y] = {}
        grid[y][x] = p
        pos[0] += 1

def cleanGrid():
    global grid
    height = len(grid)

def printGrid():
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            print(chr(grid[y][x]), end='')
        print('')


def intersect():
    global grid
    param = 0

    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[y])-1):
            if grid[y][x] == 35:
                # adj #
                adj = 0
                if grid[y][x+1] == 35:
                    adj += 1
                if grid[y][x-1] == 35:
                    adj += 1
                if grid[y+1][x] == 35:
                    adj += 1
                if grid[y-1][x] == 35:
                    adj += 1
                if adj == 4:
                    print('(' + str(x) + ',' + str(y) + ')')
                    param += y * x

    print(param)

if __name__ == "__main__":
    main()

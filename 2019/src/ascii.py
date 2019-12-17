#!/usr/bin/python3

import intCode
import curses
import sys
import time

pos = [0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 block, 3 paddle, 4 ball

def main():
    # Prepare intcode computer
    prog = intCode.Program('inputs/ascii.txt')
    prog.run(o=instr_out)
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
        pos[0] += 1
    # Add to grid
    y = pos[1]
    x = pos[0]
    if y not in grid:
        grid[y] = {}
    grid[y][x] = p

def intersect():
    global grid
    #print (str(len(grid)) + ' by ' + str(len(grid[0])))
    height = len(grid)
    width = len(grid[0])
    param = 0

    for y in range(1, height-1):
        for x in range(1, width-1):
            print(str(y) + ',' + str(x))
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
                    param += y * x

    print(param)

if __name__ == "__main__":
    main()

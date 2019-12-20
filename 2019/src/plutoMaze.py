#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Navigate the maze.")
parser.add_argument('map', metavar='map', type=str, help='Map input.')
args = parser.parse_args()

grid = {} # map[y][x] symbols
portals = {}
pos = [0,0] # x, y

def main():
    global grid, portals
    parseInput(args.map)
    printGrid(grid)
    # Part 1: Shortest route AA to ZZ
    #getPortals()
    #calcRoutes()

def parseInput(inp):
    global grid, pos
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    x = 0

    for line in grid_fh:
        line = line.strip("\n")
        grid[y] = {}
        for ch in list(line):
            grid[y][x] = ch
            x += 1
        y += 1
        x = 0

def printGrid(g):
    for y in g:
        for x in g[y]:
            print(g[y][x], end='')
        print('')

def getItems():
    global door, keys
    for y in grid:
        for x in grid[y]:
            ch = grid[y][x]
            if ch != '#' and ch != '.' and ch != '@':
                if ch.isupper():
                    door[ch] = 0
                else:
                    keys[ch] = 0
                
def calcRoutes(pos, key, doo, rou):
    global grid, bestroute
    option = {} # Key option to go for, value distance
    count = rou[0]
    grid[pos[1]][pos[0]] = ','
    done = False

    while done == False:
        count += 1
        if count >= bestroute[0]:
            done = 1
        else:
            [grid, option, done] = expand(grid, option, count)

    for k in option:
        # Only continue if this route isn't already longer
        if option[k][0] < bestroute[0]:
            # New copy for this route
            grid = deepcopy(freshg)
            newpos = [option[k][2], option[k][1]]
            newkeys = deepcopy(key)
            newdoor = deepcopy(doo)
            # Update for this route
            newrou = deepcopy(rou)
            newrou[0] = option[k][0]
            newrou.append(k)
            print(newrou)
            newkeys[k] = 1
            newdoor[k.upper()] = 1
            for y in grid:
                for x in grid[y]:
                    if grid[y][x] in newdoor and newdoor[grid[y][x]] == 1:
                        grid[y][x] = '.'
                    elif grid[y][x] in newkeys and newkeys[grid[y][x]] == 1:
                        grid[y][x] = '.'
            # Reset grid, rerun from newpos
            calcRoutes(newpos, newkeys, newdoor, newrou)

    if len(rou) == len(key) + 1:
        print("Total route: " + str(rou[0]))
        if rou[0] < bestroute[0]:
            bestroute = deepcopy(rou)

def expand(g, o, c):
    # No bound checking as surrounding wall
    expanded = []
    for y in g:
        for x in g[y]:
            if g[y][x] == ',':
                # Expand
                if g[y-1][x] == '.':
                    expanded.append([y-1, x])
                elif g[y-1][x].islower():
                    o[g[y-1][x]] = [c, y-1, x]
                    g[y-1][x] = '!'

                if g[y+1][x] == '.':
                    expanded.append([y+1, x])
                elif g[y+1][x].islower():
                    o[g[y+1][x]] = [c, y+1, x]
                    g[y+1][x] = '!'

                if g[y][x-1] == '.':
                    expanded.append([y, x-1])
                elif g[y][x-1].islower():
                    o[g[y][x-1]] = [c, y, x-1]
                    g[y][x-1] = '!'

                if g[y][x+1] == '.':
                    expanded.append([y, x+1])
                elif g[y][x+1].islower():
                    o[g[y][x+1]] = [c, y, x+1]
                    g[y][x+1] = '!'

    if len(expanded) > 0:
        for p in expanded:
            g[p[0]][p[1]] = ','
        return [g, o, False]
    else:
        return [g, o, True]

if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Navigate the maze.")
parser.add_argument('map', metavar='map', type=str, help='Map input.')
args = parser.parse_args()

grid = {} # map[y][x] symbols
keys = {} # List of keys: 1 = held, 0 = not held
door = {} # List of doors: 1 = open, 0 = locked
keyroute = [0] # 0: distance so far, 1-n: n'th key collected
pos = [0,0] # x, y

def main():
    global grid, keys, door, keyroute
    parseInput(args.map)
    # Part 1: From start calculate distance to each key, then from each key to each other with doors unlocked, etc.
    # Brute force all possible routes, and print fastest. <- No! 26 keys = 26! options (MANY)... unless only a few visible at a time
    getItems()
    calcRoutes(pos, keys, door, keyroute)

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
            if ch == '@':
                pos = [x,y]
                grid[y][x] = '.'
            else:
                grid[y][x] = ch
            x += 1
        y += 1
        x = 0

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
    # New copy for this route
    thispos = deepcopy(pos)
    thiskeys = deepcopy(key)
    thisdoor = deepcopy(doo)
    thisroute = deepcopy(rou)
    thisgrid = deepcopy(grid)

    option = {} # Key option to go for, value distance
    
    count = 0
    thisgrid[pos[1]][pos[0]] = ','
    done = False

    while done == False:
        count += 1
        [thisgrid, done] = expand(thisgrid)

    printGrid(thisgrid)
    print(count)

def expand(g):
    # No bound checking as surrounding wall
    expanded = []
    for y in g:
        for x in g[y]:
            if g[y][x] == ',':
                # Expand
                if g[y-1][x] == '.':
                    expanded.append([y-1, x])
                if g[y+1][x] == '.':
                    expanded.append([y+1, x])
                if g[y][x-1] == '.':
                    expanded.append([y, x-1])
                if g[y][x+1] == '.':
                    expanded.append([y, x+1])
    if len(expanded) > 0:
        for c in expanded:
            g[c[0]][c[1]] = ','
        return [g, False]
    else:
        return [g, True]

def printGrid(g):
    for y in g:
        for x in g[y]:
            print(g[y][x], end='')
        print('')

if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Navigate the maze.")
parser.add_argument('map', metavar='map', type=str, help='Map input.')
args = parser.parse_args()

grid = {} # map[y][x] symbols
freshg = {} # fresh grid
keys = {} # List of keys: 1 = held, 0 = not held
door = {} # List of doors: 1 = open, 0 = locked
keypos = {} # List of key positions k = [x,y]
keyroute = [0] # 0: distance so far, 1-n: n'th key collected
keymap = {}
pos = [0,0] # x, y

def main():
    global grid, freshg, keymap
    parseInput(args.map)
    freshg = deepcopy(grid)
    # Part 1: From start calculate distance to each key, then from each key to each other with doors unlocked, etc.
    # Brute force all possible routes, and print fastest. <- No! 26 keys = 26! options (MANY)... unless only a few visible at a time
    getItems()
    # Initial options
    startops = calcRoutes(pos)
    keymap = calcDiffs(keypos)
    print(keymap)

def parseInput(inp):
    global grid, pos, keypos
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
            if ch.islower():
                keypos[ch] = [x,y]
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
                
def calcRoutes(pos):
    global grid
    option = {} # Key option to go for, value distance
    count = 0
    grid[pos[1]][pos[0]] = ','
    done = False

    while done == False:
        count += 1
        [grid, option, done] = expand(grid, option, count)

    grid = deepcopy(freshg)
    return option

def calcDiffs(kp):
    global grid
    km = {}

    for k in kp:
        count = 0
        km[k] = {}
        grid[kp[k][1]][kp[k][0]] = ','
        done = False

        while done == False:
            count += 1
            [grid, km[k], done] = expanDoors(grid, km[k], count)

        print(k + ': ' + str(km[k]))
        grid = deepcopy(freshg)

    return km

def expanDoors(g, kdist, c):
    expanded = []
    for y in g:
        for x in g[y]:
            if g[y][x] == ',':
                # Expand
                if g[y-1][x] == '.' or g[y-1][x].isupper():
                    expanded.append([y-1, x])
                elif g[y-1][x].islower():
                    kdist[g[y-1][x]] = c
                    expanded.append([y-1, x])

                if g[y+1][x] == '.' or g[y+1][x].isupper():
                    expanded.append([y+1, x])
                elif g[y+1][x].islower():
                    kdist[g[y+1][x]] = c
                    expanded.append([y+1, x])

                if g[y][x-1] == '.' or g[y][x-1].isupper():
                    expanded.append([y, x-1])
                elif g[y][x-1].islower():
                    kdist[g[y][x-1]] = c
                    expanded.append([y, x-1])

                if g[y][x+1] == '.' or g[y][x+1].isupper():
                    expanded.append([y, x+1])
                elif g[y][x+1].islower():
                    kdist[g[y][x+1]] = c
                    expanded.append([y, x+1])

    if len(expanded) > 0:
        for p in expanded:
            g[p[0]][p[1]] = ','
        return [g, kdist, False]
    else:
        return [g, kdist, True]

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
                    o[g[y-1][x]] = c
                    g[y-1][x] = '!'

                if g[y+1][x] == '.':
                    expanded.append([y+1, x])
                elif g[y+1][x].islower():
                    o[g[y+1][x]] = c
                    g[y+1][x] = '!'

                if g[y][x-1] == '.':
                    expanded.append([y, x-1])
                elif g[y][x-1].islower():
                    o[g[y][x-1]] = c
                    g[y][x-1] = '!'

                if g[y][x+1] == '.':
                    expanded.append([y, x+1])
                elif g[y][x+1].islower():
                    o[g[y][x+1]] = c
                    g[y][x+1] = '!'

    if len(expanded) > 0:
        for p in expanded:
            g[p[0]][p[1]] = ','
        return [g, o, False]
    else:
        return [g, o, True]

def printGrid(g):
    for y in g:
        for x in g[y]:
            print(g[y][x], end='')
        print('')

if __name__ == "__main__":
    main()

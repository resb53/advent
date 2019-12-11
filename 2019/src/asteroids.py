#!/usr/bin/python3

import sys
import argparse
from math import degrees, atan2

# Check correct usage
parser = argparse.ArgumentParser(description="Asteroid effectiveness calculator.")
parser.add_argument('map', metavar='map', type=str, help='Asteroid map filename.')
args = parser.parse_args()

# Parse memory
try:
    map_fh = open(args.map,'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

def main():
    # Prepare map
    asteroids = []
    # Parse instructions in file. Allow for multiline just in case future need.
    for line in map_fh:
        line = line.rsplit()[0]
        asteroids.append(list(line))

    #print(asteroids)

    # Iterate through elements
    x=0
    y=0
    bestx=0
    besty=0
    maxast = 0

    for row in asteroids:
        for col in row:
            if isAsteroid(x,y,asteroids):
                astseen = seeAsteroids(x, y, asteroids)
                if astseen > maxast:
                    maxast = astseen
                    bestx = x
                    besty = y
            x += 1
        y += 1
        x = 0

    print(str(maxast) + ' at (' + str(bestx) + ',' + str(besty) + ')')

    # Part 2, shoot the things
    print("Commence firing...")
    shootAsteroids(bestx, besty, asteroids)

def shootAsteroids(x, y, grid):
    # Recaculate asteroids seen from this point
    seen = {}

    # Create list of relative positions to iterate through
    radial = radialIterator(x, y, grid)

    # Count asteroids seen
    for check in radial:
        if isAsteroid(x+check[0],y+check[1],grid):
            if check[2] not in seen:
                seen[check[2]] = ['(' + str(x+check[0]) + ',' + str(y+check[1]) + ')']
            else:
                seen[check[2]].append('(' + str(x+check[0]) + ',' + str(y+check[1]) + ')')

    # Starting at bearing 0.0, shoot one asteroid at a time in a clockwise direction. Report shooting.
    print(seen)
    shot = 1
    while len(seen) > 0:
        for angle in sorted(seen):
            hit = seen[angle].pop(0)
            print('Shot ' + str(shot) + ' hits ' + hit + '.')
            shot += 1
            # Cleanup
            if len(seen[angle]) == 0:
                del seen[angle]

def seeAsteroids(x, y, grid):
    # Work out radially from this point, blocking off routes as you see asteroid.
    count = 0
    seen = [] # asteroid blocking a direction

    # Create list of relative positions to iterate through
    radial = radialIterator(x, y, grid)

    # Count asteroids seen
    for check in radial:
        if isAsteroid(x+check[0],y+check[1],grid):
            if check[2] not in seen:
                count += 1
                seen.append(check[2])

    return count

def radialIterator(x, y, grid):
    # Return a radial list of relative locations to iterate through, and each position has an indicator as to what else is blocked
    dist = 1
    rad = []

    for dist in range(1,len(grid)+1): # This assumes at least a tall as it is wide!
        j = -dist # top row
        if y + j >= 0 and y + j < len(grid):
            for i in range(-dist,dist):
                if x + i >= 0 and x + i < len(grid[y]):
                    rad.append([i,j,bearing(i,j)])
        i = dist # right side
        if x + i >= 0 and x + i < len(grid[y]):
            for j in range(-dist,dist):
                if y + j >= 0 and y + j < len(grid):
                    rad.append([i,j,bearing(i,j)])
        j = dist # bottom
        if y + j >= 0 and y + j < len(grid):
            for i in range(dist,-dist,-1):
                if x + i >= 0 and x + i < len(grid[y]):
                    rad.append([i,j,bearing(i,j)])
        i = -dist # left side
        if x + i >= 0 and x + i < len(grid[y]):
            for j in range(dist,-dist,-1):
                if y + j >= 0 and y + j < len(grid):
                    rad.append([i,j,bearing(i,j)])

    return rad

def isAsteroid(x, y, grid):
    # Is this an asteroid?
    if grid[y][x] == '#':
        return 1
    else:
        return 0

def bearing(x, y):
    # Calculate bearing of point relative to (0,0) to 2 d.p.
    angle = degrees(atan2(y, x)) + 90
    if angle < 0:
        angle += 360
    elif angle >= 360:
        angle -= 360
    return round(angle,2)

if __name__ == "__main__":
    main()

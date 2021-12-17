#!/usr/bin/env python3

# target = {"x": (20, 30), "y": (-5, -10)}
target = {"x": (207, 263), "y": (-63, -115)}


# Find initial trajectory that ends in target
def calculateTrajectory():
    # (Max target y) - 1 initial velocity
    maxy = (target["y"][1] * -1) - 1
    posy = 0
    lasty = None
    while posy != lasty:
        lasty = posy
        posy += maxy
        maxy -= 1

    print(f"Solution to part 1: {posy}")


# Process what possible range of velocities to use
def calculateBounds():
    # Min velx must reach minx, do in reverse
    posx = 0
    velx = 0
    while posx < target["x"][0]:
        velx += 1
        posx += velx
    minx = velx
    maxx = target["x"][1]
    # Values for y:
    miny = target["y"][1]
    maxy = (target["y"][1] * -1) - 1

    return ((minx, maxx), (miny, maxy))


# See if launching a probe on these velocities will hit target area
def launchProbe(velx, vely):
    pos = [0, 0]
    hit = False

    while pos[1] >= target["y"][1]:
        pos[0] += velx
        pos[1] += vely
        if velx > 0:
            velx -= 1
        vely -= 1

        if (pos[0] >= target["x"][0]) and (pos[0] <= target["x"][1]):
            if (pos[1] <= target["y"][0]) and (pos[1] >= target["y"][1]):
                hit = True

    return hit


def main():
    # Part 1
    calculateTrajectory()

    # Part 2
    bounds = calculateBounds()
    hits = 0

    for x in range(bounds[0][0], bounds[0][1]+1):
        for y in range(bounds[1][0], bounds[1][1]+1):
            if launchProbe(x, y):
                hits += 1

    print(f"Solution to part 2: {hits}")


if __name__ == "__main__":
    main()

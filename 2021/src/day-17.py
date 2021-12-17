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


# Process harder
def calculateAll():
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

    return False


def main():
    # Part 1
    calculateTrajectory()

    # Part 2
    calculateAll()


if __name__ == "__main__":
    main()

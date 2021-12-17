#!/usr/bin/env python3

target = {"x": (20, 30), "y": (-5, -10)}
# target = {"x": (207, 263), "y": (-63, -115)}

answers = [(23,-10),
(25,-9),
(27,-5),
(29,-6),
(22,-6),
(21,-7),
(9,0),
(27,-7),
(24,-5),
(25,-7),
(26,-6),
(25,-5),
(6,8),
(11,-2),
(20,-5),
(29,-10),
(6,3),
(28,-7),
(8,0),
(30,-6),
(29,-8),
(20,-10),
(6,7),
(6,4),
(6,1),
(14,-4),
(21,-6),
(26,-10),
(7,-1),
(7,7),
(8,-1),
(21,-9),
(6,2),
(20,-7),
(30,-10),
(14,-3),
(20,-8),
(13,-2),
(7,3),
(28,-8),
(29,-9),
(15,-3),
(22,-5),
(26,-8),
(25,-8),
(25,-6),
(15,-4),
(9,-2),
(15,-2),
(12,-2),
(28,-9),
(12,-3),
(24,-6),
(23,-7),
(25,-10),
(7,8),
(11,-3),
(26,-7),
(7,1),
(23,-9),
(6,0),
(22,-10),
(27,-6),
(8,1),
(22,-8),
(13,-4),
(7,6),
(28,-6),
(11,-4),
(12,-4),
(26,-9),
(7,4),
(24,-10),
(23,-8),
(30,-8),
(7,0),
(9,-1),
(10,-1),
(26,-5),
(22,-9),
(6,5),
(7,5),
(23,-6),
(28,-10),
(10,-2),
(11,-1),
(20,-9),
(14,-2),
(29,-7),
(13,-3),
(23,-5),
(24,-8),
(27,-9),
(30,-7),
(28,-5),
(21,-10),
(7,9),
(6,6),
(21,-5),
(27,-10),
(7,2),
(30,-9),
(21,-8),
(22,-7),
(24,-9),
(20,-6),
(6,9),
(29,-5),
(8,-2),
(27,-8),
(30,-5),
(24,-7)]


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
    init = (velx, vely)
    pos = [0, 0]
    hit = False

    while pos[1] >= target["y"][1]:
        pos[0] += velx
        pos[1] += vely
        velx -= 1
        vely -= 1

        if (pos[0] >= target["x"][0]) and (pos[0] <= target["x"][1]):
            if (pos[1] <= target["y"][0]) and (pos[1] >= target["y"][1]):
                hit = True

    if hit:
        if init in answers:
            answers.remove(init)
        else:
            print(f"{init} not in answers")

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

    print(answers)

    print(f"Solution to part 2: {hits}")


if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bearing.")
parser.add_argument('input', metavar='input', type=str,
                    help='Sea navigation input.')
args = parser.parse_args()

navigation = []
pos = complex()  # positive real = E, positive imag = N
waypoint = 10 + 1j  # 10 E, 1 N, relative to ship
face = 0  # degrees = E
faceDir = {0: 'E', 90: 'N', 180: 'W', 270: 'S'}


def main():
    parseInput(args.input)

    # Part 1
    findPosition()
    print(pos)
    print(abs(pos.real) + abs(pos.imag))

    # Part 2
    moveViaWaypoint()
    print(pos)
    print(abs(pos.real) + abs(pos.imag))

    # Debug
    # printNavigation()


# Parse the input file
def parseInput(inp):
    global navigation
    try:
        navi_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in navi_fh:
        line = line.strip("\n")
        navigation.append((line[0], int(line[1:])))


# For each pass, identify its seat
def findPosition():
    global face
    # Move based on command
    for cmd, arg in navigation:
        if cmd == 'L':
            face = (face + arg) % 360
        elif cmd == 'R':
            face = (face - arg) % 360
        elif cmd == 'F':
            moveShip(faceDir[face], arg)
        else:
            moveShip(cmd, arg)


# Move ship based on cmd and arg
def moveShip(cmd, arg):
    global pos

    if cmd == 'N':
        pos = pos + arg * 1j
    elif cmd == 'S':
        pos = pos - arg * 1j
    elif cmd == 'E':
        pos = pos + arg
    elif cmd == 'W':
        pos = pos - arg
    else:
        sys.exit(f"Cannot follow move cmd: {cmd}")


# Move waypoint and move towards it
def moveViaWaypoint():
    global waypoint, pos

    # Reset
    pos = complex()
    # print(f"Pos:{pos}, Way:{waypoint}")

    for cmd, arg in navigation:
        # print(f"Cmd:{cmd}, Arg:{arg}")
        if cmd == 'N':
            waypoint = waypoint + arg * 1j
        elif cmd == 'S':
            waypoint = waypoint - arg * 1j
        elif cmd == 'E':
            waypoint = waypoint + arg
        elif cmd == 'W':
            waypoint = waypoint - arg
        elif cmd == 'L' or cmd == 'R':
            r = waypoint.real
            i = waypoint.imag

            if cmd == 'R':
                arg = 360 - arg

            arg = arg % 360

            if arg == 90:
                waypoint = -1 * i + r * 1j
            elif arg == 180:
                waypoint *= -1
            elif arg == 270:
                waypoint = i - r * 1j

        elif cmd == 'F':
            pos = pos + arg * waypoint

        # print(f"Pos:{pos}, Way:{waypoint}")


def printNavigation():
    for item in navigation:
        print(item)


if __name__ == "__main__":
    main()

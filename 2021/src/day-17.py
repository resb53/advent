#!/usr/bin/env python3

# target = {"x": (20, 30), "y": (-5, -10)}
target = {"x": (207, 263), "y": (-63, -115)}


# Find initial trajectory that ends in target
def calculateTrajectory():
    # (Max target y) - 1 initial velocity - calculate max height reached (y*(y+1)/2)
    maxy = (((target["y"][1] * -1) - 1) * (target["y"][1] * -1))/2
    print(f"Solution to part 1: {maxy}")


# Process harder
def calculateAll():
    # Min velx must reach minx

    return False


def main():
    # Part 1
    calculateTrajectory()

    # Part 2
    calculateAll()


if __name__ == "__main__":
    main()

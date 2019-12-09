#!/usr/bin/python3

import os
import sys
import argparse

# Check correct usage
parser = argparse.ArgumentParser(description="DSN image decoder.")
parser.add_argument('run', metavar='programme_file', type=str, help='Specify the program for the computer run.')
args = parser.parse_args()

# Parse input
try:
    instr_fh = open(args.run,'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

def main():
    # Parse values in input
    inp = instr_fh.readline().rsplit()[0]

    sequence = list(str(inp))
    image = {}
    layer = 0

    while len(sequence) > 0:
        layer += 1
        image[layer] = []
        # Per layer
        for x in range(6):
            image[layer].append([None] * 25)
            for y in range(25):
                image[layer][x][y] = sequence.pop(0)

    #print(image)

    #Find layer with fewest 0 digits
    #minzero = 25 * 6
    #minlayer = 0
    #for l in image:
    #    numzeros = 0
    #    for row in image[l]:
    #        for num in row:
    #            if num == '0':
    #                numzeros += 1
    #    #print('Layer: ' + str(l) + '; Numzeros: ' + str(numzeros))
    #    if numzeros < minzero:
    #        minzero = numzeros
    #        minlayer = l

    #Calculate number of 1 digits multiplied by the number of 2 digits
    #numones = 0
    #numtwos = 0
    #for row in image[minlayer]:
    #    for num in row:
    #        if num == '1':
    #            numones += 1
    #        elif num == '2':
    #            numtwos += 1
    #print(str(numones * numtwos))

    # Create image
    flatimage = []
    for x in range(6):
        flatimage.append([None] * 25)

    for l in image:
        for row in range(6):
            for col in range(25):
                if flatimage[row][col] is None and image[l][row][col] != '2':
                    flatimage[row][col] = image[l][row][col]

    print(flatimage)


if __name__ == "__main__":
    main()

#!/usr/bin/python3

import itertools
import os

def main():

    #Produce array of phases to test
    for phase in itertools.permutations(range(5), 5):
        stream = os.popen('echo "0" | ./src/intcode.py -p ' + str(phase[0]) + ' inputs/amplifier.txt | ./src/intcode.py -p ' + str(phase[1]) + ' inputs/amplifier.txt | ./src/intcode.py -p ' + str(phase[2]) + ' inputs/amplifier.txt | ./src/intcode.py -p ' + str(phase[3]) + ' inputs/amplifier.txt | ./src/intcode.py -p ' + str(phase[4]) + ' inputs/amplifier.txt')

        print(stream.read())

if __name__ == "__main__":
    main()

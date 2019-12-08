#!/usr/bin/python3

import itertools
from subprocess import Popen, PIPE

def main():

    #Produce array of phases to test
    for phase in itertools.permutations(range(5), 5):
        ampA = Popen(['./src/intcode.py', '-n', 'ampA', '-p', str(phase[0]), 'inputs/amplifier.txt'], stdin=PIPE, stdout=PIPE)
        ampB = Popen(['./src/intcode.py', '-n', 'ampB', '-p', str(phase[1]), 'inputs/amplifier.txt'], stdin=ampA.stdout, stdout=PIPE)
        ampC = Popen(['./src/intcode.py', '-n', 'ampC', '-p', str(phase[2]), 'inputs/amplifier.txt'], stdin=ampB.stdout, stdout=PIPE)
        ampD = Popen(['./src/intcode.py', '-n', 'ampD', '-p', str(phase[3]), 'inputs/amplifier.txt'], stdin=ampC.stdout, stdout=PIPE)
        ampE = Popen(['./src/intcode.py', '-n', 'ampE', '-p', str(phase[4]), 'inputs/amplifier.txt'], stdin=ampD.stdout, stdout=PIPE)

        ampA.stdin.write(str.encode("0\n"))
        ampA.stdin.flush()
        print(ampE.stdout.read().decode())

if __name__ == "__main__":
    main()

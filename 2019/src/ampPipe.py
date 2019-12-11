#!/usr/bin/python3

import argparse
import itertools
from subprocess import Popen, PIPE

# Check correct usage
parser = argparse.ArgumentParser(description="Amplifier optimiser program.")
parser.add_argument('-p', metavar='phase', type=int, help='Optionally specify the initial phase for the program. (Def=0)', default=0)
parser.add_argument('run', metavar='programme_file', type=str, help='Specify the program for the amplifier to run.')
args = parser.parse_args()

def main():

    #Produce array of phases to test
    for phase in itertools.permutations(range(args.p, args.p + 5), 5):
        ampA = Popen(['./src/intcode.py', '-n', 'ampA', '-p', str(phase[0]), args.run], stdin=PIPE, stdout=PIPE)
        ampB = Popen(['./src/intcode.py', '-n', 'ampB', '-p', str(phase[1]), args.run], stdin=ampA.stdout, stdout=PIPE)
        ampC = Popen(['./src/intcode.py', '-n', 'ampC', '-p', str(phase[2]), args.run], stdin=ampB.stdout, stdout=PIPE)
        ampD = Popen(['./src/intcode.py', '-n', 'ampD', '-p', str(phase[3]), args.run], stdin=ampC.stdout, stdout=PIPE)
        ampE = Popen(['./src/intcode.py', '-n', 'ampE', '-p', str(phase[4]), args.run], stdin=ampD.stdout, stdout=PIPE)

        ampA.stdin.write(str.encode("0\n"))
        ampA.stdin.flush()

        # This is really ugly. Need threading to add a delay? Or a better way to check when processes have ended
        while True:
            output = ampE.stdout.readline()
            if ampA.poll() == None:
                ampA.stdin.write(output)
                ampA.stdin.flush()
            else:
                print(output.decode())
                break

if __name__ == "__main__":
    main()

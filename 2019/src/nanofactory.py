#!/usr/bin/python3

import sys
import argparse

# Globals
menu = {}

def main():
    # Check correct usage
    parser = argparse.ArgumentParser(description="Nanofactory material calculator.")
    parser.add_argument('ingredients', metavar='ingredients_file', type=str, help='Specify the ingredients for the recipe.')
    args = parser.parse_args()

    init(args.ingredients)
    # Menu ready
    print(menu)
    calculateOre()


def init(fh):
    global menu
    # Parse memory
    try:
        instr_fh = open(fh,'r')
    except IOError:
        sys.exit("Unable to open input file: " + fh)

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        line = line.strip('\n')

        # Parse line
        mats, result = line.split(' => ')
        qr, result = result.split(' ')

        mix = {}
        for mat in mats.split(', '):
            qm, mat = mat.split(' ')
            mix[mat] = int(qm)

        menu[result] = [int(qr), mix]

def calculateOre():
    global menu
    # Count numbers required
    shoplist = {'FUEL': 1}
    leftover = {} # Remaining components

    #Get 1 FUEL
    while list(shoplist.keys()) != ['ORE']:
        print('S:' + str(shoplist))
        newlist = {}
        for item in shoplist:
            if item == 'ORE':
                newlist[item] = shoplist[item]
            print(item)
            for ing in menu[item][1]:
                print('<' + ing)
                # Get most efficient production from menu
                [prod, used] = getReq(shoplist[item], menu[item][1][ing], menu[item][0])
                print('Use: ' + str(used) + ' to make ' + str(prod))
                # Update lists
                if ing in newlist:
                    newlist[ing] += used
                else:
                    newlist[ing] = used
                # Use leftovers first
                if ing in leftover:
                    if leftover[ing] < newlist[ing]:
                        newlist[ing] -= leftover[ing]
                    else:
                        del(newlist[ing])
                        leftover[ing] -= newlist[ing]
                # Calculate leftovers
                if prod > shoplist[item]:
                    if item in leftover:
                        leftover[item] += prod - shoplist[item]
                    else:
                        leftover[item] = prod - shoplist[item]

        shoplist = newlist
        print('L:' + str(leftover))

    print(shoplist)

def getReq(req, need, prod):
    print('Req: ' + str(req) + '; Need: ' + str(need) + '; Prod: ' + str(prod))
    used = 0
    done = 0
    while done < req:
        used += need
        done += prod
    return [done, used]

if __name__ == "__main__":
    main()

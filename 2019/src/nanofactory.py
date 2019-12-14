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
    recipe = [] # Production recipe to follow
    leftover = {} # Remaining components
    ore = 0 # Ore required
    #Get 1 FUEL
    while len(shoplist) > 0:
        #print('S:' + str(shoplist))
        newlist = {}
        for item in shoplist:
            #print(item)
            prod = 0 # items made of this
            # Build recipt
            recipe.insert(0,[item, shoplist[item]])
            # See if we have any already
            if item in leftover:
                if leftover[item] >= shoplist[item]:
                    leftover[item] -= shoplist[item]
                    shoplist[item] = 0
                else:
                    shoplist[item] -= leftover[item]
                    leftover[item] = 0
                #print('Used leftovers - ' + 'Req: ' + str(shoplist[item]) + 'Left: ' + str(leftover[item]))
            if shoplist[item] > 0:
                for ing in menu[item][1]:
                    #print('<' + ing)
                    # Check for any leftovers
                    avail = 0
                    if ing in leftover:
                        avail = leftover[ing]
                    # Get most efficient production from menu
                    [prod, req, left] = getReq(shoplist[item], menu[item][1][ing], menu[item][0], avail)
                    if ing in leftover:
                        leftover[ing] = left
                    # Update lists
                    if ing == 'ORE':
                        ore += req
                    else:
                        if req > 0:
                            if ing in newlist:
                                newlist[ing] += req
                            else:
                                newlist[ing] = req
                # Calculate leftovers
                if prod > shoplist[item]:
                    if item in leftover:
                        leftover[item] += prod - shoplist[item]
                    else:
                        leftover[item] = prod - shoplist[item]
        shoplist = newlist
        #print('L:' + str(leftover))

    print('ORE required: ' + str(ore))
    # print recipe
    for entry in recipe:
        if entry[0] in leftover:
            entry[1] += leftover[entry[0]]
        print('Produce ' + str(entry[1]) + ' of ' + entry[0] + '.')
    print('Leftovers: ' + str(leftover))


def getReq(req, need, prod, avail):
    #print('Req: ' + str(req) + '; Need: ' + str(need) + '; Prod: ' + str(prod) + '; Avail: ' + str(avail))
    used = 0
    done = 0
    while done < req:
        used += need
        done += prod
    new = 0
    if used >= avail:
        new = used - avail
        avail = 0
    else:
        avail -= used

    #print('Use: ' + str(used) + ' to make ' + str(done) + '. Require: ' + str(new) + ' new and ' + str(avail) + ' leftover.')

    return [done, new, avail]

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import string
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    startingpos = []

    for line in input_fh:
        letters = re.findall("[A-Z]", line.strip("\n"))
        if len(letters) > 0:
            startingpos.extend(letters)

    return startingpos


# Create grid
def buildGrid(setup):
    G = nx.Graph()
    G.add_nodes_from(string.ascii_lowercase[0:15], occupied=False, occupant=None)
    '''
    #############
    #ab.c.d.e.fg#
    ###h#i#j#k###
      #l#m#n#o#
      #########
    '''
    G.add_edge("a", "b", weight=1)
    G.add_edge("b", "c", weight=2)
    G.add_edge("c", "d", weight=2)
    G.add_edge("d", "e", weight=2)
    G.add_edge("e", "f", weight=2)
    G.add_edge("f", "g", weight=1)
    G.add_edge("b", "h", weight=2)
    G.add_edge("c", "h", weight=2)
    G.add_edge("c", "i", weight=2)
    G.add_edge("d", "i", weight=2)
    G.add_edge("d", "j", weight=2)
    G.add_edge("e", "j", weight=2)
    G.add_edge("e", "k", weight=2)
    G.add_edge("f", "k", weight=2)
    G.add_edge("h", "l", weight=1)
    G.add_edge("i", "m", weight=1)
    G.add_edge("j", "n", weight=1)
    G.add_edge("k", "o", weight=1)

    # distances = nx.all_pairs_dijkstra_path_length(G)
    # for node1 in distances:
    #     for node2 in node1[1]:
    #         print(f"{node1[0]} to {node2}: {node1[1][node2]}")

    attrs = {
        "h": {"occupied": True, "occupant": setup[0]},
        "i": {"occupied": True, "occupant": setup[1]},
        "j": {"occupied": True, "occupant": setup[2]},
        "k": {"occupied": True, "occupant": setup[3]},
        "l": {"occupied": True, "occupant": setup[4]},
        "m": {"occupied": True, "occupant": setup[5]},
        "n": {"occupied": True, "occupant": setup[6]},
        "o": {"occupied": True, "occupant": setup[7]}
    }

    nx.set_node_attributes(G, attrs)

    for node in G.nodes:
        print(f"{node}: {G.nodes[node]}")

    return G


def main():
    setup = parseInput(args.input)
    G = buildGrid(setup)

    # Part 1


if __name__ == "__main__":
    main()

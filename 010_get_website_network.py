#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

# IMPORTS
import csv
import itertools
import networkx as nx
from networkx.drawing.nx_agraph import pygraphviz_layout

if __name__ == '__main__':

# VARIABLES
    infolder = "./networks"
    outfolder = "./Website/networks"

    networks = ['CRM'] # IDs of networks we are looking at
    layoutprog = "neato"   # sfdp gives more stretched out layout

    SCALE = 10

# CODE
    for network in networks:
        infile = "{}/{}_network.gexf".format(infolder, network)

        # Read in
        G = nx.read_gexf(infile) # Name lost?
        H = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0] # get giant component

        # Calculate node positions and centralities
        node_positions = pygraphviz_layout(H, prog=layoutprog) # See https://networkx.github.io/documentation/latest/reference/drawing.html#layout
        node_betweenness = nx.betweenness_centrality(H) # See https://networkx.github.io/documentation/latest/reference/algorithms.centrality.html
        i = 1
        for node, data in H.nodes_iter(data=True): # add IDs and scale
            data["id"] = i
            i += 1
            data["x"], data["y"] = tuple(x*SCALE for x in node_positions[node])
            data["betweenness"] = node_betweenness[node]

        # GRAPH VISUALIZATION
        # Generate JS
        nodes = {}
        # nodes for 'function'; groupnumber for groupvalue
        nodes['f'] = ['{id:%d,label:"%s",group:"%s",title:"%s<br></br>%s",x:%s,y:%s,value:0.5}'
            % (data["id"], data['label'], data["group"], data['label'], data["meta"], data["x"], data["y"])
            for node, data in H.nodes(data=True)]
        # nodes for 'betweenness'; betweenness as groupvalue
        nodes['b'] = ['{id:%d,label:"%s",group:%s,title:"%s<br></br>%s",x:%s,y:%s,value:1}'
            % (data["id"], data['label'], data["betweenness"], data['label'], data["meta"], data["x"], data["y"])
            for node, data in H.nodes(data=True)]
        connections = [u'{from:%d,to:%d}' % (H.node[source]["id"], H.node[target]["id"])
                  for source, target in H.edges()]

        # Write out JS
        for color in ["function", "betweenness"]:
            outfile = "{}/network-{}_{}.js".format(outfolder, network, color)
            out_text = u'var nodes=[{}];\nvar edges=[{}];'.format(','.join(nodes[color[0]]), ','.join(connections))
            with open(outfile, 'w') as ouf:
                ouf.write(out_text.encode('utf-8'))
                print "{} sucessfully saved".format(outfile)

        # RING VISUALIZATION
        # Generate JS and write out
        connections = [u'{"source":"%s","target":"%s"}' % (H.node[source]["label"], H.node[target]["label"])
                  for source, target in H.edges()]
        out_text = u'var connections = [{}]'.format(','.join(connections))
        outfile = "{}/network-{}_ring.js".format(outfolder, network)
        with open(outfile, 'w') as ouf:
            ouf.write(out_text.encode('utf-8'))
            print "{} sucessfully saved".format(outfile)

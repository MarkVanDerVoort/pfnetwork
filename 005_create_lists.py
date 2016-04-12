#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

# IMPORTS
import csv
import itertools, operator
import networkx as nx
from collections import OrderedDict

# METHODS
def return_ranking_dict(d):
    """
    Returns a dictionary with ranks as value based on another dictionary's values.
    """
    res = {}
    prev = None
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    for i, (node,v) in enumerate(sorted_d):
        if v != prev:
            rank, prev = i + 1, v
        res[node] = rank
    return res


if __name__ == '__main__':

# VARIABLES
    infile = "./networks/CRM_network.gexf"
    outfile = "./lists/most_central_in_2014.csv"

# CODE
    H = nx.read_gexf(infile)
    G = sorted(nx.connected_component_subgraphs(H), key=len, reverse=True)[0] # get giant component

    betweenness = nx.betweenness_centrality(G)
    betweenness_rank = return_ranking_dict(betweenness)

    eigenvector = nx.eigenvector_centrality_numpy(G)
    eigenvector_rank = return_ranking_dict(eigenvector)

    clustering = nx.clustering(H)

    for node, data in H.nodes(data=True):
        if clustering[node] == 0.0: # Some nodes are islands
            data["clustering"] = 'NA'
        else:
            data["clustering"] = round(clustering[node], 3)
        if node in G: # Centrality only for the giant component
            data["betweenness"] = betweenness_rank[node]
            data["eigenvector"] = eigenvector_rank[node]
        else:
            data["betweenness"] = 'NA'
            data["eigenvector"] = 'NA'

    outdict = {data['label']:
               OrderedDict([('ID', node), ('Clustering', data['clustering']), ('Rank (Betweenness centr.)', data['betweenness']),
                            ('Rank (Eigenvector centr.)', data['eigenvector']),
                            ('Fonds en functies', data['meta'].replace('Pensionfonds: ', '').replace('<br>', '\n'))])
               for node, data in H.nodes(data=True)}

# WRITE OUT
    fields = ['Naam'] + outdict.values()[0].keys()
    with open(outfile, 'wb') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for k in outdict:
            w.writerow({field: outdict[k].get(field) or k.encode('utf-8') for field in fields})

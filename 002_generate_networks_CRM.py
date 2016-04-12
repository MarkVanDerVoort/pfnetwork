#!/usr/bin/env python2.7
# coding: utf-8 -*-

__author__="""Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

# IMPORTS
import io, csv
import itertools
import networkx as nx

# METHODS
def csv_to_nested_dict(filename, keyword):
    """
    Reads a csv as a dictionary of dictionaries, where keys are set in a flexible manner.
    Returns a nested dictionary with capital letter keys.
    """
    aDict = {}
    with open(filename, 'rb') as fin:
        csvDialect = csv.Sniffer().sniff(fin.readline())
        fin.seek(0)
        csvReader = csv.DictReader(fin, dialect=csvDialect)
        for row in csvReader:
            key = row.pop(keyword)
            aDict[key] = row
    return aDict


def add_attributes_to(network, aList, attr_dict, sep='<br />'):
    """
    Appends attributes from attribute dictionary to nodes or edges.
    Expects a list of tuples of strings or strings.
    """
    not_append = ['label', 'id']

    if not isinstance(aList, list):
        raise TypeError('{} not a list'.format(aList))

    for entry in aList:
        if isinstance(entry, tuple): # edges
            d = network.edge[entry[0]][entry[1]]
        elif isinstance(entry, str) or isinstance(entry, unicode): # nodes
            d = network.node[entry.encode('utf-8').decode('utf-8')]
        else:
            raise TypeError('{} must be either list of edges (tuples) or of nodes (strings)'.format(aList))

        for datakey, value in attr_dict.iteritems():
            if datakey in d.keys() and datakey not in not_append:
                if datakey == "group": # take the smaller
                    d[datakey] = min(d[datakey], value)
                else:
                    d[datakey] += sep + value # append
            else:
                d[datakey] = value # create


if __name__ == '__main__':

# VARIABLES
    infolder = "./rawdata"
    outfolder = "./networks"

    G = nx.Graph(name="Dutch pensionsfonds network in 2014")

# READ IN
    infile = "{}/Personenfuncties_bij_pensioenfondsen.csv".format(infolder)
    outfile = "{}/CRM_network.gexf".format(outfolder)

    sourcedict = csv_to_nested_dict(infile, 'ID')

# CLEAN SOURCEDICT
    replacment_mapping = {'Bestuurder PF': 'Bestuurder', 'LidVoorzitter': 'Lid Raad van Toezicht',
                          'Voorzitter PF': 'Bestuursvoorzitter'}
    function_group_mapping = {'Accountant': 1, 'Actuaris': 1,
                              'Bestuurder': 2, 'Bestuursvoorzitter': 2, 'Mede-beleidsbepaler': 2,
                              'Lid Raad van Toezicht': 3, 'Voorzitter Raad van Toezicht': 3}
    for data in sourcedict.values():
        data['Rol'] = replacment_mapping[data['Rol']] if data['Rol'] in replacment_mapping else data['Rol']
        data['group'] = function_group_mapping[data['Rol']]

# GENERATE NETWORK
    groups = {}
    for line, data in sourcedict.iteritems(): # Add nodes with data to network and sort nodes by common funds

            name_id = data['Relatienummer persoon']
            fonds = data['Naam pensioenfonds']
            current_number = data['Relatienummer pensioenfonds']
            if current_number in groups:
                groups[current_number].append(name_id)
            else:
                groups[current_number] = [name_id]
            G.add_node(name_id)
            node_data = {'function': data['Rol'], 'id': data['Relatienummer persoon'],
                         'label': unicode(data['Naam persoon'], 'utf8'), 'group': data['group'],
                         'meta': "Pensionfonds: {} ({}) - {}".format(data['Naam pensioenfonds'], current_number, data['Rol'])}
            add_attributes_to(G, [name_id], node_data)

    for group, nodes in groups.iteritems(): # Add links between nodes in the same fonds and some data
        edges = list(itertools.combinations([node for node in nodes], 2))
        G.add_edges_from(edges)
        edge_data = {'fonds_number': group}
        add_attributes_to(G, edges, edge_data)

# WRITE OUT
    nx.write_gexf(G, outfile)
    print ">>> {} sucessfully saved - Info:".format(outfile)
    print nx.info(G)

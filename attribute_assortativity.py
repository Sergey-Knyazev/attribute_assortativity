#!/usr/bin/env python3

"""Calculates attribute assortativity coefficients for graphs
"""

import argparse
import networkx as nx
import csv

__author__ = "Sergey Knyazev"
__credits__ = ["Sergey Knyazev, Ellsworth Campbell"]
__email__ = "sergey.n.knyazev@gmail.com"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculates attribute assortativity coefficients for graphs.')
    parser.add_argument('attributes', metavar='A', type=str, nargs='+', help='attribute for assortativity calculation')
    parser.add_argument('-n', '--nodes', required=True, type=str, dest='node_csv',
                        help='list of nodes with attributes in csv format. The first column should be a node name')
    parser.add_argument('-e', '--edges', required=True, type=str, dest='edge_csv',
                        help='list of edges in csv format. The first two columns should be source ant target names')
    parser.add_argument('-o', '--out_csv', required=True, type=str, dest='out_csv',
                        help='name of output csv file')
    return parser.parse_args()


def parse_nodes(node_csv):
    nodes = dict()
    with open(node_csv) as csvfile:
        node_reader = csv.DictReader(csvfile)
        n = next(node_reader)
        attrs = list(n.keys())
        for n in node_reader:
            node_name = n[attrs[0]]
            nodes[node_name] = dict()
            for attr in attrs[1:]:
                nodes[node_name][attr] = n[attr]
    return nodes


def parse_edges(edge_csv):
    edges = list()
    with open(edge_csv) as csvfile:
        edge_reader = csv.DictReader(csvfile)
        n = next(edge_reader)
        attrs = list(n.keys())
        for n in edge_reader:
            source_name = n[attrs[0]]
            target_name = n[attrs[1]]
            edges.append((source_name, target_name))
    return edges

if __name__ == "__main__":
    args = parse_arguments()
    G = nx.Graph()
    G.add_nodes_from(parse_nodes(args.node_csv).items())
    G.add_edges_from(parse_edges(args.edge_csv))
    with open(args.out_csv, 'w') as f:
        f.write('attribute, assortativity\n')
        for attr in args.attributes:
            f.write("{},{}\n".format(attr, nx.attribute_assortativity_coefficient(G, attr)))

"""
Data structure visualizer.
"""

import jgraph
import util.serializer as serializer

def draw_garph_3d(node):
    nodes = serializer.graph_to_nodes_set(node)
    edges = []
    for node in nodes:
        for neighbor in node.neighbors:
            edges.append((str(node.uuid), str(neighbor.uuid)))
    jgraph.draw(edges)

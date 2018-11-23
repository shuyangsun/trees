"""
Graph node.
"""

import copy
import uuid

class GraphNodeUniDirection:
    """
    A uni-directional graph node class.
    """

    def __init__(self, content=None):
        self._uuid = uuid.uuid1()
        self._content = content
        self._adjacent = dict()

    @property
    def uuid(self):
        return self._uuid

    @property
    def content(self):
        return self._content

    @property
    def neighbors(self):
        return set(self._adjacent.keys())

    @property
    def edge_weights(self):
        return copy.copy(self._adjacent)

    def is_neighbor(self, node):
        return node in self._adjacent

    def get_weight(self, neighbor):
        if not self.is_neighbor(neighbor):
            raise ValueError('Not a neighbor.')
        return self._adjacent[neighbor]

    def add_neighbor_unidirection(self, neighbor, edge_weight_out=1):
        if self.is_neighbor(neighbor):
            raise ValueError('Neighbor already in graph.')
        self._adjacent[neighbor] = edge_weight_out

    def remove_neighbor_unidirection(self, neighbor):
        self._adjacent.pop(neighbor, None)

    def __hash__(self):
        return self.uuid.__hash__()

    def __eq__(self, rhs):
        if rhs is None or not isinstance(rhs, GraphNodeUniDirection):
            return False
        return self.uuid == rhs.uuid


class GraphNodeBiDirection(GraphNodeUniDirection):
    """
    A bi-directional graph node class.
    """

    def add_neighbor_bidirection(self, neighbor, edge_weight_out=1, edge_weight_in=1):
        if neighbor == self:
            self.add_neighbor_unidirection(self, edge_weight_out)
        self.add_neighbor_unidirection(neighbor, edge_weight_out)
        neighbor.add_neighbor_unidirection(self, edge_weight_in)

    def remove_neighbor_bidirection(self, neighbor):
        self.remove_neighbor_unidirection(neighbor)
        neighbor.remove_neighbor_unidirection(self)

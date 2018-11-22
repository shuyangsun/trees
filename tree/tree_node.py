"""
Any kind of tree node.
"""

from tree.graph_node import GraphNodeBiDirection


class TreeNode(GraphNodeBiDirection):
    def __init__(self, content=None):
        super().__init__(content)
        self._height = 0

    @property
    def children(self):
        neighbors = self.neighbors
        for neighbor in neighbors:
            if self.get_weight(neighbor) == -1:
                neighbors.remove(neighbor)
        return neighbors

    @property
    def parent(self):
        neighbors = self.neighbors
        for neighbor in neighbors:
            if self.get_weight(neighbor) == -1:
                return neighbor
        return None

    @property
    def is_leaf(self):
        return not self.children
    
    @property
    def height(self):
        return self._height

    def add_child(self, child):
        if self.is_neighbor(child):
            raise ValueError('Child already exist.')
        self.add_neighbor_bidirection(child, edge_weight_out=1, edge_weight_in=-1)
        new_height = max(self._height, child.height + 1)
        if new_height != self._height:
            self._update_height(new_height)

    def remove_child(self, child):
        if not self.is_neighbor(child):
            return
        self.remove_neighbor_unidirection(child)
        new_height = 0
        for node in self.children:
            new_height = max(new_height, node.height + 1)
        if new_height != self._height:
            self._update_height(new_height)

    def _update_height(self, new_height):
        cur = self
        while cur is not None:
            cur._height = max(cur.height, new_height)
            cur = cur.parent
            new_height += 1

class BinaryTreeNode(TreeNode):
    def __init__(self, content=None):
        super().__init__(content)
        self._left = None
        self._right = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        if node is None:
            self.remove_child(self._left)
        else:
            self.left = None
            self.add_child(node)
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        if node is None:
            self.remove_child(self._right)
        else:
            self.right = None
            self.add_child(node)
        self._right = node

    @property
    def has_left(self):
        return self.left is not None

    @property
    def has_right(self):
        return self.right is not None
    
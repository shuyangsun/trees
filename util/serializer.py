"""
Serialize datastructure.
"""

from tree.tree_node import BinaryTreeNode

def graph_to_nodes_set(node):
    res = set()
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur not in res:
            res.add(cur)
        neighbors = cur.neighbors
        for neighbor in neighbors:
            if neighbor not in res:
                stack.append(neighbor)
    return res


def binary_tree_to_arr(root):
    res = []
    s = []
    def __tree2arr(node, depth, path, res):
        if node is None:
            return
        capacity = 2 ** (depth + 1) - 1
        if len(res) < capacity:
            diff = capacity - len(res)
            res += [None] * diff
        starting_idx = 2 ** depth - 1
        res[starting_idx + path] = node
        __tree2arr(node.left, depth + 1, path << 1, res)
        __tree2arr(node.right, depth + 1, (path << 1) + 1, res)

    __tree2arr(root, 0, 0, res)
    return res


def arr_to_binary_tree(self, arr):
        if not arr:
            return None
        root = BinaryTreeNode(arr[0])
        s = [(root, 0)]
        while s:
            cur, idx = s.pop()
            left = 2 * idx + 1
            right = 2 * idx + 2            
            if left < len(arr) and arr[left]:
                cur.left = BinaryTreeNode(arr[left])
                s.append((cur.left, left))
            if right < len(arr) and arr[right]:
                cur.right = BinaryTreeNode(arr[right])
                s.append((cur.right, right))
        return root

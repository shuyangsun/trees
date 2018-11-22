"""
Serialize datastructure.
"""

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

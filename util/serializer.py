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

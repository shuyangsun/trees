"""
"""

from collections import deque
from tree.tree_node import BinaryTreeNode

def insert_bst(root, node, cmp_lt=lambda lhs, rhs: lhs.content < rhs.content, cmp_gt=lambda lhs, rhs: lhs.content > rhs.content):
    if not isinstance(node, BinaryTreeNode):
        insert_bst(root, BinaryTreeNode(node), cmp_lt, cmp_gt)
        return
    if root == node:
        raise ValueError('Node already exist in the tree.')
    cur = root
    while True:
        if cmp_lt(node, cur):
            if cur.has_left:
                cur = cur.left
                continue
            else:
                cur.left = node
                return
        elif cmp_gt(node, cur):
            if cur.has_right:
                cur = cur.right
                continue
            else:
                cur.right = node
                return
        else:
            return


def get_height(root):
    res = -1
    if root is None:
        return res
    q = deque([root])
    while q:
        res += 1
        cur = []
        while q:
            cur.append(q.popleft())
        for node in cur:
            if node.has_left:
                q.append(node.left)
            if node.has_right:
                q.append(node.right)
    return res

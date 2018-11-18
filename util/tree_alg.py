"""
"""

from tree.tree_node import BinaryTreeNode

def insert_bst(root, node, cmp=lambda lhs, rhs: lhs.content < rhs.content):
    if not isinstance(node, BinaryTreeNode):
        insert_bst(root, BinaryTreeNode(node), cmp)
        return
    if root == node:
        raise ValueError('Node already exist in the tree.')
    cur = root
    while True:
        if cmp(node, cur):
            if cur.left is None:
                cur.left = node
                return
            else:
               cur = cur.left
               continue
        else:
            if cur.right is None:
                cur.right = node
                return
            else:
               cur = cur.right
               continue

"""
"""


from tree.tree_node import BinaryTreeNode


def insert_bst(
        root, node,
        balance='avl',
        cmp_lt=lambda lhs, rhs: lhs.content < rhs.content,
        cmp_gt=lambda lhs, rhs: lhs.content > rhs.content
    ):
    if balance is None:
        __insert_bst_lazy(root, node, cmp_lt, cmp_gt)
    elif balance == 'avl':
        __insert_bst_avl(root, node, cmp_lt, cmp_gt)
    else:
        raise ValueError('Unrecognized balancing algorithm.')


def __insert_bst_avl(root, node, cmp_lt, cmp_gt):
    node = __insert_bst_lazy(root, node, cmp_lt, cmp_gt)
    if node is None:
        return
    unbalanced, child, grand_child = __first_unbalanced_ancestor(node)
    if unbalanced is None:
        return
    assert(child is not None)
    assert(grand_child is not None)
    is_child_left = (unbalanced.has_left and unbalanced.left == child)
    is_grand_child_left = (child.has_left and child.left == grand_child)
    scenario = (is_child_left, is_grand_child_left)
    if scenario == (True, True):
        __rotate_right(unbalanced)
    elif scenario == (True, False):
        __rotate_left(child)
        __rotate_right(unbalanced)
    elif scenario == (False, True):
        __rotate_right(child)
        __rotate_left(unbalanced)
    else:
        __rotate_left(unbalanced)


def __insert_bst_lazy(root, node, cmp_lt, cmp_gt):
    if not isinstance(node, BinaryTreeNode):
        node = BinaryTreeNode(node)
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
                return node
        elif cmp_gt(node, cur):
            if cur.has_right:
                cur = cur.right
                continue
            else:
                cur.right = node
                return node
        else:
            return None


def __first_unbalanced_ancestor(node):
    if node is None or not node.has_parent or not node.parent.has_parent:
        return None, None, None
    grand_child = node
    child = node.parent
    cur = node.parent.parent
    cur_left_height = -1 if not cur.has_left else cur.left.height
    cur_right_height = -1 if not cur.has_right else cur.right.height
    while cur is not None and abs(cur_left_height - cur_right_height) <= 1:
        grand_child = child
        child = cur
        cur = cur.parent
        if cur is not None:
            cur_left_height = -1 if not cur.has_left else cur.left.height
            cur_right_height = -1 if not cur.has_right else cur.right.height
    return cur, child, grand_child


def __rotate_left(node):
    if not node.has_parent or not node.has_right:
        return
    parent = node.parent
    is_left = None
    if parent is not None:
        is_left = parent.left == node
        if is_left:
            parent.left = None
        else:
            parent.right = None
    r = node.right
    rl = r.left
    r.left = None
    node.right = rl
    r.left = node
    if parent is not None:
        if is_left:
            parent.left = r
        else:
            parent.right = r


def __rotate_right(node):
    if node.left is None:
        return
    parent = node.parent
    is_left = None
    if parent is not None:
        is_left = parent.left == node
        if is_left:
            parent.left = None
        else:
            parent.right = None
    l = node.left
    lr = l.right
    l.right = None
    node.left = lr
    l.right = node
    if parent is not None:
        if is_left:
            parent.left = l
        else:
            parent.right = l

"""
Data structure visualizer.
"""

import jgraph
import math
import plotly.graph_objs as go
import util.serializer as serializer

from plotly.offline import iplot, init_notebook_mode


# ------------------------------------------------------- Graph --------------------------------------------------------


def draw_garph_3d(node):
    """
    Draw uni-directional or bi-directional graph in 3D space.
    """
    nodes = serializer.graph_to_nodes_set(node)
    edges = []
    for node in nodes:
        for neighbor in node.neighbors:
            edges.append((str(node.uuid), str(neighbor.uuid)))
    jgraph.draw(edges)


# ---------------------------------------------------- Binary Tree -----------------------------------------------------


def draw_binary_tree(
        root,
        title=None,
        node_color='#6175c1',
        node_opacity=1,
        line_color='#aaaaaa',
        node_label_format_func=lambda node: str(node.content),
        # TODO: find a way to customize hover text.
        # hover_text_format_func=lambda node: 'uuid: {0}\ncontent: {1}'.format(node.uuid, node.content),
        sibling_spacing=18, single_depth_height=18, node_size=18
    ):
    init_notebook_mode(connected=False)
    nodes_lst = serializer.binary_tree_to_arr(root)
    nodes_lst_no_none = [ele for ele in nodes_lst if ele is not None]
    labels = [node_label_format_func(ele) for ele in nodes_lst_no_none]
    labels_dict = {ele: node_label_format_func(ele) for ele in nodes_lst_no_none}
    tree_height = root.height
    x_pos = __create_x_pos_btree(sibling_spacing, tree_height)
    y_pos = __create_y_pos_btree(single_depth_height, tree_height)
    x_pos = [ele for idx, ele in enumerate(x_pos) if nodes_lst[idx] is not None]
    y_pos = [ele for idx, ele in enumerate(y_pos) if nodes_lst[idx] is not None]
    position = {ele: (x_pos[idx], y_pos[idx]) for idx, ele in enumerate(nodes_lst_no_none)}
    E = __create_edges_btree(root)

    xn = [x_pos[idx] for idx, ele in enumerate(nodes_lst_no_none)]
    yn = [y_pos[idx] for idx, ele in enumerate(nodes_lst_no_none)]
    xe, ye = [], []
    for edge in E:
        xe += [position[edge[0]][0], position[edge[1]][0], None]
        ye += [position[edge[0]][1], position[edge[1]][1], None]

    lines = go.Scatter(
        x=xe, y=ye, mode='lines', line=dict(color=line_color, width=1), hoverinfo='none'
    )
    dots = go.Scatter(
        x=xn, y=yn, mode='markers', name='',
        marker=dict(
            symbol='circle', size=18, color=node_color, line=dict(color='rgb(50,50,50)', width=1)
        ),
        text=labels, opacity=node_opacity, hoverinfo='none'
    )

    axis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=False)

    layout = dict(
        title=title, annotations=__make_annotations(position, labels_dict),
        font=dict(size=12), showlegend=False, xaxis=go.layout.XAxis(axis), yaxis=go.layout.YAxis(axis),          
        margin=dict(l=40, r=40, b=85, t=100), hovermode='closest', plot_bgcolor='rgb(248,248,248)'          
    )

    fig = dict(data=[lines, dots], layout=layout)
    fig['layout'].update(annotations=__make_annotations(position, labels_dict))
    iplot(fig, filename='binary_tree_plot')


# ------------------------------------------------------ Helper --------------------------------------------------------


def __create_x_pos_btree(space, tree_height):
    res = [None] * (2 ** (tree_height + 1) - 1)
    last_level_node_count = 2 ** tree_height
    res[-last_level_node_count:] = [ele * space for ele in range(last_level_node_count)]
    right = len(res) - last_level_node_count
    cur_level_len = last_level_node_count // 2
    left = right - cur_level_len
    while cur_level_len > 0:
        for i in range(cur_level_len):
            xl, xr = res[right + 2 * i], res[right + 2 * i + 1]
            res[left + i] = xl + (xr - xl) / 2
        cur_level_len //= 2
        right = left
        left = right - cur_level_len
    return res


def __create_y_pos_btree(space, tree_height):
    res = []
    for i in range(tree_height + 1):
        res += [tree_height * space - i * space] * 2 ** i
    return res


def __create_edges_btree(root):
    res = []
    s = [root]
    while s:
        cur = s.pop()
        if cur.left is not None:
            res.append((cur, cur.left))
            s.append(cur.left)
        if cur.right is not None:
            res.append((cur, cur.right))
            s.append(cur.right)
    return res


def __make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    if len(text) != len(pos):
        raise ValueError('The lists pos and text must have the same length.')
    annotations = []
    for ele in pos.keys():
        annotations.append(go.layout.Annotation(
            text=text[ele], 
            x=pos[ele][0],
            y=pos[ele][1],
            xref='x1',
            yref='y1',
            font=dict(color=font_color, size=font_size),
            showarrow=False
        ))
    return annotations


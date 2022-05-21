"""
This module contains helper functions related to 2D triangles, used for the algorithm and related visualizations.
"""
import math
import networkx as nx


def point_in_triangle(
    pt:tuple, p1:tuple, p2:tuple, p3:tuple
) -> bool:
    """Checks if point pt is included in the triangle/3-clique spanned by points/nodes p1, p2 and p3.

    Args:
        pt (tuple): Point (x, y) to be checked.
        p1 (tuple): First point/node (x, y) of the triangle/3-clique.
        p2 (tuple): Second point/node (x, y) of the triangle/3-clique.
        p3 (tuple): Third point/node (x, y) of the triangle/3-clique.

    Returns:
        bool: True if point pt is within the triangle, False if not
    """
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(pt, p1, p2)
    d2 = sign(pt, p2, p3)
    d3 = sign(pt, p3, p1)

    neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (neg and pos)


def get_circumcircle(
    p1:tuple, p2:tuple, p3:tuple
) -> tuple:
    """Calculates the circumcircle of the triangle/3-clique spanned by points/nodes p1, p2 and p3.

    Args:
        p1 (tuple): First point/node (x, y) of the triangle/3-clique.
        p2 (tuple): Second point/node (x, y) of the triangle/3-clique.
        p3 (tuple): Third point/node (x, y) of the triangle/3-clique.

    Returns:
        tuple: Contains a tuple with the x and y coordinates of the center of the circumcircle and its radius.
            E.g. ((1.2, 0.8), 2.2).
    """
    d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    ux = ((p1[0] * p1[0] + p1[1] * p1[1]) * (p2[1] - p3[1]) + (p2[0] * p2[0] + p2[1] * p2[1]) * 
            (p3[1] - p1[1]) + (p3[0] * p3[0] + p3[1] * p3[1]) * (p1[1] - p2[1])) / d
    uy = ((p1[0] * p1[0] + p1[1] * p1[1]) * (p3[0] - p2[0]) + (p2[0] * p2[0] + p2[1] * p2[1]) * 
            (p1[0] - p3[0]) + (p3[0] * p3[0] + p3[1] * p3[1]) * (p2[0] - p1[0])) / d
    r = math.sqrt((p1[0] - ux) ** 2 + (p1[1] - uy) ** 2)
    return ((ux, uy), r)


def get_smallest_enclosing_circle(
    p1:tuple, p2:tuple, p3:tuple
) -> tuple:
    """Calculates the smallest enclosing circle of the triangle/3-clique spanned by points/nodes p1, p2, p3.

    Args:
        p1 (tuple): First point/node (x, y) of the triangle/3-clique.
        p2 (tuple): Second point/node (x, y) of the triangle/3-clique.
        p3 (tuple): Third point/node (x, y) of the triangle/3-clique.

    Returns:
        tuple: Contains a tuple with the x and y coordinates of the center of the smallest enclosing circle and its radius.
            E.g. ((1.2, 0.8), 2.2).
    """

    # return circumcircle if it is already the smallest enclosing circle
    circumcircle = get_circumcircle(p1, p2, p3)
    if point_in_triangle(circumcircle[0], p1, p2, p3):
        return circumcircle

    # smallest circle is on the longest edge
    weights = {(p1, p2): math.dist(p1, p2), (p1, p3): math.dist(p1, p3), (p2, p3): math.dist(p2, p3)}
    pts = max(weights, key=lambda k: weights[k])
    center = ((pts[0][0] + pts[1][0]) / 2.0, (pts[0][1] + pts[1][1]) / 2.0)
    radius = weights[pts] / 2.0
    return (center, radius)


def get_circumcircles(
    graph:nx.Graph
) -> dict:
    """Calculates the circumcircles of all cliques of size three in the given graph.

    Args:
        graph (nx.Graph): The graph.

    Returns:
        dict: Keys are the cliques represented as tuples and values are the circumcircles
            represented as tuples containing the coordinates and the radius.
            E.g. (1, 2, 3): ((1.2, 0.8), 2.2).
    """
    circumcircles = {}
    pos = nx.get_node_attributes(G=graph, name="pos")
    for clique in nx.enumerate_all_cliques(G=graph):
        if len(clique) == 3:
            u, v, w = clique[0], clique[1], clique[2]
            circumcircles[(u, v, w)] = get_circumcircle(pos[u], pos[v], pos[w])
    return circumcircles


def get_smallest_enclosing_circles(
    graph:nx.Graph
) -> dict:
    """Calculates the smallest enclosing circle for every clique of size three in the given graph.

    Args:
        graph (nx.Graph): The graph.

    Returns:
        dict: Keys are the cliques represented as tuples and values are the circumcircles
            represented as tuples containing the coordinates and the radius.
            E.g. (1, 2, 3): ((1.2, 0.8), 2.2).
    """
    smallest_enclosing_circles = {}
    pos = nx.get_node_attributes(G=graph, name="pos")
    for clique in nx.enumerate_all_cliques(G=graph):
        if len(clique) == 3:
            u, v, w = clique[0], clique[1], clique[2]
            smallest_enclosing_circles[(u, v, w)] = get_smallest_enclosing_circle(pos[u], pos[v], pos[w])
    return smallest_enclosing_circles


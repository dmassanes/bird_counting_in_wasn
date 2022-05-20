"""This module contains helper functions related to 2D triangles, used for the algorithm and related visualizations."""
import math
import networkx as nx


def point_in_triangle(
    pt:tuple, p1:tuple, p2:tuple, p3:tuple
) -> bool:
    """Checks if point pt is included in the triangle spanned by points p1, p2 and p3.

    Args:
        pt (tuple): Point (x, y) to be checked.
        p1 (tuple): First edge point (x, y) of the triangle.
        p2 (tuple): Second edge point (x, y) of the triangle.
        p3 (tuple): Third edge point (x, y) of the triangle.

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
    """Calculates the circumcircle of the triangle spanned by points p1, p2 and p3.

    Args:
        p1 (tuple): First edge point (x, y) of the triangle.
        p2 (tuple): Second edge point (x, y) of the triangle.
        p3 (tuple): Third edge point (x, y) of the triangle.

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
    clique:tuple, pos:tuple, weights:dict
) -> tuple:
    """Calculates the smallest enclosing circle of a clique of size three
        whose circumcenter is not within the triangle spanned by that clique.

    Args:
        clique (tuple): The clique with size three.
        pos (tuple): Positions of the cliques' nodes.
        weights (dict): Weights of the cliques' edges.

    Returns:
        tuple: Contains a tuple with the x and y coordinates of the center of the circle and its radius.
            E.g. ((1.2, 0.8), 2.2).
    """
    longest_edge = max(weights, key=lambda k: weights[k])
    u, v = longest_edge[0], longest_edge[1]
    center = ((pos[u][0] + pos[v][0]) / 2.0, (pos[u][1] + pos[v][1]) / 2.0)
    radius = weights[longest_edge] / 2.0
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
            circumcircles[(u, v, w)] = get_circumcircle((pos[u], pos[v], pos[w]))
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
    smallest_circles = {}

    # iterate over all cliques with a size of three
    pos = nx.get_node_attributes(G=graph, name="pos")
    weights = nx.get_edge_attributes(G=graph, name="weight")
    for clique in nx.enumerate_all_cliques(G=graph):
        if len(clique) != 3:
            continue

        # nodes and edge weights of current clique
        u, v, w = clique[0], clique[1], clique[2]
        crt_weights = {(u, v): weights[u, v], (u, w): weights[u, w], (v, w): weights[v, w]}

        # calc get_circumcircle of current clique
        crt_circumcirc = get_circumcircle((pos[u], pos[v], pos[w]))

        # circumcenter is not in the triangle -> smallest circle is on the longest edge
        if not point_in_triangle(crt_circumcirc[0], pos[u], pos[v], pos[w]):
            crt_pos = {u: pos[u], v: pos[v], w: pos[w]}
            smallest_circles[(u, v, w)] = get_smallest_enclosing_circle(graph=graph, clique=(u, v, w), pos=crt_pos, weights=crt_weights)
        # circumcircle is already the smallest circle
        else:
            smallest_circles[(u, v, w)] = crt_circumcirc

    return smallest_circles


"""This module contains util/helper functions related to graphs."""
import networkx as nx
import itertools
import math
import numpy as np
from census.utils.triangles import get_smallest_enclosing_circles


def build_udg(
    graph:nx.Graph, hearing_radius:float=100.0
) -> nx.Graph:
    """Build the Unit Disk Graph (UDG) from the given graph by adding one edge to each pair of two nodes whose hearing radii intersect.

    Args:
        graph (nx.Graph): Initial graph containing no edges.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.

    Returns:
        nx.Graph: The constructed UDG.
    """
    for u, v in itertools.combinations(graph.nodes, 2):
        u_coords, v_coords = graph.nodes[u]["pos"], graph.nodes[v]["pos"]
        distance = math.sqrt((u_coords[0] - v_coords[0]) ** 2 + (u_coords[1] - v_coords[1]) ** 2)
        if distance <= hearing_radius * 2:
            graph.add_edge(u, v, weight=distance)

    return graph


def alter_udg(
    graph:nx.Graph, hearing_radius:float=100.0
) -> nx.Graph:
    """Alter the given graph by removing the longest edge from all cliques of size three whose
        smallest enclosing circle is larger than the hearing radius (see Gros-desormeaux et al. [1] 
        (see README in the root directory of this repository)).

    Args:
        graph (nx.Graph): The graph to alter.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.

    Returns:
        nx.Graph: The altered graph.
    """
    smallest_enclosing_circles = get_smallest_enclosing_circles(graph=graph)

    for clique, circle in smallest_enclosing_circles.items():
        if circle[1] > hearing_radius: # smallest enclosing circle is bigger than hearing radius
            u, v, w = clique[0], clique[1], clique[2]
            weights = nx.get_edge_attributes(G=graph, name="weight")
            if (u, v) not in weights.keys() or (u, w) not in weights.keys() or (v, w) not in weights.keys():
                continue # if edge was already removed
            crt_weights = {(u, v): weights[(u, v)], (u, w): weights[(u, w)], (v, w): weights[(v, w)]} # edge weights of current clique
            x, y = max(crt_weights, key=lambda k: crt_weights[k]) # find longest edge
            graph.remove_edge(x, y) # remove it

    return graph


def get_bb(
    graph:nx.Graph, hearing_radius:float=100.0
) -> tuple:
    """Calculates the bounding box of the graph, i. e. the smallest rectangle enclosing the entire
        graph including the hearing radii of the nodes.

    Args:
        graph (nx.Graph): The graph.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.

    Returns:
        tuple: Contains two tuples, each containing the min and max values of the bounding box for the x and y coordinates.
    """
    pos = nx.get_node_attributes(G=graph, name="pos")
    pos_x = np.array(list(pos.values()))[:,0]
    pos_y = np.array(list(pos.values()))[:,1]

    x_lim = (min(pos_x) - hearing_radius, max(pos_x) + hearing_radius)
    y_lim = (min(pos_y) - hearing_radius, max(pos_y) + hearing_radius)

    return x_lim, y_lim


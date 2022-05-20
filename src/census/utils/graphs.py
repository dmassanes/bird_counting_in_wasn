"""This module contains util/helper functions related to graphs."""
import networkx as nx
import pandas as pd
import itertools
import utm
import math
from census.utils.triangles import get_smallest_enclosing_circles


def build_udg(
    df:pd.DataFrame, hearing_radius:float=50.0, coords:str="2d"
) -> nx.Graph:
    """Build the Unit Disk Graph (UDG) from the input DataFrame containing either geo- or 2D coordinates for the nodes' locations.
        Geo-coordinates will be converted to 2D coordinates using the "utm" library.
        One edge is added to each pair of two nodes whose hearing radii intersect.

    Args:
        df (pd.DataFrame): DataFrame containing the node information. Must either have the columns ["node", "lat", "lon"] or ["node", "n_x", "n_y"]
            depending on the format of the coordinates contained in the DataFrame.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 50.0.
        coords (str, optional): Can either be "2d" or "geo" depending on the format of the coordinates contained in the dataframe. Defaults to "2d".

    Returns:
        nx.Graph: The constructed UDG.
    """
    graph = nx.Graph()

    # add nodes from their given 2D coordinates
    if coords == "2d":
        df_node = df[["node","n_x","n_y"]].drop_duplicates(subset="node")
        for idx, row in df_node.iterrows():
            node = int(row["node"])
            n_x = row["n_x"]
            n_y = row["n_y"]
            graph.add_node(node, pos=(n_x, n_y))

    # add nodes by converting their geo coordinates into 2D coordinates
    elif coords == "geo":
        df_node = df[["node","lat","lon"]].drop_duplicates(subset="node")
        for idx, row in df_node.iterrows():
            node = int(row["node"])
            lat = row["lat"]
            lon = row["lon"]
            u = utm.from_latlon(lat, lon)
            n_x, n_y = u[:2]
            graph.add_node(node, pos=(n_x, n_y))

    # add the edges based on the intersections given by the hearing radius
    for u, v in itertools.combinations(graph.nodes, 2):
        u_coords, v_coords = graph.nodes[u]["pos"], graph.nodes[v]["pos"]
        distance = math.sqrt((u_coords[0] - v_coords[0]) ** 2 + (u_coords[1] - v_coords[1]) ** 2)
        if distance <= hearing_radius * 2:
            graph.add_edge(u, v, weight=distance)

    return graph


def alter_udg(
    graph:nx.Graph, hearing_radius:float=50.0
) -> nx.Graph:
    """Alter the given graph by removing the longest edge from all cliques of size three whose
        smallest enclosing circle is larger than the hearing radius (see Gros-desormeaux et al. [1] 
        (see README in the root directory of this repository)).

    Args:
        graph (nx.Graph): The graph to alter.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 50.0.

    Returns:
        nx.Graph: The altered graph.
    """
    smallest_enclosing_circles = get_smallest_enclosing_circles(graph=graph, hearing_radius=hearing_radius)

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


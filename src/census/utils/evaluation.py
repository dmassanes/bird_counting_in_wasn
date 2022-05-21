"""This module contains helper functions related to evaluations of the project."""
import numpy as np
import pandas as pd
import math
import datetime as dt
import networkx as nx
from census.utils.graphs import get_bb


def generate_graph_diamond_pattern(
    x_rows:int=4, y_rows:int=4, distance_x:float=200.0, distance_y:float=200.0, distance_off:float=25.0, hearing_radius:float=100.0, seed:int=0
) -> nx.Graph:
    """Generates a new graph whose nodes are arranged in a diamond pattern.

    Args:
        x_rows (int, optional): Amount of nodes in the main rows of the x-axis. Defaults to 4.
        y_rows (int, optional): Amount of nodes in the main rows of the y-axis. Defaults to 4.
        distance_x (float, optional): Default distance between the nodes in the x-axis in meters. Defaults to 200.0.
        distance_y (float, optional): Default distance between the nodes in the y-axis in meters. Defaults to 200.0.
        distance_off (float, optional): Circular offset from the position given by the pattern in meters. Defaults to 25.0.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.
        seed (int, optional): Seed for reproducibility. Defaults to 0.

    Returns:
        nx.Graph: The generated graph.
    """
    np.random.seed(seed)

    graph = nx.Graph()
    n = 0
    for i in range(y_rows * 2 - 1):
        aux = i % 2
        for j in range(x_rows - aux):
            n_y = i * distance_y / 2
            n_x = j * distance_x + (aux * distance_x / 2)

            angle = np.random.rand() * 2 * math.pi
            x_off = np.random.rand() * distance_off
            y_off = np.random.rand() * distance_off
            n_x += np.cos(angle) * x_off
            n_y += np.sin(angle) * y_off

            graph.add_node(n, pos=(n_x, n_y))
            n += 1

    return graph


def generate_graph_random_conditional(
    n:int=25, hearing_radius:float=100.0, seed:int=0, area_overlap:float=0.33
) -> nx.Graph:
    """Generates a new graph with random positions while trying to avoid to much overlapping area.

    Args:
        n (int, optional): Amount of nodes. Defaults to 25.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.
        seed (int, optional): Seed for reproducibility. Defaults to 0.
        area_overlap (float, optional): When inserting the nodes, a check is made beforehand to see if a new random node 
            would cause too much overlap with the existing ones. This argument specifies the maximum allowed area as a 
            percentage of the area that a node includes with its hearing radius. Defaults to 0.33. Use higher values when
            the generation algorithms takes too much time.

    Returns:
        nx.Graph: The generated graph.
    """
    np.random.seed(seed)

    def find_intersection_area(c1: tuple, c2: tuple, hearing_radius:float=100.0) -> float:
        d = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
        rs = hearing_radius ** 2

        # the circle centers are the same
        if d == 0:
            return math.pi * rs

        # check if the circles are overlapping
        angle = (rs + d ** 2 - rs) / (2 * hearing_radius * d)
        if (-1 <= angle < 1):
            theta = math.acos(angle) * 2
            area = (0.5 * theta * rs) - (0.5 * rs * math.sin(theta))
            return area

        return 0

    graph = nx.Graph()
    area_circle = math.pi * hearing_radius ** 2
    len_bb = math.sqrt(area_circle * n) - hearing_radius * 2
    i = 0
    while i < n:
        pos = nx.get_node_attributes(G=graph, name="pos")
        new_pos = np.random.rand(2) * len_bb
        area = 0
        for j in pos.values():
            area += find_intersection_area(new_pos, j, hearing_radius=hearing_radius)
        if area < area_overlap * area_circle:
            graph.add_node(i, pos=new_pos)
            i += 1

    return graph


def generate_random_classification_results(
    graph:nx.Graph, hearing_radius:float=100.0, seed:int=0,
    dt_begin:dt.datetime=dt.datetime(1970, 1, 1, 0, 0, 0), dt_end:dt.datetime=dt.datetime(1970, 1, 1, 3, 0, 0), 
    amount_per_species:dict={"comcha": 3}, songs_per_bird:dict={"comcha": (125, 300)},
) -> pd.DataFrame:
    """Randomly generates classification results given a set of birds and a per-species interval containing
        the minimum and maximum number of songs per bird of that species for a given time period.

    Args:
        graph (nx.Graph): The graph.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.
        seed (int, optional): Seed for reproducibility. Defaults to 0.
        dt_begin (dt.datetime): Start of the time period. Defaults to dt.datetime(1970, 1, 1, 0, 0, 0).
        dt_end (dt.datetime): End of the time period. Defaults to dt.datetime(1970, 1, 1, 3, 0, 0).
        amount_per_species (dict): Amount of birds per species. Defaults to {"comcha": 3}.
        songs_per_bird (dict): Min and max amount of songs per bird per species. Defaults to {"comcha": (125, 300)}.

    Returns:
        pd.DataFrame: Contains all the necessary information for the algorithm. 
            Columns are ["node", "n_x", "n_y", "begin_time", "end_time", "species_code", "b_x", "b_y", "true_count"]
    """

    # length of total time window in seconds - 3
    timedelta_in_seconds = (dt_end - dt_begin).total_seconds() - 3.0

    # length of a classification result
    timedelta_result = dt.timedelta(seconds=3.0)

    # set seed for the random generator
    np.random.seed(seed)

    # initialize dataframe
    df = pd.DataFrame(columns=["node", "n_x", "n_y", "begin_time", "end_time", "species_code", "b_x", "b_y", "true_count"])

    # generate dataframe
    x_lim, y_lim = get_bb(graph=graph, hearing_radius=hearing_radius)
    limit_x = x_lim[1] - x_lim[0] # width of the bounding box
    limit_y = y_lim[1] - y_lim[0] # height of the bounding box
    pos = nx.get_node_attributes(G=graph, name="pos")
    pos_x = np.array(list(pos.values()))[:,0]
    pos_y = np.array(list(pos.values()))[:,1]
    idx = 0
    for i, (species_code, true_count) in enumerate(amount_per_species.items()):

        for j in range(true_count):
            songs_this_bird = np.random.randint(low=songs_per_bird[species_code][0], high=songs_per_bird[species_code][1] + 1)
            max_delay = timedelta_in_seconds / songs_this_bird
            for k in range(songs_this_bird):

                # generate variables for current bird
                b_pos = np.random.rand(2)
                b_pos[0] = b_pos[0] * limit_x + x_lim[0]
                b_pos[1] = b_pos[1] * limit_y + y_lim[0]
                begin_time = dt_begin + dt.timedelta(seconds=(k + np.random.rand()) * max_delay)
                end_time = begin_time + timedelta_result

                # check if bird is in hearing radius of the nodes and add classification result for every node this is true
                for node, n_x, n_y in zip(graph.nodes, pos_x, pos_y):
                    distance = math.sqrt((n_x - b_pos[0]) ** 2 + (n_y - b_pos[1]) ** 2)
                    if distance <= hearing_radius:
                        df.loc[idx] = [node, n_x, n_y, begin_time, end_time, species_code, b_pos[0], b_pos[1], true_count]
                        idx += 1

    return df.sort_values("begin_time")


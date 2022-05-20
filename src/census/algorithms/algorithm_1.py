"""This module contains the counting algorithm based on "Algorithm 1" from the paper by 
Gros-desormeaux et al. [1] (see README in the root directory of this repository)."""
import networkx as nx
import datetime as dt
import pandas as pd
from census.utils.graphs import alter_udg


def count_birds(
    df:pd.DataFrame, graph:nx.Graph, time_delta_detection:float=3.0, hearing_radius:float=50.0
) -> dict:
    """Estimates the number of birds per species using the classification results in the input DataFrame df.
        The DataFrame is expected to contain classification results for a specific time period for which
        the Birds should be counted, e. g. for one day.

    Args:
        df (pd.DataFrame): DataFrame containing the classification results. 
                            Must have the columns ["node", "species_name_en", "begin_time", "end_time"].
        graph (nx.Graph): The graph on which the algorithm will be executed.
        time_delta_detection (float, optional): Size of the time window in seconds. Defaults to 3.0.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by the node. Defaults to 50.0.

    Returns:
        dict: Keys are the name of species in English, and values are the estimated amount of observable birds for this species.
    """

    # make sure that the dataframe is sorted by begin_time
    df = df.sort_values("begin_time")

    # check if altering is necessary in the current graph
    altered_graph = alter_udg(graph.copy())
    altering_necessary = altered_graph.__str__() != graph.__str__()

    # variables to iterate and count
    wdw_delta = dt.timedelta(seconds=time_delta_detection) # time window as timedelta object
    wdw_begin = df["begin_time"].min() # begin time of the time window
    wdw_end = wdw_begin + wdw_delta # end time of the time window
    last_stamp = df["end_time"].max() # last time in the dataframe
    species_names = sorted(df["species_name_en"].drop_duplicates()) # all species contained in the dataframe
    species_count = {species: 1 for species in species_names} # initialize dictionary used for the counting

    # iterate over the dataframe with the time window and count birds
    while wdw_begin < last_stamp:

        # extract all classification results for the current time window
        mask        = (df["begin_time"] >= wdw_begin) & (df["begin_time"] < wdw_end) \
                        | (df["end_time"] > wdw_begin) & (df["end_time"] <= wdw_end)
        df_wdw      = df.loc[mask]
        wdw_begin   = wdw_end
        wdw_end     += wdw_delta

        # no classification results => continue to next window
        if len(df_wdw.index) == 0:
            continue

        # summarize redundant classification results
        df_wdw = df_wdw[["node","species_name_en"]].drop_duplicates()

        # current time window contains only one bird for the contained species
        if len(df_wdw.index) == 1 or df_wdw.nunique(axis=0)["species_name_en"] == len(df_wdw.index):
            continue

        # execute counting algorithm for every species in the current time window
        for species_name_en in df_wdw["species_name_en"].drop_duplicates():
            df_species = df_wdw.loc[df_wdw["species_name_en"] == species_name_en]
            nodes_species = list(df_species["node"].drop_duplicates())

            # only multiple classification results per species are relevant
            if len(nodes_species) > 1:

                # construct subgraph and alter it if necessary
                graph_species = nx.Graph(graph.subgraph(nodes_species))
                if altering_necessary:
                    graph_species = alter_udg(graph_species, hearing_radius)

                # count birds for current species
                count = 0
                while len(graph_species.nodes) > 0:
                    clique = max(nx.find_cliques(G=graph_species), key=len)
                    graph_species.remove_nodes_from(clique)
                    count += 1

                # overwrite estimation if the current number of birds is bigger than the previous max
                if count > species_count[species_name_en]:
                    species_count[species_name_en] = count

    return species_count


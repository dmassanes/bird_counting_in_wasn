"""
This module contains helper functions related to visualization of the graphs and algorithms.
"""
import matplotlib as mpl
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from census.utils.triangles import get_smallest_enclosing_circles
from census.utils.triangles import get_circumcircles
from census.utils.graphs import get_bb
from census.utils.definitions import taxonomy

def plot_birds(
    df:pd.DataFrame, ax:mpl.axes.Axes, species_code_list:list=None, alpha:float=1.0, cmap:mpl.colors.Colormap=None
) -> None:
    """Plots the birds' positions found in the given DataFrame. To distinct between the species they are coloured differently.

    Args:
        df (pd.DataFrame): The DataFrame containing the information about the birds. The DataFrame is expected to contain information
            about the birds' positions for a short time period, e. g. 30 seconds. The plot can get messy if there are too many
            classification results / birds in the DataFrame. Columns needed: ["species_code", "b_x", "b_y"].
        ax (mpl.axes.Axes): Axes object where the birds will be plotted.
        species_code_list (list): List containing the species codes of the birds to get plotted.
            If None all species contained in the DataFrame get plotted. Defaults to None.
        alpha (float, optional): Opacity of the plotted markers. Defaults to 1.0.
        cmap (mpl.colors.Colormap, optional): Colormap to be used to distinct between the different species.
            If None mpl.cm.hsv is used. Defaults to None.
    """
    if cmap == None:
        cmap = mpl.cm.get_cmap("hsv")
    if species_code_list == None:
        species_code_list = df["species_code"].drop_duplicates()
    colors = cmap(range(len(species_code_list)))
    for idx, species_code in enumerate(species_code_list):
        df_crt = df.loc[df["species_code"] == species_code]
        color_crt = colors[idx]
        ax.scatter(list(df_crt["b_x"]), list(df_crt["b_y"]), color=color_crt, alpha=alpha, label=taxonomy[species_code].split("_")[-1], marker="x")


def plot_bb(
    ax:mpl.axes.Axes, graph:nx.Graph, hearing_radius:float=100.0, alpha:float=0.5, xlim:float=None, ylim:float=None, with_text=True
) -> None:
    """Plot the bounding box of the graph, i. e. the smallest rectangle enclosing the entire
        graph including the hearing radii of the nodes.

    Args:
        ax (mpl.axes.Axes): Axes object where the bounding box will be plotted.
        graph (nx.Graph): The graph.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.
        alpha (float, optional): Opacity of the plotted bounding box. Defaults to 1.0.
        with_text (bool, optional): If True, add text labels describing the size of the bounding box in meters. Defaults to True.
    """
    if not xlim and not ylim:
        xlim, ylim = get_bb(graph=graph, hearing_radius=hearing_radius)

    # plot text if requested
    if with_text:
        x_dist = xlim[1] - xlim[0]
        y_dist = ylim[1] - ylim[0]
        x_text = f"{round(x_dist, 1)}m"
        y_text = f"{round(y_dist, 1)}m"
        x_pos = (xlim[0] + x_dist / 2, ylim[0] - 20)
        y_pos = (xlim[0] - 15, ylim[0] + y_dist / 2)
        ax.text(x_pos[0], x_pos[1], x_text, horizontalalignment="center", verticalalignment="center")
        ax.text(y_pos[0], y_pos[1], y_text, horizontalalignment="center", verticalalignment="center", rotation=90)

    # plot bounding box
    ax.plot([xlim[0], xlim[1]], [ylim[0], ylim[0]], c="black", alpha=alpha)
    ax.plot([xlim[1], xlim[1]], [ylim[1], ylim[0]], c="black", alpha=alpha)
    ax.plot([xlim[1], xlim[0]], [ylim[1], ylim[1]], c="black", alpha=alpha)
    ax.plot([xlim[0], xlim[0]], [ylim[0], ylim[1]], c="black", alpha=alpha)


def draw_circles(
    ax:mpl.axes.Axes, circles:list, color:str
) -> None:
    """Draw given circles into the given Axes.

    Args:
        ax (mpl.axes.Axes): Axes object where the circles will be plotted.
        circles (dict): Circles.
        color (str): Name of the color.
    """
    for circle in circles:
        circ_patch = mpl.patches.Circle(circle[0], radius=circle[1], color=color, fill=False, clip_on=False)
        ax.add_patch(circ_patch)
        ax.plot(circle[0][0], circle[0][1], marker="o", markersize=3, markeredgecolor=color, markerfacecolor=color)


def plot_graph(
    graph:nx.Graph, hearing_radius:float=100.0, ax=None, fig:mpl.figure.Figure=None, figsize:tuple=(10.0,10.0),
    with_node_labels:bool=False, with_edges:bool=True, with_edge_labels:bool=False, node_size:int=25, 
    with_hearing_radii:bool=False, with_circumcircles:bool=False, with_smallest_circles:bool=False
) -> tuple:
    """Plot the given graph together with a couple of optional, additional information.

    Args:
        graph (nx.Graph): The graph.
        hearing_radius (float, optional): Radius in meters within which birds can be detected by a node. Defaults to 100.0.
        ax (mpl.axes.Axes): Axes object where the graph will be plotted. If None, a new Axes object will be created. 
            Please note that this argument should always be assigned in combination with the fig argument, i. e. 
            either both are None or both have a value assigned. Defaults to None.
        fig (mpl.figure.Figure, optional): Figure object for the Axes object. If None, a new Figure object will be created. 
            Please note that this argument should always be assigned in combination with the ax argument, i. e. 
            either both are None or both have a value assigned. Defaults to None.
        figsize (tuple, optional): Size of the figure. If the argument fig is given, nothing happens. Defaults to (10.0,10.0).
        with_node_labels (bool, optional): If True, the node labels will be drawn. Defaults to False.
        with_edges (bool, optional): If True, the edges will be drawn. Defaults to True.
        with_edge_labels (bool, optional): If True, the edge labels will be drawn. Defaults to False.
        node_size (int, optional): Size of the nodes. Defaults to 25. See networkx documentation.
        with_hearing_radii (bool, optional): If True, the hearing radii will be drawn. Defaults to False.
        with_circumcircles (bool, optional): If True, the circumcircles will be drawn. Defaults to False.
        with_smallest_circles (bool, optional): If True, the smallest circles will be drawn. Defaults to False.

    Returns:
        tuple: A tuple containing the Figure and Axes object of the plot.
    """

    # create new or use existing figure for drawing
    if not ax:
        fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_clip_on(False)

    # actual drawing of the graph
    pos = nx.get_node_attributes(G=graph, name="pos")
    nx.draw_networkx_nodes(G=graph, pos=pos, ax=ax, node_size=node_size, node_color="tab:gray", edgecolors="black")
    if with_edges:
        nx.draw_networkx_edges(G=graph, pos=pos, ax=ax)
    if with_node_labels:
        node_labels = {node: int(str(node)[-3:]) for node in graph.nodes}
        nx.draw_networkx_labels(G=graph, pos=pos, ax=ax, labels=node_labels)
    if with_edge_labels:
        weights = nx.get_edge_attributes(G=graph, name="weight")
        edge_labels = {(u, v): round(graph.edges[u, v]["weight"], 1) for u, v in weights}
        nx.draw_networkx_edge_labels(G=graph, pos=pos, edge_labels=edge_labels)

    # draw hearing radii
    if with_hearing_radii:
        for crt_pos in pos.values():
            circ_patch = mpl.patches.Circle(crt_pos, radius=hearing_radius, color="tab:gray", fill=False, clip_on=False, alpha=1.0)
            ax.add_patch(circ_patch)

    # draw smallest circles
    if with_smallest_circles:
        smallest_circles = get_smallest_enclosing_circles(graph=graph)
        draw_circles(ax=ax, circles=smallest_circles.values(), color="red")

    # draw circumcircles
    if with_circumcircles:
        circumcircles = get_circumcircles(graph=graph)
        draw_circles(ax=ax, circles=circumcircles.values(), color="orange")

    return fig, ax


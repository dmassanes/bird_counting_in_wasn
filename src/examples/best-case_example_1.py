"""
Showcase of a best case scenario for the algorithm on a predefined graph and predefined classification results.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import pandas as pd
import datetime as dt
import math

from census.utils.graphs import build_udg, alter_udg, get_bb
from census.utils.visualization import plot_graph, plot_bb, plot_birds

# generate graph and build udg
n = 7
graph = nx.Graph()
graph.add_nodes_from(range(n))
pos = {
    0: (0.0, 0.0),
    1: (180.0, 0.0),
    2: (80.0, 125.0),
    3: (300.0, 0.0),
    4: (20.0, 290.0),
    5: (250.0, 185.0),
    6: (300.0, 300.0)
}
nx.set_node_attributes(G=graph, values=pos, name="pos")
build_udg(graph=graph)

# generate dataframe with three birds, all singing at the same time for
df = pd.DataFrame(columns=["node", "n_x", "n_y", "begin_time", "end_time", "species_code", "b_x", "b_y", "true_count"])
birds = [
    (dt.datetime(1970, 1, 1, 0, 0, 0), dt.datetime(1970, 1, 1, 0, 0, 3), "comcha", 90, 40, 3),
    (dt.datetime(1970, 1, 1, 0, 0, 0), dt.datetime(1970, 1, 1, 0, 0, 3), "comcha", 30, 360, 3),
    (dt.datetime(1970, 1, 1, 0, 0, 0), dt.datetime(1970, 1, 1, 0, 0, 3), "comcha", 300, 250, 3)
]
idx = 0
for bird in birds:
    for node in graph.nodes:
        n_x, n_y = pos[node][0], pos[node][1]
        distance = math.sqrt((n_x - bird[3]) ** 2 + (n_y - bird[4]) ** 2)
        if distance <= 100.0: # add classification result for every node that is hearing the current bird
            df.loc[idx] = [node, n_x, n_y, bird[0], bird[1], bird[2], bird[3], bird[4], bird[5]]
            idx += 1

# plotting
x_lim, y_lim = get_bb(graph=graph)
cmap = mpl.cm.get_cmap("hsv")
color = cmap(range(1))[0]

fig, ax = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("A best-case example resulting in an ideal procedure of the implemented algorithm\n" +
                "for one time window/step. The red crosses represent birds.", fontsize="x-large")

# 0 initial graph
ax[0, 0].set(title="Initial graph with all nodes")
plot_graph(graph=graph, ax=ax[0, 0], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[0, 0])
plot_bb(graph=graph, ax=ax[0, 0], x_lim=x_lim, y_lim=y_lim)

# 1 subgraph
ax[0, 1].set(title="Graph without the nodes which don't hear birds")
subgraph = nx.Graph(graph.subgraph(df["node"].drop_duplicates()))
plot_graph(graph=subgraph, ax=ax[0, 1], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[0, 1])
plot_bb(graph=subgraph, ax=ax[0, 1], x_lim=x_lim, y_lim=y_lim)

# 2 altered graph
ax[0, 2].set(title="Alternated graph")
altered_graph = alter_udg(subgraph.copy())
plot_graph(graph=altered_graph, ax=ax[0, 2], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[0, 2])
plot_bb(graph=altered_graph, ax=ax[0, 2], x_lim=x_lim, y_lim=y_lim)

# 3 first clique
ax[1, 0].set(title="First maximal clique")
clique = max(nx.find_cliques(G=altered_graph), key=len)
plot_graph(graph=altered_graph, ax=ax[1, 0], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[1, 0])
plot_bb(graph=altered_graph, ax=ax[1, 0], x_lim=x_lim, y_lim=y_lim)
for c in clique:
    circ_patch = mpl.patches.Circle(pos[c], radius=100.0, color="tab:red", fill=True, alpha=0.2, clip_on=False)
    ax[1, 0].add_patch(circ_patch)
altered_graph.remove_nodes_from(clique)
df = df.loc[(df["node"] != clique[0]) & (df["node"] != clique[1]) & (df["node"] != clique[2])]

# 4 second clique
ax[1, 1].set(title="Second maximal clique")
clique = max(nx.find_cliques(G=altered_graph), key=len)
plot_graph(graph=altered_graph, ax=ax[1, 1], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[1, 1])
plot_bb(graph=altered_graph, ax=ax[1, 1], x_lim=x_lim, y_lim=y_lim)
for c in clique:
    circ_patch = mpl.patches.Circle(pos[c], radius=100.0, color="tab:red", fill=True, alpha=0.2, clip_on=False)
    ax[1, 1].add_patch(circ_patch)
altered_graph.remove_nodes_from(clique)
df = df.loc[(df["node"] != clique[0]) & (df["node"] != clique[1])]

# 5 third clique
ax[1, 2].set(title="Third maximal clique")
clique = max(nx.find_cliques(G=altered_graph), key=len)
plot_graph(graph=altered_graph, ax=ax[1, 2], fig=fig, with_edges=True, with_hearing_radii=True)
plot_birds(df=df, ax=ax[1, 2])
plot_bb(graph=altered_graph, ax=ax[1, 2], x_lim=x_lim, y_lim=y_lim)
for c in clique:
    circ_patch = mpl.patches.Circle(pos[c], radius=100.0, color="tab:red", fill=True, alpha=0.2, clip_on=False)
    ax[1, 2].add_patch(circ_patch)
df = df.loc[(df["node"] != clique[0])]

# plt.tight_layout()
# plt.show()
plt.savefig("../images/best-case_example_1.jpg", bbox_inches="tight")


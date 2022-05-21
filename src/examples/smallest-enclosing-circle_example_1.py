"""
This example generates a plot illustrating the three possible scenarios for the smallest enclosing circle 
in a clique of size three. The circumcircle is the smallest enclosing circle, the smallest enclosing circle 
is on the longest edge of the clique, or the smallest enclosing circle is too big, which means the cliques' 
unit disks do not intersect mutually. The resulting plot is used in the main README.md of this repository.
"""
import networkx as nx
import matplotlib.pyplot as plt

from census.utils.graphs import build_udg
from census.utils.triangles import get_smallest_enclosing_circle
from census.utils.visualization import plot_graph, plot_bb


fig, ax = plt.subplots(1, 3, figsize=(12, 4))

xlim = (-120.0, 320.0)
ylim = (-120.0, 320.0)
xmid = (xlim[0] + xlim[1]) / 2
ymid = (ylim[0] + ylim[1]) / 2


# smallest circle is circumcircle
graph_1 = nx.Graph()
graph_1.add_nodes_from(range(3))
pos = {0: (0.0, 0.0), 1: (120.0, 30.0), 2: (30.0, 120.0)}
nx.set_node_attributes(G=graph_1, values=pos, name="pos")
build_udg(graph=graph_1)

ec, er = get_smallest_enclosing_circle(*nx.get_node_attributes(graph_1, "pos").values())
xlim_n = (xlim[0] - (xmid - ec[0]), xlim[1] - (xmid - ec[0])) 
ylim_n = (ylim[0] - (ymid - ec[1]), ylim[1] - (ymid - ec[1]))
ax[0].set(title="Smallest circle is circumcircle", xlim=xlim_n, ylim=ylim_n)
plot_graph(graph=graph_1, ax=ax[0], fig=fig, with_edges=True, with_hearing_radii=True, with_smallest_circles=True)
plot_bb(graph=graph_1, ax=ax[0], xlim=xlim_n, ylim=ylim_n)


# smallest circle on longest edge
graph_2 = nx.Graph()
graph_2.add_nodes_from(range(3))
pos = {0: (0.0, 0.0), 1: (180.0, 0.0), 2: (90.0, 60.0)}
nx.set_node_attributes(G=graph_2, values=pos, name="pos")
build_udg(graph=graph_2)

ec, er = get_smallest_enclosing_circle(*nx.get_node_attributes(graph_2, "pos").values())
xlim_n = (xlim[0] - (xmid - ec[0]), xlim[1] - (xmid - ec[0])) 
ylim_n = (ylim[0] - (ymid - ec[1]), ylim[1] - (ymid - ec[1]))
ax[1].set(title="Smallest circle on longest edge", xlim=xlim_n, ylim=ylim_n)
plot_graph(graph=graph_2, ax=ax[1], fig=fig, with_edges=True, with_hearing_radii=True, with_smallest_circles=True)
plot_bb(graph=graph_2, ax=ax[1], xlim=xlim_n, ylim=ylim_n)


# smallest circle is too big
graph_3 = nx.Graph()
graph_3.add_nodes_from(range(3))
pos = {0: (0.0, 0.0), 1: (190.0, 0.0), 2: (95.0, 165.0)}
nx.set_node_attributes(G=graph_3, values=pos, name="pos")
build_udg(graph=graph_3)

ec, er = get_smallest_enclosing_circle(*nx.get_node_attributes(graph_3, "pos").values())
xlim_n = (xlim[0] - (xmid - ec[0]), xlim[1] - (xmid - ec[0])) 
ylim_n = (ylim[0] - (ymid - ec[1]), ylim[1] - (ymid - ec[1]))
ax[2].set(title="Smallest circle is too big", xlim=xlim_n, ylim=ylim_n)
plot_graph(graph=graph_3, ax=ax[2], fig=fig, with_edges=True, with_hearing_radii=True, with_smallest_circles=True)
plot_bb(graph=graph_3, ax=ax[2], xlim=xlim_n, ylim=ylim_n)


# plt.tight_layout()
# plt.show()
plt.savefig("../images/smallest-enclosing-circle_example_1.jpg", bbox_inches="tight")


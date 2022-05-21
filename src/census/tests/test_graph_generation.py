import matplotlib.pyplot as plt

from census.utils.evaluation import generate_graph_diamond_pattern, generate_graph_random_conditional
from census.utils.graphs import build_udg, get_bb
from census.utils.visualization import plot_graph, plot_bb


# generate graph with diamond pattern
graph_1 = generate_graph_diamond_pattern()
build_udg(graph_1)
lim_x_1, lim_y_1 = get_bb(graph_1)


# generate graph from a uniform distribution of positions
graph_2 = generate_graph_random_conditional()
build_udg(graph_2)
lim_x_2, lim_y_2 = get_bb(graph_2)


# plot both graphs
fig, ax = plt.subplots(1, 2, figsize=(8, 8))

ax[0].set(title=f"generate_graph_diamond_pattern()\nlim_x ({round(lim_x_1[0], 1)}, {round(lim_x_1[1], 1)}), lim_y ({round(lim_y_1[0], 1)}, {round(lim_y_1[1], 1)})")
plot_graph(graph=graph_1, ax=ax[0], fig=fig, with_edges=True, with_hearing_radii=True)
plot_bb(graph=graph_1, ax=ax[0])

ax[1].set(title=f"generate_graph_random_conditional()\nlim_x ({round(lim_x_2[0], 1)}, {round(lim_x_2[1], 1)}), lim_y ({round(lim_y_2[0], 1)}, {round(lim_y_2[1], 1)})")
plot_graph(graph=graph_2, ax=ax[1], fig=fig, with_edges=True, with_hearing_radii=True)
plot_bb(graph=graph_2, ax=ax[1])

plt.tight_layout()
plt.show()

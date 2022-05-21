"""
The result of this example is used to visualize the structure of the DataFrames
used for the counting algorithm. It generates a string containing a randomly
generated DataFrame represented as a markdown table. Note that not every row
generated by the method "generate_random_classification_results" is needed
for the counting algorithm. This table is used in the main README.md of this repository.
"""
import datetime as dt

from census.utils.random import generate_graph_diamond_pattern, generate_random_classification_results
from census.utils.graphs import build_udg

seed = 1

graph = generate_graph_diamond_pattern(x_rows=2, y_rows=2, seed=seed)
build_udg(graph=graph)

df = generate_random_classification_results(
    graph=graph,
    seed=seed,
    dt_begin=dt.datetime(1970, 1, 1, 0, 0, 0),
    dt_end=dt.datetime(1970, 1, 1, 0, 0, 30),
    amount_per_species={"comcha": 2, "blucha1": 2},
    songs_per_bird={"comcha": (1, 3), "blucha1": (1, 3)}
)

print()
print(">>> Standard output of the generated DataFrame")
print(df)
print()

print(">>> Markdown output of the generated DataFrame")
print(df.to_markdown(index=False))
print()


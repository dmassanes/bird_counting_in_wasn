# Bird counting in Wireless Acoustic Sensor Networks (WASNs)

This repository contains a Python implementation of a bird counting algorithm for Wireless Acoustic Sensor Networks (WASNs). The implemented algorithm is based on "Algorithm 1", which is presented in a paper by Gros-desormeaux et al. [[1]](#1). Some changes were made to the algorithm to allow interaction with classification results as produced by the BirdNET (https://github.com/kahst/BirdNET) classifier.

# Algorithm

The following steps briefly describe the Algorithm implemented in this repository:
1. (Create the UDG) Create a Unit Disk Graph (UDG) of the underlying WASN, assuming that every node has the same hearing radius (unit disk) within which it can detect bird songs.
2. (Select the subgraph) For a one-time step, select a subgraph of the UDG containing all nodes which detected a bird within this time step.
3. (Alternate the subgraph) Ensure that the subgraph only contains cliques whose unit disks mutually intersect by removing the longest edge in every clique of size three whose unit disks don't intersect mutually.
4. (Count by removing the maximal cliques) Successively remove the maximal cliques from the subgraph until there are no nodes left. Count one bird for each maximal clique.
5. Repeat the process from step 2 for each species detected in this one-time step. Proceed to step 6 when all species are processed.
6. Repeat the process from step 2 for all time steps given. The result for each species is the maximum estimate obtained over all time steps for that species.

The following figure illustrates the procedure for a one-time step. The three red crosses represent one bird each, singing in that one-time step. The hearing radius for all nodes is 100.0 meters. This example results in the algorithm's correct estimation of birds since it removes exactly three maximal cliques.

![Best-case example](images/best-case_example_1.jpg)

## Implementation details

The implementations contained in this repository rely on the following Python libraries:
- NetworkX (https://networkx.org/): Used for generating, processing, and visualizing graphs and executing algorithms on them.
- Pandas (https://pandas.pydata.org/): Primarily used to handle the information needed by the algorithm in tables represented by DataFrames.
- NumPy (https://numpy.org/): Used mainly for randomized tasks.
- Matplotlib (https://matplotlib.org/): Used for visualizations and plots.

### Data handling

|    |   node |       n_x |       n_y | begin_time                 | end_time                   | species_code   |      b_x |      b_y |   true_count |
|---:|-------:|----------:|----------:|:---------------------------|:---------------------------|:---------------|---------:|---------:|-------------:|
|  3 |     23 | 420.095   | 606.652   | 1970-01-01 00:00:00.639325 | 1970-01-01 00:00:03.639325 | blucha1        | 355.571  | 646.651  |            2 |
|  1 |      9 | 412.266   | 196.468   | 1970-01-01 00:00:04.016717 | 1970-01-01 00:00:07.016717 | comcha         | 401.763  | 207.409  |            2 |
|  4 |      0 | -17.0454  |  -4.54963 | 1970-01-01 00:00:16.493579 | 1970-01-01 00:00:19.493579 | blucha1        | -44.5533 | -88.1407 |            2 |
|  7 |     13 | 496.266   | 290.061   | 1970-01-01 00:00:18.329747 | 1970-01-01 00:00:21.329747 | blucha1        | 549.317  | 317.862  |            2 |
|  8 |     17 | 577.107   | 400.96    | 1970-01-01 00:00:18.329747 | 1970-01-01 00:00:21.329747 | blucha1        | 549.317  | 317.862  |            2 |
|  2 |      7 |   3.50707 | 181.41    | 1970-01-01 00:00:19.948479 | 1970-01-01 00:00:22.948479 | comcha         | -69.8598 | 116.734  |            2 |
|  0 |     23 | 420.095   | 606.652   | 1970-01-01 00:00:23.164532 | 1970-01-01 00:00:26.164532 | comcha         | 376.205  | 580.644  |            2 |
|  5 |     20 | 501.494   | 513.797   | 1970-01-01 00:00:26.807565 | 1970-01-01 00:00:29.807565 | blucha1        | 530.385  | 601.539  |            2 |
|  6 |     24 | 614.96    | 597.311   | 1970-01-01 00:00:26.807565 | 1970-01-01 00:00:29.807565 | blucha1        | 530.385  | 601.539  |            2 |

### One-time step/window



### Alternating the UDG



# References
<a id="1">[1]</a> H. Gros-desormeaux, P. Hunel, and N. Vidot, Wildlife Assessment Using Wireless Sensor Networks, Wireless Sensor Networks: Application - Centric Design, 2010.


import tsplib95
import networkx
import numpy as np

# load the tsplib problem
problem = tsplib95.load('argentina.tsp')

# convert into a networkx.Graph
graph = problem.get_graph()

print(graph)
# convert into a numpy distance matrix
distance_matrix = networkx.to_numpy_matrix(graph)

# print the distance between nodes 4 and 2:
np.save(
        f"argentina_tsp",
        distance_matrix,
        allow_pickle=False
    )



# from tsplib95 import load
# import math

# print("hi")

# def distance(start, end):
#     sx, sy = start[0], start[1]
#     ex, ey = end[0], end[1]

#     distance = math.sqrt(((sx-ex)^2 + (sy-ey)^2))
#     return distance

# problem = load("chinatsp.tsp", special=distance)
# print(problem)
# print(problem.edge_weights)
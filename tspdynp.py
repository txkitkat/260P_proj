# CompSci 260P Project3 by Tiffany Mejia
# ID:  26843836

import math
import copy

from datetime import datetime

"""
Appoach:  
    Use BnB DFS with upper bound being the cost of picking the minimum available path (greedy algorithm)

    Order locations to search by lowest cost. Prune all paths if path cost is greater than
    cost of best path.

    Navigate until all paths are searched/pruned.

Psuedocode:
    Input: Adjacency graph to navigate
    Output: minimum cost path to navigate all vertices

    global min = 0
    global path = []

    def tsp_dynamic:
        greedy_path = NavigateLowestCost(Graph)
        greedy_cost = costOfJourney(greedy_path, Graph)
        dfs(graph, path=[0], greedy_cost)
        return best_path

    def dfs(path, graph):
        if costOfJourney(current_path) > global min:
            return [] # no path
        elif fully_navigated_path:
            best_path = fully_navigated_path
            min_cost = costOfJourney(fully_navigated_path, graph)
            global path = best_path
            global min = min_cost
        else:
            for every available location to travel, sorted in increasing order:
                dfs (path + next location, graph, greedy cost)
    
    def costOfJourney(path, graph):
        total_cost = 0
        for location in path:
            add location cost to total_cost
        return total_cost
    
"""
class TSP:
    def __init__(self) -> None:
        self.best_path = []
        self.min_cost = 0  
        self.graph = []

    def tsp_dynamic_program(self, graph) -> list:
        """
            A BnB DFS algorithm to solve TSP with given graph

            @param graph: (list) Adjaceny Matrix

            @return (list) Shortest path to travel all nodes
        """
        self.graph = graph
        self.best_path = self.greedy_path(self.graph)
        self.min_cost = self.costOfJourney(self.best_path, self.graph) # will be upper bound cost
        self.dfs()

        # print(self.best_path)
        # print(self.min_cost)

        self.costOfJourney(self.best_path, self.graph, 1)
        return self.best_path

    def dfs(self, path: list = [0]):
        """
            Depth first search of the graph class variable

            @param path: (list) Current navigation path

            @return None
        """
        if len(path) == len(self.best_path) - 1:
            path.append(0) #navigated through all locations, add location 0 to path

        if self.min_cost < self.costOfJourney(path, self.graph):
            return # Prune path since it is the exceeding minimum path
        
        elif len(path) ==  len(self.best_path): #path is less than current minimum
            self.best_path = copy.deepcopy(path)
            self.min_cost = self.costOfJourney(path, self.graph)
            # print(f"BEST: {self.best_path}")
            # print(f"COST: {self.min_cost}")
            return
        else:
            current_v = path[-1]
            location_order_list = self.order_locations(path, self.graph[current_v])
            for location in location_order_list:
                potential_path = copy.deepcopy(path)
                potential_path.append(location)
                # print(f"~~~ Location to visit from {current_v} -> {location}")
                self.dfs(potential_path)


    def costOfJourney(self, path: list, graph: list, verbose = 0):
        """
            Find the cost of the given journey

            @param path: (list) Path list 

            @return: (int) cost of path
        """
        total_cost = 0
        for location in range(len(path) - 1):
            start_loc = path[location]
            end_loc = path[location + 1]
            if verbose == 1:
                print(f"Traveling from {start_loc} -> {end_loc}: {graph[start_loc][end_loc]}")
            total_cost += graph[start_loc][end_loc]
        if verbose == 1:
            print(f"TOTAL: {total_cost}\nPATH: {path}")
        return total_cost

    def greedy_path(self, graph):
        """
            Find the greedy TSP path of the given graph

            @param graph: (list) Adjaceny Matrix

            @return (list) greedy path to travel all nodes
        """
        current_location = 0 # always starting at vertex 0
        path = [0]

        for vertex in graph:
            min_cost = math.inf
            min_v = -1
            current_v = graph[path[-1]]
            for i in range(len(vertex)):
                if i == current_location:
                    continue # cannot cycle through the same location. Also the cost will be inf/0
                elif i in path:
                    continue # current edge already visited
                else:
                    cost_i = current_v[i]
                    if cost_i < min_cost: # found a location will smaller cost than current local cost
                        min_cost = cost_i
                        min_v = i
            
            if min_v != -1: # still navigating all locations
                path.append(min_v)
            
            else: # All vertex have been visited so return back to location 0
                path.append(0)
        return path
    
    def order_locations(self, path, vertex_list):
        #heuristics be used here
        v_dict = {x: vertex_list[x] for x in range(len(vertex_list))}
        sorted_dict = dict(sorted(v_dict.items(), key=lambda item: item[1]))
        for key in sorted_dict.keys():
            if key in path: #remove visited nodes
                v_dict.pop(key)
        sorted_dict = dict(sorted(v_dict.items(), key=lambda item: item[1])) # redo sort of smaller pruned list      
        return list(sorted_dict.keys())


# Main used to test algorithm
# O(N!) time complexity worst case
if __name__ == "__main__":
    # Optimal: cities 0-7-4-3-9-5-2-6-1-10-8-0 = 253km
    tester = [  [0,   29, 20, 21, 16, 31, 100, 12, 4,   31, 18],
                [29,  0,  15, 29, 28, 40, 72,  21, 29,  41, 12],
                [20,  15, 0,  15, 14, 25, 81,  9,  23,  27, 13],
                [21,  29, 15, 0,  4,  12, 92,  12, 25,  13, 25],
                [16,  28, 14, 4,  0,  16, 94,  9,  20,  16, 22],
                [31,  40, 25, 12, 16, 0,  95,  24, 36,  3,  37],
                [100, 72, 81, 92, 94, 95, 0,   90, 101, 99, 84],
                [12,  21, 9,  12, 9,  24, 90,  0,  15,  25, 13],
                [4,   29, 23, 25, 20, 36, 101, 15, 0,   35, 18],
                [31,  41, 27, 13, 16, 3,  99,  25, 35,  0,  38],
                [18,  12, 13, 25, 22, 37, 84,  13, 18,  38, 0]] 

    # optimal cost = 126
    # tester = [  [0, 3, 93, 13, 33, 9, 57],
    #             [4,  0, 77, 42, 21, 16, 34],
    #             [45, 17, 0, 36, 16, 28, 25],
    #             [39, 90, 80, 0, 56, 7, 91],
    #             [28, 46, 88, 33, 0, 25, 57],
    #             [3,  88, 18, 46, 92, 0, 7],
    #             [44, 26, 33, 27, 84, 39, 0]]
    

    th = TSP()

    start = datetime.now()
    path = th.tsp_dynamic_program(tester)
    end = datetime.now()

    timedelta = (end-start).total_seconds()
    print(f"Time to execute tsp: {timedelta}")
    

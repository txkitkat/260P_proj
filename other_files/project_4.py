# CompSci 260P Project4, #1 by Tiffany Mejia
# ID:  26843836

#The double-tree algorithm for TSP
# Input is a weighted NxN graph
import copy
import time
import math
from datetime import datetime
from INPUT_TSP import tester3
from collections import defaultdict

class Project4:
    def __init__(self) -> None:
        self.total_v = 0
        self.visited = defaultdict(list)  # Dependent on the amount of nodes
        self.path = []
        self.retravel_edges = {} # (i:j)

    def doubletree(self, graph: list):
        """
            Double tree algorithm optimized for weighted graph input for 
            Traveling Salesman Problem
        """
        self.__init__()
        mst = self.minimum_spanning_tree(graph)
        self.closed_path(mst) #finds closed loop path/euler circuit from MST
        hamiltonian_path = []
        for cell in self.path: # Find hamiltonian path using closed path from MST
            start_loc, end_loc = cell
            if hamiltonian_path == []:
                hamiltonian_path.append(start_loc)
                hamiltonian_path.append(end_loc)
            elif end_loc not in hamiltonian_path:
                hamiltonian_path.append(end_loc)
            elif start_loc not in hamiltonian_path:
                hamiltonian_path.append(start_loc)
            else:
                continue
        hamiltonian_path.append(hamiltonian_path[0])
        self.costOfJourney(hamiltonian_path, graph, 1)
        return hamiltonian_path # Final path from algorithm. Not optimal path but close approximation
    
    def minimum_spanning_tree(self, graph: list):
        """
            Uses Krushkals Algorithm to find the minimum spanning tree in
            a weighted graph

        """
        verticies = len(graph) # graph will be nxn matrix with n verticies
        self.total_v = verticies

        mst = []*verticies # initializes MST adacency matrix
        for i in range(verticies):
            mst.append([])

        edges = {} # dictionary of edges w their cost
        for i in range(verticies):
            for j in range(verticies):
                if i == j or graph[i][j] == 0 or graph[i][j] == 'Inf': # Skip when cycling on the same index, or no path exists (0/Inf)
                    continue
                edge_tuple = (i, j)
                edge_tuple_inv = (j, i)
                if edge_tuple in edges.keys() or edge_tuple_inv in edges.keys(): # edge already saved
                    continue
                else:
                    edges[edge_tuple] = graph[i][j]

        sorted_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # redo sort of smaller pruned list

        visited = []

        for cell in sorted_edges.keys():
            if len(visited) == verticies - 1: # MST has been formed, no need to see remaining edges
                break
            vertex_1 = cell[0]
            vertex_2 = cell[1]
            is_cycle = self.is_cycle(cell, mst)
            if not is_cycle: # Path is not a cycle and can be added to the tree
                mst[vertex_1].append(vertex_2)
                mst[vertex_2].append(vertex_1)
                visited.append(cell)
        print(mst)
        return mst

    def is_cycle(self, cell: tuple, current_mst: list):
        """
            Adjust the current MST with the new potential edge to see if the added edge will
            create a cycle in the MST.

            @param cell: (tuple): Edge in tree (i, j) from i to j
            @param current_mst: (list) Current edges that are contained in MST

            @return: (bool) True or False if the current cell causes a cycle
        """
        v_1 = cell[0]
        v_2 = cell[1]
        temp_mst = copy.deepcopy(current_mst)
        temp_mst[v_1].append(v_2)
        temp_mst[v_2].append(v_1)
        cycle = self.dfs(v_1, temp_mst, []) # check if dfs can be performed
        return cycle
    
    def dfs(self, start_v, current_mst, visited=[]):
        """
            Runs DFS to check if there is a cycle in the new potential MST

        """
        if visited == []: # Nothing has been visited except the starting node
            visited = [start_v]

        elif len(visited) == self.total_v: # if all nodes have been visited, there cannot be a cycle
            return False
        
        next_nodes = current_mst[start_v]
        for node in next_nodes:
            temp_visited = copy.deepcopy(visited)
            if node in visited: # a cycle was formed
                return True 
            else:
                temp_visited.append(node)
                current_mst[node].remove(start_v) # clean out navigated edges to not affect visited logic above
                result = self.dfs(node, current_mst, temp_visited)
                if not result:
                    visited.append(node)
                else:
                    return result
        return False


    def closed_path(self, graph: list, node: int = None) -> None:
        """
            find closed path of adacency matrix 
            
            @param graph: (list) list[list[int]] adjacency matrix to check
            @param node: (int) Node to expand and attempt to travel from

            @return: None
        """
        if node is None: # find the best node to start with which is the node with least amount of edges
            min_e = math.inf
            for i in range(len(graph)):
                if len(graph[i]) < min_e:
                    min_e = len(graph[i])
                    node = i
                if min_e == 1:
                    break

        possible_travel = graph[node]
        for next_n in possible_travel: # Navigate to all adjacent nodes of current node
            if len(self.path) == (self.total_v -1)*2: # Done, all possible edges have been navigated twice
                return
            cell = (node, next_n)
            if self.visited.get(node, []) == [] or (self.visited.get(node, []) != [] and next_n not in self.visited[node]):
                if node in self.visited.get(next_n, []): # find that trying to go back and forth along an edge
                    self.retravel_edges[node] = next_n #travel back after other nodes have been navigated
                else:
                    self.visited[node].append(next_n) 
                    self.path.append(cell)
                    self.closed_path(graph, next_n) #transerve through the whole path of the adjacent node

            else:  
                if len(self.visited[node]) == len(graph[node]) and len(self.path) < (self.total_v - 1)*2: #Rare condition where we need to backtrack since we hit a loop
                    if len(self.path) != (self.total_v -1)*2:
                        self.retravel_edges[self.path[-1][0]] = self.path[-1][1] # hit a loop and need to go back to previous node
                        del self.path[-1]                                           # need to remove last node from path as it formed a loop
                        del self.visited[self.visited[node][-1]][-1] 
                        return
                continue

        if self.retravel_edges.get(node, None) is not None: 
                self.visited[node].append(self.retravel_edges[node])
                self.path.append((node, self.retravel_edges[node])) 

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
            print(f"TOTAL: {total_cost: 0.3f}\nPATH: {path}")
        return total_cost
    


if __name__ == "__main__":
    # Optimal: cities 0-7-4-3-9-5-2-6-1-10-8-0 = 253km
    tester1 = [  [0,   29, 20, 21, 16, 31, 100, 12, 4,   31, 18],
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
    tester2 = [  [0, 3, 93, 13, 33, 9, 57],
                [4,  0, 77, 42, 21, 16, 34],
                [45, 17, 0, 36, 16, 28, 25],
                [39, 90, 80, 0, 56, 7, 91],
                [28, 46, 88, 33, 0, 25, 57],
                [3,  88, 18, 46, 92, 0, 7],
                [44, 26, 33, 27, 84, 39, 0]]
    

    th = Project4()
    th.doubletree(tester1)
    th.doubletree(tester2)

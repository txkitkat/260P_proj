# CompSci 260P Final Project by Tiffany Mejia
# ID:  26843836

import copy
import time
import math
from datetime import datetime
from random import randint
from collections import defaultdict

class FinalProject:
    def __init__(self) -> None:
        self.total_v = 0
        self.visited = defaultdict(list)  # Dependent on the amount of nodes
        self.path = []
        self.retravel_edges = {} # (i:j)

    def nearest_neighbor(self, graph: list):
        self.__init__()
        n = len(graph)
        start_node = randint(0, n-1)
        self.path.append(start_node)
        for i in range(n): # find nearest_neighbor based on random start
            min_edge = math.inf
            min_node = -1
            current_node = self.path[-1]
            edges = graph[current_node]
            for indx in range(len(edges)): # last visited node
                edge = graph[self.path[-1]][indx]
                if edge < min_edge and indx not in self.path:
                    min_edge = edge
                    min_node = indx
            if min_node != -1:
                self.path.append(min_node)
        self.path.append(start_node)
        return self.costOfJourney(self.path, graph)

    def christofides(self, graph:list):
        self.__init__()
        mst = self.minimum_spanning_tree(graph)
        return self.find_min_wighted_graph(mst, graph)

    def doubletree(self, graph: list):
        """
            Double tree algorithm optimized for weighted graph input for 
            Traveling Salesman Problem
        """
        self.__init__()
        mst = self.minimum_spanning_tree(graph)
        # print(mst)
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
        return self.costOfJourney(hamiltonian_path, graph)
    
    def find_min_wighted_graph(self, mst: list, graph):
        """
            Computed the min wrighted grph using the vertices with odd edges
        """ 
        odd_vertices = [] # contains the list of all V with odd number of edges in the tree
        for i in range(len(mst)):
            vertex_edges = mst[i]
            if len(vertex_edges)%2 == 1:
                odd_vertices.append(i)

        min_weight_perfect_match = [] # list of edges that need to be included
        while odd_vertices:
            v = odd_vertices.pop()
            length = float("inf")
            u = 1
            closest = -1
            for u in odd_vertices:
                if v != u and graph[v][u] < length:
                    length = graph[v][u]
                    closest = u
            if closest != -1:
                min_weight_perfect_match.append((v, closest))
                mst[v].append(closest)
                mst[closest].append(v)
                odd_vertices.remove(closest)
        self.closed_path(mst)
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
        return self.costOfJourney(hamiltonian_path, graph)
        

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
        result = []
        new_graph = []
        sub_graph = copy.deepcopy(graph)

        for i in range(len(sub_graph)):
            for j in range(len(sub_graph)):
                if i != j:
                    edge = (i, j, sub_graph[i][j])
                    new_graph.append(edge)

        new_graph = sorted(new_graph,key=lambda item: item[2]) # sort all items in graph by smallest weight edge
        parent = [] 
        rank = []
        i = 0
        e = 0

        # Create V subsets with single elements
        for v in range(len(sub_graph)):
            parent.append(v)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < (len(sub_graph) - 1):

            u, v, w = new_graph[i] # pick smallest current edge
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent ,v)

            # If including this edge does't cause cycle, include it
            if x != y:
                e = e + 1 # increment edges
                result.append([u,v,w])
                self.union(parent, rank, x, y)            
            # Else discard the edge

        for edge in result:
            mst[edge[0]].append(edge[1])
            mst[edge[1]].append(edge[0])
        return mst

    def find(self, parent: list, i: int):
        """
            Given the list of parent nodes, find the parent of vertex i
        """
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
 
    def union(self, parent: list, rank: list, x: int, y: int):
        """
            Does a union of sets of vertex u and v using rank
        """
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
 
        if rank[xroot] < rank[yroot]:    # Attach smaller rank tree under root of high rank tree
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
 
        
        else : # If ranks are same, then make one as root and increment
            parent[yroot] = xroot
            rank[yroot] += 1
 
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
            if len(self.path) == (self.total_v - 1)*2: # Done, all possible edges have been navigated twice
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
    import os
    import numpy as np
    th = FinalProject()
    #Ensure change to path that will be used for test data generation
    if os.path.exists("results.txt"):
        os.remove("results.txt")
    # home_dir = "data_sets_holding3/"
    # for filename in os.listdir(home_dir):
    #     test = []
    #     data_test = np.load(f"{home_dir}{filename}", allow_pickle=False)
    #     for item in data_test:
    #         test.append(list(item))
    #     start_1 = datetime.now()
    #     c1 = th.nearest_neighbor(test)
    #     start_2 = datetime.now()
    #     c2 = th.doubletree(test)
    #     start_3 = datetime.now()
    #     c3 = th.christofides(test)
    #     end = datetime.now()
    #     t1 = (start_2-start_1).total_seconds()
    #     t2 = (start_3-start_2).total_seconds()
    #     t3 = (end-start_3).total_seconds()
    #     costs = f"{c1}, {c2}, {c3}, {t1}, {t2}, {t3}\n"
    #     print(costs)
    #     with open('results.txt','a') as tfile:
    #         tfile.write(costs)



    test = []
    data_test = np.load(f"500_100.npy", allow_pickle=False)
    for item in data_test:
        test.append(list(item))
    start_1 = datetime.now()
    c1 = th.nearest_neighbor(test)
    start_2 = datetime.now()
    c2 = th.doubletree(test)
    start_3 = datetime.now()
    c3 = th.christofides(test)
    end = datetime.now()
    t1 = (start_2-start_1).total_seconds()
    t2 = (start_3-start_2).total_seconds()
    t3 = (end-start_3).total_seconds()
    costs = f"{c1}, {c2}, {c3}, {t1}, {t2}, {t3}\n"
    print(costs)
    with open('results.txt','a') as tfile:
        tfile.write(costs)
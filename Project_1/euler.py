# CompSci 260P Project1, #1 by Tiffany Mejia
# ID:  26843836

# I want to know: can I walk along the graph from a vertex of my (or your) choice and 
# walk across each edge exactly once? I cannot omit an edge from my walk, nor may I walk across an edge more than once.
# I am allowed to revisit vertices as necessary, and a similar problem with visiting vertices
# once each is probably harder to solve efficiently than this one.

# A graph where I can produce such a walk, but it begins and ends at different vertices,
# is said to have an Eulerian Walk. If I can produce such a walk, but it begins and ends 
# at the same vertex, the graph is said to have an Eulerian Circuit.

from collections import defaultdict
class Problem1:
    def __init__(self) -> None:
        self.visited = defaultdict(list)  # Dependent on the amount of nodes
        self.odd_count = 0
        self.event_count = 0
        self.v_odd = {} #append all verticies with odd edges 
        self.path_list = []
        self.end_reached = False
        self.edge_total = 0

    def checkForEucler(self, graph: list) -> list:
        """
            Check if given graph is a euler path, euler circuit, orNone
            
            @param graph: (list) list[list[int]] graph to check

            @return: (list) Path, if empty, there is no path 
        """
        self.__init__()
        for node in range(len(graph)):
            edges = graph[node]
            self.edge_total += len(edges)
            if len(edges)%2 == 1: # ODD:
                self.odd_count += 1
                self.v_odd[node] = edges

            else: # EVEN
                self.event_count += 1

            if self.odd_count > 2:
                print("No euler path or ciruit is possible.")
                return [] # No possible Euler path or circuit
        
        if self.odd_count > 0: # max is 2
            print("Euler path Found")
            min_v = -1
            min_l = -1
            for v, length in self.v_odd.items():
                if min_v == -1 or length < min_l:
                    min_v = v
                    min_l = length
            start_node = min_v #pick node with min edge count
        else:
            print("Euler Circuit Found")
            start_node = 0 # arbituary

        self.euler_circuit_path(graph, start_node) # dont matter
        return self.path_list

    def euler_circuit_path(self, graph: list, node: int) -> None:
        """
            Check if given graph is a euler path, euler circuit, orNone
            
            @param graph: (list) list[list[int]] graph to check
            @param node: (int) Node to expand and attempt to travel from

            @return: None
        """
        possible_travel = graph[node]
        # print(f"\n~~~~~Start node: {node}")
        for next_n in possible_travel:
            # print(f"next node: {next_n}")
            if self.end_reached == True:
                return
            if self.visited.get(next_n, []) == [] or (self.visited.get(node, []) != [] and next_n not in self.visited[node]):
                self.visited[node].append(next_n)
                self.visited[next_n].append(node)
                self.path_list.append(node)
                self.euler_circuit_path(graph, next_n)
            else:  
                if len(self.visited[node]) == len(graph[node]) and not self.end_reached:
                    if len(self.path_list) != (self.edge_total/2):
                        del self.path_list[-1]
                        # print(f"--Go back, {node}, {self.visited[node][-1]}, TOTAL: {self.edge_total/2}")
                        del self.visited[self.visited[node][-1]][-1]
                        del self.visited[node][-1]
                        return
                    else:
                        self.path_list.append(node) 
                        self.end_reached = True
                continue


# Main used to test algorithm
if __name__ == "__main__":
    test_class = Problem1()
    test_1 = [[1,2,3], [0,2], [1,0], [0,4], [3]]                        # expect [0, 1, 2, 0, 3, 4]
    test_2 = [[1,2], [0,2,3], [0,1,3], [1,2]]                           # expect [2, 0, 1, 2, 3, 1]
    test_3 = [[1,2,3,4], [0,2], [0,1,4,5], [0,4], [0,2,3,5], [2, 4]]    # expect cycle: [0, 1, 2, 0, 3, 4, 2, 5, 4, 0]
    x = test_class.checkForEucler(test_1)
    print(x)
    y = test_class.checkForEucler(test_2)
    print(y)
    z = test_class.checkForEucler(test_3)
    print(z)
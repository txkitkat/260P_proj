# CompSci 260P Project1, #1 by Tiffany Mejia
# ID:  26843836

# I want to know: can I walk along the graph from a vertex of my (or your) choice and 
# walk across each edge exactly once? I cannot omit an edge from my walk, nor may I walk across an edge more than once.
# I am allowed to revisit vertices as necessary, and a similar problem with visiting vertices
# once each is probably harder to solve efficiently than this one.

# A graph where I can produce such a walk, but it begins and ends at different vertices,
# is said to have an Eulerian Walk. If I can produce such a walk, but it begins and ends 
# at the same vertex, the graph is said to have an Eulerian Circuit.


class Problem1:
    def __init__(self) -> None:
        self.visited = []  # Dependent on the amount of nodes
        self.odd_count = 0
        self.event_count = 0
        self.v_odd = [] #append all verticies with odd edges 

    def checkForEucler(self, graph: list) -> int:
        #list[list[int]]
        # TODO
        for node in len(graph):
            edges = graph[node]
            if len(edges)%2 == 1: # ODD:
                self.odd_count += 1
                self.v_odd.append(node) 
            
            else: # EVEN
                self.event_count += 1

            if self.odd_count > 2:
                return 0 # No possible Euler path or circuit
        if self.odd_count == 0:
            # Euler circuit
            path_list = self.euler_circuit_path(graph)

    def euler_circuit_path(self, graph:list):
        #returns path list
        pass # find the euler circuit path



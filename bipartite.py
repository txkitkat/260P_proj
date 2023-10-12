# CompSci 260P Project1, #3 by Tiffany Mejia
# ID:  26843836


# A simple, undirected graph is called bipartite if we can perform the following. 
# You are given two crayons, one blue and one gold. You want to color in each vertex in such a way that:
#     Each vertex is exactly one color -- none are omitted, and none are both blue and gold.
#     Each edge has two endpoints of different colors.

# Test cases
# [[1,2,3],[0,2],[0,1,3],[0,2]]
# [[1,3],[0,2],[1,3],[0,2]]

class Problem3:
    def __init__(self) -> None:
        self.visited = {}


    def isBipartite(self, graph: list, n: int = 0) -> bool:
        """
            Function determines if given inut graph is a bipirite graph
            
            @param graph: (list) list[list[int]] graph to check
            @param n: (int) test node to start search, default is 0

            @return: (bool) Is or is not Bipartite
        """
        if self.visited.get(n, None) is None:
            self.visited[n] = True # initialize start of graph iteration 
        try:   
            for neighbor in graph[n]:
                if not self.search(graph, neighbor, True):
                    return False
            return True
        except IndexError: 
            print("Invalid test node given. Give valid node to test within given graph range.")

    def search(self, graph: list, node: int, before_color: bool) -> bool:
        """
            Search function to check or assign color to nodes.
            
            @param graph: (list) list[list[int]] graph to check
            @param n: (int) test node 
            @param before_color: (bool) Color type as a True or False value

            @return: (bool) True or false if node found with matching color as a connected node
        """
        if self.visited.get(node, None) is not None:
            return self.visited.get(node) != before_color
        self.visited[node] = not before_color
     
        neighbors  = graph[node]
        for n in neighbors:
            if not self.search(graph, n, not(before_color)):
                return False
        return True

if __name__ == "__main__":
    test_class = Problem3()
    test_1 = [[1,2,3],[0,2],[0,1,3],[0,2]]  # expect False
    test_2 = [[1,3],[0,2],[1,3],[0,2]]      # expect True
    x = test_class.isBipartite(test_1, 0)
    print(x)
    y = test_class.isBipartite(test_2, 0)
    print(y)
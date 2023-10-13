# CompSci 260P Project1, #2 by Tiffany Mejia
# ID:  26843836

# Inspritation Sources:
# https://www.interviewcake.com/concept/java/topological-sort#:~:text=The%20topological%20sort%20algorithm%20takes,is%20called%20a%20topological%20ordering.
# https://www.geeksforgeeks.org/topological-sorting/

class Problem2:
    def __init__(self) -> None:
        self.visited = []  # Dependent on the amount of nodes
        self.stack = []


    def topologicalSort(self, n: int, dislikes: list) -> list: 
        """
        Function prints out the order of dislikes
            @param n: (int) Amount of dislikes
            @param dislikes: (list[list[int]) Graph of dislikes

            @return: (list) sorted graph
        """
        self.stack = []
        self.visited = [0] * n

        for node in range(n):
            self.sort(dislikes, node)
            if len(self.stack) == n: # already sorted
                break
        reversed_stack = reversed(self.stack)
        return list(reversed_stack)

    def sort(self, graph: list, node: int) -> bool:
        """
            Sort graph in reverse order
            
            @param graph: (list) list[list[int]] graph to check
            @param n: (int) test node 

            @return: (bool) True or false if node found with matching color as a connected node
        """
        # print(f"---{node}---")
        neighbors = graph[node]
        self.visited[node] = True

        if neighbors == [] or neighbors is None: # condition is no directed edges
            self.visited[node] = True
            if node not in self.stack:
                self.stack.append(node)
        
        for next_node in neighbors:
            if not self.iscycle(graph, node, next_node):
                if self.visited[next_node]:
                    if next_node not in self.stack:
                        self.stack.append(node)
                else:
                    self.sort(graph, next_node)
        if node not in self.stack:
            self.stack.append(node)

    def iscycle(self, graph, node, next_node):
        next_neighbors = graph[next_node]
        if node in next_neighbors:
            print("EXCEPTION: Cycle is contained in graph")
            exit(1)
        for node in next_neighbors:
            if self.visited[node] == True and node not in self.stack:
                print("EXCEPTION: Cycle is contained in graph")
                exit(1)


# Main used to test algorithm
if __name__ == "__main__":
    test_class = Problem2()
    test_1 = [[1,2], [3, 4], [3], [4], []]          # expect [0, 2, 1, 3, 4]
    test_2 = [[], [], [3], [1], [0,1], [0,2]]       # expect [5, 4, 2, 3, 1, 0]
    test_3 = [[], [5], [3], [1], [0,1], [0,2]]       # expect cycle
    x = test_class.topologicalSort(len(test_1), test_1)
    print(x)
    y = test_class.topologicalSort(len(test_2), test_2)
    print(y)
    z = test_class.topologicalSort(len(test_3), test_3)
    print(z)
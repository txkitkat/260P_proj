# CompSci 260P Project1, #2 by Tiffany Mejia
# ID:  26843836


class Problem2:
    def __init__(self) -> None:
        self.visited = []  # Dependent on the amount of nodes


    def topologicalSort(self, n: int, dislikes: list) -> list: 
        """
        Function prints out the order of dislikes
            @param n: (int) Amount of dislikes
            @param dislikes: (list[list[int]) Graph of dislikes

            @return: (list) list[list[int]] graph
        """
        #TODO
        self.visited = [False] * n
        pass
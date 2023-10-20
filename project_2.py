import random
import copy

class Project2:
    def __init__(self):
        self.dimension = 0
        self.G = None
        self.path = [] # list of tuples

    def solve(self, G: list, start_health: int = 0):
        """
            @param G: 2D given graph maze
            @param start_health: (int) start health of player, assumming 0 for testing
        """
        self.dimension = len(G)
        self.G = G
        return self.find_best_path(0, 0, health=start_health) #start

    def find_best_path(self, row: int, col: int, path: list = [], health: int = 0, p_perk:int = 0, d_perk: int = 0):
        cell_tuple = (row, col)
        path.append(cell_tuple)
        if row == self.dimension - 1 and col == self.dimension - 1:
            return health, path
        elif row == self.dimension or col  == self.dimension:
            return -1, path # hit edge condition without meeting goal
        
        else:
            cell_val = self.G[row][col]
            health_check = True #above 0 health
            if cell_val == "P":
                p_perk = 1
            elif cell_val == "D":
                d_perk = 1
            else:
                health_check, info = self.adjust_heatlh(int(cell_val), health, p_perk, d_perk)
                health = info['health']
                p_perk = info['p_perk']
                d_perk = info['d_perk']

            if health_check:
                print(f"Current: {cell_tuple}, health: {health}")
                
                right_move = self.find_best_path(row, col + 1, copy.deepcopy(path), health, p_perk, d_perk)
                down_move  = self.find_best_path(row + 1, col, copy.deepcopy(path), health, p_perk, d_perk)

                # return max path
                if right_move[0] > down_move[0]:
                    return right_move
                else:
                    return down_move
            else:
                return -1, path

    def adjust_heatlh(self, cell_value: int, health: int, p_perk, d_perk):
        health_check = True
        if cell_value > 0:
            if d_perk:
                health = health + cell_value*2
                d_perk = 0
            else:
                health = health + cell_value
        elif cell_value < 0:
            if not p_perk:
                health = health - cell_value
                p_perk = 0

        if health > 1000:
            health = 1000

        elif health <= 0:
            health_check = False
        
        info = {
            "health": health,
            "p_perk": p_perk,
            "d_perk": d_perk
        }

        return health_check, info
    
    @staticmethod
    def generate_2d_matrix(N: int = 2):
        test_list = []
        for _ in range (N):
            row = []
            for _ in range(N):
                rand_v = random.randrange(-100, 200 + 1)
                possible_v = [str(rand_v), "P", "D"]
                index = random.randint(0,2)
                row.append(possible_v[index])
            test_list.append(row)

        for item in test_list:
            print(item)
        
        return test_list


# Main used to test algorithm
if __name__ == "__main__":
    test_list = [['P', '19', 'D', 'D', 'P'],
                 ['D', 'P', 'D', 'D', 'P'],
                 ['171', 'D', 'D', '123', 'D'],
                 ['P', '-11', 'P', 'P', 'P'],
                 ['-41', 'D', 'P', 'P', 'P']] # expect 588 max given health start is 4
    c = Project2()
    h, path = c.solve(test_list)
    print(f"Max: {h}")
    for i in path:
        print(i)
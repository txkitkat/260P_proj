# CompSci 260P Project2 by Tiffany Mejia
# ID:  26843836

# This algorithm goes at O(N^2) time complexity. 

import random
import copy

class Project2:
    def __init__(self):
        self.dimension = 0
        self.G = None
        self.possible_path = {} # list of tuples

    def solve(self, G: list, start_health: int = 0):
        """
            @param G: 2D given graph maze
            @param start_health: (int) start health of player, assumming 0 for testing

            @return max and path. if min = -1, No path found 
        """
        self.dimension = len(G)
        self.G = G
        self.find_best_path(0, 0) #start
        health, path =  self.possible_path.get('min', -1), self.possible_path.get('best_path', [])
        self.show_path_nav(path, health)
        return path

    def find_best_path(self, row: int, col: int, path: list = [], health: int = 0, 
                       p_perk:int = 0, d_perk: int = 0, min_health: int = 0):
        cell_tuple = (row, col)
        path.append(cell_tuple)
        
        if self.possible_path.get('min', 1001) == 1: #found a possible min health path
                return 1001, path
        
        if self.possible_path.get('min', 1001) < abs(min_health) + 1: # Can skip path since it is increasing
                return 1001, path
        elif row == self.dimension or col  == self.dimension:
            return 1001, path # hit edge condition without meeting goal
        else:
            cell_val = self.G[row][col]
            if cell_val == "P":
                p_perk = 1
            elif cell_val == "D":
                d_perk = 1
            else:
                info = self.adjust_heatlh(int(cell_val), health, p_perk, d_perk, min_health)
                health = info['health']
                p_perk = info['p_perk']
                d_perk = info['d_perk']
                min_health = info['min_health']

            if row == self.dimension - 1 and col == self.dimension - 1:
                if self.possible_path.get('min', 1001) > (abs(min_health) + 1):
                    self.possible_path['min'] = abs(min_health) + 1
                    self.possible_path['best_path'] = path
                return abs(min_health), path
            
            right_move = self.find_best_path(row, col + 1, copy.deepcopy(path), health, p_perk, d_perk, min_health)
            down_move  = self.find_best_path(row + 1, col, copy.deepcopy(path), health, p_perk, d_perk, min_health)
            
            # return min path closest to 0
            if abs(right_move[0]) < abs(down_move[0]):
                return right_move
            else:
                return down_move
            
    def adjust_heatlh(self, cell_value: int, health: int, p_perk, d_perk, min_health: int = 0):
        """
            adjusts the current health given the current cell value 
            and perks active at this point in the path 
        """
        if cell_value > 0:
            if d_perk:
                health = health + cell_value*2
                d_perk = 0
            else:
                health = health + cell_value
        elif cell_value < 0:
            if not p_perk:
                health = health + cell_value
            else:
                p_perk = 0
                                                                                    
        if health > 1000:
            health = 1000
        if min_health >= health:
            min_health = health
        
        info = {
            "health": health,
            "p_perk": p_perk,
            "d_perk": d_perk,
            "min_health": min_health
        }
        return info

    
    @staticmethod
    def generate_2d_matrix(N: int = 2):
        # for debugging purposes, generates an NxN matrix to test min HP algorithm.
        # Default N = 2. 
        test_list = []
        for _ in range (N):
            row = []
            for _ in range(N):
                rand_v = random.randrange(-100,200)
                rand_v2 = random.randrange(-100, 0)
                rand_v3 = random.randrange(-100, 0)
                possible_v = [str(rand_v), str(rand_v2), "P", "D", str(rand_v3)]
                index = random.randint(0,3)
                row.append(possible_v[index])
            test_list.append(row)

        for item in test_list:
            print(item)
        
        return test_list
    
    def show_path_nav(self, path, start_health):
        print(f"Minimum start health: {start_health}")
        current_health = start_health
        p_perk = 0
        d_perk = 0
        for cell in path:
            row, col = cell
            cell_val = self.G[row][col]
            new_health = current_health
            if cell_val == "P":
                p_perk = 1
            elif cell_val == "D":
                d_perk = 1
            else:
                info = self.adjust_heatlh(int(cell_val), current_health, p_perk, d_perk)
                new_health = info['health']
                p_perk = info['p_perk']
                d_perk = info['d_perk']
            print(f"cell: {cell}, start health: {current_health}, cell_val: {cell_val}, new health: {new_health}")
            current_health = new_health


# Main used to test algorithm
if __name__ == "__main__":

    # test_list = [['D', 'P', 'P', 'P', '-59', 'P', '-36', '-45', '-42', 'D'],
    #             ['36', '193', '-72', '-59', '-91', '198', '-46', '164', '36', 'P'],
    #             ['D', 'P', '-67', 'P', 'D', '-95', '-1', '115', '142', '73'],
    #             ['-24', '-83', 'D', 'P', 'P', 'P', '188', '-24', '193', '-83'],
    #             ['146', '-29', '115', '-80', '-32', '-23', '-5', '132', '-1', '108'],
    #             ['D', '47', 'D', '97', '-43', 'D', 'D', '-100', 'P', '-46'],
    #             ['83', 'D', 'P', 'D', '-43', '-4', '-14', '-69', '-59', 'D'],
    #             ['-45', '31', '-85', 'P', 'P', '55', 'D', '-19', 'D', 'D'],
    #             ['P', '-4', '-14', '132', '-32', '71', 'D', '75', 'D', '-80'],
    #             ['P', '-82', '-18', '-28', 'D', 'P', '160', 'D', '-75', 'P']] # min health  = 1

    c = Project2()
    # the following is my testcase generator for Project 2
    # Given that a testcase may have N^2 time, I leave the size of N
    # as 10. Max wait time calculated for worst case scenario with N=10 
    # is roughly 30s on my Desktop. The above list is my base testcase.
    test_list = c.generate_2d_matrix(10)
    path = c.solve(test_list)

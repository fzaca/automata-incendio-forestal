from copy import deepcopy
from random import randint, choice
import numpy as np

class Automata:
    def __init__(self):
        self.size = (50, 50)
        self.options_size = ['25x25', '50x50', '100x100', '200x200', '250x250']

        self.burn_prob = 0.3
        self.points_of_fire = 0.99
        self.noise_grid()

    def update_generation(self):
        new_grid = deepcopy(self.grid)
        for dy, row in enumerate(self.grid):
            for dx, col in enumerate(row):
                # Neighbours
                nb  = self.neighbours(dy, dx)
                # Rules # 0.1 0.3
                if col == 1 and nb.count(2) > 0 and probability(self.burn_prob, True, False): new_grid[dy][dx] = 2
                if col == 2: new_grid[dy][dx] = 3
        self.grid = new_grid

    def neighbours(self, y, x):
        global nb
        if y == 0 or x == 0 or y == len(self.grid)-1 or x == len(self.grid[0])-1:
            if y == 0 and x == 0:
                nb = [self.grid[y][x-1], self.grid[y+1][x+1], self.grid[y+1][x]]
            elif y == 0 and x == len(self.grid[0])-1:
                nb = [self.grid[y][x-1], self.grid[y+1][x-1], self.grid[y+1][x]]
            elif y == len(self.grid)-1 and x == 0:
                nb = [self.grid[y-1][x], self.grid[y-1][x+1], self.grid[y][x+1]]
            elif y == len(self.grid)-1 and x == len(self.grid[0])-1:
                nb = [self.grid[y-1][x], self.grid[y-1][x-1], self.grid[y][x-1]]
            elif y == 0 and (x > 0 and x < len(self.grid[0])-1):
                nb = [self.grid[y][x-1], self.grid[y+1][x-1], self.grid[y+1][x], self.grid[y+1][x+1], self.grid[y][x+1]]
            elif y == len(self.grid)-1 and (x > 0 and x < len(self.grid[0])-1):
                nb = [self.grid[y][x-1], self.grid[y-1][x-1], self.grid[y-1][x], self.grid[y-1][x+1], self.grid[y][x+1]]
        else:
            nb = [ 
                self.grid[y-1][x-1], self.grid[y-1][x],
                self.grid[y-1][x+1], self.grid[y][x-1],
                self.grid[y][x+1], self.grid[y+1][x-1],
                self.grid[y+1][x], self.grid[y+1][x+1]
            ]
        return nb

    def noise_grid(self):
        self.grid = np.array([[probability(self.points_of_fire, 1, 2) for col in range(self.size[0])] for row in range(self.size[1])])

    def clear_grid(self):
        self.grid = np.zeros(self.size) 

    def setSize(self, reso):
        reso = reso.split('x')
        reso = int(reso[0]), int(reso[1])
        self.size = (tuple(reso))
        self.noise_grid()

def probability(prob, a, b):
    list_prob = [a] * int(prob*100) + [b] * int((1-prob)*100)
    return choice(list_prob)
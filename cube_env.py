import random
import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
from cube_class import cube

class CubeEnv:
    def __init__(self, scramble_depth=1):
        self.scramble_depth = scramble_depth
        self.cube = cube()
        self.moves = [
            self.cube.move_u, self.cube.move_u_inv,
            self.cube.move_r, self.cube.move_r_inv,
            self.cube.move_l, self.cube.move_l_inv,
            self.cube.move_f, self.cube.move_f_inv,
            self.cube.move_b, self.cube.move_b_inv,
            self.cube.move_d, self.cube.move_d_inv,
        ]
    
    def reset(self):
        self.cube = cube()
        for _ in range(self.scramble_depth):
            random.choice(self.moves)()
        
        return self.cube.to_one_hot()
    
    def step(self, action):
        self.moves[action]()
        obs = self.cube.to_one_hot()
        solved = self.cube.is_solved()
        reward = 0 if solved else -1
        done = solved
        return obs, reward, done
    

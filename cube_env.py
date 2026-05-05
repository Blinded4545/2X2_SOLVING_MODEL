import random
import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
from cube_class import cube

class CubeEnv:
    def __init__(self, scramble_depth=2, max_steps=30, ndim = 3):
        self.max_steps = max_steps
        self.scramble_depth = scramble_depth
        self.steps = 0
        self.last_action = None # IMPLEMENTAR LUEGO
        self.ndim = ndim
        self.cube = cube(ndim=ndim)
        self.moves = [
            self.cube.move_u, self.cube.move_u_inv,
            self.cube.move_r, self.cube.move_r_inv,
            self.cube.move_l, self.cube.move_l_inv,
            self.cube.move_f, self.cube.move_f_inv,
            self.cube.move_b, self.cube.move_b_inv,
            self.cube.move_d, self.cube.move_d_inv,
        ]
        self.move_names = [
            "move_u", "move_u_inv",
            "move_r", "move_r_inv",
            "move_l", "move_l_inv",
            "move_f", "move_f_inv",
            "move_b", "move_b_inv",
            "move_d", "move_d_inv"
        ]
    
    def is_inverse(self, a, b):
        return (a // 2 == b // 2) and (a % 2 != b % 2)
    
    
    def reset(self):
        self.steps = 0
        self.cube = cube(self.ndim)
        last_move = None
        moves_done=[]
        for i in range(self.scramble_depth):
            move = random.randint(0, 11)
            if last_move is not None and self.is_inverse(move, last_move):
                continue
            
            getattr(self.cube, self.move_names[move])()
            
            last_move = move
            moves_done.append(self.move_names[move])
            
        print(moves_done)
        self.cube.plt_faces(i, self.move_names[move])
        
        
        return self.cube.to_one_hot()
    
    def step(self, action):
        prev_dist = self.cube.distance()
        
        getattr(self.cube, self.move_names[action])()
        
        obs = self.cube.to_one_hot()
        new_dist = self.cube.distance()
        
        if self.cube.is_solved():
            reward = 200
            done = True
        else:
            reward = prev_dist - new_dist
            done = False
        
        self.steps += 1
        if self.steps >= self.max_steps:
            done = False
        return obs, reward, done
    
    def test_moves(self):
        self.cube = cube(ndim=self.ndim)
        moves_done = []
        for i in range(12):
            j = random.randint(0, 11)
            while j in moves_done: 
                j = random.randint(0, 11)
            
            getattr(self.cube, self.move_names[j])()
            moves_done.append(j)
            print(self.move_names[j])
            self.cube.plt_faces(i, self.move_names[j])

import matplotlib.pyplot as plt
from cube_net_print import print_net

class cube:
    def __init__(self):
        self.TOP = 0
        self.LEFT = 1
        self.FRONT = 2
        self.RIGHT = 3
        self.DOWN = 4
        self.BACK = 5
        
        self.faces=[
            [1, 1, 1, 1],  # 0 -> top
            [2, 2, 2, 2],  # 1 -> left
            [3, 3, 3, 3],  # 2 -> front
            [4, 4, 4, 4],  # 3 -> right
            [5, 5, 5, 5],  # 4 -> down
            [6, 6, 6, 6],  # 5 -> back
        ]
        
        self.color_map = {
            1: "blue",
            2: "orange",
            3: "white",
            4: "red",
            5: "green",
            6: "yellow"
        }
    
    def move_r(self):
        old_faces = self.faces
        top = [old_faces[0][0], old_faces[2][1], old_faces[0][2], old_faces[2][3]]
        front = [old_faces[2][0], old_faces[4][1], old_faces[2][2], old_faces[4][3]]
        down = [old_faces[4][0], old_faces[5][1], old_faces[4][2], old_faces[5][3]]
        back = [old_faces[0][3], old_faces[5][1], old_faces[0][1], old_faces[5][3]]
        right = [old_faces[3][2], old_faces[3][0], old_faces[3][3], old_faces[3][1]]
        
        left = old_faces[1]
        
        self.faces = [top, left, front, right, down, back]

    def move_r_inv(self):
        old_faces = self.faces
        top = [old_faces[0][0], old_faces[5][2], old_faces[0][2], old_faces[5][0]]
        front = [old_faces[2][0], old_faces[0][1], old_faces[2][2], old_faces[0][3]]
        down = [old_faces[4][0], old_faces[2][1], old_faces[4][2], old_faces[2][3]]
        back = [old_faces[4][3], old_faces[5][1], old_faces[4][1], old_faces[5][3]]
        right = [old_faces[3][1], old_faces[3][3], old_faces[3][0], old_faces[3][2]]
        
        left = old_faces[1]
        
        self.faces = [top, left, front, right, down, back]

    def move_l(self):
        old_faces = self.faces
        top = [old_faces[5][0], old_faces[0][1], old_faces[5][2], old_faces[0][3]]
        front = [old_faces[0][0], old_faces[2][1], old_faces[0][2], old_faces[2][3]]
        down = [old_faces[2][0], old_faces[4][1], old_faces[2][2], old_faces[4][3]]
        back = [old_faces[5][0], old_faces[4][2], old_faces[5][2], old_faces[4][3]]
        left = [old_faces[1][2], old_faces[1][0], old_faces[1][3], old_faces[1][1]]
        
        right = old_faces[3]
        
        self.faces = [top, left, front, right, down, back]

    def move_l_inv(self):
        old_faces = self.faces
        top = [old_faces[2][0], old_faces[0][1], old_faces[2][2], old_faces[0][3]]
        front = [old_faces[4][0], old_faces[2][1], old_faces[4][2], old_faces[2][3]]
        down = [old_faces[5][0], old_faces[4][1], old_faces[5][2], old_faces[4][3]]
        back = [old_faces[5][0], old_faces[0][1], old_faces[5][2], old_faces[0][3]]
        left = [old_faces[1][1], old_faces[1][3], old_faces[1][0], old_faces[1][2]]
        
        right = old_faces[3]
        
        self.faces = [top, left, front, right, down, back]
        
    def move_f(self):
        old_faces = self.faces
        top = [old_faces[0][0], old_faces[0][1], old_faces[1][1], old_faces[1][3]]
        left = [old_faces[1][0], old_faces[4][1], old_faces[1][2], old_faces[4][3]]
        down = [old_faces[3][2], old_faces[3][0], old_faces[4][2], old_faces[4][3]]
        right = [old_faces[0][2], old_faces[3][1], old_faces[0][3], old_faces[3][3]]
        front = [old_faces[2][2], old_faces[2][0], old_faces[2][3], old_faces[2][1]]
        
        back = old_faces[5]
        
        self.faces = [top, left, front, right, down, back]
        
    def move_f_inv(self):
        old_faces = self.faces
        top = [old_faces[0][0], old_faces[0][1], old_faces[3][0], old_faces[3][2]]
        left = [old_faces[1][0], old_faces[0][3], old_faces[1][2], old_faces[0][2]]
        down = [old_faces[1][1], old_faces[1][3], old_faces[4][2], old_faces[4][3]]
        right = [old_faces[4][1], old_faces[3][1], old_faces[4][0], old_faces[3][3]]
        front = [old_faces[2][1], old_faces[2][3], old_faces[2][0], old_faces[2][2]]
        
        back = old_faces[5]
        
        self.faces = [top, left, front, right, down, back]
    
    def move_b(self):
        old_faces = self.faces
        top = [old_faces[3][1], old_faces[3][3], old_faces[0][2], old_faces[0][3]]
        left = [old_faces[0][1], old_faces[1][1], old_faces[0][0], old_faces[1][3]]
        down = [old_faces[4][0], old_faces[4][1], old_faces[1][0], old_faces[1][2]]
        right = [old_faces[3][0], old_faces[4][3], old_faces[3][2], old_faces[4][2]]
        back = [old_faces[5][2], old_faces[5][0], old_faces[5][3], old_faces[5][1]]
        
        front = old_faces[2]
        
        self.faces = [top, left, front, right, down, back]
        
    def move_b_inv(self):
        old_faces = self.faces
        top = [old_faces[1][2], old_faces[1][0], old_faces[0][2], old_faces[0][3]]
        left = [old_faces[4][2], old_faces[1][1], old_faces[4][3], old_faces[1][3]]
        down = [old_faces[4][0], old_faces[4][1], old_faces[3][3], old_faces[3][1]]
        right = [old_faces[3][0], old_faces[0][0], old_faces[3][2], old_faces[0][1]]
        back = [old_faces[5][1], old_faces[5][3], old_faces[5][0], old_faces[5][2]]
        
        front = old_faces[2]
        
        self.faces = [top, left, front, right, down, back]
    
    def move_u(self):
        old_faces = self.faces
        top = [old_faces[0][2], old_faces[0][0], old_faces[0][3], old_faces[0][1]]
        left = [old_faces[2][0], old_faces[2][1], old_faces[1][2], old_faces[1][3]]
        front = [old_faces[3][0], old_faces[3][1], old_faces[2][2], old_faces[2][3]]
        right = [old_faces[5][0], old_faces[5][1], old_faces[3][2], old_faces[3][3]]
        back = [old_faces[1][0], old_faces[1][1], old_faces[5][2], old_faces[5][3]]
        
        down = old_faces[4]
        
        self.faces = [top, left, front, right, down, back]
        
    def move_u_inv(self):
        old_faces = self.faces
        top = [old_faces[0][1], old_faces[0][3], old_faces[0][0], old_faces[0][2]]
        left = [old_faces[5][0], old_faces[5][1], old_faces[1][2], old_faces[1][3]]
        front = [old_faces[1][0], old_faces[1][1], old_faces[2][2], old_faces[2][3]]
        right = [old_faces[2][0], old_faces[2][1], old_faces[3][2], old_faces[3][3]]
        back = [old_faces[3][0], old_faces[3][1], old_faces[5][2], old_faces[5][3]]
        
        down = old_faces[4]
        
        self.faces = [top, left, front, right, down, back]
    
    def move_d(self):
        old_faces = self.faces
        left = [old_faces[1][0], old_faces[1][1], old_faces[5][2], old_faces[5][3]]
        front = [old_faces[2][0], old_faces[2][1], old_faces[1][2], old_faces[1][3]]
        right = [old_faces[3][0], old_faces[3][1], old_faces[2][2], old_faces[2][3]]
        down = [old_faces[4][2], old_faces[4][0], old_faces[4][3], old_faces[4][1]]
        back = [old_faces[5][0], old_faces[5][1], old_faces[3][2], old_faces[3][3]]
        
        top = old_faces[0]
        
        self.faces = [top, left, front, right, down, back]
        
    def move_d_inv(self):
        old_faces = self.faces
        left = [old_faces[1][0], old_faces[1][1], old_faces[2][2], old_faces[2][3]]
        front = [old_faces[2][0], old_faces[2][1], old_faces[3][2], old_faces[3][3]]
        right = [old_faces[3][0], old_faces[3][1], old_faces[5][2], old_faces[5][3]]
        down = [old_faces[4][1], old_faces[4][3], old_faces[4][0], old_faces[4][2]]
        back = [old_faces[5][0], old_faces[5][1], old_faces[1][2], old_faces[1][3]]
        
        top = old_faces[0]
        
        self.faces = [top, left, front, right, down, back]
    
    def to_one_hot(self):
        import numpy as np
        vector = []
        for face in self.faces:
            for color in face:
                one_hot = [0] * 6
                one_hot[color - 1] = 1
                vector.extend(one_hot)
        return np.array(vector, dtype=np.float32)
    
    def is_solved(self):
        return all(len(set(face)) == 1 for face in self.faces)
    
    def distance(self):
        return sum([len(set(face))-1 for face in self.faces])
    
    def print_cube(self):
        print_net(self.faces)
        print('\n')
        
    def plt_faces(self):
        titles = ["Top", "Left", "Front", "Right", "Down", "Back"]
        fig, axs = plt.subplots(2, 3, figsize=(8, 6))
        
        for idx, ax in enumerate(axs.flat):
            face = self.faces[idx]
            
            for i in range(2):
                for j in range(2):
                    val=face[i*2 + j]
                    color = self.color_map[val]
                    square = plt.Rectangle((j, 1-i), 1, 1, facecolor=color, edgecolor='black')
                    ax.add_patch(square)
        
            ax.set_xlim(0, 2)
            ax.set_ylim(0, 2)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(titles[idx])
            
        plt.tight_layout()
        plt.show()
        
        
   
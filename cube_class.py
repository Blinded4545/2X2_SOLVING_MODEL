import matplotlib.pyplot as plt
import numpy as np
from cube_net_print import print_net

class cube:
    def __init__(self, ndim=3):
        self.TOP = 0
        self.LEFT = 1
        self.FRONT = 2
        self.RIGHT = 3
        self.DOWN = 4
        self.BACK = 5
        self.ndim = ndim
        self.dimensions = (ndim, ndim)
        self.face = np.zeros((ndim, ndim))
        
        self.faces=[np.full((ndim, ndim), i+1) for i in range(6)]
        
        self.color_map = {
            1: "yellow",
            2: "orange",
            3: "blue",
            4: "red",
            5: "white",
            6: "green"
        }
    
    def move_r(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][:, n-1].copy()
        front = self.faces[2][:, n-1].copy()
        down  = self.faces[4][:, n-1].copy()
        back  = self.faces[5][:, 0].copy()

        new_faces[0][:, n-1] = front
        new_faces[2][:, n-1] = down
        new_faces[4][:, n-1] = back[::-1]
        new_faces[5][:, 0] = top[::-1]

        new_faces[3] = np.rot90(self.faces[3], k=-1)

        self.faces = new_faces

    def move_r_inv(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][:, n-1].copy()
        front = self.faces[2][:, n-1].copy()
        down  = self.faces[4][:, n-1].copy()
        back  = self.faces[5][:, 0].copy()

        new_faces[0][:, n-1] = back[::-1]
        new_faces[2][:, n-1] = top
        new_faces[4][:, n-1] = front
        new_faces[5][:, 0] = down[::-1]

        new_faces[3] = np.rot90(self.faces[3], k=1)

        self.faces = new_faces

    def move_l(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][:, 0].copy()
        front = self.faces[2][:, 0].copy()
        down  = self.faces[4][:, 0].copy()
        back  = self.faces[5][:, n-1].copy()

        new_faces[0][:, 0] = back[::-1]
        new_faces[2][:, 0] = top
        new_faces[4][:, 0] = front
        new_faces[5][:, n-1] = down[::-1]

        new_faces[1] = np.rot90(self.faces[1], k=-1)

        self.faces = new_faces

    def move_l_inv(self):
        
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][:, 0].copy()
        front = self.faces[2][:, 0].copy()
        down  = self.faces[4][:, 0].copy()
        back  = self.faces[5][:, n-1].copy()

        new_faces[0][:, 0] = front
        new_faces[2][:, 0] = down
        new_faces[4][:, 0] = back[::-1]
        new_faces[5][:, n-1] = top[::-1]

        new_faces[1] = np.rot90(self.faces[1], k=1)

        self.faces = new_faces
        
    def move_f(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        # Guardar referencias
        top = self.faces[0][n-1, :].copy()
        left = self.faces[1][:, n-1].copy()
        down = self.faces[4][0, :].copy()
        right = self.faces[3][:, 0].copy()

        # Ciclo con flips correctos
        new_faces[0][n-1, :] = left[::-1]
        new_faces[3][:, 0]   = top
        new_faces[4][0, :]   = right[::-1]
        new_faces[1][:, n-1] = down

        # Rotar cara frontal
        new_faces[2] = np.rot90(self.faces[2], k=-1)

        self.faces = new_faces
        
    def move_f_inv(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top = self.faces[0][n-1, :].copy()
        left = self.faces[1][:, n-1].copy()
        down = self.faces[4][0, :].copy()
        right = self.faces[3][:, 0].copy()

        new_faces[0][n-1, :] = right
        new_faces[1][:, n-1] = top[::-1]
        new_faces[4][0, :]   = left
        new_faces[3][:, 0]   = down[::-1]

        new_faces[2] = np.rot90(self.faces[2], k=1)

        self.faces = new_faces
    
    def move_b(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][0, :].copy()
        left  = self.faces[1][:, 0].copy()
        down  = self.faces[4][n-1, :].copy()
        right = self.faces[3][:, n-1].copy()

        new_faces[0][0, :]   = right
        new_faces[1][:, 0]   = top[::-1]
        new_faces[4][n-1, :] = left[::-1]
        new_faces[3][:, n-1] = down[::-1]

        new_faces[5] = np.rot90(self.faces[5], k=-1)

        self.faces = new_faces
        
    def move_b_inv(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        top   = self.faces[0][0, :].copy()
        left  = self.faces[1][:, 0].copy()
        down  = self.faces[4][n-1, :].copy()
        right = self.faces[3][:, n-1].copy()

        new_faces[0][0, :]   = left[::-1]
        new_faces[3][:, n-1] = top
        new_faces[4][n-1, :] = right[::-1]
        new_faces[1][:, 0]   = down

        new_faces[5] = np.rot90(self.faces[5], k=1)

        self.faces = new_faces
    
    def move_u(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        left  = self.faces[1][0, :].copy()
        front = self.faces[2][0, :].copy()
        right = self.faces[3][0, :].copy()
        back  = self.faces[5][0, :].copy()

        new_faces[1][0, :] = front
        new_faces[2][0, :] = right
        new_faces[3][0, :] = back
        new_faces[5][0, :] = left

        new_faces[0] = np.rot90(self.faces[0], k=-1)

        self.faces = new_faces
        
    def move_u_inv(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        left  = self.faces[1][0, :].copy()
        front = self.faces[2][0, :].copy()
        right = self.faces[3][0, :].copy()
        back  = self.faces[5][0, :].copy()

        new_faces[1][0, :] = back
        new_faces[2][0, :] = left
        new_faces[3][0, :] = front
        new_faces[5][0, :] = right

        new_faces[0] = np.rot90(self.faces[0], k=1)

        self.faces = new_faces
    
    def move_d(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        left  = self.faces[1][n-1, :].copy()
        front = self.faces[2][n-1, :].copy()
        right = self.faces[3][n-1, :].copy()
        back  = self.faces[5][n-1, :].copy()

        new_faces[1][n-1, :] = back
        new_faces[2][n-1, :] = left
        new_faces[3][n-1, :] = front
        new_faces[5][n-1, :] = right

        new_faces[4] = np.rot90(self.faces[4], k=-1)

        self.faces = new_faces
        
    def move_d_inv(self):
        new_faces = [np.copy(f) for f in self.faces]
        n = self.ndim

        left  = self.faces[1][n-1, :].copy()
        front = self.faces[2][n-1, :].copy()
        right = self.faces[3][n-1, :].copy()
        back  = self.faces[5][n-1, :].copy()

        new_faces[1][n-1, :] = front
        new_faces[2][n-1, :] = right
        new_faces[3][n-1, :] = back
        new_faces[5][n-1, :] = left

        new_faces[4] = np.rot90(self.faces[4], k=1)

        self.faces = new_faces
    
    def to_one_hot(self):
        vector = []
        
        for face in self.faces:
            for i in range(self.ndim):
                for j in range(self.ndim):
                    color = int(face[i, j])
                    one_hot = [0]*6
                    one_hot[color-1] = 1
                    vector.extend(one_hot)
                    
        return np.array(vector, dtype=np.float32)
    
    def from_one_hot(self, vector):
        idx = 0
        faces = []

        for _ in range(6):
            face = np.zeros((self.ndim, self.ndim), dtype=int)
            
            for i in range(self.ndim):
                for j in range(self.ndim):
                    one_hot = vector[idx:idx+6]
                    color = int(np.argmax(one_hot)) + 1
                    face[i, j] = color
                    idx += 6
            
            faces.append(face)
        
        self.faces = faces
    
    def is_cross_solved(self):
        n = self.ndim
        c = n//2
        
        lateral_faces = [1, 2, 3, 5]
        for idx in lateral_faces:
            face = self.faces[idx]
            center_color = int(face[c, c])
            bottom_edge = int(face[n-1, c])
            
            if bottom_edge != center_color:
                return False
        
        down = self.faces[4]
        down_color = int(down[c, c])
        cross_cells = [down[0, c], down[c, 0], down[c, n-1], down[n-1, c]]
        
        if not all(int(cell) == down_color for cell in cross_cells):
            return False
        
        return True
    
    def is_f2l_solved(self):
        n = self.ndim
        c = n//2
        
        lateral_faces = [1, 2, 3, 5]
        for idx in lateral_faces:
            face = self.faces[idx]
            center_color = int(face[c, c])
            lower_half = np.concatenate(face[1, :])
            if np.mean(lower_half) != center_color:
                return False
            
        down = self.faces[4]
        down_color = int(down[c, c])
        for i in range(n):
            if not all (down[i, :] == down_color):
                return False
        
        return True
    
    def is_oll_cross_solved(self): #ESTO ES PARA EL FRIDRICH REDUCIDO
        n = self.ndim
        c = n//2
        
        top = self.faces[0]
        top_color = int(top[c, c])
        cross_cells = [top[0, c], top[c, 0], top[c, n-1], top[n-1, c]]
        
        if not all(int(cell) == top_color for cell in cross_cells):
            return False
        
        return True
    
    
    def is_oll_solved(self):
        n = self.ndim
        c = n//2
        
        top = self.faces[0]
        top_color = int(top[c, c])
        
        if not all(top == top_color):
            return False
        
        return True
    
    def is_solved(self):
        for face in self.faces:
            if not np.all(face == face[0,0]):
                return False
        return True
    
    def distance(self):
        dist = 0
        
        for face in self.faces:
            center_color = face[0,0]
            dist += np.sum(face != center_color)
        
        return dist
    
    def print_cube(self):
        faces_list = [face.tolist() for face in self.faces]
        print_net(faces_list)
        print('\n')
        
    def step_print(self, step):
        faces_list = [face.tolist() for face in self.faces]
        print_net(faces_list, step=step)
        print('\n')
        
    def plt_faces(self, step=0, move=""):
        titles = ["Top", "Left", "Front", "Right", "Down", "Back"]
        fig, axs = plt.subplots(2, 3, figsize=(8, 6))
        fig.suptitle(f"Step: {step} | Move: {move}")
        
        for idx, ax in enumerate(axs.flat):
            face = self.faces[idx]
            
            for i in range(self.ndim):
                for j in range(self.ndim):
                    val = int(face[i, j])
                    color = self.color_map[val]
                    
                    square = plt.Rectangle(
                        (j, self.ndim-1-i),  # invertir eje Y
                        1, 1,
                        facecolor=color,
                        edgecolor='black'
                    )
                    ax.add_patch(square)
            
            ax.set_xlim(0, self.ndim)
            ax.set_ylim(0, self.ndim)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(titles[idx])
        
        plt.tight_layout()
        plt.show()
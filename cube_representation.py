
import numpy as np
import random
from cube_class import cube
from cube_env import CubeEnv


cubeenv = CubeEnv(3)
cubeenv.scramble_depth=20

cubeenv.reset()

# new_cube = cube(ndim=3)

# new_cube.move_u()
# new_cube.move_f()
# new_cube.print_cube()
# new_cube.move_l_inv()
# new_cube.print_cube()
# new_cube.move_l_inv()

# new_cube.print_cube()
# new_cube.plt_faces()

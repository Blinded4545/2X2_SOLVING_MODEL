import gymnasium as gym

# env = gym.make("2X2-SOLVER", render_mode="rgb_array")

for i in gym.envs.registry.keys():
    print(i)
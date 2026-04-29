from dqn_agent import DQNAgent
from cube_env import CubeEnv
from rewards_analysis import graphicate
import numpy as np

np.random.seed(0)

episodes = 100

rewards_per_episode = []

def train(agent, env, episodes=500):
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        
        while True:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            
            agent.buffer.add(state, action, reward, next_state, done)
            
            if episode%4==0:
                agent.train_step()
            state = next_state
            total_reward += reward
            
            if done:
                break
        agent.decay_epsilon()
        agent.rewards_per_episode.append(total_reward)
        success = 1 if env.cube.is_solved() else 0
        agent.success_history.append(success)
        
        if episode%50 == 0 or episode == episodes-1:
            print(f"Ep {episode} | Reward: {total_reward} | Eps: {agent.epsilon:.3f}")
        if episode%300 == 0:
            env.scramble_depth += 1
            
def test(agent, env):
    agent.epsilon = 0
    success = 0
    trials = 100
    for _ in range(trials):
        state = env.reset()
        for _ in range(50):
            action = agent.select_action(state)
            state, reward, done = env.step(action)
            
            if done and env.cube.is_solved():
                success += 1
                break
    
    print(success/trials)            
            
env = CubeEnv()
agent = DQNAgent()

train(agent, env, 5000)

graphicate(agent)

test(agent, env)
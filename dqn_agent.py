import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)
    
    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        return(
            torch.tensor(np.array(states), dtype=torch.float32),
            torch.tensor(np.array(actions), dtype=torch.long),
            torch.tensor(np.array(rewards), dtype=torch.float32),
            torch.tensor(np.array(next_states), dtypes=torch.float32),
            torch.tensor(np.array(dones), dtype=torch.float32)
        )
    
    def __len__(self):
        return len(self.buffer)
    
    
class DQN(nn.Module):
    def __init__(self, num_inputs, num_actions):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(144, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 12)
        )
    
    def forward(self, x):
        return self.net(x)
    
class DQNAgent:
    def __init__(self, lr=1e-4, gamma=0.99, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.995, batch_size=64, target_update_freq=500):
        
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        self.steps_done = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        
        self.net      = DQN().to(self.device)
        self.target_net = DQN().to(self.device)
        self.target_net.load_state_dict(self.net.state_dict())  # pesos iguales al inicio
        self.target_net.eval()  # la target nunca se entrena directamente

        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.buffer    = ReplayBuffer()
        
    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 11)

        state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.net(state_t)
        return q_values.argmax().item()
    
    def train_step(self):
        if len(self.buffer) < self.batch_size:
            return None
        
        states, actions, rewards, next_states, dones = self.buffer.sample(self.batch_size)
        
        states = states.to(self.device)
        actions = actions.to(self.device)
        rewards = rewards.to(self.device)
        next_states = next_states.to(self.device)
        dones = dones.to(self.device)
        
        current_Q = self.net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_q = self.target_net(next_states).max(1).values
            
        target_q = rewards + self.gamma*next_q*(1-dones)
        
        loss = nn.MSELoss()(current_Q, target_q)
        
        self.optimizer.zero_grad()
        loss.backward()
        
        self.optimizer.step()
        
        self.steps_done += 1
        if self.steps_done%self.target_update_freq==0:
            self.target_net.load_state_dict(self.net.state_dict())
            
        return loss.item()
    
    def decay_epsilon(self):
        self.epsion = max(self.epsilon_min, self.epsion*self.epsiolon_decay)
        
    def save(self, path="model.pth"):
        torch.save(self.net.state_dict(), path)

    def load(self, path="model.pth"):
        self.net.load_state_dict(torch.load(path, map_location=self.device))
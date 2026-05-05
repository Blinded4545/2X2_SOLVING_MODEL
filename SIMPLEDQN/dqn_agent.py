import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    
    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        return(
            torch.from_numpy(np.array(states)).float().to(self.device),
            torch.from_numpy(np.array(actions)).long().to(self.device),
            torch.from_numpy(np.array(rewards)).float().to(self.device),
            torch.from_numpy(np.array(next_states)).float().to(self.device),
            torch.from_numpy(np.array(dones)).float().to(self.device)
        )
    
    def __len__(self):
        return len(self.buffer)
    
    
# class DQN(nn.Module):
#     def __init__(self, num_inputs=144, num_actions=12):
#         super(DQN, self).__init__()
#         self.net = nn.Sequential(
#             nn.Linear(num_inputs, 256),
#             nn.ReLU(),
#             nn.Linear(256, 512),
#             nn.ReLU(),
#             nn.Linear(512, 256),
#             nn.ReLU(),
#             nn.Linear(256, num_actions)
#         )
    
#     def forward(self, x):
#         return self.net(x)
    
class DuelingDQN(nn.Module):
    def __init__(self, num_inputs=144, num_actions=12):
        super(DuelingDQN, self).__init__()
        
        self.feature = nn.Sequential(
            nn.Linear(num_inputs, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU()
        )
        
        self.value = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        
        self.advantage = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )
    
    def forward(self, x):
        x = self.feature(x)
        v = self.value(x)
        A = self.advantage(x)
        Q = v+(A - A.mean(dim=1, keepdim=True))
        
        return Q
class DQNAgent:
    def __init__(self, lr=1e-4, gamma=0.99, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.995, batch_size=64, target_update_freq=200):
        
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        self.steps_done = 0
        self.rewards_per_episode = []
        self.success_history = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        
        self.net = DuelingDQN(num_inputs=144, num_actions=12).to(self.device)
        self.target_net = DuelingDQN(144, 12).to(self.device)
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
        
        current_Q = self.net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_actions = self.net(next_states).argmax(1)
            next_q = self.target_net(next_states).gather(1, next_actions.unsqueeze(1)).squeeze(1)
            
        target_q = rewards + self.gamma*next_q*(1-dones)
        
        loss = nn.SmoothL1Loss()(current_Q, target_q)
        
        self.optimizer.zero_grad()
        loss.backward() #NO CAMBIAR A SMOOTHL1LOSS
        
        self.optimizer.step()
        
        self.steps_done += 1
        if self.steps_done%self.target_update_freq==0:
            self.target_net.load_state_dict(self.net.state_dict())
            
        return loss.item()
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon*self.epsilon_decay)
        
    def save(self, path="model.pth"):
        torch.save(self.net.state_dict(), path)

    def load(self, path="model.pth"):
        self.net.load_state_dict(torch.load(path, map_location=self.device))
import random, copy
import torch
import torch.nn as nn
import numpy as np

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.shared = nn.Sequential(
            nn.Linear(144, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
        )
        self.value_head = nn.Linear(256, 1)
        self.policy_head = nn.Linear(256, 12)
        
    def forward(self, x):
        x = self.shared(x)
        value = self.value_head(x)
        policy = torch.softmax(self.policy_head(x), dim=1)
        
        return value.squeeze(1), policy
    
def generate_states(env, k, l):
    x = []
    depths = []

    for _ in range(l):
        state = env.reset()
        
        for d in range(k):
            action = random.randint(0, 11)
            state, _, _ = env.step(action)
            
            x.append(state)
            depths.append(d)
            
    return x, depths

def get_children(env, state):
    children = []
    
    for a in range(12):
        env.cube.from_one_hot(state)
        env.moves[a]()
        
        next_state = env.cube.to_one_hot()
        children.append((a, next_state))
        
    return children

def compute_targets(net, env, state):
    children = get_children(env, state)
    
    actions = [a for a,_ in children]
    children_states = [child for _, child in children]
    
    children_t = torch.tensor(children_states, dtype=torch.float32)

    with torch.no_grad():
        values, _ = net(children_t)

    values = values.squeeze(1).cpu().numpy()

    # reward por cada hijo
    rewards = []
    for child in children_states:
        env.cube.from_one_hot(child)
        rewards.append(1 if env.cube.is_solved() else -1)

    total_values = np.array(rewards) + values

    best_idx = np.argmax(total_values)
    
    y_v = values[best_idx]
    y_p = actions[best_idx]
    
    return y_v, y_p

def loss_fn(pred_v, pred_p, y_v, y_p):
    value_loss = nn.MSELoss()(pred_v, y_v)
    
    policy_loss = nn.CrossEntropyLoss()(pred_p, y_p)
    
    return value_loss + policy_loss
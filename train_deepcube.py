import torch
from cube_env import CubeEnv
from DEEPCUBE import compute_targets, generate_states, Net, loss_fn

def train_loop(net, env, optimizer, epochs):
    for epoch in range(epochs):
        X, _ = generate_states(env, k=10, l=100)
        
        for state in X:
            y_v, y_p = compute_targets(net, env, state)
            
            y_v = torch.tensor([y_v], dtype=torch.float32)
            y_p = torch.tensor([y_p], dtype=torch.long)
            
            state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            
            pred_v, pred_p = net(state_t)
            
            loss = loss_fn(pred_v=pred_v, pred_p=pred_p, y_p=y_p, y_v=y_v)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        if epoch % 5 == 0 or epoch==epochs-1:
            sr, _ = evaluate(net, env)
            print(f"Epoch {epoch} | SR: {sr:.2f}")
            
def solve(state, net, env):
    for step in range(20):
        state_t = torch.tensor(state).unsqueeze(0)
        _, policy = net(state_t)
        
        action = policy.argmax().item()
        
        state, _, done = env.step(action)
        
        if done:
            return True
        
def evaluate(net, env, num_tests = 50, max_steps=20):
    net.eval()
    success = 0
    steps_list = []
    
    for _ in range(num_tests):
        state = env.reset()
        
        for step in range(max_steps):
            state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            
            with torch.no_grad():
                _, policy = net(state_t)
                
            action = policy.argmax().item()
            state, _, done = env.step(action)
            
            if done:
                success += 1
                steps_list.append(step)
                break
    success_rate = success/num_tests
    avg_steps = sum(steps_list)/len(steps_list) if steps_list else None
    
    return success_rate, avg_steps

net = Net()
env = CubeEnv()

optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)

train_loop(net, env, optimizer, 50)

sr, steps = evaluate(net, env)

print(f"Success Rate: {sr:.2f}")
print(f"Avg Steps: {steps}")
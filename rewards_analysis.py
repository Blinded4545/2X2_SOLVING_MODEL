import matplotlib.pyplot as plt

def graphicate(agent):
    rewards = agent.rewards_per_episode
    successes = agent.success_history
    plt.plot(rewards, label='Reward por episodio')
    
    window = 50
    moving_avg = [sum(rewards[max(0, i-window):i+1])/(i+1 if i < window else window) for i in range(len(rewards))] # Esto funciona raro, pero funciona
    success_rate = [sum(successes[max(0,i-window):i+1])/(i+1 if i < window else window) for i in range(len(successes))]

    
    fig, ax = plt.subplots(1, 2, figsize=(12,4))
    ax[0].plot(moving_avg, label='Media movil(50)', linewidth=2)
    ax[1].plot(success_rate, label='Success rate(50)', linewidth=2)
    
    plt.show()
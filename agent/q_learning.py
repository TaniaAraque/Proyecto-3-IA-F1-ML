import numpy as np
import random

def train_q_learning(env, episodes=10000,
                     alpha=0.1, gamma=0.95,
                     epsilon_start=1.0, epsilon_end=0.05):

    n_states = env.n_states
    n_actions = env.n_actions

    Q = np.zeros((n_states, n_actions))

    epsilon = epsilon_start
    eps_decay = (epsilon_start - epsilon_end) / episodes

    rewards_log = []

    for ep in range(episodes):
        state = env.reset()

        if random.random() < epsilon:
            action = random.randint(0, n_actions - 1)
        else:
            action = int(np.argmax(Q[state]))

        next_state, reward, done, info = env.step(action)
        rewards_log.append(reward)

        target = reward  
        Q[state, action] += alpha * (target - Q[state, action])

        epsilon = max(epsilon_end, epsilon - eps_decay)

    return Q, rewards_log

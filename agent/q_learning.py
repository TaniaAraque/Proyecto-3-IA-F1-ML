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
    
    print(f"Iniciando entrenamiento con {episodes} episodios...")
    print(f"Alpha={alpha}, Gamma={gamma}, Epsilon={epsilon_start}->{epsilon_end}")
    print("-" * 60)

    for ep in range(episodes):
        state = env.reset()

        if random.random() < epsilon:
            action = random.randint(0, n_actions - 1)
        else:
            action = int(np.argmax(Q[state]))

        next_state, reward, done, info = env.step(action)

        # Target: Recompensa inmediata + (Gamma * Valor futuro máximo)
        target = reward

        # Actualización de la Q-Table
        Q[state, action] += alpha * (target - Q[state, action])

        # Decaimiento de Epsilon
        epsilon = max(epsilon_end, epsilon - eps_decay)

        rewards_log.append(reward)
        
        # Imprimir progreso cada cierto número de episodios
        if (ep + 1) % 500 == 0:
            recent_rewards = rewards_log[-500:]
            win_rate = sum(recent_rewards) / len(recent_rewards) * 100
            print(f"Episodio {ep + 1}/{episodes} | Win Rate (últimos 500): {win_rate:.2f}% | Epsilon: {epsilon:.3f}")
    
    print("-" * 60)
    total_wins = sum(rewards_log)
    total_win_rate = (total_wins / episodes) * 100
    print(f"Entrenamiento completado!")
    print(f"Victorias totales: {total_wins}/{episodes} ({total_win_rate:.2f}%)")
    print(f"Q-table final:\n{Q}")
    print("-" * 60)
    
    # Mostrar política óptima aprendida
    print("\n🏆 🏎️  ESTRATEGIA ÓPTIMA APRENDIDA:")
    print("=" * 60)
    
    estados = ["Pole Position", "P2-P3", "P4-P6"]
    acciones = ["Conservadora", "Normal", "Agresiva"]
    emojis = ["🥇", "🥈", "🥉"]
    
    for i, (estado, emoji) in enumerate(zip(estados, emojis)):
        best_action = np.argmax(Q[i])
        best_value = Q[i, best_action]
        win_probability = best_value * 100
        
        print(f"{emoji} Desde {estado}:")
        print(f"   → Estrategia: {acciones[best_action]}")
        print(f"   → Probabilidad de victoria: {win_probability:.2f}%")
        print(f"   → Q-values: Cons={Q[i,0]:.3f}, Norm={Q[i,1]:.3f}, Agre={Q[i,2]:.3f}")
        print()
    
    print("=" * 60)

    return Q, rewards_log


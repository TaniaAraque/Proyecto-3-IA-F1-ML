import numpy as np
from agent.q_learning import train_q_learning
from f1_env.environment import F1NorrisEnv
from utils.visualization import plot_rewards, plot_q_table, plot_policy
from utils.sim_pygame_race import F1RaceSim
import os

if __name__ == "__main__":
    env = F1NorrisEnv()

    print("Entrenando agente Q-learning...")
    Q, rewards = train_q_learning(env, episodes=5000)

    os.makedirs("results", exist_ok=True)
    np.save("results/Q_table.npy", Q)

    print("Generando gráficas...")
    plot_rewards(rewards)
    plot_q_table(Q)
    plot_policy(Q)

    # Descomentar para ejecutar la simulación animada de la carrera

    print("Iniciando simulación animada de carrera...")
    sim = F1RaceSim(env, Q, episodes=150)
    sim.run()
    
    print("Entrenamiento completado. Gráficas guardadas en /results")

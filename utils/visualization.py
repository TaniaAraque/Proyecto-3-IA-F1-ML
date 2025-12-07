import matplotlib.pyplot as plt
import numpy as np
import os

RESULTS_DIR = "results/"

def plot_rewards(rewards):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    plt.figure(figsize=(10,5))
    plt.plot(rewards, alpha=0.7)
    plt.title("Recompensas durante entrenamiento")
    plt.xlabel("Episodio")
    plt.ylabel("Recompensa")
    plt.grid(True)
    plt.savefig(RESULTS_DIR + "reward_curve.png")
    plt.close()


def plot_q_table(Q):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    plt.figure(figsize=(6,4))
    plt.imshow(Q, cmap="viridis")
    plt.colorbar()
    plt.title("Heatmap Q-table")
    plt.xlabel("Acciones (0=Cons,1=Norm,2=Agre)")
    plt.ylabel("Estados")
    plt.savefig(RESULTS_DIR + "Qtable_heatmap.png")
    plt.close()


def plot_policy(Q):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    best_actions = np.argmax(Q, axis=1)

    labels = ["Pole", "P2–P3", "P4–P6"]

    plt.figure(figsize=(6,4))
    plt.bar(labels, best_actions)
    plt.title("Mejor acción por estado")
    plt.ylabel("Acción")
    plt.savefig(RESULTS_DIR + "policy.png")
    plt.close()

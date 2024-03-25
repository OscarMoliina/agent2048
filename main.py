import matplotlib
matplotlib.use('TkAgg')  # Cambia 'TkAgg' por el backend de tu elección

import matplotlib.pyplot as plt

import numpy as np

from agent2048 import Env2048, RandomAgent

def ask() -> int:
    s = 'Choose action:\n\t0: up\n\t1: down\n\t2: left\n\t3: right\n'
    return int(input(s))

def show(rewards, max_values) -> None:
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Gráfica de recompensas por turno
    axs[0].plot(rewards, label='Recompensa por turno')
    axs[0].set_title('Recompensa Acumulada por Turno')
    axs[0].set_xlabel('Turno')
    axs[0].set_ylabel('Recompensa')
    axs[0].legend()
    axs[0].grid(True)

    # Gráfica del valor máximo en el tablero por turno
    axs[1].plot(max_values, label='Valor máximo por turno', color='r')
    axs[1].set_title('Valor Máximo en el Tablero por Turno')
    axs[1].set_xlabel('Turno')
    axs[1].set_ylabel('Valor Máximo')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

def main() -> None:
    env = Env2048()
    agent = RandomAgent()
    
    state = env.reset()
    env.render()

    rewards = []
    max_values = []  

    while True:
        action = agent.choose_action()
        state, reward, terminated, _ = env.step(action)
        rewards.append(reward)
        max_values.append(np.max(state)) 
        env.render()
        print(f"Reward: {reward}")

        if terminated:
            print("Game Over!")
            break

    show(rewards, max_values) 

if __name__ == '__main__':
    main()
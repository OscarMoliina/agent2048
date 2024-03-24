from typing import Tuple
import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt

def ask() -> int:
    s = 'Choose action:\n\t0: up\n\t1: down\n\t2: left\n\t3: right\n'
    return int(input(s))

class Env2048(gym.Env):
    metadata = {
        'render.modes':['console'],
    }

    def __init__(self) -> None:
        super(Env2048,self).__init__()

        # 0: up, 1: down, 2: left, 3: right
        self.action_space = spaces.Discrete(4)
        self.width, self.heigth = 4, 4
        self.observation_space = spaces.Box(low=0, high=2**16, shape=(self.width,self.heigth), dtype=np.int32)

        self.state = None
        self.reset()
    
    def emptycells(self) -> np.ndarray[np.intp]:
        return np.argwhere(self.state == 0)

    def generate(self) -> None:
        emptycells = self.emptycells()
        if list(emptycells):
            cell = emptycells[np.random.choice(len(emptycells))]
            self.state[tuple(cell)] = 2

    def combine(self, lst:list[int], size:int = 4, reverse:bool = False) -> np.ndarray[np.int32]:
        if reverse:
            lst = lst[::-1]
        nonzero = [x for x in lst if x != 0]
        combined = []
        skip = False
        for i in range(len(nonzero)):
            if skip:
                skip = False
                continue
            if i+1 < len(nonzero) and nonzero[i] == nonzero[i+1]:
                combined.append(2*nonzero[i])
                skip = True
            else:
                combined.append(nonzero[i])
        if reverse:
            combined = np.array(combined[::-1] + [0] * (size - len(combined)))
        else:
            combined = np.array([0] * (size - len(combined)) + combined)
        return combined

    def vertical(self,type:str) -> None:
        for idx in range(self.width):
            col = [self.state[i][idx] for i in range(self.heigth)]
            if type == 'up':
                combined = self.combine(lst=col, size=self.heigth, reverse=True)
            else:
                combined = self.combine(lst=col, size=self.heigth, reverse=False)
            for i in range(self.heigth):
                self.state[i][idx] = combined[i]

    def horizontal(self, type:str) -> None:
        for idx in range(self.width):
            row = self.state[idx]
            if type == 'left':
                combined = self.combine(lst=row, size=self.width, reverse=True)
            else:
                combined = self.combine(lst=row, size=self.width, reverse=False)
            self.state[idx] = combined

    def step(self, a):
        ant = self.state.copy()

        if a == 0:
            self.vertical('up')
        elif a == 1:
            self.vertical('down')
        elif a == 2:
            self.horizontal('left')
        elif a == 3:
            self.horizontal('right')

        self.generate()
        reward = int(np.sum(self.state))
        
        terminated = not self.emptycells().size > 0
        info = {}
        
        return self.state, reward, terminated, info
    
    def render(self, mode = 'console'):
        if mode != 'console':
            raise NotImplementedError
        
        print(self.state)
    
    def reset(self) -> np.ndarray[np.int32]:
        self.state = np.zeros((4,4), dtype=np.int32)
        self.generate()
        self.generate()
        return self.state


def main():
    env = Env2048()
    state = env.reset()
    env.render()

    rewards = []

    while True:
        action = ask()
        state, reward, terminated, _ = env.step(action)
        rewards.append(reward)
        env.render()
        print(f"Reward: {reward}")

        if terminated:
            print("Game Over!")
            break

if __name__ == '__main__':
    main()
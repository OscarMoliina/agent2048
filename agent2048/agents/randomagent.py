import random

class RandomAgent:
    def __init__(self) -> None:
        pass
    
    def choose_action(self) -> int:
        return random.randint(0,3)
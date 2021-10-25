import gym
from gym import error, spaces, utils
from gym.utils import seeding

class NoitaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()

    def step(self, action):
        print('\nimplement step\n')

    def reset(self):
        print('\nimplement reset\n')
    
    def render(self, mode='human'):
        print('\nimplement render\n')
    
    def close(self):
        print('\nimplement close\n')
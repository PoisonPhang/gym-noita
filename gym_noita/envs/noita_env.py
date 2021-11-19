import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_noita.util.noita_connection import NoitaConnection

class NoitaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.noita_connection = NoitaConnection()
        self.noita_connection.start()
        self.last_observation = self.noita_connection.state

    def step(self, action):
        observation = self.noita_connection.state
        reward = self.calculate_reward(self.last_observation, observation)
        done = self.noita_connection.is_dead
        info = {}
        return observation, reward, done, info

    def reset(self):
        self.noita_connection = NoitaConnection()
        self.noita_connection.start()
        self.last_observation = self.noita_connection.state
    
    def render(self, mode='human'):
        print('\nimplement render\n')
    
    def close(self):
        print('\nimplement close\n')
    
    def calculate_reward(last, current):
        pass
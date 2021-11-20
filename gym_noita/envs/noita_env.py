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
        reward = self.calculate_reward(observation)
        done = self.noita_connection.is_dead
        info = {}
        self.last_observation = observation
        return observation, reward, done, info

    def reset(self):
        self.noita_connection = NoitaConnection()
        self.noita_connection.start()
        self.last_observation = self.noita_connection.state
    
    def render(self, mode='human'):
        pass
    
    def close(self):
        pass
    
    def calculate_reward(self, current):
        last = self.last_observation
        reward = 0

        if self.noita_connection.is_dead:
            return 0
        
        if last['pos']['y'] > current['pos']['y']:
            reward += 1
        if last['max_hp'] < current['max_hp']:
            reward += 1
        if last['hp'] < current['hp']:
            reward += 1
        if last['money'] < current['money']:
            reward += 1
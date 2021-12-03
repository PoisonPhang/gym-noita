import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import asyncio

from gym_noita.util.noita_connection import NoitaConnection
from gym_noita.util.controller_input import ControllerInput

MAX_ENEMIES_TRACKED = 30

class NoitaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.controller_input = ControllerInput()
        self.noita_connection = NoitaConnection()
        
        self.action_space = spaces.Tuple((
            spaces.Box(low=-1, high=1, shape=(2,), dtype=float), # move
            spaces.Box(low=-1, high=1, shape=(2,), dtype=float), # aim
            spaces.Discrete(0), # kick
            spaces.Discrete(0), # attack
            spaces.Discrete(0), # toggle flight
        ))

        self.observation_space = spaces.Dict({
            'position': spaces.Box(low=1000000, high=1000000, shape=(2,), dtype=float), # player position (x,y)
            'hp': spaces.Box(low=0, high=100, shape=(1,), dtype=float), # player hp
            'max_hp': spaces.Box(low=0, high=100, shape=(1,), dtype=float), # player max hp
            'money': spaces.Box(low=0, high=1000000, shape=(1,), dtype=float), # player money
            'north_blocked': spaces.Discrete(2), # if direction is blocked
            'northeast_blocked': spaces.Discrete(2), # if direction is blocked
            'east_blocked': spaces.Discrete(2), # if direction is blocked
            'southeast_blocked': spaces.Discrete(2), # if direction is blocked
            'south_blocked': spaces.Discrete(2), # if direction is blocked
            'southwest_blocked':spaces.Discrete(2),  # if direction is blocked
            'west_blocked': spaces.Discrete(2), # if direction is blocked
            'northwest_blocked': spaces.Discrete(2), # if direction is blocked
            'enemies': spaces.Box(low=1000000, high=1000000, shape=(MAX_ENEMIES_TRACKED, 4), dtype=float) # enemies (enemy type, x, y, has line of sight)
        })

    def step(self, action):
        action_index = action[0]
        act = self.controller_input.ACTION_LOOKUP[action_index]
        param = action[1][action_index][0]
        self.controller_input.perform_action(act, param) 

        observation = self.json_to_state(self.noita_connection.state) 
        reward = self.calculate_reward(observation)
        done = self.noita_connection.is_dead
        info = {}
        self.last_observation = observation
        return observation, reward, done, info

    def reset(self):
        self.noita_connection = NoitaConnection()
        self.controller_input = ControllerInput()
        asyncio.run(self.noita_connection.start())
        self.last_observation = self.noita_connection.state
    
    def render(self, mode='human'):
        pass
    
    def calculate_reward(self, current):
        last = self.last_observation
        reward = 0

        if self.noita_connection.is_dead:
            return 0
        
        reward += np.clip(0, None, current['position']['y']) / 100 # Reward agent for moving down 

        if last['max_hp'] < current['max_hp']: # Reward agent for increasing max hp
            reward += 1
        if last['hp'] < current['hp']: # Reward agent for healing
            reward += 1
        if last['money'] < current['money']: # Reward agent for getting money
            reward += 1

    def json_to_state(self, json_state):
        state = {}
        player_x = json_state['pos']['x']
        player_y = json_state['pos']['y']
        player_hp = json_state['hp']
        player_max_hp = json_state['max_hp']
        player_money = json_state['money']
        enemies = []

        for enemy in json_state[enemies]:
            enemies.append([1, enemy['x'], enemy['y'], enemy['has_shot']])
            if len(enemies) >= MAX_ENEMIES_TRACKED:
                break
        
        state['position'] = [player_x, player_y]
        state['hp'] = [player_hp]
        state['max_hp'] = [player_max_hp]
        state['money'] = [player_money]
        state['north_blocked'] = json_state['north_blocked']
        state['northeast_blocked'] = json_state['northeast_blocked']
        state['east_blocked'] = json_state['east_blocked']
        state['southeast_blocked'] = json_state['southeast_blocked']
        state['south_blocked'] = json_state['south_blocked']
        state['southwest_blocked'] = json_state['southwest_blocked']
        state['west_blocked'] = json_state['west_blocked']
        state['northwest_blocked'] = json_state['northwest_blocked']
        state['enemies'] = enemies
        
        return state

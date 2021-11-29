import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_noita.util.noita_connection import NoitaConnection

MAX_ENEMIES_TRACKED = 30

class NoitaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.noita_connection = NoitaConnection()
        self.noita_connection.start()
        self.last_observation = self.noita_connection.state
        
        self.action_space = spaces.Tuple(
            spaces.Box(low=-2, high=1, shape=2), # move
            spaces.Box(low=-2, high=1, shape=2), # aim
            spaces.Discrete(0), # kick
            spaces.Discrete(0), # attack
            spaces.Discrete(0), # toggle flight
        )

        self.observation_space = spaces.Dict({
            'position': spaces.Box(shape=2), # player position (x,y)
            'hp': spaces.Box(low=0, shape=1), # player hp
            'max_hp': spaces.Box(low=0, shape=1), # player max hp
            'money': spaces.Box(low=0, shape=1), # player money:7
            'enemies': spaces.Box(low=0, shape=(MAX_ENEMIES_TRACKED, 4)) # enemies (enemy type, x, y, has line of sight)
        })

    def step(self, action):

        observation = self.json_to_state(self.noita_connection.state) 
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
        
        if last['pos']['y'] - current['pos']['y'] > 30: # Reward agent for moving down
            reward += 1
        if last['max_hp'] < current['max_hp']: # Reward agent for increasing max hp
            reward += 1
        if last['hp'] < current['hp']: # Reward agent for healing
            reward += 1
        if last['money'] < current['money']: # Reward agent for getting money
            reward += 1

    def json_to_state(json_state):
        state = {}
        player_x = json_state['pos']['x']
        player_y = json_state['pos']['y']
        player_hp = json_state['hp']
        player_max_hp = json_state['max_hp']
        player_money = json_state['money']
        enemies = []

        for enemy in json_state[enemies]:
            enemies.append([1, enemy['x'], enemy['y'], enemy['has_shot']])
            if len(enemies >= MAX_ENEMIES_TRACKED):
                break
        
        state['position'] = [player_x, player_y]
        state['hp'] = [player_hp]
        state['max_hp'] = [player_max_hp]
        state['money'] = [player_money]
        state['enemies'] = enemies
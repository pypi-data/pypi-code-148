import gymnasium as gym
from gymnasium import spaces
class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    def __init__(self):
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(2)
        self.reward_range = (-1, 1)
        self.additional_info = None
    def step(self, action):
        observation = self.observation_space.sample()
        reward = 1.0
        done = True
        info = {}
        return observation, reward, done, info
    def reset(self):
        observation = self.observation_space.sample()
        info = {}
        #print(observation)
        return observation,info  # reward, done, info can't be included
    def render(self, mode="human"):
        pass
    def close(self):
        pass

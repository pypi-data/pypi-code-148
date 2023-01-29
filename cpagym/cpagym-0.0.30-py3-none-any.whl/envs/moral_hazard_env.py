import gymnasium as gym
from gymnasium import spaces
import numpy as np
class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    def __init__(self):
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(2)
        self.reward_range = (-1, 1)
        self.additional_info = None
    def transition(self):
        pass
    def reward(self, x, a, y):
        pass
    def step(self, action):
        observation = self.observation_space.sample()
        reward = 1.0
        terminated = True
        info = {}
        truncated = False
        return observation, reward, terminated, truncated, info
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation = self.observation_space.sample()
        info = {}
        #print(observation)
        return observation,info  # reward, done, info can't be included
    def render(self, mode="human"):
        pass
    def close(self):
        pass
if __name__ == '__main__':
    a=Moral_HazardEnv()
    print(a.action_space)
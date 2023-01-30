import gymnasium as gym
from gymnasium import spaces
import numpy as np
class AsymmetricInfoEnv(gym.Env):
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
        if action == 0:
            if self.additional_info is None:
                reward = -1
            else:
                reward = 1
        else:
            reward = 0
        terminated = False
        info = {}
        truncated = False
        return observation, reward, terminated, truncated, info
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.additional_info = None
        info = {}
        return 0,info
    def provide_additional_info(self, info):
        self.additional_info = info
    def render(self, mode="human"):
        pass
    def close(self):
        pass
if __name__ == '__main__':
    a=AsymmetricInfoEnv()
    print(a.action_space)
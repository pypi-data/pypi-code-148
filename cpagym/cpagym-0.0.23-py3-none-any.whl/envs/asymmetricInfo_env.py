import gymnasium as gym
from gymnasium import spaces
class AsymmetricInfoEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    def __init__(self):
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(2)
        self.reward_range = (-1, 1)
        self.additional_info = None
    def step(self, action):
        observation = self.observation_space.sample()
        if action == 0:
            if self.additional_info is None:
                reward = -1
            else:
                reward = 1
        else:
            reward = 0
        done = False
        info = {}
        return observation, reward, done, info
    def reset(self):
        self.additional_info = None
        info = {}
        return 0,info
    def provide_additional_info(self, info):
        self.additional_info = info
    def render(self, mode="human"):
        pass
    def close(self):
        pass
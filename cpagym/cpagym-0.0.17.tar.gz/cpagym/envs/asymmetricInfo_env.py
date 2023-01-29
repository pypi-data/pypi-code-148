import gym
from gym import spaces
class AsymmetricInfoEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(2)
        self.reward_range = (-1, 1)
        self.additional_info = None

    def step(self, action):
        if action == 0:
            if self.additional_info is None:
                reward = -1
            else:
                reward = 1
        else:
            reward = 0

        return self.additional_info, reward, False, {}
    def reset(self):
        self.additional_info = None
        return 0
    def provide_additional_info(self, info):
        self.additional_info = info
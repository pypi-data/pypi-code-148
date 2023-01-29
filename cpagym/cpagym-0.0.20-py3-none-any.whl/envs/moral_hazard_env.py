import gymnasium as gym
from gymnasium import spaces
class Moral_HazardEnv(gym.Env):
     def __init__(self):
         self.observation_space = spaces.Discrete(2)
         self.action_space = spaces.Discrete(2)
         self.reward_range = (-1, 1)
         self.additional_info = None

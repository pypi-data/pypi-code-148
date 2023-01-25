import abc
import random
from typing import Optional, Tuple
import torch
import numpy as np


class BaseEnvTrait(abc.ABC):
    @property
    @abc.abstractmethod
    def renderable(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def observation_dim(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def action_dim(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def action_n(self):
        raise NotImplementedError

    @abc.abstractmethod
    def awake(self):
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def step(self, action):
        raise NotImplementedError

    @abc.abstractmethod
    def sample_action(self):
        raise NotImplementedError

    @abc.abstractmethod
    def render(self):
        raise NotImplementedError

    @abc.abstractmethod
    def destory(self):
        raise NotImplementedError


class EnvWrapper(BaseEnvTrait):
    def __init__(self, *, env: BaseEnvTrait) -> None:
        self.env: BaseEnvTrait = env
        self.__awaked = False
        self.__reseted = False
        self.__destoryed = False

    @property
    def renderable(self):
        return self.env.renderable

    @property
    def observation_dim(self):
        return self.env.observation_dim

    @property
    def action_dim(self):
        return self.env.action_dim

    @property
    def action_n(self):
        return self.env.action_n

    def awake(
        self,
    ):
        assert not self.__destoryed, "env must not be destoryed before awake"
        self.__awaked = True
        self.env.awake()
        return self

    def reset(self):
        assert not self.__destoryed, "env must not be destoryed before awake"
        assert self.__awaked, "env must be awaked before reset"
        self.__reseted = True
        return self.env.reset()

    def step(self, action):
        assert not self.__destoryed, "env must not be destoryed before awake"
        assert self.__awaked, "env must be awaked before step"
        assert self.__reseted, "env must be reseted before step"
        return self.env.step(action)

    def sample_action(self):
        return self.env.sample_action()

    def render(self):
        assert not self.__destoryed, "env must not be destoryed before awake"
        assert self.__awaked, "env must be awaked before render"
        assert self.__reseted, "env must be reseted before render"
        self.env.render()

    def destory(self):
        self.__destoryed = True
        return self.env.destory()


# class BaseCudaEnv(BaseEnv):
#     def __init__(self, *, eposide_len: int, device_id: int, seed: int = 314) -> None:
#         super().__init__(eposide_len=eposide_len, seed=seed)
#         self.device_id = device_id

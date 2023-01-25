from typing import Optional, Union, Tuple, List
import torch
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Box, Discrete
from rlvortex.envs.base_env import BaseEnvTrait
from rlvortex.utils.trainer_utils import unscale_actions, scale_actions


class GymEnv(BaseEnvTrait):
    def __init__(self, *, normalize_act, viz: bool, seed: int) -> None:
        super().__init__()
        self._normalize_act: bool = normalize_act
        self._renderable = viz
        self._seed: Optional[int] = seed
        self.gym_env: Optional[gym.Env] = None

    @property
    def seed(self):
        return self._seed

    @property
    def renderable(self):
        return self._renderable

    @property
    def observation_dim(self) -> Optional[Tuple[int]]:
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        return self.gym_env.observation_space.shape

    def awake(self) -> None:
        # only box action space can be normalized
        if self._normalize_act and self.gym_env is not None:
            assert isinstance(
                self.gym_env.action_space, Box
            ), f"only box action space can be normalized, get type {type(self.gym_env.action_space)}"
        assert self.gym_env is not None, "self.gym must be a gym env, not None"

    def reset(self):
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        return self.gym_env.reset(seed=self._seed)

    def step(self, action: Union[int, float, np.ndarray, torch.Tensor]):
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        if (
            self._normalize_act
            and isinstance(self.gym_env.action_space, Box)
            and (isinstance(action, np.ndarray) or isinstance(action, torch.Tensor))
        ):
            action = scale_actions(action, self.gym_env.action_space.low, self.gym_env.action_space.high)
        observation, reward, terminated, truncated, info = self.gym_env.step(action)
        return (
            observation,
            reward,
            terminated or truncated,
            info,
        )

    def sample_action(self):
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        if self._normalize_act and isinstance(self.gym_env.action_space, Box):
            return unscale_actions(
                self.gym_env.action_space.sample(),
                self.gym_env.action_space.low,
                self.gym_env.action_space.high,
            )
        return self.gym_env.action_space.sample()

    def render(self):
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        assert self._renderable, "environment rendering is not enabled"
        self.gym_env.render()

    def destory(self):
        assert self.gym_env is not None, "self.gym must be a gym env, not None"
        return self.gym_env.close()


class CartPoleEnv(GymEnv):
    def __init__(self, viz: bool = False, seed: int = 19970314) -> None:
        super().__init__(normalize_act=False, viz=viz, seed=seed)
        if viz:
            self.gym_env: gym.Env = gym.make("CartPole-v1", render_mode="human")
        else:
            self.gym_env: gym.Env = gym.make("CartPole-v1")

    @property
    def action_dim(self) -> Tuple[int, ...]:
        return ()

    @property
    def action_n(self) -> int:
        assert isinstance(self.gym_env.action_space, Discrete)
        return self.gym_env.action_space.n


class MountainCarContinuousEnv(GymEnv):
    def __init__(self, *, viz: bool = False, seed: int = 19970314) -> None:
        super().__init__(normalize_act=False, viz=viz, seed=seed)
        if viz:
            self.gym_env: gym.Env = gym.make("MountainCarContinuous-v0", render_mode="human")
        else:
            self.gym_env: gym.Env = gym.make("MountainCarContinuous-v0")

    @property
    def action_dim(self) -> Tuple[int]:
        assert isinstance(self.gym_env.action_space, Box)
        return self.gym_env.action_space.shape

    @property
    def action_n(self) -> int:
        return 0


class PendulumEnv(GymEnv):
    def __init__(self, viz: bool = False, seed: int = 19970314) -> None:
        super().__init__(normalize_act=True, viz=viz, seed=seed)
        if viz:
            self.gym_env: gym.Env = gym.make("Pendulum-v1", render_mode="human")
        else:
            self.gym_env: gym.Env = gym.make(
                "Pendulum-v1",
            )

    @property
    def action_dim(self) -> Tuple[int]:
        assert isinstance(self.gym_env.action_space, Box)
        return self.gym_env.action_space.shape

    @property
    def action_n(self) -> int:
        return 0


class LunarLanderEnv(GymEnv):
    def __init__(self, *, continuous: bool = True, viz: bool = False, seed: int = 19970314) -> None:
        super().__init__(normalize_act=False, viz=viz, seed=seed)
        self.continuous = continuous
        if viz:
            self.gym_env: gym.Env = gym.make(
                "LunarLander-v2",
                render_mode="human",
                continuous=continuous,
            )
        else:
            self.gym_env: gym.Env = gym.make("LunarLander-v2", continuous=continuous)

    @property
    def action_dim(
        self,
    ) -> Tuple[int, ...]:
        if self.continuous:
            assert isinstance(self.gym_env.action_space, Box)
            return self.gym_env.action_space.shape
        else:
            return ()

    @property
    def action_n(self) -> int:
        if self.continuous:
            return 0
        else:
            assert isinstance(
                self.gym_env.action_space, Discrete
            ), "LunarLander enabled continuous action space, action_n is not defined for continuous action"
            return self.gym_env.action_space.n

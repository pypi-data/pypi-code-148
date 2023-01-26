""" Register Gym environments """

import numpy as np
from gym.envs.registration import register
from .env_kwargs import kwargs_dicts


register(
    id='widowx_reacher-v250',
    entry_point='gym_envs.widowx_env.widowx_env:WidowxEnv',
    max_episode_steps=100,
    kwargs=kwargs_dicts['widowx_reacher-v250'],
    )


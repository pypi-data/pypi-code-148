import os
import argparse
from typing import Callable, Dict


import torch
from rlvortex.envs.base_env import EnvWrapper
from rlvortex.envs.gym_wrapper.gym_envs import (
    CartPoleEnv,
    MountainCarContinuousEnv,
    PendulumEnv,
    LunarLanderEnv,
)

from rlvortex.task_archive.ppo.hyperparams.gym_envs_params import CartpoleEnvParams


available_env_dict: Dict[str, Callable] = {
    "cartpole": CartPoleEnv,
    "mountaincarc": MountainCarContinuousEnv,
    "pendulum": PendulumEnv,
    "lunar_lander": LunarLanderEnv,
}

trained_model_path_dict = {
    "cartpole": os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/cartpole_v1.pth"),
    "mountaincarc": None,
    "pendulum": os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/pendulum_v1.pth"),
    "lunar_lander": os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/lunarlanderc_v1.pth"),
}


def main(args):
    assert args.env[0] in available_env_dict.keys(), f"Unknow Environment {args.env}"
    env_wrapper: EnvWrapper = EnvWrapper(env=available_env_dict[args.env[0]](viz=args.render))
    loaded_model = torch.load(trained_model_path_dict[args.env[0]])

    while True:
        o, _ = env_wrapper.reset()
        d = False
        while not d:
            a = loaded_model.act(torch.as_tensor(o, dtype=torch.float32))  # in torch.Tensor,no gradient computed
            next_o, r, d, cache = env_wrapper.step(a.cpu().numpy())
            o = next_o


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--render", action="store_true")
    parser.add_argument("--env", required=True, nargs=1, choices=available_env_dict.keys())

    args = parser.parse_args()
    main(args)

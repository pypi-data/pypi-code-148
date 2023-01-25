import os
import argparse
from typing import Dict, Callable
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv
from rlvortex.trainer.ppo_trainer import NativePPOTrainer
from rlvortex.utils import vlogger
from rlvortex.task_archive.ppo.hyperparams.gym_envs_params import (
    CartpoleEnvParams,
    PendulumEnvParams,
    LunarLanderContinuousEnvParams,
    MountainCarContinuousEnvParams,
)

available_env_params_dict: Dict[str, Callable] = {
    "cartpole": CartpoleEnvParams,
    "pendulum": PendulumEnvParams,
    "mountaincarc": MountainCarContinuousEnvParams,
    "lunarlanderc": LunarLanderContinuousEnvParams,
}
solved_scores_dict: Dict[str, float] = {
    "cartpole": 450,
    "pendulum": -150,
    "mountaincarc": 90,
    "lunarlanderc": 250,
}


def main(
    render: bool,
    env_name: str,
):
    assert (
        env_name in available_env_params_dict.keys()
    ), f"Unknow Environment {args.env}"

    target_env_params = available_env_params_dict[env_name]
    train_batch = 5
    trainer: NativePPOTrainer = target_env_params.trainer
    sub_steps = int(target_env_params.epochs // train_batch)
    trainer.evaluate(1, env=target_env_params.env_fn(viz=render))
    for _ in range(train_batch):
        trainer.train(sub_steps)
        ep_rtn, ep_mean = trainer.evaluate(10, env=target_env_params.env_fn(viz=render))
        print("evalution: ep_rtn:", ep_rtn, "ep_mean:", ep_mean)
    ep_rtn, ep_mean = trainer.evaluate(10, env=target_env_params.env_fn(viz=render))
    assert (
        ep_rtn >= solved_scores_dict[env_name]
    ), f"the final reward does not reach target reward, get {ep_rtn} with {solved_scores_dict[env_name]} as solved reward"
    print(f"{env_name} solved with reward {ep_rtn}/{solved_scores_dict[env_name]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--render", action="store_true")
    parser.add_argument(
        "--env", required=True, nargs=1, choices=available_env_params_dict.keys()
    )

    args = parser.parse_args()
    main(args.render, args.env[0])

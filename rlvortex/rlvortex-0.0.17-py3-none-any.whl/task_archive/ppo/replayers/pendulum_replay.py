import torch
import os
from vortex.envs.gym_wrapper.gym_envs import PendulumEnv
from vortex.utils import trainer_utils
from vortex.task_archive.ppo.hyperparams.gym_envs_params import (
    PendulumEnvParams,
    global_seed,
)

if __name__ == "__main__":
    trainer_utils.set_global_random_seed(rd_seed=global_seed)
    loaded_model = torch.load(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../models/pendulum_v1.pth"
        )
    )
    env = PendulumEnv(render=True, seed=global_seed)
    while True:
        o, _ = env.reset()
        d = False
        while not d:
            a = loaded_model.act(
                torch.as_tensor(o, dtype=torch.float32)
            )  # in torch.Tensor,no gradient computed
            next_o, r, d, cache = env.step(a.cpu().numpy())
            o = next_o

    env.destory()

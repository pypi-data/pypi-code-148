import os
import torch
from vortex.envs.gym_wrapper.gym_envs import LunarLanderEnv
from vortex.utils import trainer_utils
from vortex.task_archive.ppo.hyperparams.gym_envs_params import (
    LunarLanderContinuousEnvParams,
)

if __name__ == "__main__":
    trainer_utils.set_global_random_seed(rd_seed=LunarLanderContinuousEnvParams.seed)
    loaded_model = torch.load(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../models/lunarlander_continuous.pth",
        )
    )
    env = LunarLanderEnv(render=True, seed=LunarLanderContinuousEnvParams.seed)
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

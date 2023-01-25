import os
import torch
from rlvortex.utils import trainer_utils
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv
from rlvortex.task_archive.ppo.hyperparams.gym_envs_params import CartpoleEnvParams

if __name__ == "__main__":
    loaded_model = torch.load(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../models/cartpole_v1.pth"
        )
    )
    env = CartPoleEnv(viz=True)
    env.awake()
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

import abc
from collections import deque
import random
from typing import Optional, Callable
import torch
import numpy as np
from rlvortex.envs.base_env import EnvWrapper
from datetime import datetime
import os
from collections import namedtuple
from rlvortex.utils import vlogger
from torch.utils.tensorboard.writer import SummaryWriter
from rlvortex.policy.ppo_policy import BaseCritic, BasePPOPolicy, CategoricalActor
import tqdm

TrainerMonitorTable = namedtuple(
    "TrainMonitorTale",
    [
        "start_time",
        "start_time_str",
        "trainer_dir",
        "trainer_name",
        "trainer_path",
        "tensorboard_path",
        "save_path",
        "log_path",
    ],
)


class BaseTrainer(abc.ABC):
    def __init__(
        self,
        *,
        env: EnvWrapper,
        policy: BasePPOPolicy,
        optimizer: Callable,
        init_lr: float,
        steps_per_env: int,
        device_id: int,
        trainer_dir: str,
        enable_tensorboard: bool,
        save_freq: int,  # if save_freg == -1, then disable save, if save_freq == 0, then save at the end of training,otherwise save every save_freq epochs
        log_type: vlogger.LogType,
        comment: str,
        seed: int,
    ) -> None:
        self.env: EnvWrapper = env
        self.steps_per_env: int = steps_per_env
        self.steps: int = 0
        self.epoch: int = 0
        self.device_id: int = device_id
        self.device: torch.device = (
            torch.device(f"cuda:{device_id}") if device_id >= 0 else torch.device("cpu")
        )
        self.policy: BasePPOPolicy = policy.to(self.device)
        self._learning_rate: float = init_lr
        self.policy_optimizer: Callable = optimizer(
            self.policy.parameters(), lr=init_lr
        )
        self.save_freq: int = save_freq
        self.enable_tensorboard: bool = enable_tensorboard
        self.log_type: vlogger.LogType = log_type
        self.comment: str = comment
        self.seed: int = seed
        # log and save
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        trainer_name = f"ppo_trainer_{start_time_str}_cmt_{self.comment}"
        trainer_path = os.path.join(trainer_dir, trainer_name)
        self.trainer_montior_table: TrainerMonitorTable = TrainerMonitorTable(
            start_time=start_time,
            start_time_str=start_time_str,
            trainer_dir=trainer_dir,
            trainer_name=trainer_name,
            trainer_path=os.path.join(trainer_path),
            save_path=os.path.join(trainer_path, "models"),
            tensorboard_path=os.path.join(trainer_path, "runs"),
            log_path=os.path.join(trainer_path, "trainer.log"),
        )
        self.__gen_trainer_dirs_and_tb()
        self.logger: vlogger.VLogger = vlogger.VLogger(
            log_type=self.log_type,
            log_path=self.trainer_montior_table.log_path,
        )
        self.info_buffer = {
            "rollout": {
                "eposide_return": [],
                "eposide_length": [],
                "moving_avg_return_100": deque(maxlen=100),
                "moving_avg_length_100": deque(maxlen=100),
            },
            "trainer": {
                "total_loss": [],
                "pi_loss": [],
                "v_loss": [],
                "entropy_loss": [],
                "kl_div": [],
                "learning_rate": [],
                "act_prob": [],
            },
        }

        self.sample_steps = 0
        self.log_buffer_size = 0
        self.customized_log_info = {}
        self.customized_tb_info = {}
        self.saved_model_pathes = []

    def _update_learning_rate(self):
        for param_group in self.policy_optimizer.param_groups:
            param_group["lr"] = self._learning_rate

    def __gen_trainer_dirs_and_tb(self):
        if (
            not self.log_type.File
            and not self.enable_tensorboard
            and not self.save_freq
        ):
            return
        if not os.path.exists(self.trainer_montior_table.trainer_dir):
            os.mkdir(self.trainer_montior_table.trainer_dir)
        if not os.path.exists(self.trainer_montior_table.trainer_path):
            os.mkdir(self.trainer_montior_table.trainer_path)
        if self.save_freq and not os.path.exists(self.trainer_montior_table.save_path):
            os.mkdir(self.trainer_montior_table.save_path)
        if self.enable_tensorboard:
            self._tb_writer = SummaryWriter(
                self.trainer_montior_table.tensorboard_path,
                comment=self.trainer_montior_table.trainer_name,
            )

    def append_eposide_rollout_info(self, *, ep_return: float, ep_length: float):
        self.info_buffer["rollout"]["eposide_return"].append(ep_return)
        self.info_buffer["rollout"]["eposide_length"].append(ep_length)
        self.info_buffer["rollout"]["moving_avg_return_100"].append(ep_return)
        self.info_buffer["rollout"]["moving_avg_length_100"].append(ep_length)
        if self.enable_tensorboard:
            self._tb_writer.add_scalar("eposide/return", ep_return, self.sample_steps)
            self._tb_writer.add_scalar("eposide/length", ep_length, self.sample_steps)

        self.log_buffer_size += 1

    def append_trainer_info(
        self,
        *,
        total_loss: float,
        pi_loss: float,
        v_loss: float,
        entropy_loss: float,
        kl_div: float,
        learning_rate: float,
        act_prob: float,
    ):
        self.info_buffer["trainer"]["total_loss"].append(total_loss)
        self.info_buffer["trainer"]["pi_loss"].append(pi_loss)
        self.info_buffer["trainer"]["v_loss"].append(v_loss)
        self.info_buffer["trainer"]["entropy_loss"].append(entropy_loss)
        self.info_buffer["trainer"]["kl_div"].append(kl_div)
        self.info_buffer["trainer"]["learning_rate"].append(learning_rate)
        self.info_buffer["trainer"]["act_prob"].append(act_prob)

    def clear_ep_info(self):
        self.info_buffer["rollout"]["eposide_return"] = []
        self.info_buffer["rollout"]["eposide_length"] = []
        self.info_buffer["trainer"]["total_loss"] = []
        self.info_buffer["trainer"]["pi_loss"] = []
        self.info_buffer["trainer"]["v_loss"] = []
        self.info_buffer["trainer"]["entropy_loss"] = []
        self.info_buffer["trainer"]["kl_div"] = []
        self.info_buffer["trainer"]["learning_rate"] = []
        self.info_buffer["trainer"]["act_prob"] = []
        self.log_buffer_size = 0

    def _record_info_buffer(self, epoch: int):
        steps = self.steps_per_env * epoch
        if self.log_buffer_size > 0:
            rtn_mean, rtn_max, rtn_min, rtn_std = (
                np.mean(self.info_buffer["rollout"]["eposide_return"]),
                np.max(self.info_buffer["rollout"]["eposide_return"]),
                np.min(self.info_buffer["rollout"]["eposide_return"]),
                np.std(self.info_buffer["rollout"]["eposide_return"]),
            )

            len_mean, len_max, len_min, len_std = (
                np.mean(self.info_buffer["rollout"]["eposide_length"]),
                np.max(self.info_buffer["rollout"]["eposide_length"]),
                np.min(self.info_buffer["rollout"]["eposide_length"]),
                np.std(self.info_buffer["rollout"]["eposide_length"]),
            )
        else:
            (
                rtn_mean,
                rtn_max,
                rtn_min,
                rtn_std,
                len_mean,
                len_max,
                len_min,
                len_std,
            ) = (
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            )
            self.info_buffer["rollout"]["moving_avg_return_100"].append(0.0)
            self.info_buffer["rollout"]["moving_avg_length_100"].append(0.0)
        total_loss = np.mean(self.info_buffer["trainer"]["total_loss"])
        pi_loss = np.mean(self.info_buffer["trainer"]["pi_loss"])
        v_loss = np.mean(self.info_buffer["trainer"]["v_loss"])
        entropy_loss = np.mean(self.info_buffer["trainer"]["entropy_loss"])
        kl_div = np.mean(self.info_buffer["trainer"]["kl_div"])
        lr = np.mean(self.info_buffer["trainer"]["learning_rate"])
        act_prob = np.mean(self.info_buffer["trainer"]["act_prob"])
        log_buffer = {
            "epoch": epoch,
            "steps": steps,
            "rollout": {
                "avg_ep_return": f"mean: {rtn_mean:.4f},max: {rtn_max:.4f}, min: {rtn_min:.4f}, std: {rtn_std:.4f}",
                "avg_ep_length": f"mean: {len_mean:.4f},max: {len_max:.4f}, min: {len_min:.4f}, std: {len_std:.4f}",
            },
            "trainer": {
                "total_loss": f"{total_loss:.4f}",
                "pi_loss": f"{pi_loss:.4f}",
                "v_loss": f"{v_loss:.4f}",
                "entropy_loss": f"{entropy_loss:.4f}",
                "kl_div": f"{kl_div:.4f}",
                "learning_rate": f"{lr:.4f}",
                "act_prob": f"{act_prob:.4f}",
            },
        }
        self.logger.info_dict(log_buffer)
        if self.enable_tensorboard:
            self._tb_writer.add_scalar("epoch_avg/return", rtn_mean, steps)
            self._tb_writer.add_scalar("epoch_avg/length", len_mean, steps)
            self._tb_writer.add_scalar(
                "moving_avg_100/return",
                np.mean(self.info_buffer["rollout"]["moving_avg_return_100"]),
                steps,
            )
            self._tb_writer.add_scalar(
                "moving_avg_100/length",
                np.mean(self.info_buffer["rollout"]["moving_avg_length_100"]),
                steps,
            )
            self._tb_writer.add_scalar("trainer/total_loss", total_loss, steps)
            self._tb_writer.add_scalar("trainer/pi_loss", pi_loss, steps)
            self._tb_writer.add_scalar("trainer/v_loss", v_loss, steps)
            self._tb_writer.add_scalar("trainer/entropy_loss", entropy_loss, steps)
            self._tb_writer.add_scalar("trainer/kl_div", kl_div, steps)
            self._tb_writer.add_scalar(
                "trainer/learning_rate", self.learning_rate, steps
            )
            self._tb_writer.add_scalar("trainer/act_prob", act_prob, steps)
    def clear_customized_tb_info(self):
        self.customized_tb_info = {}

    def append_customized_tb_info(self, info: dict):
        for key, val in info.items():
            if key in self.customized_tb_info:
                self.customized_tb_info[key].append(val)
            else:
                self.customized_tb_info[key] = []

    def _log_customized_info(self):
        self.logger.info_dict(self.customized_log_info)

    def _tb_customized_info(self, epoch: int):
        for key, val in self.customized_tb_info.items():
            self._tb_writer.add_scalar(f"customized/{key}_mean", np.mean(val), epoch * self.steps_per_env)

    def _log_all(self, epoch: int):
        self._record_info_buffer(epoch)
        self._log_customized_info()
        self._tb_customized_info(epoch)

    def get_saved_model_pathes(self):
        return self.saved_model_pathes

    def train(self):
        raise NotImplementedError

    def evaluate(self, eposides: int = -1, env: Optional[EnvWrapper] = None):
        ext_env = env != None
        ep_rtns = []
        ep_lens = []
        if not ext_env:
            env = self.env
        current_eposide = 0
        while current_eposide != eposides:
            env.awake()
            o, _ = env.reset()
            d = False
            ep_ret = 0
            ep_len = 0
            while not d:
                a = self.policy.act(
                    torch.as_tensor(o, dtype=torch.float32, device=self.device)
                )  # in torch.Tensor,no gradient computed
                next_o, r, d, cache = env.step(a.cpu().numpy())
                o = next_o
                ep_len += r
                ep_ret += 1

            ep_rtns.append(ep_ret)
            ep_lens.append(ep_len)
            current_eposide += 1

        if ext_env:
            env.destory()
        else:
            env.reset()
        return np.mean(ep_rtns), np.mean(ep_lens)

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, lr: float):
        self._learning_rate = lr
        for param_group in self.policy_optimizer.param_groups:
            param_group["lr"] = self.learning_rate

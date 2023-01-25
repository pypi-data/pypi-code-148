from contextlib import AsyncExitStack
from lib2to3.pytree import Base
from turtle import forward
from typing import List
import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.distributions.normal import Normal

from rlvortex.utils.trainer_utils import v_debug
from rlvortex.policy.quick_build import init_weights


class BaseActor(nn.Module):
    def __init__(self, *, net: nn.Module):
        super().__init__()
        self.logits_net = net

    def _distribution(self, obs):
        raise NotImplementedError

    def _log_prob_from_distribution(self, pi, act):
        raise NotImplementedError


class BaseCritic(nn.Module):
    def __init__(self, *, net: nn.Module):
        super().__init__()
        self.v_net = net

    def forward(self, obs):
        # return torch.squeeze(
        #     self.v_net(obs), -1
        # )  # squeeze values from (obs_dim, 1) to (obs_dim,)
        return self.v_net(obs)


class CategoricalActor(BaseActor):
    def __init__(self, *, net: nn.Module):
        super().__init__(net=net)

    def _distribution(self, obs):
        logits = self.logits_net(obs)
        return Categorical(logits=logits)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act)

class GaussianActor(BaseActor):
    """
    net is the torch neural network module with the first layer fist the environment observation dimension
    init_log_stds is a torch.Tensor with the size of environment action observation
    """

    def __init__(self, *, net: nn.Module, init_log_stds: torch.Tensor):
        super().__init__(net=net)
        self.log_std = torch.nn.Parameter(init_log_stds)

    def _distribution(self, obs):
        mu = self.logits_net(obs)
        std = torch.exp(self.log_std)
        return Normal(mu, std)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act).sum(axis=-1)

    def to(self, device):
        self.logits_net = self.logits_net.to(device)
        self.log_std = self.log_std.to(device)
        return self


class GaussianSepActor(BaseActor):
    def __init__(
        self,
        *,
        preprocess_net: nn.Module,
        logits_net: nn.Module,
        log_std_net: nn.Module
    ):
        super().__init__(net=logits_net)
        self.preprocess_net = preprocess_net
        self.log_std_net = log_std_net

    def _distribution(self, obs):
        obs_feats = self.preprocess_net(obs)
        mu = self.logits_net(obs_feats)
        std = torch.exp(self.log_std_net(obs_feats))
        # print(obs_feats, mu, std)
        # import pdb
        # pdb.set_trace()
        return Normal(mu, std)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act).sum(axis=-1)


class BasePPOPolicy(nn.Module):
    def __init__(
        self,
        actor: BaseActor,
        critic: BaseCritic,
    ) -> None:
        super().__init__()
        self.actor: BaseActor = actor
        self.critic: BaseCritic = critic
        self.actor.apply(init_weights)
        self.critic.apply(init_weights)

    """
    This method is used to interact with the environment for experience collection. No gradient is computed.
    """

    def step(self, obs):
        with torch.no_grad():
            pi = self.actor._distribution(obs)
            a = pi.sample()
            logp_a = self.actor._log_prob_from_distribution(pi, a)
            v = self.critic(obs)
        return a, v, logp_a

    """
    This method is used to interact with the environment for evaluation by trained model .
    """

    def act(self, obs):
        with torch.no_grad():
            pi = self.actor._distribution(obs)
            a = pi.sample()
        return a

    """
    This method is used to compute the loss. Graident is computed.
    """

    def forward(self, actions, observations):
        pi = self.actor._distribution(observations)
        logp_a = self.actor._log_prob_from_distribution(pi, actions)
        v = self.critic(observations)
        entropy = pi.entropy().mean()
        return logp_a, v, entropy

    def to(self, device):
        self.actor = self.actor.to(device)
        self.critic = self.critic.to(device)
        return self


import torch.nn.functional as F


class PenCritic(nn.Module):
    def __init__(self, in_dim: int):
        super().__init__()
        """Initialize."""
        self.net = nn.Sequential(*[nn.Linear(in_dim, 64), nn.ReLU(), nn.Linear(64, 1)])

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward method implementation."""
        value = self.net(state)
        return value


class PenActor(nn.Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
    ):
        """Initialize."""
        super().__init__()
        self.preprocess_net = nn.Sequential(nn.Linear(in_dim, 32), nn.ReLU())
        self.logits_net = nn.Sequential(nn.Linear(32, out_dim), nn.Tanh())
        self.log_std_layer = nn.Sequential(nn.Linear(32, out_dim), nn.Tanh())

    def _distribution(self, obs):
        x = self.preprocess_net(obs)
        mu = self.logits_net(x)
        log_std = self.log_std_layer(x)
        std = torch.exp(log_std)
        return Normal(mu, std)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act)


class PenPPOPolicy(nn.Module):
    def __init__(
        self,
        actor: BaseActor,
        critic: BaseCritic,
    ) -> None:
        super().__init__()
        self.actor: BaseActor = actor
        self.critic: BaseCritic = critic
        self.actor.apply(init_weights)
        self.critic.apply(init_weights)

    """
    This method is used to interact with the environment for experience collection. No gradient is computed.
    """

    def actor_forward(self, obs):
        return self.actor(obs)

    def critic_forward(self, obs):
        return self.critic(obs)

    """
    This method is used to interact with the environment for evaluation by trained model .
    """

    """
    This method is used to compute the loss. Graident is computed.
    """

    def step(self, obs):
        with torch.no_grad():
            pi = self.actor._distribution(obs)
            a = pi.sample()
            logp_a = self.actor._log_prob_from_distribution(pi, a)
            v = self.critic(obs)
        return a, v, logp_a

    def forward(self, actions, observations):
        pi = self.actor._distribution(observations)
        logp_a = self.actor._log_prob_from_distribution(pi, actions)
        v = self.critic(observations)
        entropy = pi.entropy().mean()
        return logp_a, v, entropy

    def to(self, device):
        self.actor = self.actor.to(device)
        self.critic = self.critic.to(device)
        return self
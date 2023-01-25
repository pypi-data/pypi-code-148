import os
import torch
from rlvortex.policy.ppo_policy import (
    BasePPOPolicy,
    GaussianActor,
    GaussianSepActor,
    CategoricalActor,
    BaseCritic,
)
from rlvortex.policy.quick_build import mlp
from rlvortex.envs.base_env import EnvWrapper
from rlvortex.envs.gym_wrapper.gym_envs import (
    CartPoleEnv,
    PendulumEnv,
    LunarLanderEnv,
    MountainCarContinuousEnv,
)
from rlvortex.utils import trainer_utils, vlogger
from rlvortex.trainer.ppo_trainer import NativePPOTrainer

global_seed = 19970314

# trainer_utils.set_global_random_seed(rd_seed=global_seed)
# torch.set_printoptions(precision=10)


class CartpoleEnvParams:
    env_fn = CartPoleEnv
    env = EnvWrapper(env=CartPoleEnv(viz=False, seed=global_seed))
    assert env.observation_dim is not None
    policy = BasePPOPolicy(
        actor=CategoricalActor(
            net=mlp([*env.observation_dim, 32, env.action_n], torch.nn.Tanh)
        ),
        critic=BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.Tanh)),
    )
    optimizer = torch.optim.Adam
    init_lr = 1e-3
    epochs = 50
    trainer: NativePPOTrainer = NativePPOTrainer(
        env=env,
        policy=policy,
        optimizer=optimizer,
        init_lr=init_lr,
        enable_tensorboard=True,
        device_id=-1,
        save_freq=5,
        log_type=vlogger.LogType.Screen,
        trainer_dir=os.path.join(os.getcwd(), "trainer_cache"),
        comment="cartpole",
        seed=global_seed,
    )


class PendulumEnvParams:
    """
    In the environment, large value loss can lead the training become slow. I use smaller gamma = 0.9 to reduce the long-term rewards.
    """

    env_fn = PendulumEnv
    env = EnvWrapper(env=PendulumEnv(viz=False, seed=global_seed))
    policy = BasePPOPolicy(
        actor=GaussianSepActor(
            preprocess_net=mlp(
                [*env.observation_dim, 32],
                torch.nn.Tanh,
                output_activation=torch.nn.ReLU,
            ),
            logits_net=mlp(
                [32, *env.action_dim],
                torch.nn.Tanh,
                output_activation=torch.nn.Tanh,
            ),
            log_std_net=mlp(
                [32, *env.action_dim],
                torch.nn.Tanh,
                output_activation=torch.nn.Tanh,
            ),
        ),
        critic=BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.ReLU)),
    )
    optimizer = torch.optim.Adam
    init_lr = 1e-3
    gamma = 0.9
    epochs = 150
    max_grad_norm = None
    trainer = NativePPOTrainer(
        env=env,
        policy=policy,
        optimizer=optimizer,
        init_lr=init_lr,
        device_id=-1,
        gamma=gamma,
        # normalize_adv=False,
        desired_kl=1e-4,
        enable_tensorboard=True,
        save_freq=50,
        log_type=vlogger.LogType.Screen,
        trainer_dir=os.path.join(os.getcwd(), "trainer_cache"),
        comment="pendulum",
        seed=global_seed,
    )


class LunarLanderContinuousEnvParams:
    seed = global_seed
    env_fn = LunarLanderEnv
    env = EnvWrapper(env=LunarLanderEnv(viz=False, continuous=True))
    policy = BasePPOPolicy(
        actor=GaussianActor(
            net=mlp([*env.observation_dim, 32, *env.action_dim], torch.nn.Tanh),
            init_log_stds=-0.5 * torch.ones(env.action_dim),
        ),
        critic=BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.Tanh)),
    )
    steps_per_env = 1024
    num_batches_per_env = 16
    learning_iterations = 32
    val_loss_coef = 1.0
    init_lr = 1e-3
    random_sampler = True
    normalize_adv = True
    optimizer = torch.optim.Adam
    epochs = 200
    trainer = NativePPOTrainer(
        env=env,
        policy=policy,
        optimizer=optimizer,
        steps_per_env=steps_per_env,
        num_batches_per_env=num_batches_per_env,
        learning_iterations=learning_iterations,
        val_loss_coef=val_loss_coef,
        init_lr=init_lr,
        random_sampler=random_sampler,
        normalize_adv=normalize_adv,
        enable_tensorboard=True,
        save_freq=10,
        log_type=vlogger.LogType.Screen,
        trainer_dir=os.path.join(os.getcwd(), "trainer_cache"),
        comment="lunarlander-continuous",
    )


class MountainCarContinuousEnvParams:
    env_fn = MountainCarContinuousEnv
    env = EnvWrapper(env=MountainCarContinuousEnv(viz=False))
    policy = BasePPOPolicy(
        actor=GaussianSepActor(
            preprocess_net=mlp(
                [*env.observation_dim, 32],
                torch.nn.Tanh,
                output_activation=torch.nn.ReLU,
            ),
            logits_net=mlp(
                [32, *env.action_dim], torch.nn.Tanh, output_activation=torch.nn.Tanh
            ),
            log_std_net=mlp(
                [32, *env.action_dim], torch.nn.Tanh, output_activation=torch.nn.Tanh
            ),
        ),
        critic=BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.ReLU)),
    )
    optimizer = torch.optim.Adam
    init_lr = 5e-3
    val_loss_coef = 2.0
    normalize_adv = False
    steps_per_env = 1000
    num_batches_per_env = 1
    learning_iterations = 128
    entropy_loss_coef = 0.01
    max_grad_norm = None
    epochs = 30
    trainer = NativePPOTrainer(
        env=env,
        policy=policy,
        optimizer=optimizer,
        init_lr=init_lr,
        val_loss_coef=val_loss_coef,
        num_batches_per_env=num_batches_per_env,
        steps_per_env=steps_per_env,
        learning_iterations=learning_iterations,
        entropy_loss_coef=entropy_loss_coef,
        max_grad_norm=max_grad_norm,
        normalize_adv=normalize_adv,
        enable_tensorboard=True,
        save_freq=50,
        log_type=vlogger.LogType.Screen,
        trainer_dir=os.path.join(os.getcwd(), "trainer_cache"),
        comment="mountaincar-continuous",
        seed=global_seed,
    )

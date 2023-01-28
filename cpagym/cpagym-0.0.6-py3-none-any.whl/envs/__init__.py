from gym.envs.registration import register

register(
    id='envs/GridWorld-v0',
    entry_point='envs.envs:GridWorldEnv',
    max_episode_steps=300,
)
from gym.envs.registration import register

register(
    id='gym_examples/GridWorld-v0',
    entry_point='cpagym.envs.grid_world:GridWorldEnv',
    max_episode_steps=300,
)
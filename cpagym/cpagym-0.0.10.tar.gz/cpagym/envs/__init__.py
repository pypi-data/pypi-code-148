from gym.envs.registration import register

register(
    id='Inventory-v0',
    entry_point='cpagym.envs.grid_world:InventoryEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)
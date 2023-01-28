from gym.envs.registration import register

register(
    id='Inventory-v0',
    entry_point='cpagym.envs.grid_world:InventoryEnv',
)
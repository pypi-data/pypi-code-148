from gym.envs.registration import register

register(
    id='Inventory-v0',
    entry_point='cpagym.envs.grid_world:InventoryEnv',
)

register(
    id='forex-v0',
    entry_point='cpagym.envs.forex_env:ForexEnv',
)

register(
    id='stocks-v0',
    entry_point='cpagym.envs.stocks_env:StocksEnv',
)
register(
    id='trading-v0',
    entry_point='cpagym.envs.trading_env:TradingEnv',
)

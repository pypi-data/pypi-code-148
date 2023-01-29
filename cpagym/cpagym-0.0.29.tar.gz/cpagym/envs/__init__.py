from gymnasium.envs.registration import register

register(
    id='Inventory-v1',
    entry_point='cpagym.envs.inventory_env:InventoryEnv',
)
register(
    id='forex-v1',
    entry_point='cpagym.envs.forex_env:ForexEnv',
)
register(
    id='stocks-v1',
    entry_point='cpagym.envs.stocks_env:StocksEnv',
)
register(
    id='trading-v1',
    entry_point='cpagym.envs.trading_env:TradingEnv',
)
register(
    id='AsymmetricInfo-v1',
    entry_point='cpagym.envs.asymmetricInfo_env:AsymmetricInfoEnv',
)
register(
    id='Moral_Hazard-v1',
    entry_point='cpagym.envs.moral_hazard_env:Moral_HazardEnv',
)
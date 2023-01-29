from typing import Dict

class Configs:

    def __init__(
        self,
        wallet_base_url: str,
        x_api_key: str,
        wallet_id: str,
        seed_key: str = None,
        seed: str = None,

    ):
        self.wallet_base_url = wallet_base_url
        self.x_api_key = x_api_key
        self.wallet_id = wallet_id
        self.seed_key = seed_key
        self.seed = seed

    def setup(self) -> Dict[str, str]:

        configs: Dict[str, str] = {
            'wallet_base_url': self.wallet_base_url,
            'headers': {
                'X-API-KEY': self.x_api_key,
                'X-Wallet-Id': self.wallet_id,
            },
            'data': {
                'wallet-id': self.wallet_id,
                'seed_key': self.seed_key,
                'seed': self.seed,
            }
        }

        return configs

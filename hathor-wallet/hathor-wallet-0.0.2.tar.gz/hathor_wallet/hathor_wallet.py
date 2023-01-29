from typing import Optional, List, Dict

from hathor_wallet.exception import HathorWalletError

import requests
from urllib import parse


class HathorWallet:

    def __init__(
        self,
        **configs
        ):
        self.configs: dict = configs

    def start(self):
        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/start')
            response = requests.post(url=url, headers=self.configs.get('headers'), data=self.configs.get('data'))
            
            if response.status_code != 200:
                raise HathorWalletError('Erro stating wallet.')

            from time import sleep
            sleep(5)
            
            return response.json()

        except:
            raise HathorWalletError('Error in the request.')

    def status(self):
        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/wallet/status')
            response = requests.get(url=url, headers=self.configs.get('headers'), data=self.configs.get('data'))
            
            if response.status_code != 200:
                raise HathorWalletError('Error getting wallet status.')

            return response.json()
        except:
            raise HathorWalletError('Error in the request.')

    def balance(self):
        # Not implemented other UID.
        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/wallet/balance')
            response = requests.get(url=url, headers=self.configs.get('headers'))
            
            if response.status_code != 200:
                raise HathorWalletError('Error getting wallet balance.')

            return response.json()

        except:
            raise HathorWalletError('Error in the request.')
            
    def stop(self):
        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/wallet/stop')
            response = requests.post(url=url, headers=self.configs.get('headers'))
            
            if response.status_code != 200:
                raise HathorWalletError('Error stop wallet.')

            return response.json()
            
        except:
            raise HathorWalletError('Error in the request.')

    def current_address(self, mark_as_used: Optional[str] = None):
        params: Optional[Dict[str, str]] = None

        if mark_as_used:
            params = {'mark_as_used': mark_as_used}

        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/wallet/address')
            response = requests.get(url=url, headers=self.configs.get('headers'), params=params)
            
            if response.status_code != 200:
                raise HathorWalletError(f'Error return the current address')

            return response.json()
            
        except:
            raise HathorWalletError('Error in the request.')

    def all_generated_addres(self) -> Dict[str, List]:
        try:
            url = parse.urljoin(self.configs.get('wallet_base_url'), '/wallet/addresses')
            response = requests.get(url=url, headers=self.configs.get('headers'))
            
            if response.status_code != 200:
                raise HathorWalletError(f'Error return all generated addresses of the wallet.')

            return response.json()
            
        except:
            raise HathorWalletError('Error in the request.')
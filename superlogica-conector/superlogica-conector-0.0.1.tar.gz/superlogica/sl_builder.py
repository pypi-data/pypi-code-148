from superlogica.buider import Builder
from superlogica.sl_conector import SLConector

class SuperlogicaBuilder(Builder):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._conector = SLConector()

    @property
    def conector(self) -> SLConector:
        conector = self._conector
        self.reset()
        return conector

    def auth(self, token, api_key) -> None:
        self._conector.add_headers(api_key, token)

    def configs(self, object='planos', **kwargs) -> None:
        method = 'GET' 
        url=f'https://api.superlogica.net/v2/financeiro/{object}'
         
        self._conector.add_params(method=method, url=url, **kwargs)

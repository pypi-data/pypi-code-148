import os
import pandas as pd
import itertools

from superlogica.conn import Connection

token = os.environ.get('TOKEN')
api_key = os.environ.get('APIKEY')

dict_config = {
    'token': token,
    'api_key': api_key,
    'object': 'produtos',
    'args': {
        'itensPorPagina': 200
    }
}

produtos = Connection(parameters=dict_config)

results = produtos.get(pages=3)

## Exemplo 1 iterando no genarator
# for r in results:
#     if len(r) > 0:
#         print(r)

## Exemplo 2 unificando lista de listas retornada da API

produtos = list(results)
print(len(produtos))
produtos = list(itertools.chain(*produtos))
print(len(produtos))

df_produtos = pd.DataFrame(produtos)
print(df_produtos.head(10))
from hestia_earth.utils.api import search, download_hestia
from hestia_earth.utils.tools import non_empty_list

from ..log import logger


TERM_NAME_MATCH_QUERY = {
    'products': lambda name: {
        'nested': {
            'path': 'products',
            'query': {
                'bool': {
                    'must': [
                        {'match': {'products.term.name.keyword': name}},
                        {'match': {'products.primary': 'true'}}
                    ]
                }
            }
        }
    },
    'inputs': lambda name: {
        'nested': {
            'path': 'inputs',
            'query': {
                'bool': {
                    'must': [
                        {'match': {'inputs.term.name.keyword': name}}
                    ]
                }
            }
        }
    }
}


def find_cycles(country_id: str, term_id: str, key: str, limit: int, recalculated: bool = False):
    country_name = download_hestia(country_id).get('name')
    term_name = download_hestia(term_id).get('name')
    cycles = search({
        'bool': {
            'must': [
                {
                    'match': {'@type': 'Cycle'}
                },
                TERM_NAME_MATCH_QUERY[key](term_name),
                {
                    'match': {
                        'site.country.name.keyword': country_name
                    }
                }
            ],
            'must_not': [{'match': {'aggregated': True}}]
        }
    }, limit=limit)
    logger.info(f"Found {len(cycles)} non-aggregated cycles with {key} '{term_name}' in '{country_name}'.")
    cycles = [download_hestia(c['@id'], 'Cycle', 'recalculated' if recalculated else None) for c in cycles]
    return non_empty_list(cycles)

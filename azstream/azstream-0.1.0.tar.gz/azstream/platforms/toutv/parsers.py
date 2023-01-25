import json
from ..platform import Platform
from typing import List, Dict, Any, Union
from ...types import SearchResult, TitleType, Title

def parse_search_results(platform: Platform, raw_titles: List[Dict[str, Any]]) -> List[SearchResult]:
    titles: List[SearchResult] = []
    unparsable = 0
    for raw_title in raw_titles:
        try:
            title = SearchResult(
                platform_tag=platform.tag,
                platform_id=platform.id,
                id=raw_title['Url'].split('/')[1],
                title=raw_title.get('DisplayText', 'N/A'),
                poster_url=raw_title.get('ImageUrl', None)
            )
            if not raw_title.get('IsFree', False):
                if not 'extra' in platform.get_available_channels():
                    title.has_access = False
            titles.append(title)
        except:
            unparsable += 1

    if unparsable > 0:
        platform.logger.warn(f'{unparsable} unparsable titles.')

    return titles


def parse_title(platform: Platform, raw_title: Dict[str, Any]) -> Union[Title, None]:
    try:
        title = Title(
            platform_tag=platform.tag,
            platform_id=platform.id,
            id=raw_title['Url'].split('/')[1],
            title=raw_title.get('Title', 'N/A'),
            poster_url=raw_title.get('ImageUrl', None),
            backdrop_url=raw_title.get('BackgroundImageUrl', None),
            synopsis=raw_title.get('Description', None)
        )
        try:
            metadata = json.loads(raw_title['StructuredMetadata'])
            for person in metadata.get('actor', []):
                if 'name' in person:
                    title.actors.append(person['name'])
            for person in metadata.get('director', []):
                if 'name' in person:
                    title.directors.append(person['name'])
            for person in metadata.get('author', []):
                if 'name' in person:
                    title.authors.append(person['name'])
            for person in metadata.get('producer', []):
                if 'name' in person:
                    title.producers.append(person['name'])
            for genre in metadata.get('genre', []):
                title.genres.append(genre)
            title_type = metadata.get('@type')
            if 'series' in title_type.lower():
                title.title_type = TitleType.SERIES
            elif 'movie' in title_type.lower():
                title.title_type = TitleType.MOVIE

        except:
            pass
        if not raw_title.get('IsFree', False):
            if not 'extra' in platform.get_available_channels():
                title.has_access = False
        return title
    except:
        platform.logger.error(f'Unable to parse the title.')
        return None

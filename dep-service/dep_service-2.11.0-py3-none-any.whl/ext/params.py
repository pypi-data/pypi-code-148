"""Api query params."""

from fastapi import Query


default_limit = 25

lang = Query(default='ru', example='en')

page = Query(default=1, example=2)
limit = Query(default=default_limit, example=default_limit)
sort_on = Query(default='desc', example='asc', alias='sortOn')
sort_by_name = Query(default=None, example='name', alias='sortBy')
sort_by_title = Query(default=None, example='title', alias='sortBy')
sort_by_event = Query(default=None, example='event', alias='sortBy')
layout_id = Query(default=None, example=118, alias='layout_id')
fragment_type = Query(default=None, example=3, alias='fragment_type')
fragment_parent = Query(
    default=None,
    example='0e22eb6e-fafe-4ef4-b408-6dffaff12900',
    alias='parent_id',
)

filter_name = Query(default=None, example='name', alias='search')
filter_title = Query(default=None, example='title', alias='search')
filter_hall = Query(default=None, example=100, alias='hall_id')
filter_company = Query(default=None, example=5, alias='company_id')
filter_pattern_type = Query(default=None, example=1, alias='pattern_type')
filter_place_in = Query(default=None, example='101,102,103', alias='place__in')
filter_layout_in = Query(default=None, example='599,600', alias='layout__in')
filter_outdated = Query(default=False, example=True, alias='outdated')
filter_label_name = Query(default=None, example='Сектор', alias='search')

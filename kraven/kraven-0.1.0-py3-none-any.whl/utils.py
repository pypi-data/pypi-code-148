import os
import pathlib
import sys
from typing import List

from glom import glom
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from . import constant
from .__main__ import BLACKLIST

PATH = pathlib.Path( __file__ ).parent


def resolve_token():

    try:
        token = os.environ[ "PRODUCT_HUNT_TOKEN" ]
    except KeyError:
        print( "Please set the environment variable PRODUCT_HUNT_TOKEN" )
        sys.exit( 1 )

    return token


TOKEN = resolve_token()

transport = RequestsHTTPTransport(
    url=constant.PRODUCT_HUNT_API, headers={
        "Authorization": f"Bearer {TOKEN}", "Content": "application/json"
        }
    )

client = Client( transport=transport, fetch_schema_from_transport=False )


def fetcher( schema: str, **kwargs ):

    # Use the frontend API for specific endpoints
    if BLACKLIST.count( schema ):
        transport.url = constant.PRODUCT_HUNT + "/frontend/graphql"

    try:
        with open( PATH.parent / f"schemas/{schema}.gql" ) as schema:
            plain = schema.read()
    except FileNotFoundError:
        print( "Invalid schema" )
        sys.exit( 1 )

    query = gql( plain )
    result = client.execute( query, variable_values=kwargs or None )

    return result


def format_node( schema: str, data: List[ dict ] ):
    _list_ = []

    for item in data:
        _list_.append( glom( item[ "node" ], schema ) )

    return _list_

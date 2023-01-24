import argparse
import sys

from rich import print_json
from rich.table import Table
from rich.console import Console

from . import constant, utils

table = Table()
console = Console()

BLACKLIST = constant.ENDPOINTS[ : 2 ]
JSON_ARGS = { "sort_keys": True, "indent": 2}

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description="Kraven - A Product Hunt CLI", usage="" )

    parser.add_argument( "action" )
    parser.add_argument( "slug", nargs="?", default=None )
    args = parser.parse_args()

    if not constant.ENDPOINTS.count( args.action ):
        print( "Invalid argument" )
        sys.exit( 1 )

    is_trending = args.action == "trending"

    params = { "kind": "POPULAR"} if is_trending else { "slug": args.slug}
    data = utils.fetcher( args.action, **params )

    if not BLACKLIST.count( args.action ):
        print_json( data=data, **JSON_ARGS )
        sys.exit( 1 )
    else:
        entry = constant.SCHEMAS[ args.action ]
        key = entry[ "key" ]
        entry.pop( "key" )

        base = data[ key ][ "edges" ]
        items = base[ 0 ][ "node" ][ "items" ] if is_trending else base
        nodes = items if is_trending else utils.format_node( entry, items )

        for col in [ "", *entry.keys() ]:
            table.add_column( col )

        for index, node in enumerate( nodes ):
            table.add_row( str( index + 1 ), *[ str( value ) for value in node.values() ] )

    console.print( table )

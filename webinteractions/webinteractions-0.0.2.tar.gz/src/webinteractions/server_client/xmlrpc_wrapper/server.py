"""Function to create xml-rpc server with functions provided by user"""

import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    """Request handler class used for creating simple
        xmlrpc server"""
    rpc_paths = ("/RPC2",)

def create_xmlrpc_server(
    paths=("/",),
    function_map={},
    hostname="localhost",
    port=8000,
    allow_none=False
):
    """Function creates a xmlrpc server and registers the functions provided
        in the form of a function map

        ARGS:
            paths: specify valid path of url for receiving xml-rpc requests
            function_map: dictionary of functions mapped with their function name
            hostname: hostname at which the xml-rpc server will listen for requests
            port: port number at which the xml-rpc server will listen for requests
            allow_none: if set to default value of False, calling functions with no return statement
            from client will return in Fault
    """

    RequestHandler.rpc_paths = paths

    with SimpleXMLRPCServer((hostname, port), requestHandler=RequestHandler, allow_none=allow_none) as server:
        for func_name in function_map.keys():
            server.register_function(function_map[func_name], name=func_name)

        print("Server listening on {}:{}".format(hostname, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt received, exiting...")
            sys.exit(0)

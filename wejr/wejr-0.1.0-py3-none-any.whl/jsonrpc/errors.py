from wejr.jsonrpc.response import Error

parse_json_error = Error(code=-32700, message="Parse error")
request_invalid_error = Error(code=-32600, message="Invalid Request")
method_not_found_error = Error(code=-32601, message="Method not found")
invalid_params_error = Error(code=-32602, message="Invalid params")
internal_error = Error(code=-32603, message="Internal error")

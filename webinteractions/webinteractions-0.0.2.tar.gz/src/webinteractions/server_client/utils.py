"""Provides helper functions for other modules"""

def get_synchronous_response(request_data, client_address):
    """Function returns response data for requests in synchronous server"""
    print(request_data)
    print("Received data from {}".format(client_address))

    if request_data == "ping":
        print("Ping sent back")
        response = bytes("ping received", "ascii")
    elif request_data == "get":
        print("Received a get request")
        response = bytes("html corresponding to a webpage", "ascii")
    elif request_data == "post":
        print("Received a post request")
        response = bytes("database was updated successfully", "ascii")

    return response


def get_threaded_response(request_data, thread_name, client_address):
    """Function return response data for requests in threaded server"""
    print(request_data)
    print("Received data from {}".format(client_address))

    if request_data == "ping":
        print("Ping sent back")
        response = bytes("{}: ping received".format(thread_name), "ascii")
    elif request_data == "get":
        print("Received a get request")
        response = bytes("{}: html corresponding to a webpage".format(thread_name), "ascii")
    elif request_data == "post":
        print("Received a post request")
        response = bytes("{}: database was updated successfully".format(thread_name), "ascii")

    return response

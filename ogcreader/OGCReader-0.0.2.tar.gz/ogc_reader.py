from wms.wms_111 import web_map_service


def web_map_service_111(url, xml=None, username=None, password=None, parse_remote_metadata=False, timeout=30,
                        headers=None, auth=None):
    """
    Create a WebMapService (OWSLib) object from a WMS 1.1.1 service URL.
    :param url: The URL of the WMS service.
    :param xml: The XML document to parse.
    :param username: The username to use for authentication.
    :param password: The password to use for authentication.
    :param parse_remote_metadata: If True, parse remote metadata.
    :param timeout: The timeout in seconds.
    :param headers: The headers to use for the request.
    :param auth: The authentication to use for the request.
    :return: A WebMapService (OWSLib) object.
    """
    base_url = url.strip()
    base_url = base_url.split('?')[0]
    return web_map_service(base_url, '1.1.1', xml, username, password, parse_remote_metadata, timeout, headers, auth)

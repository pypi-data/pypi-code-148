class Error(Exception):
    pass

class UnknownConnectorError(Error):
    def __init__(self, name):
        super().__init__(f'Unknown connector name {name}')

class UnsupportedFormatError(Error):
    def __init__(self, fmt):
        super().__init__(f'Unsupported format {fmt}')

class MissingConfiguration(Error):
    def __init__(self, name):
        super().__init__(f'{name} is required')

class JobError(Error):
    pass

class RateLimitedForTooLongError(Error):
    def __init__(self, max_rate_limit_retry_s):
        super().__init__(f'Rate-limited retries exceeded {max_rate_limit_retry_s} seconds')

class HTTPError(Error):
    def __init__(self, method, response, error_message):
        status_code = response.status_code
        url = response.url
        super().__init__(f'{status_code} code for {method} {url}: {error_message}')

class UnsupportedCloudServiceSchemeError(Error):
    def __init__(self, scheme):
        super().__init__(f'The cloud service scheme {scheme} is unsupported')

class UnsupportedCloudServiceError(Error):
    def __init__(self, service):
        super().__init__(f'The cloud service {service} is unsupported')

__all__ = ('JSONRPCHeaders',)


class JSONRPCHeaders:
    """List of JSONRPC request / response headers."""

    APP_ID_HEADER = 'X-App-Id'
    CORRELATION_ID_HEADER = 'X-Correlation-Id'
    ABORT_ON_ERROR = 'X-Abort-On-Error'
    SERVER_ID_HEADER = 'X-Server-Id'
    REQUEST_DEADLINE_HEADER = 'X-Request-Deadline'
    REQUEST_TIMEOUT_HEADER = 'X-Request-Timeout'
    CONTENT_TYPE_HEADER = 'Content-Type'
    SESSION_ID_HEADER = 'X-Session-Id'
    CALLBACK_ID = 'X-Callback-Id'
    AUTHORIZATION = 'Authorization'

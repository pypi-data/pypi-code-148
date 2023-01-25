"""
`Configs` is a class that contains the global configuration variables/parameters
to be used in the services
"""


class Configs:
    GRAPHQL_URL: str = "https://api-{env}.in.sportsxapp.com/graphiql"
    WS_URL: str = "wss://api-{env}.in.sportsxapp.com/socket/websocket"
    API_ENV = "staging"
    LOGIN_API: str = "login"
    CONFIRM_2FA: str = "confirm2Fa"
    REFRESH_TOKEN_API: str = "newToken"
    CHANNEL_CONNECTION_URL: str = "{url}?token={token}&vsn=2.0.0"

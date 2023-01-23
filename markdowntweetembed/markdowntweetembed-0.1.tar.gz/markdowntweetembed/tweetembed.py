import markdown
import tweepy


def setup_twitter_api(**kwargs):
    """Gets the API object after authorization
    and authentication.
    :keyword tweepy_api_key: The consumer API key.
    :keyword tweepy_api_key_secret: The consumer API key secret.
    :keyword tweepy_access_token: The access token.
    :keyword tweepy_access_token_secret: The access token secret.
    :returns: The Tweepy API object.
    """
    auth = tweepy.OAuthHandler(
        kwargs["tweepy_api_key"], kwargs["tweepy_api_key_secret"]
    )
    auth.set_access_token(
        kwargs["tweepy_access_token"], kwargs["tweepy_access_token_secret"]
    )
    return tweepy.API(auth)


class TweetEmbedExtension(markdown.Extension):
    def __init__(self, **kwargs):
        self.config = {
            "TW_API_KEY": [kwargs["TW_API_KEY"], "twitter developer api key"],
            "TW_API_KEY_SECRET": [
                kwargs["TW_API_KEY_SECRET"],
                "twitter developer api key secret",
            ],
            "TW_ACCESS_TOKEN": [
                kwargs["TW_ACCESS_TOKEN"],
                "twitter developer access token",
            ],
            "TW_ACCESS_TOKEN_SECRET": [
                kwargs["TW_ACCESS_TOKEN_SECRET"],
                "twitter developer access token secret",
            ],
            "twapi": [
                setup_twitter_api(
                    tweepy_api_key=kwargs["TW_API_KEY"],
                    tweepy_api_key_secret=kwargs["TW_API_KEY_SECRET"],
                    tweepy_access_token=kwargs["TW_ACCESS_TOKEN"],
                    tweepy_access_token_secret=kwargs["TW_ACCESS_TOKEN_SECRET"],
                ),
                "tweepy api",
            ],
        }
        super(TweetEmbedExtension, self).__init__(**kwargs)
        # super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            TwitterEmbedPattern(md, self.getConfigs()), "twitter_embed", 100
        )


class TwitterEmbedPattern(markdown.inlinepatterns.Pattern):
    url_RE = r"{{:twitter (https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})}}"

    def __init__(self, md, config):
        self.md = md
        self.twapi = config["twapi"]
        markdown.inlinepatterns.Pattern.__init__(self, self.url_RE, md)

    def handleMatch(self, m):
        tweet_url = m.group(2)
        resp = self.twapi.get_oembed(tweet_url)
        if resp["html"] is not None:
            return self.md.htmlStash.store(resp["html"])
        else:
            return "Error: Could not retrieve tweet embed"


def makeExtension(configs={}):
    return TweetEmbedExtension(configs=configs)

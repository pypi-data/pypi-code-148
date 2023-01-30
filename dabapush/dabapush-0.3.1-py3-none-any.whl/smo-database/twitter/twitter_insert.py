from hashlib import md5
from sqlalchemy import null
from . import twitter_schema as tw
import datetime
from sqlalchemy.orm import sessionmaker
from loguru import logger as log

class Twitter_Data:
    def __init__(self, engine):

        self.engine = engine

    def create_local_session(self):

        Session = sessionmaker()
        self.local_session = Session(bind=self.engine)

    def close_local_session(self):

        self.local_session.close()

    def strp_date(self, y):

        x = datetime.datetime.strptime(y, "%Y-%m-%dT%H:%M:%S.%fZ")

        return x

    def twitter_insert(self, data):

        data_dict = data

        new_tweet = tw.TwitterTweet(
            tweet_id=data_dict.get("id"),
            user_id=data_dict.get("author_id"),
            text=data_dict.get("text"),
            created_at=data_dict.get("created_at"),
            conversation_id=data_dict.get("conversation_id")
            if "conversation_id" in data_dict
            else "",
            in_reply_to_user_id=data_dict.get("in_reply_to_user_id")
            if "in_reply_to_user_id" in data_dict
            else "",
            lang=data_dict.get("lang") if "lang" in data_dict else "",
            possibly_sensitive=data_dict.get("possibly_sensitive")
            if "possibly_sensitive" in data_dict
            else False,
            retweet_count=data_dict.get(
                "public_metrics.retweet_count"
            ) if "public_metrics.retweet_count" in data_dict else 0,
            quote_count=data_dict.get("public_metrics.quote_count") if "public_metrics.quote_count" in data_dict else 0,
            like_count=data_dict.get("public_metrics.like_count") if "public_metrics.like_count" in data_dict else 0,
            reply_count=data_dict.get("public_metrics.reply_count") if "public_metrics.reply_count" in data_dict else 0,
            reply_settings=data_dict.get("reply_settings")
            if "reply_settings" in data_dict
            else None,
            year=self.strp_date(data_dict.get("created_at")).year,
            month=self.strp_date(data_dict.get("created_at")).month,
            day=self.strp_date(data_dict.get("created_at")).day,
            source=data_dict.get("source") if 'source' in data_dict else ''
        )
        self.local_session.merge(new_tweet)

        if "referenced_tweets" in data_dict:

            for i in range(len(data_dict.get("referenced_tweets"))):

                new_referenced_tweet = tw.TwitterReferencedTweet(
                    tweet_id=data_dict.get("id"),
                    referred_tweet_id=data_dict.get("referenced_tweets")[i].get("id"),
                    type=data_dict.get("referenced_tweets")[i].get("type"),
                )
                self.local_session.merge(new_referenced_tweet)

        if "entities.hashtags" in data_dict:
            for hashtag in data_dict.get("entities.hashtags"):
                new_hashtag = tw.TwitterHashtag(
                    tweet_id=data_dict.get("id"), tag=hashtag.get("tag")
                )

                self.local_session.merge(new_hashtag)

        if "entities.urls" in data_dict:
            for url_object in data_dict.get("entities.urls"):
                url: str = url_object.get("url")
                expanded_url: str = url_object.get("expanded_url")

                new_url = tw.TwitterUrl(
                    url_id = md5(expanded_url.encode("utf8")).hexdigest(),
                    url=url,
                    expanded_url=expanded_url
                )
                self.local_session.merge(new_url)

                new_referenced_url = tw.TwitterReferencedUrl(
                    tweet_id=data_dict.get("id"),
                    url_id=new_url.url_id
                )
                self.local_session.merge(new_referenced_url)

        if "entities.mentions" in data_dict:
            for mention in data_dict.get("entities.mentions"):
                
                try:
                    user_id = mention.get("username")
                    tweet_id = data_dict.get("id")
                    new_user_mention = tw.TwitterUserMention(
                        tweet_id=tweet_id,
                        username=user_id,
                    )

                    self.local_session.merge(new_user_mention)
                except AssertionError:
                    log.warning(f'Found malformed data: {data_dict}')
                except AttributeError:
                    log.warning(f'Someting is fishy here: {data_dict}')

        if "media" in data_dict:
            for i in range(len(data_dict.get("media"))):

                new_media = tw.TwitterMedia(
                    media_key=data_dict.get("media")[i].get("media_key"),
                    type=data_dict.get("media")[i].get("type"),
                    duration_ms=data_dict.get("media")[i].get("duration_ms")
                    if "duration_ms" in data_dict.get("media")[i]
                    else 0,
                    view_count=data_dict.get("media")[i]
                    .get("public_metrics")
                    .get("view_count") if 'public_metrics' in data_dict.get('media')[i] else 0,
                    preview_image_url=data_dict.get("media")[i].get(
                        "preview_image_url"
                    ),
                    height=data_dict.get("media")[i].get("height") if 'height' in data_dict.get('media')[i] else 0,
                    width=data_dict.get("media")[i].get("width") if 'width' in data_dict.get('media')[i] else 0,
                    media_url=None,  # insert if present
                    imagehash="",
                    imagehash_binary=None,
                )

                new_referenced_media = tw.TwitterReferencedMedia(
                    tweet_id=data_dict.get("id"),
                    media_key=data_dict.get("media")[i].get("media_key"),
                )

                self.local_session.merge(new_media)
                self.local_session.merge(new_referenced_media)

        new_user = tw.TwitterUser(
            user_id=data_dict.get("user.id"),
            name=data_dict.get("user.name"),
            username=data_dict.get("user.username"),
            created_at=data_dict.get("user.created")
            if "user.created_at" in data_dict
            else None,
            description=data_dict.get("user.description")
            if "user.description" in data_dict
            else "",
            profile_image_url=data_dict.get("user.profile_image_url")
            if "user.profile_image_url" in data_dict
            else "",
            verified=data_dict.get("user.verified")
            if "user.verified" in data_dict
            else False,
            protected=data_dict.get("user.protected")
            if "user.protected" in data_dict
            else False,
            location=data_dict.get("user.location")
            if "user.location" in data_dict
            else "",
        )

        self.local_session.merge(new_user)

        # self.local_session.commit()

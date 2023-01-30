from sqlalchemy import null
from . import telegram_schema as tg
import datetime
from sqlalchemy.orm import sessionmaker
from loguru import logger as log
from hashlib import md5

class Telegram_Data:
    def __init__(self, engine):

        self.engine = engine

    def create_local_session(self):

        Session = sessionmaker()
        self.local_session = Session(bind=self.engine)

    def close_local_session(self):

        self.local_session.close()

    def strp_date(self, y):

        x = datetime.datetime.strptime(y, "%Y-%m-%d %H:%M:%S")

        return x

    def telegram_insert(self, data):

        new_post = tg.TelegramPost(
            post_id=data.get("user.id") + "/" + data.get("id"),
            message_type=data.get("_"),
            post_number=data.get("id"),
            user_id=data.get("user.id"),
            message=data.get("message"),
            created_at=data.get("date"),
            edited_at=data.get("edit_date"),
            forward_count=data.get("forwards") \
                if data.get("forwards") is not None \
                else 0,
            view_count=data.get("views") \
                if data.get("views") is not None \
                else 0,
            reply_count=data.get("replies") \
                if data.get("replies") is not None \
                else 0,
            year=self.strp_date(data.get("date")).year,
            month=self.strp_date(data.get("date")).month,
            day=self.strp_date(data.get("date")).day,
        )
        self.local_session.merge(new_post)

        # if "referenced_tweets" in data_dict:

        #     for i in range(len(data_dict.get("referenced_tweets"))):

        #         new_referenced_tweet = tw.TwitterReferencedTweet(
        #             tweet_id=data_dict.get("id"),
        #             referred_tweet_id=data_dict.get("referenced_tweets")[i].get("id"),
        #             type=data_dict.get("referenced_tweets")[i].get("type"),
        #         )
        #         self.local_session.merge(new_referenced_tweet)

        if "fwd_from.from_id.channel_id" in data and \
            "fwd_from.channel_post" in data and \
            data.get("fwd_from.from_id.channel_id") is not None and \
            data.get("fwd_from.channel_post") is not None:

            new_forward = tg.TelegramReferencedPost(
                post_id = data.get("user.id") + "/" + data.get("id"),
                referred_post_id = data.get("fwd_from.from_id.channel_id") + \
                    "/" + data.get("fwd_from.channel_post"),
                referred_channel_id = data.get("fwd_from.from_id.channel_id"),
                referred_post_number = data.get("fwd_from.channel_post"),
                type = "forward"
            )

            log.info(f'Found referenced post in {data.get("user.id") + "/" + data.get("id")}.')

            self.local_session.merge(new_forward)

        if "entities" in data:

            for entity in data.get("entities"):

                if entity["_"] == "MessageEntityHashtag":

                    new_hashtag = tg.TelegramHashtag(
                        post_id=data.get("user.id") + "/" + data.get("id"),
                        tag=data.get("message")[
                            int(entity["offset"]) :
                            int(entity["offset"]) + int(entity["length"])
                        ]
                    )

                    self.local_session.merge(new_hashtag)

                # if entity["_"] == "MessageEntityTextUrl":

                #     new_url = tg.TelegramUrl(
                #         url=entity.get("url")
                #     )

                #     new_referenced_url = tg.TelegramReferencedUrl(
                #         post_id=data.get("user.id") + "/" + data.get("id")
                #     )

                #     self.local_session.merge(new_url)
                #     self.local_session.merge(new_referenced_url)

                if entity["_"] == "MessageEntityUrl" or entity["_"] == "MessageEntityTextUrl":
                    url = data.get("message")[
                            int(entity["offset"]) :
                            int(entity["offset"]) + int(entity["length"])
                    ]
                    if url is not None and isinstance(url, str):
                        url_id = md5(url.encode()).hexdigest(),
                        new_url = tg.TelegramUrl(
                            url_id = url_id,
                            url=url
                        )

                        self.local_session.merge(new_url)

                        new_referenced_url = tg.TelegramReferencedUrl(
                            post_id=data.get("user.id") + "/" + data.get("id"),
                            url_id=url_id
                        )

                        self.local_session.merge(new_referenced_url)

                if entity["_"] == "MessageEntityMentionName":

                    new_mention = tg.TelegramUserMention(
                        post_id = data.get("user.id") + "/" + data.get("id"),
                        user_id = entity["user_id"]
                    )
                    log.info(f'Found mention of {entity["user_id"]}for {data["user.title"]}')
                    self.local_session.merge(new_mention)

        # if "media" in data:
        #     media = data.get("media")
            # cpt_pk@smo-ubuntu-8gb-nbg1-1:~/mrna_neighbours$ cat 112*.jsonl | jq -s "[.[].media._] | unique"
            # [
            #   null,
            #   "MessageMediaDocument",
            #   "MessageMediaPhoto",
            #   "MessageMediaPoll",
            #   "MessageMediaWebPage"
            # ]
            # As it seems there are four types of media, where a Document is either
            # audio or video or something else which does not interest us. Polls
            # do not interest us, either. WebPage are questionable, whether they
            # have been already included in the entities.

            # cpt_pk@smo-ubuntu-8gb-nbg1-1:~/mrna_neighbours$ cat 112*.jsonl | jq -s "[.[].media.document.mime_type] | unique"
            # [
            # null,
            # "application/pdf",
            # "application/zip",
            # "audio/mpeg",
            # "audio/mpeg3",
            # "audio/ogg",
            # "audio/x-m4a",
            # "image/gif",
            # "image/jpeg",
            # "image/png",
            # "image/webp",
            # "video/mp4",
            # "video/quicktime"
            # ]

            # if media["_"] == "MessageMediaDocument":
            #     pass
            # elif media["_"] == "Document" and media["mime_type"] == "video/mp4":
            #     pass
            # elif media["_"] == "Document" and media["mime_type"] == "audio/ogg":
            #     pass

            # data.get("media")
            # new_media = tg.TelegramMedia(

            #     media_key=data.get("id"),
            #     type=data.get("media")[i].get("type"),
            #     duration_ms=data.get("media")[i].get("duration_ms")
            #     if "duration_ms" in data.get("media")[i]
            #     else 0,
            #     view_count=data.get("media")[i]
            #     .get("public_metrics")
            #     .get("view_count") if 'public_metrics' in data.get('media')[i] else 0,
            #     preview_image_url=data.get("media")[i].get(
            #         "preview_image_url"
            #     ),
            #     height=data.get("media")[i].get("height") if 'height' in data.get('media')[i] else 0,
            #     width=data.get("media")[i].get("width") if 'width' in data.get('media')[i] else 0,
            #     media_url=None,  # insert if present
            #     imagehash="",
            #     imagehash_binary=None,
            # )

            # new_referenced_media = tw.TwitterReferencedMedia(
            #     tweet_id=data_dict.get("id"),
            #     media_key=data_dict.get("media")[i].get("media_key"),
            # )

            # self.local_session.merge(new_media)
            # self.local_session.merge(new_referenced_media)

        new_user = tg.TelegramChannel(
            id=data.get("user.id"),
            title=data.get("user.title"),
            username=data.get("user.username"),
            created_at=data.get("user.date")
            if "user.date" in data
            else None,
            # description=data_dict.get("user.description")
            # if "user.description" in data_dict
            # else "",
            # profile_image_url=data_dict.get("user.profile_image_url")
            # if "user.profile_image_url" in data_dict
            # else "",
            verified=data.get("user.verified") or False,
            restricted=data.get("user.restricted") or False,
            # location=data_dict.get("user.location")
            # if "user.location" in data_dict
            # else "",
            signatures=data.get("user.signatures") or False,
            creator=data.get("user.creator") or False,
            megagroup=data.get("user.megagroup") or False,
            broadcast=data.get("user.broadcast") or False,
            gigagroup=data.get("user.gigagroup") or False,
            scam=data.get("user.scam") or False,
            min=data.get("user.min") or False,
            has_geo=data.get("user.has_geo") or False,
            has_link=data.get("user.has_link") or False,
        )

        self.local_session.merge(new_user)

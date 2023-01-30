from . import instagram_schema as insta
import json
import os
import datetime
from sqlalchemy.orm import sessionmaker


class Instagram_Data:
    def __init__(self, engine):

        self.engine = engine

    def create_local_session(self):

        Session = sessionmaker()
        self.local_session = Session(bind=self.engine)

    def close_local_session(self):

        self.local_session.close()

    def strp_date(self, y):

        x = datetime.datetime.strptime(y, "%Y-%m-%d  %H:%M:%S")

        return x

    def insta_insert(self, data):

        data_dict = data
        user_ids = {}

        if data_dict.get("account.id") not in user_ids:
            new_user = insta.InstagramUser(
                ct_id=data_dict.get("account.id"),
                instagram_id=data_dict.get("account.platformId")
                if "account.platformId" in data_dict
                else "",
                name=data_dict.get("account.name"),
                handle=data_dict.get("account.handle")
                if ("account.handle") in data_dict
                else "",
                profile_image_url=data_dict.get("account.profileImage"),
                verified=data_dict.get("account.verified"),
            )
            user_ids[data_dict.get("account.id")] = True
            self.local_session.merge(new_user)

        new_post = insta.InstagramPost(
            post_id=data_dict.get("platformId"),
            ct_id=data_dict.get("account.id"),
            description=data_dict.get("description")
            if "description" in data_dict
            else "",
            created_at=data_dict.get("date"),
            media=data_dict.get("type"),
            score=data_dict.get("score"),
            subscriber_count=data_dict.get("subscriberCount"),
            favourite_count=data_dict.get("statistics.actual.favoriteCount"),
            comment_count=data_dict.get("statistics.actual.commentCount"),
            entry_datetime=data_dict.get("written_at"),
            year=self.strp_date(data_dict.get("date")).year,
            month=self.strp_date(data_dict.get("date")).month,
            date=self.strp_date(data_dict.get("date")).day,
            source="CrowdTangle",
            like_view_counts_disabled=data_dict.get("likeAndViewCountsDisabled"),
        )
        self.local_session.merge(new_post)

        if "media" in data_dict:

            for i in range(len(data_dict.get("media"))):
                new_media = insta.InstagramMedia(
                    media_url=data_dict.get("media")[i].get("url"),
                    type_of_media=data_dict.get("media")[i].get("type"),
                    height=data_dict.get("media")[i].get("height"),
                    width=data_dict.get("media")[i].get("width"),
                    imagehash="",
                    imagehash_binary=None,
                )
                new_post_to_media = insta.InstagramPostToMedia(
                    post_id=data_dict.get("platformId")
                )

                self.local_session.merge(new_media)
                self.local_session.merge(new_post_to_media)

        if "expandedLinks" in data_dict:
            for i in range(len(data_dict.get("expandedLinks"))):

                new_ref_url = insta.InstagramReferencedUrl(
                    expanded_url=data_dict.get("expandedLinks")[i].get("expanded")
                )

                new_post_to_referenced_url = insta.InstagramPostToReferencedUrl(
                    post_id=data_dict.get("platformId")
                )

                self.local_session.merge(new_ref_url)
                self.local_session.merge(new_post_to_referenced_url)

        self.local_session.commit()

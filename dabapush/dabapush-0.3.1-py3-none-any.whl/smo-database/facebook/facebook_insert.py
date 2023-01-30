from . import facebook_schema as fb
import datetime
from sqlalchemy.orm import sessionmaker


class Facebook_Data:
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

    def fb_insert(self, data):

        data_dict = data

        user_ids = {}

        if data_dict.get("account.id") not in user_ids:

            new_user = fb.FacebookUser(
                ct_id=data_dict.get("account.id"),
                facebook_id=data_dict.get("account.platformId")
                if "account.platformId" in data_dict
                else "",
                handle=data_dict.get("account.handle")
                if ("account.handle") in data_dict
                else "",
                name=data_dict.get("account.name"),
                profile_image_url=data_dict.get("account.profileImage"),
                account_type=data_dict.get("account.accountType"),
                verified=data_dict.get("account.verified"),
            )

            user_ids[data_dict.get("account.id")] = True
            self.local_session.merge(new_user)

        new_post = fb.FacebookPost(
            post_id=data_dict.get("platformId"),
            ct_id=data_dict.get("account.id"),
            text=data_dict.get("message") if "message" in data_dict else "",
            description=data_dict.get("description")
            if "description" in data_dict
            else "",
            caption=data_dict.get("caption") if "caption" in data_dict else "",
            title=data_dict.get("title") if "title" in data_dict else "",
            image_text=data_dict.get("imageText") if "imageText" in data_dict else "",
            created_at=data_dict.get("date"),
            type=data_dict.get("type"),
            score=data_dict.get("score"),
            subcriber_count=data_dict.get("subscriberCount"),
            like_count=data_dict.get("statistics.actual.likeCount"),
            share_count=data_dict.get("statistics.actual.shareCount"),
            comment_count=data_dict.get("statistics.actual.commentCount"),
            love_count=data_dict.get("statistics.actual.loveCount"),
            wow_count=data_dict.get("statistics.actual.wowCount"),
            haha_count=data_dict.get("statistics.actual.hahaCount"),
            sad_count=data_dict.get("statistics.actual.sadCount"),
            angry_count=data_dict.get("statistics.actual.angryCount"),
            thankful_count=data_dict.get("statistics.actual.thankfulCount"),
            care_count=data_dict.get("statistics.actual.careCount"),
            entry_datetime=data_dict.get("written_at"),
            year=self.strp_date(data_dict.get("date")).year,
            month=self.strp_date(data_dict.get("date")).month,
            date=self.strp_date(data_dict.get("date")).day,
            source="CrowdTangle",
        )

        self.local_session.merge(new_post)

        if "media" in data_dict:

            for i in range(len(data_dict.get("media"))):

                new_media = fb.FacebookMedia(
                    media_url=data_dict.get("media")[i].get("url"),
                    type=data_dict.get("media")[i].get("type"),
                    full=data_dict.get("media")[i].get("full"),
                    height=data_dict.get("media")[i].get("height"),
                    width=data_dict.get("media")[i].get("width"),
                    imagehash="",
                    imagehash_binary=None,
                )

                new_post_to_media = fb.FacebookPostToMedia(
                    post_id=data_dict.get("platform_Id")
                )

                self.local_session.merge(new_media)
                self.local_session.merge(new_post_to_media)

        if "expandedLinks" in data_dict:

            for i in range(len(data_dict.get("expandedLinks"))):

                new_ref_url = fb.FacebookReferencedUrl(
                    expanded_url=data_dict.get("expandedLinks")[i].get("expanded")
                )

                new_post_to_referenced_url = fb.FacebookPostToReferencedUrl(
                    post_id=data_dict.get("platformId")
                )

                self.local_session.merge(new_ref_url)
                self.local_session.merge(new_post_to_referenced_url)

        self.local_session.commit()

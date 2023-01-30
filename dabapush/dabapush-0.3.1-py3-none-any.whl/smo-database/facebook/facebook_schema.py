# coding: utf-8
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    Sequence,
    SmallInteger,
    Text,
    DDL,
)
from sqlalchemy.dialects.postgresql import ENUM, VARCHAR, BYTEA
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import event

Base = declarative_base()
metadata = Base.metadata

schema_name = "facebook"
event.listen(
    Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS facebook")
)


class FacebookMedia(Base):
    __tablename__ = "media"
    __table_args__ = {"schema": schema_name}

    media_id = Column(
        Integer, Sequence("media_id_seq", schema=schema_name), primary_key=True
    )
    media_url = Column(VARCHAR(), nullable=False)
    type = Column(ENUM("photo", "video", name="media_type", schema=schema_name))
    full = Column(VARCHAR())
    height = Column(Integer)
    width = Column(Integer)
    imagehash = Column(VARCHAR(), index=True)
    imagehash_binary = Column(BYTEA)


class FacebookPostToMedia(Base):
    __tablename__ = "post_to_media"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_id = Column(
        Integer,
        Sequence("post_to_media_id_seq", schema=schema_name),
        primary_key=True,
        nullable=False,
    )


class FacebookPost(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True)
    ct_id = Column(BigInteger, nullable=False, index=True)
    text = Column(Text)
    description = Column(Text)
    caption = Column(Text)
    title = Column(Text)
    image_text = Column(Text, nullable=True)
    type = Column(
        ENUM(
            "photo",
            "link",
            "youtube",
            "native_video",
            "live_video_scheduled",
            "live_video_completed",
            "status",
            name="media_type",
            schema=schema_name,
        ),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, index=True)
    score = Column(Float)
    subscriber_count = Column(Integer)
    like_count = Column(Integer)
    share_count = Column(Integer)
    comment_count = Column(Integer)
    love_count = Column(Integer)
    wow_count = Column(Integer)
    haha_count = Column(Integer)
    sad_count = Column(Integer)
    angry_count = Column(Integer)
    thankful_count = Column(Integer)
    care_count = Column(Integer)
    entry_datetime = Column(DateTime, nullable=False)
    year = Column(SmallInteger, nullable=False, index=True)
    month = Column(SmallInteger, nullable=False, index=True)
    date = Column(SmallInteger, nullable=False, index=True)
    source = Column(VARCHAR(), nullable=False)
    multi_media = Column(Boolean)


class FacebookReferencedUrl(Base):
    __tablename__ = "referenced_urls"
    __table_args__ = {"schema": schema_name}

    expanded_url_id = Column(
        Integer, Sequence("expanded_url_id_seq", schema=schema_name), primary_key=True
    )
    expanded_url = Column(VARCHAR(), primary_key=True, nullable=False)


class FacebookUser(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": schema_name}

    ct_id = Column(BigInteger, primary_key=True)
    facebook_id = Column(BigInteger, nullable=True, index=True)
    name = Column(VARCHAR(), nullable=False)
    handle = Column(VARCHAR(), nullable=True)
    profile_image_url = Column(VARCHAR())
    verified = Column(Boolean)
    account_type = Column(
        ENUM(
            "facebook_page",
            "facebook_profile",
            "facebook_group",
            name="account_type",
            schema=schema_name,
        )
    )
    page_category = Column(VARCHAR())


class FacebookPostToReferencedUrl(Base):
    __tablename__ = "post_to_referenced_url"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_id = Column(
        Integer,
        Sequence("post_to_referenced_url_id_seq", schema=schema_name),
        primary_key=True,
        nullable=False,
    )

# coding: utf-8
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Sequence,
    SmallInteger,
    Text,
    ForeignKey,
    DDL,
)
from sqlalchemy.dialects.postgresql import ENUM, VARCHAR, BYTEA
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import event

Base = declarative_base()
metadata = Base.metadata

schema_name = "twitter"
event.listen(Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS twitter"))


class TwitterHashtag(Base):
    __tablename__ = "hashtags"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    tag = Column(VARCHAR(), primary_key=True, nullable=False)

class TwitterMedia(Base):
    __tablename__ = "media"
    __table_args__ = {"schema": schema_name}

    media_key = Column(VARCHAR(), primary_key=True)
    type = Column(
        ENUM("photo", "video", "animated_gif", name="media_type", schema=schema_name)
    )
    duration_ms = Column(Integer)
    preview_image_url = Column(VARCHAR())
    view_count = Column(Integer)
    height = Column(Integer)
    width = Column(Integer)
    media_url = Column(VARCHAR(), nullable=True)
    imagehash = Column(VARCHAR(), index=True)
    imagehash_binary = Column(BYTEA)


class TwitterReferencedMedia(Base):
    __tablename__ = "referenced_media"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_key = Column(VARCHAR(), primary_key=True, nullable=False)


class TwitterReferencedTweet(Base):
    __tablename__ = "referenced_tweets"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    referred_tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    type = Column(
        ENUM(
            "retweeted",
            "quoted",
            "replied_to",
            name="reference_type",
            schema=schema_name,
        ),
        nullable=False,
    )


class TwitterReferencedUrl(Base):
    __tablename__ = "twitter_referenced_urls"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    url_id = Column(Text)


class TwitterTweet(Base):
    __tablename__ = "tweets"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True)
    user_id = Column(VARCHAR(), nullable=False, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)
    conversation_id = Column(VARCHAR(), index=True)
    in_reply_to_user_id = Column(VARCHAR(), index=True)
    lang = Column(VARCHAR())
    possibly_sensitive = Column(Boolean)
    retweet_count = Column(Integer)
    quote_count = Column(Integer)
    like_count = Column(Integer)
    reply_count = Column(Integer)
    reply_settings = Column(
        ENUM(
            "everyone",
            "mentionedUsers",
            "following",
            "other",
            name="reply_settings",
            schema=schema_name,
        )
    )
    year = Column(SmallInteger, nullable=False, index=True)
    month = Column(SmallInteger, nullable=False, index=True)
    day = Column(SmallInteger, nullable=False, index=True)
    source = Column(VARCHAR())

class TwitterUrl(Base):
    __tablename__ = "urls"
    __table_args__ = {"schema": schema_name}

    url_id = Column(
        Text,
        primary_key=True,
    )
    url = Column(VARCHAR(), nullable=False)
    expanded_url = Column(VARCHAR(), nullable=False)


class TwitterUserMention(Base):
    __tablename__ = "user_mentions"
    __table_args__ = {"schema": schema_name}

    tweet_id = Column(VARCHAR(), primary_key=True, nullable=False)
    username = Column(VARCHAR(), primary_key=True, nullable=False)

class TwitterUser(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": schema_name}

    user_id = Column(VARCHAR(), primary_key=True)
    name = Column(VARCHAR(), nullable=False)
    username = Column(VARCHAR(), nullable=False)
    created_at = Column(DateTime)
    description = Column(VARCHAR())
    profile_image_url = Column(VARCHAR())
    verified = Column(Boolean)
    protected = Column(Boolean)
    location = Column(VARCHAR())

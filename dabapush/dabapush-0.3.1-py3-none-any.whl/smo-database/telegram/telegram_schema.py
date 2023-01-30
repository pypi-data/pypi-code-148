# coding: utf-8
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Sequence,
    SmallInteger,
    Text,
    DDL,
)
from sqlalchemy.dialects.postgresql import VARCHAR, ENUM, BYTEA
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import event

Base = declarative_base()
metadata = Base.metadata

schema_name = "telegram"
event.listen(Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS telegram"))

class TelegramPost(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": schema_name}

    post_id = Column(Text, primary_key=True)
    user_id = Column(Text, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, index=True)
    message = Column(Text)
    message_type = Column(Text)
    post_number = Column(Integer)
    edited_at = Column(DateTime)
    forward_count = Column(Integer)
    view_count = Column(Integer)
    reply_count = Column(Integer)
    year = Column(SmallInteger, nullable=False, index=True)
    month = Column(SmallInteger, nullable=False, index=True)
    day = Column(SmallInteger, nullable=False, index=True)

class TelegramChannel(Base):
    """ORM-Wrapper for Telegram Channels"""
    __tablename__ = "channels"
    __table_args__ = {"schema": schema_name}

    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    created_at = Column(DateTime)
    # description = Column(Text)
    chat_image_id = Column(Text)
    verified = Column(Boolean)
    restricted = Column(Boolean)
    signatures = Column(Boolean) # ??
    creator = Column(Boolean) # ??
    broadcast = Column(Boolean)
    megagroup = Column(Boolean)
    gigagroup = Column(Boolean)
    scam = Column(Boolean)
    min = Column(Boolean) # ??
    has_link = Column(Boolean)
    has_geo = Column(Boolean)

class TelegramHashtag(Base):
    __tablename__ = "hashtags"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    tag = Column(VARCHAR(), primary_key=True, nullable=False)

class TelegramReferencedUrl(Base):
    __tablename__ = "referenced_urls"
    __table_args__ = {"schema": schema_name}

    post_id = Column(Text, primary_key=True, nullable=False)
    url_id = Column(Text, primary_key=True, nullable=False)

class TelegramUrl(Base):
    __tablename__ = "urls"
    __table_args__ = {"schema": schema_name}

    url_id = Column(
        Text,
        primary_key=True,
    )
    url = Column(VARCHAR(), nullable=False)

class TelegramReferencedPost(Base):
    ''' Collects referenced posts which originate from public channels.
    Posts from (private) should be ignored and do not fit into the below specs.
    '''
    __tablename__ = "referenced_post"
    __table_args__ = {"schema": schema_name}

    post_id =               Column(Text, primary_key=True, nullable=False)
    referred_post_id =      Column(Text, primary_key=True, nullable=False)
    referred_channel_id =   Column(Text)
    referred_post_number =  Column(Text)
    type = Column(
        ENUM(
            "forward",
            name="reference_type",
            schema=schema_name,
        ),
        nullable=False,
    )

class TelegramUserMention(Base):
    __tablename__ = "user_mentions"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    user_id = Column(VARCHAR())
    username = Column(VARCHAR())

class TelegramMedia(Base):
    __tablename__ = "media"
    __table_args__ = {"schema": schema_name}

    media_id = Column(VARCHAR(), primary_key=True)
    type = Column(
        ENUM(
            "photo",
            "video",
            "audio"
            "animated_gif",
            name="media_type",
            schema=schema_name)
    )
    date = Column(DateTime)
    duration_ms = Column(Integer)
    preview_image_url = Column(VARCHAR())
    view_count = Column(Integer)
    height = Column(Integer)
    width = Column(Integer)
    media_url = Column(VARCHAR(), nullable=True)
    imagehash = Column(VARCHAR(), index=True)
    imagehash_binary = Column(BYTEA)


class TelegramReferencedMedia(Base):
    __tablename__ = "referenced_media"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_id = Column(VARCHAR(), primary_key=True, nullable=False)

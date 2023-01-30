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

schema_name = "instagram"
event.listen(
    Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS instagram")
)


class InstagramMedia(Base):
    __tablename__ = "media"
    __table_args__ = {"schema": schema_name}

    media_id = Column(
        Integer, Sequence("media_id_seq", schema=schema_name), primary_key=True
    )
    media_url = Column(VARCHAR(), nullable=False)
    type_of_media = Column(
        ENUM(
            "photo",
            "video",
            "link",
            "youtube",
            "igtv",
            "album",
            name="media_type",
            schema=schema_name,
        )
    )
    height = Column(Integer)
    width = Column(Integer)
    imagehash = Column(VARCHAR(), index=True)
    imagehash_binary = Column(BYTEA)


class InstagramPostToMedia(Base):
    __tablename__ = "post_to_media"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_id = Column(
        Integer,
        Sequence("post_to_media_id_seq", schema=schema_name),
        primary_key=True,
        nullable=False,
    )


class InstagramPost(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True)
    ct_id = Column(BigInteger, nullable=False, index=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)
    media = Column(
        ENUM(
            "photo",
            "video",
            "link",
            "youtube",
            "igtv",
            "album",
            name="media_type",
            schema=schema_name,
        )
    )
    score = Column(Float)
    subscriber_count = Column(Integer)
    favourite_count = Column(Integer)
    comment_count = Column(Integer)
    entry_datetime = Column(DateTime, nullable=False)
    year = Column(SmallInteger, nullable=False, index=True)
    month = Column(SmallInteger, nullable=False, index=True)
    date = Column(SmallInteger, nullable=False, index=True)
    source = Column(VARCHAR(), nullable=False)
    like_view_counts_disabled = Column(Boolean)


class InstagramUser(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "instagram"}

    ct_id = Column(BigInteger, primary_key=True)
    instagram_id = Column(BigInteger)
    name = Column(VARCHAR(), nullable=False)
    handle = Column(VARCHAR())
    profile_image_url = Column(VARCHAR())
    verified = Column(Boolean)


class InstagramPostToReferencedUrl(Base):
    __tablename__ = "post_to_referenced_url"
    __table_args__ = {"schema": schema_name}

    post_id = Column(VARCHAR(), primary_key=True, nullable=False)
    media_id = Column(
        Integer,
        Sequence("post_to_referenced_url_id_seq", schema=schema_name),
        primary_key=True,
        nullable=False,
    )


class InstagramReferencedUrl(Base):
    __tablename__ = "referenced_urls"
    __table_args__ = {"schema": schema_name}

    expanded_url_id = Column(
        Integer, Sequence("expanded_url_id_seq", schema=schema_name), primary_key=True
    )
    expanded_url = Column(VARCHAR(), primary_key=True, nullable=False)

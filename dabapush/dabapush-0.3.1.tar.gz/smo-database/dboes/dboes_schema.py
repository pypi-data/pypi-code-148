# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Integer, Sequence, SmallInteger, DDL
from sqlalchemy.dialects.postgresql import ENUM, VARCHAR, REAL, UUID
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import event

Base = declarative_base()
metadata = Base.metadata

schema_name = "dboes"
event.listen(Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS dboes"))


class DboesEntity(Base):
    __tablename__ = "entities"
    __table_args__ = {"schema": schema_name}

    # generic fields
    dboes_id = Column(UUID, primary_key=True)
    list = Column(VARCHAR(), nullable=False)
    name = Column(VARCHAR(), nullable=False)
    comment = Column(VARCHAR(), nullable=True)
    picture = Column(VARCHAR(), nullable=True)
    wikipedia = Column(VARCHAR(), nullable=True)
    homepage = Column(VARCHAR(), nullable=True)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(VARCHAR(), nullable=False)
    modified_at = Column(DateTime, nullable=False)
    modified_by = Column(VARCHAR(), nullable=False)

    # specific fields
    party = Column(VARCHAR(), nullable=True)
    district = Column(VARCHAR(), nullable=True)
    gender = Column(
        ENUM("männlich", "weiblich", "divers", name="gender", schema=schema_name),
        nullable=True,
    )

    # Twitter
    sm_twitter_id = Column(VARCHAR())
    sm_twitter_user = Column(VARCHAR())
    sm_twitter_verified = Column(Boolean)

    # Facebook
    sm_facebook_id = Column(VARCHAR())
    sm_facebook_user = Column(VARCHAR())
    sm_facebook_verified = Column(Boolean)

    # Instagram
    sm_instagram_id = Column(VARCHAR())
    sm_instagram_user = Column(VARCHAR())
    sm_instagram_verified = Column(Boolean)

    # Youtube
    sm_youtube_id = Column(VARCHAR())
    sm_youtube_user = Column(VARCHAR())
    sm_youtube_verified = Column(Boolean)

    # Telegram
    sm_telegram_id = Column(VARCHAR())
    sm_telegram_user = Column(VARCHAR())
    sm_telegram_verified = Column(Boolean)

    # Tik Tok
    sm_tiktok_id = Column(VARCHAR())
    sm_tikok_user = Column(VARCHAR())
    sm_tiktok_verified = Column(Boolean)


class DboesTag(Base):
    __tablename__ = "tags"
    __table_args__ = {"schema": schema_name}

    tag_id = Column(
        Integer, Sequence("media_id_seq", schema=schema_name), primary_key=True
    )
    tag_name = Column(VARCHAR(), nullable=False)
    tag_category = Column(VARCHAR(), nullable=True)


class DboesEntityToTag(Base):
    __tablename__ = "entity_to_tag"
    __table_args__ = {"schema": schema_name}

    dboes_id = Column(UUID, primary_key=True)
    tag_id = Column(Integer, primary_key=True)


class DboesMetric(Base):
    __tablename__ = "metrics"
    __table_args__ = {"schema": schema_name}

    dboes_id = Column(UUID, primary_key=True)
    metric = Column(VARCHAR(), primary_key=True, index=True)
    year = Column(SmallInteger, nullable=False, primary_key=True, index=True)
    month = Column(SmallInteger, nullable=False, primary_key=True, index=True)
    date = Column(SmallInteger, nullable=False, primary_key=True, index=True)
    value = Column(REAL, nullable=False)

"""add is_generated_from_ldap column to person

Revision ID: 82ee682204ab
Revises: 29df910f04a4
Create Date: 2022-10-14 13:09:59.006291

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from zou.migrations.utils.base import BaseMixin
from sqlalchemy_utils import UUIDType, EmailType, LocaleType, TimezoneType
from babel import Locale
from pytz import timezone as pytz_timezone
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = "82ee682204ab"
down_revision = "29df910f04a4"
branch_labels = None
depends_on = None

base = declarative_base()


class Department(base, BaseMixin):
    """
    Studio department like modeling, animation, etc.
    """

    __tablename__ = "department"
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    color = sa.Column(sa.String(7), nullable=False)


department_link = sa.Table(
    "department_link",
    base.metadata,
    sa.Column("person_id", UUIDType(binary=False), sa.ForeignKey("person.id")),
    sa.Column(
        "department_id", UUIDType(binary=False), sa.ForeignKey("department.id")
    ),
)


class Person(base, BaseMixin):
    """
    Describe a member of the studio (and an API user).
    """

    __tablename__ = "person"
    first_name = sa.Column(sa.String(80), nullable=False)
    last_name = sa.Column(sa.String(80), nullable=False)
    email = sa.Column(EmailType, unique=True)
    phone = sa.Column(sa.String(30))

    active = sa.Column(sa.Boolean(), default=True)
    archived = sa.Column(sa.Boolean(), default=False)
    last_presence = sa.Column(sa.Date())

    password = sa.Column(sa.LargeBinary(60))
    desktop_login = sa.Column(sa.String(80))
    shotgun_id = sa.Column(sa.Integer, unique=True)
    timezone = sa.Column(
        TimezoneType(backend="pytz"),
        default=pytz_timezone("Europe/Paris"),
    )
    locale = sa.Column(LocaleType, default=Locale("en", "US"))
    data = sa.Column(JSONB)
    role = sa.Column(sa.String(30), default="user")
    has_avatar = sa.Column(sa.Boolean(), default=False)

    notifications_enabled = sa.Column(sa.Boolean(), default=False)
    notifications_slack_enabled = sa.Column(sa.Boolean(), default=False)
    notifications_slack_userid = sa.Column(sa.String(60), default="")
    notifications_mattermost_enabled = sa.Column(sa.Boolean(), default=False)
    notifications_mattermost_userid = sa.Column(sa.String(60), default="")
    notifications_discord_enabled = sa.Column(sa.Boolean(), default=False)
    notifications_discord_userid = sa.Column(sa.String(60), default="")

    departments = orm.relationship(
        "Department", secondary=department_link, lazy="joined"
    )

    is_generated_from_ldap = sa.Column(sa.Boolean(), default=False)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person",
        sa.Column("is_generated_from_ldap", sa.Boolean(), default=False),
    )
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    persons = session.query(Person).all()
    for person in persons:
        if person.password == b"default":
            person.password = None
            person.is_generated_from_ldap = True
        else:
            person.is_generated_from_ldap = False
    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    persons = session.query(Person).all()
    for person in persons:
        if person.is_generated_from_ldap:
            person.password = b"default"
    session.commit()
    op.drop_column("person", "is_generated_from_ldap")
    # ### end Alembic commands ###

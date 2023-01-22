#!/usr/bin/env python

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import DataClassJsonMixin

###############################################################################


class IngestionModel:
    """Base class for IngestionModel type."""


###############################################################################


@dataclass
class Person(IngestionModel, DataClassJsonMixin):
    """
    Primarily the council members, this could technically include the mayor or city
    manager, or any other "normal" presenters and attendees of meetings.

    Notes
    -----
    If router_string is not provided, and the Person did not exist prior to ingestion,
    router_string will be generated from name.

    The email, phone, website will be updated if changed from prior values.
    The picture will be uploaded or updated in the CDP file storage system.

    If person is operating under new roles or new seat, new Role and Seat documents will
    be stored.
    """

    name: str
    is_active: bool = True
    router_string: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None
    picture_uri: str | None = None
    seat: Seat | None = None
    external_source_id: str | None = None


@dataclass
class Vote(IngestionModel, DataClassJsonMixin):
    """
    A reference tying a specific person and an event minutes item together.

    Notes
    -----
    The in_majority field stored in the database will be calculated from the provided
    list of votes.
    """

    person: Person
    decision: str
    external_source_id: str | None = None


@dataclass
class SupportingFile(IngestionModel, DataClassJsonMixin):
    """
    A file related tied to a matter or minutes item.

    Notes
    -----
    This file is not stored in the CDP file storage system.
    """

    name: str
    uri: str
    external_source_id: str | None = None


@dataclass
class Matter(IngestionModel, DataClassJsonMixin):
    """
    A matter is a specific legislative document.
    e.g. A bill, resolution, initiative, etc.
    """

    name: str
    matter_type: str
    title: str
    result_status: str | None = None
    sponsors: list[Person] | None = None
    external_source_id: str | None = None


@dataclass
class MinutesItem(IngestionModel, DataClassJsonMixin):
    """
    An item referenced during a meeting.
    This can be a matter but it can be a presentation or budget file, etc.
    """

    name: str
    description: str | None = None
    external_source_id: str | None = None


@dataclass
class EventMinutesItem(IngestionModel, DataClassJsonMixin):
    """
    Details about a specific item during an event.

    Notes
    -----
    If index is not provided, the index will be set to the index of the item in the
    whole EventMinutesItem list on Event.

    If matter is provided, the supporting_files will be additionally be stored as
    MatterFile.
    """

    minutes_item: MinutesItem
    index: int | None = None
    matter: Matter | None = None
    supporting_files: list[SupportingFile] | None = None
    decision: str | None = None
    votes: list[Vote] | None = None


@dataclass
class Session(IngestionModel, DataClassJsonMixin):
    """
    A session is a working period for an event.
    For example, an event could have a morning and afternoon session.

    Notes
    -----
    video_start_time is a duration relative to the beginning of the video in
    HH:MM:SS format. It does not affect nor is relative to session_datetime
    or any other datetime. If the portion of the video relavent to the session
    begins 37m50s into the full video, video_start_time will be "37:50".
    An absent start time is equivalent to the beginning of the video, and an
    absent end time is equivalent to the end of the video, so either can be omitted.
    """

    session_datetime: datetime
    video_uri: str
    session_index: int
    video_start_time: str | None = None
    video_end_time: str | None = None
    caption_uri: str | None = None
    external_source_id: str | None = None

    def __post_init__(self) -> None:
        """Operations to run after initialization."""
        # validate start/end time pair during ingestion
        if self.video_start_time and self.video_end_time:
            # fill in potentially missing hh:mm:s
            # for flexible input format [h[h:[m[m:[s]]]]]s
            start = list(map(int, ("00:00:0" + self.video_start_time).split(":")))
            end = list(map(int, ("00:00:0" + self.video_end_time).split(":")))
            start.reverse()
            end.reverse()
            start_seconds = start[0] + start[1] * 60 + start[2] * 3600
            end_seconds = end[0] + end[1] * 60 + end[2] * 3600
            if start_seconds >= end_seconds:
                raise ValueError("start_time must be less than end_time if both exist")


@dataclass
class Body(IngestionModel, DataClassJsonMixin):
    """
    A meeting body. This can be full council, a subcommittee, or "off-council" matters
    such as election debates.

    Notes
    -----
    If start_datetime is not provided, and the Body did not exist prior to ingestion,
    the session datetime associated with this ingestion will be used as start_datetime
    during storage.
    """

    name: str
    is_active: bool = True
    start_datetime: datetime | None = None
    description: str | None = None
    end_datetime: datetime | None = None
    external_source_id: str | None = None


@dataclass
class Role(IngestionModel, DataClassJsonMixin):
    """
    A role is a person's job for a period of time in the city council. A person can
    (and should) have multiple roles. For example: a person has two terms as city
    council member for district four then a term as city council member for a citywide
    seat. Roles can also be tied to committee chairs. For example: a council member
    spends a term on the transportation committee and then spends a term on the finance
    committee.

    Notes
    -----
    If start_datetime is not provided, and the Role did not exist prior to ingestion,
    the session datetime associated with this ingestion will be used as start_datetime
    during storage.
    """

    title: str
    body: Body | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    external_source_id: str | None = None


@dataclass
class Seat(IngestionModel, DataClassJsonMixin):
    """
    An electable office on the City Council. I.E. "Position 9".

    Notes
    -----
    The electoral_area and electoral_type will be updated if changed from prior values.
    The image will be uploaded or updated in the CDP file storage system.
    """

    name: str
    electoral_area: str | None = None
    electoral_type: str | None = None
    image_uri: str | None = None
    external_source_id: str | None = None
    roles: list[Role] | None = None


@dataclass
class EventIngestionModel(IngestionModel, DataClassJsonMixin):
    """
    An event can be a normally scheduled meeting, a special event such as a press
    conference or election debate, and, can be upcoming or historical.

    Notes
    -----
    If static_thumbnail_uri and/or hover_thumbnail_uri is not provided,
    it will be generated during pipeline processing.

    The earliest session_datetime will be used for the overall event_datetime.
    """

    body: Body
    sessions: list[Session]
    event_minutes_items: list[EventMinutesItem] | None = None
    agenda_uri: str | None = None
    minutes_uri: str | None = None
    static_thumbnail_uri: str | None = None
    hover_thumbnail_uri: str | None = None
    external_source_id: str | None = None


###############################################################################


EXAMPLE_MINIMAL_EVENT = EventIngestionModel(
    body=Body(name="Full Council"),
    sessions=[
        Session(
            session_datetime=datetime.utcnow(),
            video_uri=(
                "https://video.seattle.gov/media/council/brief_072219_2011957V.mp4"
            ),
            session_index=0,
        ),
    ],
)


EXAMPLE_FILLED_EVENT = EventIngestionModel(
    body=Body(name="Full Council"),
    sessions=[
        Session(
            session_datetime=datetime.utcnow(),
            video_uri=(
                "https://video.seattle.gov/media/council/council_101220_2022077V.mp4"
            ),
            session_index=0,
        ),
        Session(
            session_datetime=datetime.utcnow(),
            video_uri=(
                "https://video.seattle.gov/media/council/council_113020_2022091V.mp4"
            ),
            video_start_time=("00:00:00"),
            video_end_time=("99:59:59"),
            caption_uri=(
                "https://www.seattlechannel.org/documents/seattlechannel/closedcaption/2020/council_113020_2022091.vtt"  # noqa: E501
            ),
            session_index=1,
        ),
    ],
    event_minutes_items=[
        EventMinutesItem(
            minutes_item=MinutesItem(name="Inf 1656"),
        ),
        EventMinutesItem(
            minutes_item=MinutesItem(name="CB 119858"),
            matter=Matter(
                name="CB 119858",
                matter_type="Council Bill",
                title=(
                    "AN ORDINANCE relating to the financing of the West Seattle Bridge"
                ),
                result_status="Adopted",
                sponsors=[
                    Person(
                        name="M. Lorena González",
                        seat=Seat(
                            name="Position 9",
                            roles=[
                                Role(title="Council President"),
                                Role(
                                    title="Chair",
                                    body=Body(name="Governance and Education"),
                                ),
                            ],
                        ),
                    ),
                    Person(
                        name="Teresa Mosqueda",
                        seat=Seat(
                            name="Position 8",
                            roles=[
                                Role(
                                    title="Chair",
                                    body=Body(name="Finance and Housing"),
                                ),
                                Role(
                                    title="Vice Chair",
                                    body=Body(name="Governance and Education"),
                                ),
                            ],
                        ),
                        picture_uri="https://www.seattle.gov/Images/Council/Members/Mosqueda/Mosqueda_225x225.jpg",  # noqa: E501
                    ),
                ],
            ),
            supporting_files=[
                SupportingFile(
                    name="Amendment 3",
                    uri=(
                        "http://legistar2.granicus.com/seattle/attachments/"
                        "789a0c9f-dd9c-401b-aaf5-6c67c2a897b0.pdf"
                    ),
                ),
            ],
            decision="Passed",
            votes=[
                Vote(
                    person=Person(
                        name="M. Lorena González",
                        seat=Seat(
                            name="Position 9",
                            roles=[
                                Role(title="Council President"),
                                Role(
                                    title="Chair",
                                    body=Body(name="Governance and Education"),
                                ),
                            ],
                        ),
                    ),
                    decision="Approve",
                ),
                Vote(
                    person=Person(
                        name="Teresa Mosqueda",
                        seat=Seat(
                            name="Position 8",
                            roles=[
                                Role(
                                    title="Chair",
                                    body=Body(name="Finance and Housing"),
                                ),
                                Role(
                                    title="Vice Chair",
                                    body=Body(name="Governance and Education"),
                                ),
                            ],
                        ),
                    ),
                    decision="Approve",
                ),
                Vote(
                    person=Person(
                        name="Andrew Lewis",
                        seat=Seat(
                            name="District 7",
                            image_uri="http://www.seattle.gov/Images/Clerk/district7_50x50.jpg",  # noqa: E501
                            roles=[
                                Role(
                                    title="Vice Chair",
                                    body=Body(name="Community Economic Development"),
                                ),
                            ],
                        ),
                    ),
                    decision="Approve",
                ),
                Vote(
                    person=Person(
                        name="Alex Pedersen",
                        seat=Seat(
                            name="District 4",
                            roles=[
                                Role(
                                    title="Chair",
                                    body=Body("Transportation and Utilities"),
                                ),
                            ],
                        ),
                    ),
                    decision="Reject",
                ),
            ],
        ),
    ],
)

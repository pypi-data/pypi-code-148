import logging
from typing import Dict
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from scrobbles.mixins import ScrobblableMixin

logger = logging.getLogger(__name__)
BNULL = {"blank": True, "null": True}


class VideoGameCollection(TimeStampedModel):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid4, editable=False, **BNULL)
    cover = models.ImageField(upload_to="games/series-covers/", **BNULL)
    igdb_id = models.IntegerField(**BNULL)

    def __str__(self):
        return self.name


class VideoGame(ScrobblableMixin):
    COMPLETION_PERCENT = getattr(settings, 'GAME_COMPLETION_PERCENT', 100)

    collection = models.ForeignKey(VideoGameCollection, **BNULL)
    igdb_id = models.IntegerField(**BNULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("videogames:game_detail", kwargs={'slug': self.uuid})

    @classmethod
    def find_or_create(cls, data_dict: Dict) -> "Event":
        """Given a data dict from Jellyfin, does the heavy lifting of looking up
        the video and, if need, TV Series, creating both if they don't yet
        exist.

        """
        league_dict = {
            "abbreviation_str": data_dict.get("LeagueName", ""),
            "thesportsdb_id": data_dict.get("LeagueId", ""),
        }
        league, _created = League.objects.get_or_create(**league_dict)

        home_team_dict = {
            "name": data_dict.get("HomeTeamName", ""),
            "thesportsdb_id": data_dict.get("HomeTeamId", ""),
            "league": league,
        }
        home_team, _created = Team.objects.get_or_create(**home_team_dict)

        away_team_dict = {
            "name": data_dict.get("AwayTeamName", ""),
            "thesportsdb_id": data_dict.get("AwayTeamId", ""),
            "league": league,
        }
        away_team, _created = Team.objects.get_or_create(**away_team_dict)

        event_dict = {
            "title": data_dict.get("Name"),
            "event_type": data_dict.get("ItemType"),
            "home_team": home_team,
            "away_team": away_team,
            "start": data_dict['Start'],
            "league": league,
            "run_time_ticks": data_dict.get("RunTimeTicks"),
            "run_time": data_dict.get("RunTime", ""),
        }
        event, _created = cls.objects.get_or_create(**event_dict)

        return event


#!/usr/bin/env python3

import json
import requests
import datetime
import logging; logger = logging.getLogger(__name__)
from dateutil.parser import parse
from importlib import import_module
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google.auth.exceptions import RefreshError
    from googleapiclient._auth import is_valid, refresh_credentials
    from googleapiclient.discovery import build
    from social_django.models import UserSocialAuth
except ImportError:
    class UserSocialAuth:
        pass

from django.conf import settings
from django.utils import timezone
from lino.core.site import has_socialauth

from lino.api import dd
user_mod = import_module([app for app in settings.INSTALLED_APPS if app.endswith('users')][0] + ".models")
User = user_mod.User


def get_credentials(user: UserSocialAuth) -> Credentials:

    with open(dd.plugins.google.client_secret_file) as f:
        client_secret = json.load(f)

    if type(user.extra_data['scopes']) == str:
        user.extra_data['scopes'] = user.extra_data['scopes'].split()

    def get_expiry(creds):
        from_auth_time_and_delta = datetime.datetime.fromtimestamp(
            creds['auth_time']) + datetime.timedelta(seconds=creds['expires_in'])
        if creds['expiry']:
            return max(datetime.datetime.fromtimestamp(creds['expiry']),
                        from_auth_time_and_delta)
        return from_auth_time_and_delta

    creds = Credentials(
        token_uri=client_secret['web']['token_uri'],
        client_id=client_secret['web']['client_id'],
        client_secret=client_secret['web']['client_secret'],
        token=user.extra_data['access_token'],
        refresh_token=user.extra_data['refresh_token'],
        rapt_token=user.extra_data['rapt_token'],
        id_token=user.extra_data['id_token'],
        expiry=get_expiry(user.extra_data),
        scopes=user.extra_data['scopes']
    )

    if not is_valid(creds):
        try:
            refresh_credentials(creds)
            user.extra_data['access_token'] = creds.token
            user.extra_data['expiry'] = datetime.datetime.timestamp(creds.expiry)
            user.extra_data['refresh_token'] = creds.refresh_token
            user.extra_data['rapt_token'] = creds.rapt_token
            user.full_clean()
            user.save()
        except RefreshError as e:
            requests.post('https://oauth2.googleapis.com/revoke',
                params={'token': creds.token},
                headers={'content-type': 'application/x-www-form-urlencoded'})
            logger(f"{user.user}'s Token has been revoked, because of this:\n{e}\nNeeds re-authentication.")
            user.delete()

    return creds

def get_resource(user: User):
    social_user = user.social_auth.get(provider='google')
    creds = get_credentials(social_user)
    return build('calendar', 'v3', credentials=creds)

def map_calendar_into_dbModel(cls, cal):
    calendar, _ = cls.objects.get_or_create(google_id=cal.get('id'))
    calendar.name=cal.get('summary')
    calendar.description=cal.get('description')
    calendar.time_zone=cal.get('timeZone')
    return calendar

def map_event_into_dbModel(cls, event, user_s_cal):
    e, _ = cls.objects.get_or_create(
        google_id=event['id'], google_calendar=user_s_cal.calendar)
    e.status = event.get('status') # possible values are 'confirmed', 'tentative', 'cancelled'
    e.summary = event.get('summary') # The title of the event
    e.description = event.get('description')
    e.sequence = event.get('sequence')

    def resolve_datetime(stamp):
        return timezone.make_naive(parse(stamp))

    def resolve_date_time(stamp):
        dt = resolve_datetime(stamp)
        return dt.date(), dt.time()

    if start := event.get('start'):
        if dateTime := start.get('dateTime'):
            e.start_date, e.start_time = resolve_date_time(dateTime)
        else:
            e.start_date = datetime.date(
                *map(int, start['date'].split('-')))
    elif originalStart := event.get('originalStartTime'):
        if dateTime := originalStart.get('dateTime'):
            e.start_date, e.start_time = resolve_date_time(dateTime)
        else:
            e.start_date = datetime.date(
                *map(int, originalStart['date'].split('-')))

    if end := event.get('end'):
        if dateTime := end.get('dateTime'):
            e.end_date, e.end_time = resolve_date_time(dateTime)
        else:
            e.end_date = datetime.date(
                *map(int, end['date'].split('-')))

    e.location = event.get('location')

    if created := event.get('created'):
        e.created = resolve_datetime(created)

    if updated := event.get('updated'):
        e.modified = resolve_datetime(updated)

    return e

def map_recurrent_event(cls, event, user_s_cal):
    pass

"""Allauth Social Account adapter"""

import logging

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.db import IntegrityError

from astronauth.models import UserProfile

logger = logging.getLogger(__name__)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """Populates a user and creates a UserProfile with
        location information"""
        user = super().populate_user(request, sociallogin, data)

        user, _ = User.objects.get_or_create(username=user.username)
        try:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"location": sociallogin.account.extra_data.get("l")},
            )
        except IntegrityError:
            logger.warning("Could not create UserProfile for %s", user.username)

        return user

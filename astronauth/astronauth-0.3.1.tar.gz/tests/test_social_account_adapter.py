from allauth.socialaccount.models import SocialAccount, SocialLogin
from django.contrib.auth.models import User
from django.test import TestCase

from astronauth.models import UserProfile
from astronauth.socialaccount.adapter import SocialAccountAdapter


class SocialAdapterTests(TestCase):
    def test_user_info_stored(self):
        adapter = SocialAccountAdapter()

        request = {}
        sociallogin = SocialLogin(
            user=User(username="test@example.com", password="secret"),
            account=SocialAccount(
                extra_data={
                    "email_verified": False,
                    "name": "Piebe Gealle",
                    "preferred_username": "test@example.com",
                    "given_name": "Piebe",
                    "family_name": "Gealle",
                    "email": "test.example.com",
                    "id": "a663b6b4-4cf3-4438-910c-8390d798fc21",
                    "l": "The Netherlands",
                }
            ),
        )
        data = {
            "email": "test@example.com",
            "username": "test@example.com",
            "name": "Piebe Gealle",
            "user_id": None,
            "picture": None,
        }

        # TODO: verify input
        u = adapter.populate_user(request, sociallogin, data)

        # TODO: save?
        u.save()

        user = User.objects.get(username="test@example.com")
        self.assertTrue(user, "user not created")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.location, "The Netherlands")

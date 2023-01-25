""" ASTRONauth Django Admin configuration """
from django.contrib import admin

from astronauth.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile ModelAdmin class"""

    list_display = (
        "user",
        "location",
    )


admin.site.register(UserProfile, UserProfileAdmin)

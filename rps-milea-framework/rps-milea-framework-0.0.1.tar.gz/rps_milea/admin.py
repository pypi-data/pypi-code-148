from django.contrib import admin
from rps_milea import settings as milea
from django.utils.translation import gettext_lazy as _
from email_users.models import User
from email_users.admin import UserAdmin

# Default Naming
admin.site.site_header = admin.site.site_title = '%s Verwaltung' % getattr(milea, 'FW_NAME', "Django")
admin.site.index_title = 'Dashboard'

admin.site.unregister(User)
@admin.register(User)
class NewUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('id',)

    fieldsets = (
        (_("Personal info"), {'fields': (('email', 'password'), ('first_name', 'last_name'),)}),
        (_("Permissions"), {"fields": ('is_active', 'is_staff', 'is_superuser', ('groups', 'user_permissions'))}),
        (_("Important dates"), {'fields': (('last_login', 'date_joined'),)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )

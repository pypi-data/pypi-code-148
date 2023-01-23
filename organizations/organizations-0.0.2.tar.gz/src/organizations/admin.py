from django.contrib import admin
from .models import (
    Intermediary,
    Organization,
    OrganizationDID,
    OrganizationKeys,
    Issuer,
    UserProxy,
)
from .enums import OrganizationsSwitches
import waffle


class IntermediaryAdmin(admin.ModelAdmin):
    model = Intermediary

    def get_model_perms(self, request):

        if (
            not waffle.switch_is_active(OrganizationsSwitches.Organizations.value)
            or waffle.switch_is_active(OrganizationsSwitches.Organizations.value)
            and not waffle.switch_is_active(
                OrganizationsSwitches.OrganizationsIntermediary.value
            )
        ):
            return {}

        return super(IntermediaryAdmin, self).get_model_perms(request)


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization

    def get_model_perms(self, request):

        if not waffle.switch_is_active(OrganizationsSwitches.Organizations.value):
            return {}

        return super(OrganizationAdmin, self).get_model_perms(request)


class OrganizationDIDAdmin(admin.ModelAdmin):
    model = OrganizationDID

    def get_model_perms(self, request):

        if not waffle.switch_is_active(OrganizationsSwitches.Organizations.value):
            return {}

        return super(OrganizationDIDAdmin, self).get_model_perms(request)


class OrganizationKeysAdmin(admin.ModelAdmin):
    model = OrganizationKeys

    def get_model_perms(self, request):

        if not waffle.switch_is_active(OrganizationsSwitches.Organizations.value):
            return {}

        return super(OrganizationKeysAdmin, self).get_model_perms(request)


class IssuerAdmin(admin.ModelAdmin):
    model = Issuer

    def get_model_perms(self, request):

        if (
            not waffle.switch_is_active(OrganizationsSwitches.Organizations.value)
            or waffle.switch_is_active(OrganizationsSwitches.Organizations.value)
            and not waffle.switch_is_active(
                OrganizationsSwitches.OrganizationsIssuer.value
            )
        ):
            return {}

        return super(IssuerAdmin, self).get_model_perms(request)


class UserProxyAdmin(admin.ModelAdmin):
    model = UserProxy
    fields = ("username", "first_name", "last_name", "email")

    def get_model_perms(self, request):

        if not waffle.switch_is_active(OrganizationsSwitches.Organizations.value):
            return {}

        return super(UserProxyAdmin, self).get_model_perms(request)


admin.site.register(Intermediary, IntermediaryAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationDID, OrganizationDIDAdmin)
admin.site.register(OrganizationKeys, OrganizationKeysAdmin)
admin.site.register(Issuer, IssuerAdmin)
admin.site.register(UserProxy, UserProxyAdmin)

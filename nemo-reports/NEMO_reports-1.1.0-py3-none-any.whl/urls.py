from django.urls import include, path

from NEMO_reports.views import reporting, reporting_active_users

urlpatterns = [
    path("reporting/", include([
        path("", reporting.reports, name="reporting"),
        path("reporting/active_users", reporting_active_users.active_users, name="reporting_active_users"),
    ])),
]

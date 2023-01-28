from django.urls import include, path

from NEMO_reports.views import reporting, reporting_active_users

urlpatterns = [
    path("reporting/", include([
        path("", reporting.reports, name="reporting"),
        path("active_users", reporting_active_users.active_users, name="reporting_active_users"),
    ])),
]

if reporting.billing_installed():
    from NEMO_reports.views import reporting_invoice_charges
    urlpatterns += [
        path("reporting/invoice_charges", reporting_invoice_charges.invoice_charges, name="reporting_invoice_charges")
    ]

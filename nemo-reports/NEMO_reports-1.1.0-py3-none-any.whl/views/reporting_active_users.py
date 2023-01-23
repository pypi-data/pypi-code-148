from NEMO.models import Discipline, User
from django.db.models import QuerySet
from django.shortcuts import render

from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    DataDisplayTable,
    SummaryDisplayTable,
    area_access,
    billing_installed,
    consumable_withdraws,
    custom_charges,
    get_date_range,
    report_export,
    reporting_dictionary,
    staff_charges,
    training_sessions,
    usage_events,
)


@accounting_or_manager_required
def active_users(request):
    start, end = get_date_range(request)
    user_ids = set("")
    if request.GET.get("tool_usage") == "on":
        user_ids.update(set(usage_events(start, end, only=["user_id"], values_list="user_id")))
    if request.GET.get("area_access") == "on":
        user_ids.update(set(area_access(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("staff_charges") == "on":
        user_ids.update(set(staff_charges(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("consumables") == "on":
        user_ids.update(set(consumable_withdraws(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("training") == "on":
        user_ids.update(set(training_sessions(start, end, only=["trainee_id"], values_list="trainee_id")))
    if billing_installed() and request.GET.get("custom_charges") == "on":
        user_ids.update(set(custom_charges(start, end, only=["customer_id"], values_list="customer_id")))
    active_user_qs: QuerySet = User.objects.filter(id__in=user_ids)
    data = DataDisplayTable()
    data.headers = [
        ("first", "First name"),
        ("last", "Last name"),
        ("username", "Username"),
        ("email", "Email"),
        ("active", "Active"),
        ("access_expiration", "Access expiration"),
    ]
    if Discipline.objects.exists():
        data.add_header(("discipline", "Discipline"))
    for user in active_user_qs:
        user: User = user
        data.add_row(
            {
                "first": user.first_name,
                "last": user.last_name,
                "username": user.username,
                "email": user.email,
                "active": user.is_active,
                "access_expiration": user.access_expiration,
                "discipline": ", ".join([project.discipline.name for project in user.projects.all() if project.discipline]),
            }
        )
    summary = SummaryDisplayTable()
    if active_user_qs:
        summary.add_header(("item", "Item"))
        summary.add_header(("value", "Value"))
        summary.add_row({"item": "Active users", "value": active_user_qs.count()})
        if Discipline.objects.exists():
            summary.add_row({"item": "By discipline"})
            for discipline in Discipline.objects.all():
                summary.add_row(
                    {"item": f"{discipline.name}", "value": active_user_qs.filter(projects__discipline=discipline).count()}
                )
    if request.GET.get("export"):
        return report_export([summary, data], "active_users", start, end)
    dictionary = {
        "start": start,
        "end": end,
        "tool_usage": request.GET.get("tool_usage"),
        "area_access": request.GET.get("area_access"),
        "training": request.GET.get("training"),
        "consumables": request.GET.get("consumables"),
        "staff_charges": request.GET.get("staff_charges"),
        "custom_charges": request.GET.get("custom_charges"),
        "data": data,
        "summary": summary,
    }
    return render(request, "NEMO_reports/report_active_users.html", reporting_dictionary("active_users", dictionary))

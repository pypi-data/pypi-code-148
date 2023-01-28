import datetime

from NEMO.models import Discipline, User
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.decorators.http import require_GET

from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    DataDisplayTable,
    SummaryDisplayTable,
    area_access,
    billing_installed,
    consumable_withdraws,
    custom_charges,
    get_date_range_and_split,
    get_month_range,
    get_monthly_rule,
    get_rate_category,
    missed_reservations,
    order_and_unique,
    report_export,
    reporting_dictionary,
    staff_charges,
    training_sessions,
    usage_events,
)


@accounting_or_manager_required
@require_GET
def active_users(request):
    start, end, split_by_month = get_date_range_and_split(request)
    RateCategory = get_rate_category()

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
        data.add_header(("discipline", "Discipline(s)"))
    if RateCategory:
        if RateCategory.objects.exists():
            data.add_header(("rate_category", "Rate category(-ies)"))

    total_data_qs = get_active_user_query_set(request, start, end)
    for user in total_data_qs:
        data_row = {
            "first": user.first_name,
            "last": user.last_name,
            "username": user.username,
            "email": user.email,
            "active": user.is_active,
            "access_expiration": user.access_expiration,
            "discipline": ", ".join(
                order_and_unique([project.discipline.name for project in user.projects.all() if project.discipline])
            ),
        }
        if RateCategory:
            data_row["rate_category"] = ", ".join(
                order_and_unique(
                    [
                        project.projectbillingdetails.category.name
                        for project in user.projects.all()
                        if getattr(project, "projectbillingdetails") and project.projectbillingdetails.category
                    ]
                )
            )
        data.add_row(data_row)

    summary = SummaryDisplayTable()
    summary.add_header(("item", "Item"))
    summary.add_row({"item": "Active users"})
    if Discipline.objects.exists():
        summary.add_row({"item": "By discipline"})
        for discipline in Discipline.objects.all():
            summary.add_row({"item": f"{discipline.name}"})
    if RateCategory:
        if RateCategory.objects.exists():
            summary.add_row({"item": "By rate category"})
            for category in RateCategory.objects.all():
                summary.add_row({"item": f"{category.name}"})

    if split_by_month:
        for month in get_monthly_rule(start, end):
            month_key = f"month_{month.strftime('%Y')}_{month.strftime('%m')}"
            summary.add_header((month_key, month.strftime("%b %Y")))
            month_start, month_end = get_month_range(month)
            add_summary_info(request, summary, month_start, month_end, month_key)
    else:
        summary.add_header(("value", "Value"))
        add_summary_info(request, summary, start, end)

    if request.GET.get("export"):
        return report_export([summary, data], "active_users", start, end)
    dictionary = {
        "start": start,
        "end": end,
        "split_by_month": request.GET.get("split_by_month"),
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


def add_summary_info(request, summary: SummaryDisplayTable, start, end, summary_key=None):
    RateCategory = get_rate_category()
    summary_key = summary_key or "value"
    monthly_active_user_qs = get_active_user_query_set(request, start, end)
    summary.rows[0][summary_key] = monthly_active_user_qs.count()
    current_row = 1
    for discipline in Discipline.objects.all():
        current_row += 1
        summary.rows[current_row][summary_key] = (
            monthly_active_user_qs.filter(projects__discipline=discipline).distinct().count()
        )
    if RateCategory:
        current_row += 1  # For mid table header
        for category in RateCategory.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = (
                monthly_active_user_qs.filter(projects__projectbillingdetails__category=category).distinct().count()
            )


def get_active_user_query_set(request, start: datetime.datetime, end: datetime.datetime) -> QuerySet[User]:
    user_ids = set("")
    if request.GET.get("tool_usage", "on") == "on":
        user_ids.update(set(usage_events(start, end, only=["user_id"], values_list="user_id")))
    if request.GET.get("area_access", "on") == "on":
        user_ids.update(set(area_access(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("staff_charges", "on") == "on":
        user_ids.update(set(staff_charges(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("consumables", "on") == "on":
        user_ids.update(set(consumable_withdraws(start, end, only=["customer_id"], values_list="customer_id")))
    if request.GET.get("training", "on") == "on":
        user_ids.update(set(training_sessions(start, end, only=["trainee_id"], values_list="trainee_id")))
    if request.GET.get("missed_reservations", "on") == "on":
        user_ids.update(set(missed_reservations(start, end, only=["user_id"], values_list="user_id")))
    if billing_installed() and request.GET.get("custom_charges", "on") == "on":
        user_ids.update(set(custom_charges(start, end, only=["customer_id"], values_list="customer_id")))
    return User.objects.filter(id__in=user_ids)

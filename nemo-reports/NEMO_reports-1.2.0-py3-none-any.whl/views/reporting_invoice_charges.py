import datetime
from _decimal import Decimal

from NEMO.models import Discipline
from NEMO_billing.invoices.models import Invoice
from NEMO_billing.rates.models import RateCategory
from django.db.models import QuerySet, Sum
from django.shortcuts import render
from django.views.decorators.http import require_GET

from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    DataDisplayTable,
    SummaryDisplayTable,
    get_date_range_and_split,
    get_month_range,
    get_monthly_rule,
    report_export,
    reporting_dictionary,
)


@accounting_or_manager_required
@require_GET
def invoice_charges(request):
    start, end, split_by_month = get_date_range_and_split(request)
    # Split since invoices are by month, any day in that month counts as the full month
    start, start_month_end = get_month_range(start)
    end_month_start, end = get_month_range(end)

    data = DataDisplayTable()
    data.headers = [
        ("invoice_number", "Invoice #"),
        ("invoice_project", "Project"),
        ("invoice_date", "Date"),
        ("invoice_total", "Amount"),
    ]

    if Discipline.objects.exists():
        data.add_header(("discipline", "Discipline"))
    if RateCategory.objects.exists():
        data.add_header(("rate_category", "Rate category"))

    total_data_qs = get_invoice_query_set(request, start, end)
    for invoice in total_data_qs:
        invoice: Invoice = invoice
        discipline = invoice.project_details.project.discipline
        data_row = {
            "invoice_number": invoice.invoice_number,
            "invoice_project": invoice.project_details.name,
            "invoice_date": invoice.start.strftime("%B %Y"),
            "invoice_total": invoice.total_amount,
            "discipline": discipline.name if discipline else "",
            "rate_category": invoice.project_details.category.name if invoice.project_details.category else "",
        }
        data.add_row(data_row)

    summary = SummaryDisplayTable()
    summary.add_header(("item", "Item"))
    summary.add_row({"item": "Total amount"})
    if Discipline.objects.exists():
        summary.add_row({"item": "By discipline"})
        for discipline in Discipline.objects.all():
            summary.add_row({"item": f"{discipline.name}"})
    if RateCategory.objects.exists():
        summary.add_row({"item": "By rate category"})
        for category in RateCategory.objects.all():
            summary.add_row({"item": f"{category.name}"})

    if split_by_month:
        # Create new start/end of month dates
        for month in get_monthly_rule(start, end):
            month_key = f"month_{month.strftime('%Y')}_{month.strftime('%m')}"
            summary.add_header((month_key, month.strftime("%b %Y")))
            month_start, month_end = get_month_range(month)
            add_summary_info(request, summary, month_start, month_end, month_key)
    else:
        summary.add_header(("value", "Value"))
        add_summary_info(request, summary, start, end)

    if request.GET.get("export"):
        return report_export([summary, data], "invoice_charges", start, end)
    dictionary = {
        "start": start.date(),
        "end": end.date(),
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
    return render(request, "NEMO_reports/report_base.html", reporting_dictionary("invoice_charges", dictionary))


def add_summary_info(request, summary: SummaryDisplayTable, start, end, summary_key=None):
    summary_key = summary_key or "value"
    monthly_invoices = get_invoice_query_set(request, start, end)
    summary.rows[0][summary_key] = monthly_invoices.aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
    current_row = 1
    for discipline in Discipline.objects.all():
        current_row += 1
        summary.rows[current_row][summary_key] = monthly_invoices.filter(
            project_details__project__discipline=discipline
        ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
    if RateCategory:
        current_row += 1  # For mid table header
        for category in RateCategory.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = monthly_invoices.filter(
                project_details__category=category
            ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)


def get_invoice_query_set(request, start: datetime.datetime, end: datetime.datetime) -> QuerySet[Invoice]:
    return Invoice.objects.filter(voided_date__isnull=True, start__gte=start, start__lte=end)

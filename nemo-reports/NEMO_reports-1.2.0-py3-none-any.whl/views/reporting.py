import csv
import datetime
from _decimal import Decimal
from datetime import timedelta
from typing import List, Optional, Type, Union

from NEMO.models import (
    AreaAccessRecord,
    BaseModel,
    ConsumableWithdraw,
    Reservation,
    StaffCharge,
    TrainingSession,
    UsageEvent,
)
from NEMO.utilities import (
    BasicDisplayTable,
    beginning_of_the_day,
    capitalize,
    end_of_the_day,
    export_format_datetime,
    extract_optional_beginning_and_end_dates,
)
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

from NEMO_reports.customizations import ReportsCustomization
from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.templatetags.reports_tags import app_installed


class BasicDisplayTableFormatted(BasicDisplayTable):
    def formatted_value(self, value, html: bool = False):
        if value is None:
            return ""
        if isinstance(value, Decimal):
            amount = display_amount(value)
            return f'<div class="text-right">{amount}</div>' if html else amount
        elif isinstance(value, bool) and html:
            if value:
                return '<span class="glyphicon glyphicon-ok success-highlight"></span>'
            else:
                return '<span class="glyphicon glyphicon-remove danger-highlight"></span>'
        return super().formatted_value(value)


class SummaryDisplayTable(BasicDisplayTableFormatted):
    def to_html(self):
        result = '<table id="summary-table" class="table table-bordered">'
        result += "<thead>"
        result += f'<tr class="success"><th colspan="{len(self.headers)}" class="text-center">Summary</th></tr>'
        result += '<tr class="info">'
        for header_key, header_display in self.headers:
            result += f'<th class="text-center">{header_display if header_key != "item" else ""}</th>'
        result += "</tr>"
        result += "</thead>"
        result += "<tbody>"
        for row in self.rows:
            if len(row) == 1 and "item" in row:
                result += f'<tr class="info"><td colspan="{len(self.headers)}" style="font-weight: bold">{row["item"]}</td></tr>'
            else:
                result += "<tr>"
                for key in row.keys():
                    result += f'<td>{self.formatted_value(row.get(key, ""), html=True)}</td>'
                result += "</tr>"
        result += "</tbody>"
        result += "</table>"
        return mark_safe(result)


class DataDisplayTable(BasicDisplayTableFormatted):
    def to_html(self):
        result = '<table id="data-table" class="table table-bordered table-hover table-striped">'
        result += "<thead>"
        result += f'<tr class="success"><th colspan="{len(self.headers)}" class="text-center">Aggregate data</th></tr>'
        result += '<tr class="info">'
        for key, value in self.headers:
            result += f"<th>{value}</th>"
        result += "</tr></thead>"
        result += "<tbody>"
        for row in self.rows:
            result += "<tr>"
            for key, value in self.headers:
                result += f'<td>{self.formatted_value(row.get(key, ""), html=True) or ""}</td>'
            result += "</tr>"
        result += "</tbody>"
        result += "</table>"
        return mark_safe(result)


# Create your views here.
@accounting_or_manager_required
@require_GET
def reports(request):
    return render(request, "NEMO_reports/reports.html", {"report_dict": get_report_dict()})


def report_export(tables: List[BasicDisplayTable], key: str, start: datetime.date, end: datetime.date):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    for table in tables:
        if table.headers:
            writer.writerow([capitalize(display_value) for key, display_value in table.headers])
            for row in table.rows:
                writer.writerow([table.formatted_value(row.get(key, "")) for key, display_value in table.headers])
            writer.writerow([])
    filename = f"{key}_data_{export_format_datetime(start, t_format=False)}_to_{export_format_datetime(end, t_format=False)}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def get_date_range_and_split(request) -> (datetime.date, datetime.date, bool):
    start, end = extract_optional_beginning_and_end_dates(request.GET, date_only=True)
    today = datetime.datetime.now().astimezone()  # Today's datetime in our timezone
    reports_default_daterange = ReportsCustomization.get("reports_default_daterange")
    if not start or not end:
        if reports_default_daterange == "this_year":
            start = today.replace(month=1, day=1)
            end = today.replace(month=12, day=31)
        elif reports_default_daterange == "this_month":
            start = today.replace(day=1)
            end = today + relativedelta(day=31)
        elif reports_default_daterange == "this_week":
            first_day_of_the_week = ReportsCustomization.get_int("reports_first_day_of_week")
            weekday = today.weekday() if first_day_of_the_week else today.isoweekday()
            start = today - timedelta(days=weekday)
            end = start + timedelta(days=6)
        elif reports_default_daterange == "yesterday":
            start = today - timedelta(days=1)
            end = today - timedelta(days=1)
        else:
            start = today
            end = today
    return start.date(), end.date(), request.GET.get("split_by_month") == "on"


def get_month_range(day_in_month: datetime.datetime) -> (datetime.datetime, datetime.datetime):
    if isinstance(day_in_month, datetime.date):
        day_in_month = datetime.datetime(year=day_in_month.year, month=day_in_month.month, day=day_in_month.day)
    first_day, last_day = day_in_month.replace(day=1), day_in_month + relativedelta(day=31)
    return beginning_of_the_day(first_day), end_of_the_day(last_day)


def get_monthly_rule(start, end):
    # Split to make sure we are getting the correct full months
    start_month_start, start_month_end = get_month_range(start)
    end_month_start, end_month_end = get_month_range(end)
    return rrule(MONTHLY, dtstart=start_month_start.date(), until=end_month_end.date())


def order_and_unique(list_with_duplicates: List) -> List:
    unique_value_list = list(set(list_with_duplicates))
    unique_value_list.sort()
    return unique_value_list


def billing_installed():
    return app_installed("NEMO_billing")


def get_rate_category() -> Type[BaseModel]:
    if billing_installed():
        from NEMO_billing.rates.models import RateCategory

        return RateCategory


def reporting_dictionary(key, dictionary):
    # Adds report information (url, title, description...) to the given dictionary
    return {**get_report_dict().get(key), **dictionary}


def usage_events(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = UsageEvent.objects.only(*((only or []) + ["end"])).filter(end__date__gte=start, end__date__lte=end)
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def area_access(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = AreaAccessRecord.objects.only(*((only or []) + ["end"])).filter(end__date__gte=start, end__date__lte=end)
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def staff_charges(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = StaffCharge.objects.only(*((only or []) + ["end"])).filter(end__date__gte=start, end__date__lte=end)
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def consumable_withdraws(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = ConsumableWithdraw.objects.only(*((only or []) + ["date"])).filter(
        date__date__gte=start, date__date__lte=end
    )
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def training_sessions(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = TrainingSession.objects.only(*((only or []) + ["date"])).filter(
        date__date__gte=start, date__date__lte=end
    )
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def missed_reservations(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    queryset = Reservation.objects.only(*((only or []) + ["end"])).filter(
        missed=True, end__date__gte=start, end__date__lte=end
    )
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def custom_charges(start, end, only: List = None, values_list: str = None) -> Union[QuerySet, List]:
    from NEMO_billing.models import CustomCharge

    queryset = CustomCharge.objects.only(*((only or []) + ["date"])).filter(date__date__gte=start, date__date__lte=end)
    return queryset if not values_list else queryset.values_list(values_list, flat=True)


def display_amount(amount: Optional[Decimal]) -> str:
    # We need to specifically check for None since amount = 0 will evaluate to False
    if amount is None:
        return ""
    rounded_amount = round(amount, 2)
    if amount < 0:
        return f"({number_format(abs(rounded_amount), decimal_pos=2)})"
    else:
        return f"{number_format(rounded_amount, decimal_pos=2)}"


def get_report_dict():
    dictionary = report_dict
    if billing_installed():
        dictionary.update(billing_reports_dict)
    return dictionary


report_dict = {
    "active_users": {
        "report_url": "reporting_active_users",
        "report_title": "Active users report",
        "report_description": "Lists active users, meaning any user with recorded activity <b>ending</b> during the date range (Tool usage, Area access, Consumable withdraw, Training, Staff charge, Missed reservation)",
        "allow_split_by_month": True,
    }
}

billing_reports_dict = {
    "invoice_charges": {
        "report_url": "reporting_invoice_charges",
        "report_title": "Invoice charges report",
        "report_description": "Displays total invoiced charges during the date range (tax and discounts included)",
        "allow_split_by_month": True,
    }
}

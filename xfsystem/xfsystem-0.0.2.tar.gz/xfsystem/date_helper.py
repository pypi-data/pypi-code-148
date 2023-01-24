from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from pyspark.sql.types import DateType
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf


def transform_string_column_to_date(dataframe : DataFrame, column_name: str, current_date_format:str = "%Y-%m-%d") -> DataFrame:
    date_convertor =  udf (lambda x: datetime.strptime(x, current_date_format), DateType())
    dataframe = dataframe.withColumn('tmp_column_name', date_convertor(col(column_name)))
    dataframe = dataframe.drop(col(column_name))
    dataframe = dataframe.withColumnRenamed('tmp_column_name', column_name)
    return dataframe


def get_month_offset(self, calender_type: str = 'c') -> int:
    month_offset = 0
    if calender_type == 'c':
        month_offset = 0
    elif calender_type == 'g':
        month_offset = 6
    elif calender_type == 'p':
        month_offset == 3
    else:
        month_offset = 0
    return month_offset


def get_quarter_period(day_date: datetime, calender_type: str = 'c') -> str:
    month_offset = get_month_offset(calender_type)
    new_date = day_date + relativedelta(months=month_offset)
    year_number = new_date.year
    month_number = new_date.month
    quarter_number = int((month_number - 1) / 3) + 1
    year_name = str(year_number)[-2:]
    quarter_name = 'Q' + str(quarter_number) + 'FY' + year_name
    return quarter_name


def get_semi_annual_period(day_date: datetime, calender_type: str = 'c') -> str:
    month_offset = get_month_offset(calender_type)
    new_date = day_date + relativedelta(months=month_offset)
    year_number = new_date.year
    month_number = new_date.month
    quarter_number = int((month_number - 1) / 6) + 1
    year_name = str(year_number)[-2:]
    semi_annual_name = 'S' + str(quarter_number) + 'FY' + year_name
    return semi_annual_name


def get_annual_period(day_date: datetime, calender_type: str = 'c') -> str:
    month_offset = get_month_offset(calender_type)
    new_date = day_date + relativedelta(months=month_offset)
    year_number = new_date.year
    year_name = str(year_number)[-2:]
    annual_period = 'FY' + year_name
    return annual_period


def get_calendar_year(day_date: datetime, calender_type: str = 'c') -> str:
    year_number = str(day_date.year)
    return year_number


def get_month_from_date(day_date: datetime) -> str:
    year_number = day_date.year
    year_name = str(year_number)[-2:]
    month_name = calendar.month_abbr[day_date.month]
    month_period = month_name.upper() + year_name
    return month_period


def get_dates(start_date: datetime, end_date: datetime = datetime.now()) -> list:
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = []

    date_diff = end_date - start_date
    for i in range(date_diff.days + 1):
        day = start_date + timedelta(days=i)

        day_dct = {
            "date_id": i + 1,
            "date": day.strftime('%Y-%m-%d'),
            "day_name": week[day.weekday()],
            "calendar_year": get_calendar_year(day),
            "semi_annual_period": get_semi_annual_period(day),
            "quarter_period": get_quarter_period(day),
            "month_period": get_month_from_date(day)
        }
        days.append(day_dct)
    return days
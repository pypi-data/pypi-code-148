from datetime import datetime

def get_default_year():
    now = datetime.today()
    return now.year if now.month == 12 else now.year-1

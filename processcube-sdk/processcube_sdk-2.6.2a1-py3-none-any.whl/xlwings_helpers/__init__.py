import pandas as pd

def sheet_by_name(book, sheet_name, create=True):
    if sheet_name in [sheet.name for sheet in book.sheets]:
        sheet = book.sheets[sheet_name]
    else:
        if create:
            sheet = book.sheets.add(sheet_name)
        else:
            sheet = None

    return sheet

def get_config(book):
    sheet = sheet_by_name(book, 'Report_Config', create=False)
    
    if sheet is None:
        sheet = sheet_by_name(book, 'Config', create=False)

    if sheet is None:
        raise Exception('Config-Sheet not found')

    config = {}

    data = sheet.range("A1").expand().value

    if type(data) is not list:
        data = [data]

    for entry in data:
        key, value = entry[0], entry[1]

        config[str(key).lower()] = str(value)

    return config

def fill_sheet(book, sheet_name: str, df: pd.DataFrame):
    report_sheet = sheet_by_name(book, sheet_name)

    report_cell = report_sheet["A1"]
    report_cell.expand().clear_contents()
    report_cell.options(index=False).value = df
    report_cell.offset(row_offset=1).columns.autofit()

def fill_sheet_and_result_json(book, sheet_name: str, df: pd.DataFrame):
    fill_sheet(book, sheet_name, df)
    
    book_json = book.json()
    
    return book_json

def fill_report_sheet_and_result_json(book, df: pd.DataFrame):
    book_config = get_config(book)
    
    return fill_sheet_and_result_json(book, book_config['sheet'], df)
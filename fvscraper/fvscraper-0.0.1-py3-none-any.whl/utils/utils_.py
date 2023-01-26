from typing import List


def construct_table_from_data(headers: List[str], table: List[str]) -> list:
    data = []

    if len(table) < 1 or len(headers) < 1:
        return []
    
    number_of_rows = len(table)//len(headers)

    for i in range(number_of_rows):
        ticker_sub = {}
        row = table[i*len(headers):][:len(headers)]
        for j, header in enumerate(headers):
            ticker_sub[header] = row[j]

        data.append(ticker_sub)

    return data
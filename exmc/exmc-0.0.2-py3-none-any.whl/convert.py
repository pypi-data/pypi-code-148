import clipboard

BREAK_N = "\n"
BREAK_RN = "\r\n"
BREAK_BR = "<br>"
BREAK_CELL = "\t"
DOUBLE_QUOTE = '"'
SEPERATOR_VERTICAL_LINE = "|"


def join_with_vertical_line(cells):
    cell_list = []
    for cell in cells:
        cell = cell.strip()
        if cell:
            if BREAK_N in cell and BREAK_RN not in cell and DOUBLE_QUOTE in cell:
                cell_list.append(
                    cell.replace(BREAK_N, BREAK_BR).replace(DOUBLE_QUOTE, "")
                )
            else:
                cell_list.append(cell)
    rows = f"|{'|'.join(cell_list)}|"
    return rows


def excel2markdown(args):
    content = clipboard.paste()

    if args.debug == "true":
        print([content])

    rows = content.split(BREAK_RN)

    title = rows[0]
    len_columns = len(title.split(BREAK_CELL))
    rows_data = rows[1:]

    markdown_list = []
    title_list = title.split(BREAK_CELL)
    title = join_with_vertical_line(title_list)
    markdown_list.append(title)

    title_seperator = join_with_vertical_line(["---"] * len_columns)
    markdown_list.append(title_seperator)

    for row in rows_data:
        row = row.strip()
        if row:
            row_list = row.split(BREAK_CELL)
            row = join_with_vertical_line(row_list)
            markdown_list.append(row)

    markdown_str = f"{BREAK_N}".join(markdown_list)
    clipboard.copy(markdown_str)
    print(markdown_str)


def markdown2excel(args):
    content = clipboard.paste()

    if args.debug == "true":
        print([content])

    if BREAK_RN in content:
        rows = content.split(BREAK_RN)
    else:
        rows = content.split(BREAK_N)

    excel_list = []
    title_str = rows[0].strip()
    title_str = title_str[1:-1].replace(SEPERATOR_VERTICAL_LINE, BREAK_CELL)
    excel_list.append(title_str)

    rows_data = rows[2:]
    for row in rows_data:
        row = row.strip()
        if row:
            row_str = row[1:-1].replace(SEPERATOR_VERTICAL_LINE, BREAK_CELL)
            excel_list.append(row_str)
    excel_str = f"{BREAK_N}".join(excel_list)
    clipboard.copy(excel_str)
    print(excel_str)


def run(args):
    if args.reverse == "true":
        markdown2excel(args)
    else:
        excel2markdown(args)

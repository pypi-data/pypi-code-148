"""
Description: 
Author: MALossov
Date: 2023-01-27 16:56:56
LastEditTime: 2023-01-28 01:47:31
LastEditors: MALossov
Reference: 
"""
import ptt_clk_mal.pc_dao as pc_dao
import rich
from rich.console import Console
import datetime
import rich.table

console = Console()


def prettierPrintTable(data: list, days: int, hobby: list):
    if not data:
        console.print("[red bold underline]No data in the database!!!")
        return
    # use rich to print a table
    table = rich.table.Table(
        show_header=True,
        header_style="bold magenta",
        title="Potato History",
        title_style="bold magenta italic",
    )
    table.add_column("ID", style="dim sky_blue2", width=4)
    table.add_column("Date", style="dim spring_green1", width=12)
    table.add_column("Time", style="dim spring_green2", width=8)
    table.add_column("Aim", style="dim cyan2", width=10)
    table.add_column("Last", style="dim slate_blue3", width=4)
    sum_time = 0
    for row in data:
        sum_time += row[3]
        # let row[2] be the date&HH:MM from datetime
        Date = datetime.datetime.strptime(row[1][:-7], "%Y-%m-%d %H:%M:%S").strftime(
            "%Y-%m-%d"
        )
        Time = datetime.datetime.strptime(row[1][:-7], "%Y-%m-%d %H:%M:%S").strftime(
            "%H:%M"
        )
        table.add_row(str(row[0]), Date, Time, str(row[2]), str(row[3]))
    console.print(table)
    console.rule(
        "[bold italic wheat4]Common Statistics", style="bold orange2", align="left"
    )
    console.print(
        "Experienced {} times potatoes in total!".format(len(data)),
        style="bold hot_pink3",
        end="\t|\t",
    )
    console.print(
        "Total time is {} mins!".format(sum_time), style="bold deep_sky_blue1", end="\n"
    )
    console.print(
        "Your average is {} mins per time!".format(sum_time // len(data)),
        style="bold green",
        end="\n",
    )
    if days:
        console.rule(
            "[bold italic salmon1]Daily Statistics", style="bold plum2", align="left"
        )
        console.print(
            "Experienced {} days in total!".format(days),
            style="bold dark_olive_green3",
            end="\n",
        )
        console.print(
            "Your average is {} minutes per day!".format(sum_time // len(data)),
            style="bold italic sea_green2",
            end="\t|\t",
        )
        console.print(
            "Your average is {} times per day!".format(len(data) // days),
            style="bold salmon1 italic",
            end="\n",
        )
    if hobby:
        console.rule(
            "[bold italic dark_orange1]Hobby Statistics",
            style="bold dark_orange1",
            align="left",
        )
        # from hobbies create a dict
        hobby_dict = {hobby[i]: 0 for i in range(len(hobby))}
        for row in data:
            hobby_dict[row[2]] += 1
        for key in hobby_dict:
            console.print(
                "{}:{} times".format(key, hobby_dict[key]),
                style="bold dark_slate_gray3",
                end="\t|\t",
            )
        console.print("")
    console.rule(
        "[bold italic cyan1]Enjoy Nice New Days!", style="bold green", align="left"
    )


def potato_history(args):
    pc_dao.create_table()
    if args.clear:
        pc_dao.clean_table()
        console.rule(
            "[bold italic chartreuse2]History cleared!Enjoy Nice New Days!",
            style="bold green",
        )
    elif args.query and args.groups:
        queryGroupsAndArgs(args.query, args.groups)
    elif args.query:
        queryByDays(args.query)
    elif args.groups:
        queryByGroup(args.groups)
    else:
        console.print(
            "[cyan3 Italic underline]type: ",
            "[bold cyan]<CMD> his -h [/bold cyan]",
            "[cyan3 Italic underline]for help",
        )


# noinspection PyTypeChecker
def queryByDays(dayCount):
    if dayCount == "today":
        data, dayCount = pc_dao.query_last_xdays(1), 1
    elif dayCount == "week":
        data, dayCount = pc_dao.query_last_xdays(7), 7
    elif dayCount == "month":
        data, dayCount = pc_dao.query_last_xdays(30), 30
    elif dayCount == "all":
        data = pc_dao.query_potato()
        dayCount = len(data)
    else:
        try:
            data = pc_dao.query_last_xdays(int(dayCount))
            dayCount = len(data)
        except ValueError:
            console.print("Error: Invalid query string!!\n", style="bold red")
            console.print(
                "[bold dark_blue]Your query must be: [Italic cyan]today, yesterday, week, month, all or a number"
            )
            exit(1)
    prettierPrintTable(data, dayCount, None)


def queryGroupsAndArgs(query, group):
    try:
        data = pc_dao.query_xdays_and_groups(int(query), group)
        prettierPrintTable(data, int(query), group)
    except ValueError:
        console.print("Error: Invalid query string!!\n", style="bold red")
        console.print(
            "[Bold dark_blue]Your query must be: {Number} for query & Right Names for {Group}"
        )
        exit(1)


def queryByGroup(group):
    try:
        data = pc_dao.query_by_groups(group)
        # noinspection PyTypeChecker
        prettierPrintTable(data, None, group)
    except ValueError:
        console.print("Error: Invalid query string!!\n", style="bold red")
        console.print("[bold dark_blue]Your query must be: Right Names for {Group}")
        exit(1)

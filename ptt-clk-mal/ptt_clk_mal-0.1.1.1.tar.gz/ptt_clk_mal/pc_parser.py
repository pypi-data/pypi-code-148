#!/usr/bin/python3
"""
Description: 
Author: MALossov
Date: 2023-01-27 11:44:22
LastEditTime: 2023-01-27 11:48:58
LastEditors: MALossov
Reference: 
"""


import argparse
import os
import ptt_clk_mal.pc_clk as pc_clk
import ptt_clk_mal.pc_his as pc_his
import ptt_clk_mal.pc_set as pc_set
from rich.console import Console

console = Console()


def cli():
    sets = pc_set.Settings()
    if os.path.exists("%s" % pc_set.confYaml):
        sets.load()
    else:
        console.print(
            "[bold red]Warning!: pttsets.yaml does not exist!!Use DEFAULT SETTINGS!"
        )
        console.print(
            "[bold dark_blue]Please run [italic cyan]pttClk set -i[/] to init the settings"
        )
    parser = argparse.ArgumentParser(description="Set the clock on a pttClk router")
    # 参数部分
    parser.add_argument(
        "-t",
        "--time",
        type=int,
        help="Set the time of the clock",
        dest="time",
        required=False,
        default=sets.default_time,
    )
    parser.add_argument(
        "-n",
        "--notify",
        type=float,
        help="Notice intervals of the clock",
        dest="Intervals",
        required=False,
        default=sets.default_intervals,
    )
    parser.add_argument(
        "-a" "--aim",
        type=str,
        help="Set the aim of the clock",
        dest="aim",
        required=False,
        default=sets.default_aim,
    )
    parser.add_argument(
        "-c",
        "--color",
        type=str,
        help="Set colors of progress",
        dest="color",
        required=False,
        default=sets.default_color,
    )
    parser.add_argument(
        "-b",
        "--background",
        type=str,
        help="Set colors of progress' backend",
        dest="back",
        required=False,
        default=sets.default_bg,
    )
    parser.add_argument(
        "-p",
        "--pulse",
        type=str,
        help="Set colors of progress' pulse",
        dest="pulse",
        required=False,
        default=sets.default_pulse,
    )
    parser.add_argument(
        "-y",
        "--confirm",
        dest="start",
        action="store_true",
        help="Confirm the autostart啊 of bar",
        default=sets.default_confirm,
    )
    # 子命令部分
    subparsers = parser.add_subparsers(help="sub-commands")

    history_parse = subparsers.add_parser(
        "his", help="show your pttClks' history"
    )
    history_parse.add_argument(
        "-q",
        "--query",
        help="Query the history of pttClk times",
        dest="query",
        type=str,
        default=sets.default_queryT,
        required=False,
    )
    history_parse.add_argument(
        "-c",
        "--clear",
        dest="clear",
        action="store_true",
        help="Clear the history of pttClk times",
    )
    history_parse.add_argument(
        "-g",
        "--groups",
        dest="groups",
        nargs="+",
        type=str,
        required=False,
        default=sets.default_queryG,
        help="Query the history of pttClk times by groups",
    )
    #

    history_parse.set_defaults(handle=history)

    setting_parse = subparsers.add_parser(
        "set", help="Change the settings of default pttClk clocks"
    )
    setting_parse.add_argument(
        "-s", "--show", help="Show the settings", action="store_true"
    )
    setting_parse.add_argument(
        "-c", "--clear", help="Clear the settings", action="store_true"
    )
    setting_parse.add_argument(
        "-i", "--init", help="Init the settings", action="store_true"
    )
    setting_parse.add_argument(
        "-e", "--edit", help="Edit the settings", action="store_true"
    )
    setting_parse.set_defaults(handle=settings)

    args = parser.parse_args()
    if hasattr(args, "handle"):
        args.handle(args)
    else:
        pc_clk.potato_clock(args)


def history(args):
    pc_his.potato_history(args)


def settings(args):
    pc_set.sets(args)


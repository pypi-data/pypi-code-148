from datetime import datetime
from pathlib import Path
from typing import Any

import click
import pandas as pd
from rich import print

from .constants import DEFAULT_FEEDBACK_FILEPATH
from .feedback import read_feedback


@click.command(name="hours")
@click.option(
    "-f",
    "--feedback",
    "feedback_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=DEFAULT_FEEDBACK_FILEPATH,
)
@click.option("-s", "--start", type=click.DateTime(), default=pd.Timestamp.min)
@click.option("-e", "--end", type=click.DateTime(), default=pd.Timestamp.max)
def main(feedback_path: str | Path, start: datetime, end: datetime) -> None:
    feedback: pd.DataFrame = read_feedback(filepath=feedback_path)
    feedback = feedback[(feedback["提交答卷时间"] >= start) & (feedback["提交答卷时间"] < end)]
    groups = feedback.groupby(by="志愿者")
    hours: list[dict[str, Any]] = list()
    for raw_name, df in groups:
        name: str = str(raw_name)
        hours.append({"name": name, "hours": df["服务时长/分钟"].sum() / 60})
    results: pd.DataFrame = pd.DataFrame(hours)
    results.to_csv("hours.csv")
    print("start :", start)
    print("end   :", end)

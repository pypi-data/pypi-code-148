import os
from datetime import datetime
from pathlib import Path
from typing import Any

import click
import matplotlib
import pandas as pd
from jinja2 import Environment, FileSystemLoader, Template
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from .account import read_accounts, set_accounts
from .constants import (
    DEFAULT_ACCOUNT_FILEPATH,
    DEFAULT_FEEDBACK_FILEPATH,
    DEFAULT_PREFIX,
    GRADING_ITEMS,
    NAME,
    TEMPLATE_DIR,
    TEMPLATE_PATH,
)

matplotlib.rcParams["font.sans-serif"] = "Noto Sans CJK SC"
matplotlib.rc(group="axes", unicode_minus=False)
matplotlib.use(backend="agg")

import matplotlib.pyplot as plt


def read_feedback(filepath: str | Path = DEFAULT_FEEDBACK_FILEPATH) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    df = df[
        [
            "提交答卷时间",
            "您的姓名",
            "志愿者",
            "答疑科目",
            "服务时长/分钟",
            "评分—业务能力",
            "启发程度",
            "服务态度",
            "满意程度",
            "想说的话",
        ]
    ]
    df["提交答卷时间"] = pd.to_datetime(df["提交答卷时间"])
    df.rename(columns={"评分—业务能力": "业务能力"}, inplace=True)
    for item in GRADING_ITEMS:
        df[item] = pd.to_numeric(df[item], errors="coerce")
    df["想说的话"].replace(to_replace="(空)", value="", inplace=True)
    return df


def plot_time(
    df: pd.DataFrame, prefix: str | Path = DEFAULT_PREFIX, top_k: int = 9
) -> None:
    prefix = Path(prefix)
    subjects = df[["答疑科目", "服务时长/分钟"]].groupby(by="答疑科目").sum()
    subjects.sort_values(by="服务时长/分钟", ascending=False, inplace=True)
    data: pd.Series = subjects["服务时长/分钟"].head(n=top_k)
    if top_k < len(subjects):
        data["其他"] = subjects["服务时长/分钟"][top_k:].sum()

    plt.figure(dpi=300)
    plt.pie(data, labels=data.keys(), autopct="%.1f%%")
    plt.tight_layout()
    plt.savefig(prefix / "pie.png")
    plt.close()

    plt.figure(dpi=300)
    plt.barh(y=data.index, width=data / 60)
    plt.xlabel("服务时长/小时")
    plt.tight_layout()
    plt.savefig(prefix / "bar.png")
    plt.close()


def process_feedback(
    name: str,
    df: pd.DataFrame,
    readme: Template,
    last_updated_at: datetime,
    prefix: str | Path = DEFAULT_PREFIX,
) -> None:
    prefix = Path(prefix)
    os.makedirs(name=prefix, exist_ok=True)

    data: dict[str, Any] = {"name": name, "last_updated_at": last_updated_at}

    count: int = len(df)
    data["count"] = count
    time: float = df["服务时长/分钟"].sum(skipna=True)
    data["hours"] = round(number=time / 60, ndigits=2)

    for item in GRADING_ITEMS:
        score: float = df[item].mean(skipna=True)
        data[item] = round(score, ndigits=2)

    plot_time(df=df, prefix=prefix)

    readme_filepath: Path = prefix / "README.md"
    readme_filepath.write_text(data=readme.render(data))


@click.command(name="feedback")
@click.option(
    "-p",
    "--prefix",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default=DEFAULT_PREFIX,
)
@click.option(
    "-a",
    "--account",
    "account_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=DEFAULT_ACCOUNT_FILEPATH,
)
@click.option(
    "-f",
    "--feedback",
    "feedback_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=DEFAULT_FEEDBACK_FILEPATH,
)
def main(
    prefix: str | Path, account_path: str | Path, feedback_path: str | Path
) -> None:
    prefix = Path(prefix)

    with Progress(
        TextColumn("{task.description}", style="bold bright_green"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        accounts = read_accounts(filepath=account_path)
        set_accounts(accounts=accounts, prefix=prefix, progress=progress)

        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        readme: Template = env.get_template(str(TEMPLATE_PATH))
        feedback: pd.DataFrame = read_feedback(filepath=feedback_path)
        last_updated_at = feedback["提交答卷时间"].max()
        process_feedback(
            name=NAME,
            df=feedback,
            readme=readme,
            last_updated_at=last_updated_at,
            prefix=prefix,
        )
        groups = feedback.groupby(by="志愿者")
        for raw_name, df in progress.track(
            sequence=groups, description="Processing Data"
        ):
            name: str = str(raw_name)
            process_feedback(
                name=name,
                df=df,
                readme=readme,
                last_updated_at=last_updated_at,
                prefix=prefix / name,
            )
            df.drop(columns=["您的姓名"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.to_csv(prefix / name / f"{name}.csv")

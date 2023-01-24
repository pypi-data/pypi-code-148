import asyncio
import hashlib
import sys
from typing import Dict

import typer
from hitfactorpy.parsers.match_report.pandas import parse_match_report
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .. import defaults as _defaults
from .. import env as _env

cli = typer.Typer()


@cli.command()
def match_report(
    file: typer.FileText = typer.Argument(sys.stdin, help="Report file in raw (.txt) format"),
    sqlalchemy_url: str = typer.Option(
        _defaults.HITFACTORPY_SQLALCHEMY_URL,
        envvar=_env.HITFACTORPY_SQLALCHEMY_URL,
        help="Full database URI including driver",
    ),
):
    """import a match report"""
    from hitfactorpy_sqlalchemy.orm.models import (
        MatchReport,
        MatchReportCompetitor,
        MatchReportStage,
        MatchReportStageScore,
    )

    async def command_main():
        file_text = "\n".join(file.readlines())
        file_hash = hashlib.md5(file_text.encode()).hexdigest()
        parsed_match_report = parse_match_report(file_text)

        engine = create_async_engine(sqlalchemy_url)
        Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
        async with Session() as session:
            match_report = MatchReport(
                name=parsed_match_report.name,
                date=parsed_match_report.date,
                match_level=parsed_match_report.match_level,
                report_hash=file_hash,
            )
            session.add(match_report)

            competitors: Dict[int, MatchReportCompetitor] = {}
            for c in parsed_match_report.competitors:
                competitor_model = MatchReportCompetitor(
                    member_number=c.member_number,
                    first_name=c.first_name,
                    last_name=c.last_name,
                    division=c.division,
                    power_factor=c.power_factor,
                    classification=c.classification,
                    dq=c.dq,
                    reentry=c.reentry,
                    match=match_report,
                )
                session.add(competitor_model)
                competitors[c.internal_id] = competitor_model

            stages: Dict[int, MatchReportCompetitor] = {}
            for s in parsed_match_report.stages:
                stage_model = MatchReportStage(
                    name=s.name,
                    min_rounds=s.min_rounds,
                    max_points=s.max_points,
                    classifier=s.classifier,
                    classifier_number=s.classifier_number,
                    scoring_type=s.scoring_type,
                    stage_number=s.internal_id,
                    match=match_report,
                )
                session.add(stage_model)
                stages[s.internal_id] = stage_model

            for sc in parsed_match_report.stage_scores:
                stage_score_model = MatchReportStageScore(
                    a=sc.a,
                    b=sc.b,
                    c=sc.c,
                    d=sc.d,
                    m=sc.m,
                    npm=sc.npm,
                    ns=sc.ns,
                    procedural=sc.procedural,
                    late_shot=sc.late_shot,
                    extra_shot=sc.extra_shot,
                    extra_hit=sc.extra_hit,
                    other_penalty=sc.other_penalty,
                    t1=sc.t1,
                    t2=sc.t2,
                    t3=sc.t3,
                    t4=sc.t4,
                    t5=sc.t5,
                    time=sc.time,
                    dq=sc.dq,
                    dnf=sc.dnf,
                    match=match_report,
                    competitor=competitors[sc.competitor_id],
                    stage=stages[sc.stage_id],
                )
                session.add(stage_score_model)

            typer.echo("Committing changes...")
            await session.commit()
            await session.close()

    asyncio.run(command_main())


if __name__ == "__main__":
    cli()

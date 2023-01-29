# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <sa@adercon.com>
#
# LOGGING: designed to run at INFO loglevel.

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import pycouchdb
import requests
import typer
import urllib3
from rich import box, print
from rich.console import Console
from rich.panel import Panel

import mpbroker.tools
from mpbroker.config.config import APP_NAME, APP_VERSION, user_cfg
from mpbroker.models.ingest import IngestLog, IngestLogReason, IngestLogStatus
from mpbroker.models.media import Media, MediaPlay, MediaPlayRating, MediaPlayStatus
from mpbroker.utils import (
    db_not_available,
    determine_status_from_flags,
    extract_metadata,
    make_doc,
    play_item,
    results_by_name,
    results_to_table,
)

# disable InsecureRequestWarnings which come up if you are proxying couchdb through haproxy with ssl termination.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = pycouchdb.Server(user_cfg.database.db_uri)
app = typer.Typer()
app.add_typer(mpbroker.tools.app, name="tools")


@app.command()
def info():
    """
    All about your Library
    """

    # NOTICE: this command is not 'user' aware, info is for complete Library.

    try:
        db = server.database("media")

        _total = db.query(
            "filters/stats_total",
            # ~ group='true',
            # ~ keys=[name],
            # ~ startkey=name,
            # ~ endkey=f"{name}\ufff0",
            as_list=True,
            # ~ flat="key"
        )
        if not _total or len(_total) < 1:
            typer.secho(
                "Your Library appears to be empty try, ingesting something!",
                fg=typer.colors.MAGENTA,
                bold=True,
            )
            raise typer.Exit()

        _status = db.query(
            "filters/stats_status",
            group="true",
            as_list=True,
        )

        _sources = db.query(
            "filters/stats_sources",
            group="true",
            as_list=True,
        )

        _sources_list = [
            f"\n  • {source['key'][0]} ({source['value']})" for source in _sources
        ]
        _new = [item for item in _status if item["key"] == MediaPlayStatus.new]
        _played = [item for item in _status if item["key"] == MediaPlayStatus.played]
        _watched = [item for item in _status if item["key"] == MediaPlayStatus.watched]

        _about = f"""{APP_NAME} v{APP_VERSION}
Copyright 2022 drad <sa@adercon.com>"""
        _account = f"- Database: [bold]{user_cfg.database.db_uri}[/bold]"
        _defaults = f"""- User:   {user_cfg.defaults.user}
- Source: {user_cfg.defaults.source}
- Base:   {user_cfg.defaults.base}"""
        _preferences = f"""- Use Pager: {user_cfg.use_pager}
- Player:    {user_cfg.player}"""
        _library = f"""- Total:   [bold]{_total[0]['value']}[/bold]
- New:     {_new[0]['value'] if _new else 0}
- Played:  {_played[0]['value'] if _played else 0}
- Watched: {_watched[0]['value'] if _watched else 0}
- Sources {''.join(_sources_list)}"""

        _width = 100
        print(Panel(_about, expand=True, width=_width, box=box.MINIMAL, style=""))
        print(
            Panel(
                _account, title="Account", expand=True, width=_width, style="on gray30"
            )
        )
        print(
            Panel(
                _defaults,
                title="Defaults",
                expand=True,
                width=_width,
                style="on gray30",
            )
        )
        print(
            Panel(
                _preferences,
                title="Preferences",
                expand=True,
                width=_width,
                style="on gray30",
            )
        )
        print(
            Panel(
                _library, title="Library", expand=True, width=_width, style="on gray30"
            )
        )

    except requests.exceptions.ConnectionError:
        db_not_available()
    except pycouchdb.exceptions.NotFound:
        typer.secho(
            "Your Library appears to be empty try, ingesting something!",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit()


@app.command()
def ingest(
    base: str = typer.Option(
        user_cfg.defaults.base,
        "--base",
        help="the base path to search for media items to ingest",
    ),
    source: str = typer.Option(
        user_cfg.defaults.source,
        "--source",
        help="source to use for ingest (ingested data will have this source)",
    ),
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="user to use for ingest (ingested data will belong to this user)",
    ),
    extract_metadata_flag: bool = typer.Option(
        False,
        "--extract-metadata",
        help="extract media metadata (e.g. duration, size, encoding type, etc.) - this increases ingest time significantly",
    ),
    no_confirm: bool = typer.Option(
        False,
        "--no-confirm",
        help="do not confirm - run ingest immediately (useful if you are running via cron or a script)",
    ),
):
    """
    ingest media
    """

    typer.echo(f"Scanning base ({base}) for media...")
    _user = user if len(user) > 0 else None

    _base = Path(base)
    if not _base.exists() or not _base.is_dir():
        typer.echo(f"Directory [{_base}] not found or not a directory, cannot proceed!")
        raise typer.Exit()

    all_files = []
    for ext in user_cfg.ingest.file_types:
        all_files.extend(_base.rglob(ext))

    if no_confirm == False:

        typer.echo(
            f"""
    ---------- Confirm Ingest ----------
    - file types:       {user_cfg.ingest.file_types}
    - base:             {_base.as_posix()}
    - user:             {_user}
    - source:           {source}
    - extract metadata: {extract_metadata_flag}
    - number of items:  {len(all_files)}
    """
        )

        typer.confirm("Do you want to continue?", abort=True)

    _start = time.time()
    _batchid = datetime.now().strftime("%Y-%m-%d_%H:%M:S.%f")

    with typer.progressbar(all_files) as progress:
        for f in progress:
            ingest_file(
                source=source,
                filepath=f,
                base=_base.as_posix(),
                extract_metadata_flag=extract_metadata_flag,
                batchid=_batchid,
                user=_user,
            )

    _stop = time.time()

    # get ingest_logs info
    try:
        db = server.database("injest_logs")
        _il_status = db.query(
            "filters/status",
            group="true",
            # ~ keys=['2022-05-03_12:24:35.4292'],
            startkey=[_batchid],
            endkey=[f"{_batchid}\ufff0"],
            as_list=True,
            # ~ flat="key"
        )
        # typer.echo(f"ingest_logs info: {_il_status}")
        _rr = []
        for row in _il_status:
            _rr.append(f"\n\t- {row['key'][1]} ({row['key'][2]}): {row['value']}")

    except requests.exceptions.ConnectionError:
        db_not_available()

    typer.echo(
        f"""
---------- Ingest Summary ----------
Details
\t- location:        {_base.as_posix()}
\t- user:            {_user}
\t- source:          {source}
\t- files to ingest: {len(all_files)}
\t- batchid:         {_batchid}
Number Ingested{"".join(_rr)}
Ingestion took {_stop - _start}s
"""
    )


def ingest_file(
    source: str,
    filepath: str,
    base: str,
    extract_metadata_flag: bool = False,
    batchid: str = None,
    user: str = None,
):
    """
    Ingest a file.
    """

    # ensure base ends with /
    _base = base if base.endswith("/") else f"{base}/"
    _user = f"{user}:" if user else ""
    # directory is filepath.parent - base
    directory = str(filepath.parent).replace(_base, "")

    # create IngestLog instance.
    il = IngestLog(
        batchid=batchid,
        source=source,
        status=IngestLogStatus.ok,
        reason=IngestLogReason.ok,
        message=None,
        created=datetime.now(),
        creator=_user,
    )

    m = Media(
        doc_id=f"{_user}{filepath.name}",
        # sid=make_sid(filepath.name),
        name=filepath.name,
        base=_base,
        directory=directory,
        sources=[source],
        media_type=filepath.suffix,
        # ~ notes="",
        play=MediaPlay(),
        metadata=None,  # added later
        creator=None,
        updator=None,
    )
    _doc_id = f"{_user}{filepath.name}"

    try:
        db = server.database("media")
        # NOTICE: this is the 'update' path, most calls should drop to the pycouchdb.exceptions.NotFound path.
        # check if doc already exists.
        _doc = db.get(_doc_id)
        # update the doc as needed.
        if source not in _doc["sources"]:
            _doc["sources"].append(source)
            il.reason = IngestLogReason.updated

        if extract_metadata_flag:
            _metadata, _error = extract_metadata(filepath)
            _doc["metadata"] = json.loads(_metadata.json()) if _metadata else None
            il.reason = IngestLogReason.updated
            if _error:
                il.status = IngestLogStatus.issue
                il.reason = IngestLogReason.metadata_extract_issue

        if (
            il.reason == IngestLogReason.updated
            or il.reason == IngestLogReason.metadata_extract_issue
        ):
            _doc["updated"] = datetime.timestamp(datetime.now())
            db.save(_doc)
        else:
            il.status = IngestLogStatus.ok
            il.reason = IngestLogReason.already_exists

    except requests.exceptions.ConnectionError:
        db_not_available()
    except pycouchdb.exceptions.NotFound:
        # new item: add to Library
        il.status = IngestLogStatus.ok
        il.reason = IngestLogReason.ok
        metadata = None
        if extract_metadata_flag:
            m.metadata, error = extract_metadata(filepath)
            # if no metadata returned check error.
            if not metadata:
                il.status = IngestLogStatus.issue
                il.reason = IngestLogReason.metadata_extract_issue

        dts = make_doc(doc=m, rename_doc_id=True)

        db.save(dts)

    except pycouchdb.exceptions.Conflict:
        il.status = IngestLogStatus.fail
        il.reason = IngestLogReason.already_exists
        il.message = f"Duplicate item not ingested: {m.directory}/{m.name}, source(s): {_doc['sources']}"

    # write the IngestLog record.
    try:
        db = server.database("injest_logs")
        db.save(
            # stopped here, need to get an _id on the il doc somewhere and go...
            make_doc(doc=il, rename_doc_id=False)
        )
    except requests.exceptions.ConnectionError:
        db_not_available()


@app.command()
def list(
    name: str,
    directory: str = typer.Option(
        None, "--directory", help="directory/partial directory to filter on"
    ),
    new: bool = typer.Option(False, "--new", "-n", help="only select new items"),
    played: bool = typer.Option(
        False, "--played", "-p", help="only select played items"
    ),
    watched: bool = typer.Option(
        False, "--watched", "-w", help="only select watched items"
    ),
    auto_play: bool = typer.Option(
        False, "--auto-play", "-a", help="auto-play the first item returned in list"
    ),
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="only show for user (leave empty to use default user)",
    ),
):
    """
    List media
    """

    _status = determine_status_from_flags(new=new, played=played, watched=watched)
    _results = results_by_name(
        name=name, user=user, status=_status, filter_directory=directory
    )

    if auto_play:
        try:
            db = server.database("media")
            # play first item
            _doc = db.get(_results[0]["id"])
            _fmt_item = typer.style(
                f"{_doc['directory']}/{_doc['name']}", bg=typer.colors.RED, bold=True
            )
            typer.echo(f"Auto-Play of item: {_fmt_item}")
            play_item(doc=_doc, name=name, user=user)
        except requests.exceptions.ConnectionError:
            db_not_available()
    else:
        table = results_to_table(_results, name=name, user=user, directory=directory)
        console = Console()
        if user_cfg.use_pager:
            with console.pager(styles=True):
                console.print(table)
        else:
            console.print(table)


@app.command()
def play(
    name: str,
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="user to use for playing",
    ),
):
    """
    Play media
    """

    _base = Path(name)
    media_item = _base.name
    # typer.echo(f"Playing item [{name}/{media_item}]")

    # lookup item to get source.
    try:
        db = server.database("media")
        _id = f"{user}:{media_item}"
        # ~ typer.echo(f"- getting media item with id={_id} of name={name}")
        # add 'play next' logic; I think we should create a 'get_or_select_media_item' function here which tries to get a doc, if more then one is found it prints list and lets user choose, then returns doc
        _doc = db.get(_id)

        play_item(doc=_doc, name=name, user=user)

    except requests.exceptions.ConnectionError:
        db_not_available()
    # ~ except pycouchdb.exceptions.NotFound:
    # ~ typer.secho(
    # ~ f"Media item {name} not found for user {user}.",
    # ~ fg=typer.colors.RED,
    # ~ bold=True,
    # ~ )
    # ~ raise typer.Exit()


@app.command()
def remove(
    name: str,
    directory: str = typer.Option(
        None, "--directory", help="directory/partial directory to filter on"
    ),
    new: bool = typer.Option(False, "--new", "-n", help="only select new items"),
    played: bool = typer.Option(
        False, "--played", "-p", help="only select played items"
    ),
    watched: bool = typer.Option(
        False, "--watched", "-w", help="only select watched items"
    ),
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="only show for user (leave empty to use default user)",
    ),
):
    """
    Remove media
    """

    _status = determine_status_from_flags(new=new, played=played, watched=watched)

    try:
        results = results_by_name(
            name=name, user=user, status=_status, filter_directory=directory
        )
        table = results_to_table(results, name=name, user=user)
        console = Console()
        # NOTE: no pagination for delete display
        console.print(table)
        _action = typer.style("Remove ALL", bg=typer.colors.RED, bold=True)
        typer.confirm(
            f"Are you sure you want to {_action} items listed above?", abort=True
        )
        _removed = 0
        db = server.database("media")
        with typer.progressbar(results) as progress:
            for item in progress:
                db.delete(item["id"])
                _removed += 1

        typer.secho(
            f"Deleted {_removed} items from your Library!",
            fg=typer.colors.MAGENTA,
            bold=True,
        )

    except requests.exceptions.ConnectionError:
        db_not_available()
    except pycouchdb.exceptions.NotFound:
        typer.secho(
            f"Media item {name} not found for user {user}.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit()


@app.command()
def update(
    name: str,
    directory: str = typer.Option(
        None, "--directory", help="directory/partial directory to filter on"
    ),
    new: bool = typer.Option(False, "--new", "-n", help="only select new items"),
    played: bool = typer.Option(
        False, "--played", "-p", help="only select played items"
    ),
    watched: bool = typer.Option(
        False, "--watched", "-w", help="only select watched items"
    ),
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="only show for user (leave empty to use default user)",
    ),
):
    """
    Update media
    """

    _status = determine_status_from_flags(new=new, played=played, watched=watched)

    # @TODO: flake8 complexity of this method is 20, need to refactor to bring it down to 18 at most.
    try:
        results = results_by_name(
            name=name, user=user, status=_status, filter_directory=directory
        )
        table = results_to_table(results, name=name, user=user)
        console = Console()
        # NOTE: no pagination for update display.
        console.print(table)

        typer.confirm("Do you want to continue?", abort=True)
        _rating_list = [str(i) for i in MediaPlayRating._value2member_map_]
        _rating_list.append("")
        _status = None

        if typer.confirm("  Update Status?"):
            _status = typer.prompt(
                "    New Status",
                default=MediaPlayStatus.watched,
                type=click.Choice([str(i) for i in MediaPlayStatus._value2member_map_]),
            )
        _update_rating = typer.confirm("  Update Rating?")
        if _update_rating:
            _rating = typer.prompt(
                "    New Rating (blank to clear)",
                default="",
                type=click.Choice(_rating_list),
            )
        _update_rating_notes = typer.confirm("  Update Rating Notes?")
        if _update_rating_notes:
            _rating_notes = typer.prompt(
                "  New Rating Notes (blank to clear)",
                default="",
                show_default=False,
            )
        _update_notes = typer.confirm("  Update Notes?")
        if _update_notes:
            _notes = typer.prompt(
                "    New Notes (blank to clear)",
                default="",
                show_default=False,
            )
        _extract_metadata = typer.confirm("  Extract Metadata for item?")
        # iterate over docs and update accordingly.
        _updated = 0
        db = server.database("media")
        _errors = []
        with typer.progressbar(results) as progress:
            for item in progress:
                _doc = db.get(item["id"])
                _dirty = False
                if _status:
                    _doc["play"]["status"] = _status
                    _dirty = True
                if _update_rating:
                    if _rating:
                        _doc["play"]["rating"] = int(_rating)
                    else:
                        _doc["play"]["rating"] = None
                    _dirty = True
                if _update_rating_notes:
                    if _rating_notes:
                        _doc["play"]["rating_notes"] = _rating_notes
                    else:
                        _doc["play"]["rating_notes"] = None
                    _dirty = True
                if _update_notes:
                    if _notes:
                        _doc["play"]["notes"] = _notes
                    else:
                        _doc["play"]["notes"] = None
                    _dirty = True
                if _extract_metadata:
                    _filepath = f"{_doc['base']}{_doc['directory']}/{_doc['name']}"
                    # ~ typer.echo(f"    ::> {_filepath}")
                    metadata, error = extract_metadata(_filepath)
                    if metadata and not error:
                        _doc["metadata"] = json.loads(metadata.json())
                        _dirty = True
                    else:
                        _errors.append(f"  ✦ {error}")
                if _dirty:
                    _updated += 1
                    _doc["updated"] = datetime.timestamp(datetime.now())
                    _doc["updator"] = user
                    db.save(_doc)
        if len(_errors) > 0:
            typer.secho("\nMetadata Extraction Issues:", fg=typer.colors.MAGENTA)
            typer.secho("\n".join(_errors), fg=typer.colors.YELLOW)
        typer.secho(
            f"Updated {_updated} items from your Library!",
            fg=typer.colors.MAGENTA,
            bold=True,
        )

    except requests.exceptions.ConnectionError:
        db_not_available()
    except pycouchdb.exceptions.NotFound:
        typer.secho(
            f"Media item {name} not found for user {user}.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit()


def version_callback(value: bool):
    if value:
        typer.echo(f"{APP_NAME} {APP_VERSION}")

        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Show application version and exit",
    ),
):

    pass


if __name__ == "__main__":
    app()

"""
    MastodonAmnesia - deletes old Mastodon toots
    Copyright (C) 2021, 2022  Mark S Burgunder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import asyncio
import json
import logging
import sys
from math import ceil
from typing import Any
from typing import cast
from typing import Optional

import aiohttp
import arrow
import click
from aiohttp.client_exceptions import ClientError
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError
from minimal_activitypub.client_2_server import RatelimitError
from rich import print  # pylint: disable=redefined-builtin
from rich import traceback
from tqdm import tqdm
from tqdm import trange

from . import __display_name__
from . import __version__
from . import Toot
from .config import Configuration
from .config import setup_shop
from .util import AuditLog
from .util import check_updates

traceback.install(show_locals=True)
logger = logging.getLogger(__display_name__)
logger.setLevel(logging.DEBUG)


async def main(  # noqa: max-complexity: 13
    config_file: str,
    is_dry_run: bool,
    debug_log_file: Optional[str],
    audit_log_file: Optional[str],
    audit_log_style: Optional[str],
    batch_size: Optional[int],
    limit: Optional[int],
) -> None:
    """Main logic to run MastodonAmnesia."""

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments

    config = await setup_shop(
        config_file=config_file,
        debug_log_file=debug_log_file,
    )

    oldest_to_keep = arrow.now().shift(seconds=-config.bot.delete_after)

    print(f"Welcome to {__display_name__} {__version__}")
    logger.debug("main -Welcome to %s %s", __display_name__, __version__)

    check_updates()

    try:
        session = aiohttp.ClientSession()

        instance = ActivityPub(
            instance=config.mastodon.instance,
            access_token=config.mastodon.access_token,
            session=session,
        )
        await instance.determine_instance_type()
        user_info = await instance.verify_credentials()
        print(
            f"We are removing toots older than {oldest_to_keep} "
            f"from {config.mastodon.instance}@{user_info['username']}"
        )

        audit_log = None
        if audit_log_file:
            print(
                f"A record of all deleted toots will be recorded in the audit log file at {audit_log_file}"
            )
            audit_log = await AuditLog.open(
                audit_log_file=audit_log_file,
                style=audit_log_style,
            )

        toots = await instance.get_account_statuses(account_id=user_info["id"])
    except RatelimitError:
        print(
            f"RateLimited during startup, [red]Please wait until[/red] "
            f"{instance.ratelimit_reset} before trying again"
        )
        sys.exit(429)
    except (ClientError, ActivityPubError):
        logger.exception("!!! Cannot continue.")
        sys.exit(100)

    toots_to_delete: list[Toot] = []
    title = "Finding toots to delete"
    progress_bar = tqdm(
        desc=f"{title:.<60}",
        ncols=120,
        unit="toots",
        position=0,
        bar_format="{l_bar} {n_fmt} at {rate_fmt}",
    )
    while True:
        try:
            for toot in toots:
                logger.debug(
                    "Processing toot: %s from %s",
                    toot.get("url"),
                    arrow.get(toot.get("created_at")).to(tz="local"),
                )

                logger.debug(
                    "Oldest to keep vs toot created at %s > %s",
                    oldest_to_keep,
                    arrow.get(toot.get("created_at")).to(tz="local"),
                )

                if should_keep(
                    toot=toot,
                    oldest_to_keep=oldest_to_keep,
                    config=config,
                ):
                    logger.info(
                        "Not deleting toot: "
                        "Bookmarked: %s - "
                        "My Fav: %s - "
                        "Pinned: %s - "
                        "Poll: %s - "
                        "Attachements: %s - "
                        "Faved: %s - "
                        "Boosted: %s - "
                        "DM: %s -+- "
                        "Created At: %s -+- "
                        "%s",
                        toot.get("bookmarked"),
                        toot.get("favourited"),
                        toot.get("pinned"),
                        (toot.get("poll") is not None),
                        len(toot.get("media_attachments")),
                        toot.get("favourites_count"),
                        toot.get("reblogs_count"),
                        (toot.get("visibility") == "direct"),
                        arrow.get(toot.get("created_at")).to(tz="local"),
                        toot.get("url"),
                    )

                elif limit and len(toots_to_delete) >= limit:
                    break

                else:
                    toots_to_delete.append(toot)

                progress_bar.update()

            if limit and len(toots_to_delete) >= limit:
                break

            # Get More toots if available:
            logger.debug("Main - get next batch of toots if available.")
            logger.debug("Main - instance.pagination: %s", instance.pagination)
            if (
                instance.pagination["next"]["max_id"]
                or instance.pagination["next"]["min_id"]
            ):
                toots = await instance.get_account_statuses(
                    account_id=user_info["id"],
                    max_id=instance.pagination["next"]["max_id"],
                    min_id=instance.pagination["next"]["min_id"],
                )
                logger.debug("Main - scrolling - len(toots): %s", len(toots))
                if len(toots) == 0:
                    break
            else:
                break

        except RatelimitError:
            await sleep_off_ratelimiting(instance=instance)

    progress_bar.close()

    total_toots_to_delete = len(toots_to_delete)
    logger.debug(
        "Main - start deleting - total_toots_to_delete: %s", total_toots_to_delete
    )
    for toot in toots_to_delete:
        logger.debug(
            "Start of deleting - toot to delete: %s @ %s",
            toot["id"],
            toot["url"],
        )

    # If dry-run has been specified, print out list of toots that would be deleted
    if is_dry_run:
        print("\n--dry-run or -d specified. [yellow][bold]No toots will be deleted")
        for toot in toots_to_delete:
            print(
                f"[red]Would[/red] delete toot"
                f" {toot.get('url')} from {toot.get('created_at')}"
            )
        print(f"Total of {total_toots_to_delete} toots would be deleted.")

    # Dry-run has not been specified... delete toots!
    else:
        await delete_toots(
            instance=instance,
            toots_to_delete=toots_to_delete,
            audit=audit_log,
            batch_size=batch_size,
        )
        print(f"All old toots deleted! Total of {total_toots_to_delete} toots deleted")

    if audit_log:
        await audit_log.close()
    await session.close()


async def delete_toots(
    instance: ActivityPub,
    toots_to_delete: list[Toot],
    audit: Optional[AuditLog],
    batch_size: Optional[int],
) -> None:
    """Method to delete all toots that should be deleted."""
    title = "Deleting toots"
    total_toots_to_delete = len(toots_to_delete)
    if total_toots_to_delete > 0:
        with tqdm(
            desc=f"{title:.<60}",
            ncols=120,
            total=total_toots_to_delete,
            unit="toots",
            position=0,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} at {rate_fmt}",
        ) as progress_bar:

            while len(toots_to_delete) > 0:

                tasks = []
                for toot in toots_to_delete:
                    tasks.append(
                        delete_single_toot(toot=toot, instance=instance, audit=audit)
                    )
                    if batch_size and len(tasks) >= batch_size:
                        break

                responses = await asyncio.gather(*tasks)

                # Filter out any responses that are None...
                # Those encountered Rate Limiting
                deleted_toots = [toot for toot in responses if toot is not None]
                logger.debug(
                    "delete_toots - len(deleted_toots): %s",
                    len(deleted_toots),
                )

                progress_bar.update(len(deleted_toots))

                if len(deleted_toots) < len(toots_to_delete):
                    await sleep_off_ratelimiting(instance=instance)

                for toot in deleted_toots:
                    toots_to_delete.remove(toot)


async def sleep_off_ratelimiting(
    instance: ActivityPub,
) -> None:
    """Determines time needed to wait and waits for rate limiting to be
    over."""

    logger.debug(
        "sleep_off_ratelimiting - Rate limited: Limit: %s - resetting at: %s",
        instance.ratelimit_remaining,
        instance.ratelimit_reset,
    )
    reset_at = arrow.get(instance.ratelimit_reset).datetime
    now = arrow.now().datetime
    need_to_wait = ceil((reset_at - now).total_seconds())

    logger.info(
        "Need to wait %s seconds (until %s) to let server 'cool down'",
        need_to_wait,
        arrow.get(instance.ratelimit_reset),
    )
    bar_title = "Waiting to let server 'cool-down'"
    for _i in trange(
        need_to_wait,
        desc=f"{bar_title:.<60}",
        unit="s",
        ncols=120,
        bar_format="{desc}: {percentage:3.0f}%|{bar}| Eta: {remaining} - Elapsed: {elapsed}",
        position=1,
    ):
        await asyncio.sleep(1)


async def delete_single_toot(
    toot: Toot,
    instance: ActivityPub,
    audit: Optional[AuditLog],
) -> Optional[dict[str, Any]]:
    """Deletes a single toot."""
    logger.debug(
        "delete_single_toot(toot=%s, instance=%s)",
        toot["id"],
        instance.instance,
    )
    return_toot: Optional[dict[str, Any]] = toot
    try:
        await instance.delete_status(status=toot)
        logger.info(
            "delete_single_toot - Deleted toot %s from %s",
            toot.get("url"),
            toot.get("created_at"),
        )
        if audit:
            await audit.add_entry(toot=toot)
    except RatelimitError:
        logger.debug(
            "delete_single_toot - toot id = %s - ratelimit_remaining = %s - ratelimit_reset = %s",
            toot["id"],
            instance.ratelimit_remaining,
            instance.ratelimit_reset,
        )
        return_toot = None
    except ActivityPubError as error:
        logger.debug(
            "delete_single_toot - encountered error: %s",
            error,
        )
        logger.debug("delete_single_toot - toot: %s", json.dumps(toot, indent=4))
        raise error

    return return_toot


def should_keep(toot: Toot, oldest_to_keep: arrow.Arrow, config: Configuration) -> bool:
    """Function to determine if toot should be kept even though it might be a
    candidate for deletion."""

    # Kind of agree, but alternative would be harder to read IMHO
    # pylint: disable=too-many-return-statements

    toot_created_at = arrow.get(cast(int, toot.get("created_at")))
    if toot_created_at >= oldest_to_keep:
        return True

    if config.bot.skip_deleting_bookmarked and bool(toot.get("bookmarked")):
        return True

    if config.bot.skip_deleting_faved and bool(toot.get("favourited")):
        return True

    if config.bot.skip_deleting_pinned and bool(toot.get("pinned")):
        return True

    if config.bot.skip_deleting_poll and bool(toot.get("poll")):
        return True

    if config.bot.skip_deleting_dm and toot.get("visibility") == "direct":
        return True

    medias = toot.get("media_attachments")
    if (
        config.bot.skip_deleting_media
        and isinstance(medias, list)
        and bool(len(medias))
    ):
        return True

    favourites = toot.get("favourites_count", 0)
    if (
        config.bot.skip_deleting_faved_at_least
        and favourites >= config.bot.skip_deleting_faved_at_least
    ):
        return True

    reblogs = toot.get("reblogs_count", 0)
    if (
        config.bot.skip_deleting_boost_at_least
        and reblogs >= config.bot.skip_deleting_boost_at_least
    ):
        return True

    return False


@click.command()
@click.option(
    "-c",
    "--config-file",
    help="Name of configuration file to use",
    default="config.json",
    type=click.Path(
        exists=True,
    ),
)
@click.option(
    "-d",
    "--dry-run",
    help="Only print out which toots would be deleted. No actual deletion occurs",
    is_flag=True,
)
@click.option(
    "--debug-log-file",
    help="Path of filename to save DEBUG log messages to",
    type=click.Path(
        writable=True,
    ),
)
@click.option(
    "-a",
    "--audit-log-file",
    help="Path of filename to save audit log to",
    type=click.Path(
        writable=True,
    ),
)
@click.option(
    "--audit-log-style",
    help="Style to use for audit log entries",
    type=click.Choice([style.name for style in AuditLog.Style]),
    default=AuditLog.Style.PLAIN.name,
)
@click.option(
    "-b",
    "--batch-size",
    help="How many deletes to process in one batch",
    type=click.INT,
)
@click.option(
    "-l",
    "--limit",
    help="Maximum number of of deletes to process",
    type=click.INT,
)
def start(
    config_file: str,
    dry_run: bool,
    debug_log_file: Optional[str],
    audit_log_file: Optional[str],
    audit_log_style: Optional[str],
    batch_size: Optional[int],
    limit: Optional[int],
) -> None:
    """Main entry point for app."""

    # pylint: disable=too-many-arguments

    asyncio.run(
        main(
            config_file=config_file,
            is_dry_run=dry_run,
            debug_log_file=debug_log_file,
            audit_log_file=audit_log_file,
            audit_log_style=audit_log_style,
            batch_size=batch_size,
            limit=limit,
        )
    )

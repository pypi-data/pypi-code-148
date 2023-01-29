import logging
import time

from datetime import datetime

from case_insensitive_dict import CaseInsensitiveDict

# from door.utils.collections import CaseInsensitiveDict

from sentry_sdk import init, start_span, serializer, utils
from sentry_sdk.integrations.atexit import AtexitIntegration
from sentry_sdk.integrations.dedupe import DedupeIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger
from sentry_sdk.integrations.threading import ThreadingIntegration
from sentry_sdk.tracing import Span

# Sentry uses urllib3; don't want to see those log messages
logging.getLogger("urllib3").setLevel(logging.WARNING)


def configure_sentry(settings: CaseInsensitiveDict | None = None) -> str | None:
    """Configure https://sentry.io for performance metrics and error tracking"""

    # only initialize Sentry logging if the Data Source Name (DSN) is provided
    if not settings or not (dsn := settings.get("SENTRY_DSN")):
        return None

    # Removes ModulesIntegration, StdlibIntegration and ArgvIntegration from the normal defaults
    # The default LoggingIntegration levels are INFO for breadcrumbs and ERROR for events
    integrations = [
        (LoggingIntegration, (), {"level": logging.DEBUG, "event_level": logging.WARNING}),
        (ExcepthookIntegration, (), {}),
        (DedupeIntegration, (), {}),
        (AtexitIntegration, (), {}),
        (ThreadingIntegration, (), {}),
    ]

    serializer.MAX_DATABAG_DEPTH = 7  # defaults to 5 stack frames
    serializer.MAX_DATABAG_BREADTH = 25  # defaults to 10 variables per frame
    utils.MAX_STRING_LENGTH = 2048  # defaults to 1024

    rv = init(
        dsn=dsn,
        max_breadcrumbs=settings.get("SENTRY_MAX_BREADCRUMBS", 10),
        environment=settings.get("SENTRY_ENVIRONMENT"),  # defaults to "production" if not set
        traces_sample_rate=settings.get("SENTRY_TRACES_SAMPLE_RATE", 1.0),
        default_integrations=False,
        integrations=[integration(*args, **kwargs) for integration, args, kwargs in integrations],
    )
    # other things that can be passed to 'init': release, server_name, shutdown_timeout, dist,
    # send_default_pii, http_proxy, https_proxy, ignore_errors, before_send, before_breadcrumb,
    # debug, attach_stacktrace, ca_certs, propagate_traces... (see consts.py in the SDK for more)

    # aiorun logs a critical "Stopping the loop" message whenever you exit,
    # which generates a Sentry issue, so ignore it
    ignore_logger("aiorun")

    # return the project number at the end of the Sentry DSN URL
    return dsn.rsplit("/", 1)[-1] if rv else None


def adjust_start(ts: str | int | float, transaction: Span) -> None:
    """Adjust the start time of a transaction to an earlier timestamp, and classify
    it in a "Slack Latency" span"""

    try:
        # Slack now sends bogus timestamps for `link_shared` events, like this:
        # Uxxxxxxx-909b5454-75f8-4ac4-b325-1b40e230bbd8-gryl3kb80b3wm49ihzoo35fyqoq08n2y
        if isinstance(ts, str):
            ts = float(ts)
    except ValueError:
        return

    # The Sentry SDK doesn't use offset-aware datetimes, so can't use
    # datetime.fromtimestamp(ts, pytz.utc), so need to suppress DTZ004
    transaction.start_timestamp = datetime.utcfromtimestamp(ts)  # noqa: DTZ004
    # since the monotonic timer starts at 0 when the app starts, deal with older events
    transaction._start_timestamp_monotonic = max(time.perf_counter() - (time.time() - ts), 0)

    with start_span(op="slack_event_ts_latency") as span:
        span.start_timestamp = transaction.start_timestamp
        span._start_timestamp_monotonic = transaction._start_timestamp_monotonic


# available "set_status" values
# (Sentry considers anything other than "ok", "cancelled" and "unknown" a "failure")
# see "status" in https://develop.sentry.dev/sdk/event-payloads/transaction/
# "ok", "cancelled", "unknown", "invalid_argument", "deadline_exceeded", "not_found",
# "already_exists", "permission_denied", "resource_exhausted", "failed_precondition",
# "aborted", "out_of_range", "unimplemented", "internal_error", "unavailable",
# "data_loss", "unauthenticated"

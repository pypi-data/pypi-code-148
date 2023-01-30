import logging

import pytest
from _pytest.reports import BaseReport

logger = logging.getLogger("pytest_result_log")

__test_set = set()


def pytest_cmdline_parse():
    global __test_set

    __test_set = set()


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_report_teststatus(report: BaseReport):
    outcome = yield
    result = outcome.get_result()

    if report.nodeid in __test_set:
        return

    if report.when == "setup":
        match result[1]:
            case "s":
                reason, reason_details = get_reason(report, "s")
                logger.info(f"test status is {result[2]} ({report.nodeid}): {reason}")
                logger.debug(f"{report.nodeid}: {reason_details}")
                __test_set.add(report.nodeid)
            case "E":
                reason, reason_details = get_reason(report, "E")
                logger.error(f"test status is {result[2]} ({report.nodeid}): {reason}")
                logger.debug(f"{report.nodeid}: {reason_details}")
                __test_set.add(report.nodeid)

    if report.when == "call":

        match result[1]:
            case ".":
                logger.info(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)

            case _:
                if result[1] in ["F", "x"]:
                    reason, reason_details = get_reason(report)
                    logger.warning(
                        f"test status is {result[2]} ({report.nodeid}): {reason}"
                    )
                    logger.debug(f"{report.nodeid}: {reason_details}")
                else:  # XPASS do not have reason
                    logger.warning(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)


def get_reason(report: BaseReport, result="F"):
    reason = "unknown"

    match result:
        case "F":
            try:
                reason = report.longrepr.reprtraceback.reprentries[
                    -1
                ].reprfileloc.message
            except Exception:
                ...
        case "E":
            try:
                reason = report.longrepr.errorstring.split("\n")[0]
            except Exception:
                ...
        case "s":
            try:
                reason = report.longrepr[2]
            except Exception:
                ...

    return reason, report.longreprtext

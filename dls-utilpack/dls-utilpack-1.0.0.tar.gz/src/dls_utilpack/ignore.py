from dls_logformatter.functions import format_exception_causes

# Marker string in the message containing a cause chain.
EXCEPTION_CAUSE_CHAIN_MARKER = "ignoring exception"
EXCEPTION_CAUSE_CHAIN_PREFIX = "... "


# -------------------------------------------------------------------------------------
def ignore(logger, exception, doing):
    ignore_flat_trace(logger, exception, doing)


# -------------------------------------------------------------------------------------
def ignore_full_trace(logger, exception, doing):
    logger.warning(
        f"{EXCEPTION_CAUSE_CHAIN_MARKER} while {doing}",
        exc_info=exception,
    )


# -----------------------------------------------------------------------------------
def ignore_flat_trace(logger, exception, doing):
    join_string = f"{EXCEPTION_CAUSE_CHAIN_PREFIX}"
    formatted_exception_causes = format_exception_causes(
        exception, join_string=join_string
    )
    logger.warning(
        f"{EXCEPTION_CAUSE_CHAIN_MARKER} while {doing}{join_string}"
        f"{formatted_exception_causes}"
    )

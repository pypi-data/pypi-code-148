from dls_logformatter.functions import format_exception_causes, list_exception_causes

# Marker string in the message containing a cause chain.
EXCEPTION_CAUSE_CHAIN_MARKER = "exception cause chain"
EXCEPTION_CAUSE_CHAIN_PREFIX = "-- "


# ----------------------------------------------------------------------------------------
def explain(exception, doing):
    return f"{type(exception).__name__} while {doing}"


# ----------------------------------------------------------------------------------------
def explain2(exception, doing):
    formatted_exception_causes = format_exception_causes(exception)
    return f"exception while {doing}... {formatted_exception_causes}"


# ----------------------------------------------------------------------------------------
def explain_cause_chain(exception, doing):
    join_string = f"\n{EXCEPTION_CAUSE_CHAIN_PREFIX}"
    formatted_exception_causes = format_exception_causes(
        exception, join_string=join_string
    )
    return (
        f"{EXCEPTION_CAUSE_CHAIN_MARKER}{join_string}exception"
        f" while {doing}{join_string}{formatted_exception_causes}"
    )


# ----------------------------------------------------------------------------------------
def explain_cause_chain_error_lines(exception, doing):
    formatted_exception_list = list_exception_causes(exception)

    error_lines = [f"exception while {doing}"]
    error_lines.extend(formatted_exception_list)

    return error_lines

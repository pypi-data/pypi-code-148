from typing import Literal


class Statuses:
    add = "ADD"
    queue = "QUEUE"
    run = "RUN"
    success = "SUCCESS"
    error = "ERROR"
    fatal_error = "CRITICAL"

    default = add
    all_statuses = (add, queue, run, success, error, fatal_error)
    error_statuses = (error, fatal_error)
    run_statuses = (run, queue)
    for_executed = (add, queue)

    LiteralT = Literal[add, queue, run, success, error, fatal_error]


class Error:
    expired = "ExpiredError"


class Operators:
    equal = "="
    not_equal = "!="
    less = "<"
    more = ">"
    more_or_equal = ">="
    less_or_equal = "<="

    like = "like"
    not_like = "not like"
    ilike = "ilike"
    not_ilike = "not ilike"
    in_ = "in"
    not_in = "not in"
    contains = "contains"
    not_contains = "not contains"

    LiteralT = Literal[
        equal,
        less,
        more,
        not_equal,
        more_or_equal,
        less_or_equal,
        like,
        not_like,
        ilike,
        not_ilike,
        in_,
        not_in,
        contains,
        not_contains,
    ]

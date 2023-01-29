import sys

from lupin_grognard.core.config import (
    SUCCESS,
    FAILED,
    TITLE_FAILED,
    BODY_FAILED,
    MERGE_FAILED,
    COMMIT_TYPE_MUST_HAVE_SCOPE,
)


class ErrorCount:
    title_error = 0
    body_error = 0
    merge_error = 0
    title_scope_error = 0
    title_scope_error_list = []

    def __init__(self):
        pass

    @classmethod
    def increment_title_error(cls):
        cls.title_error += 1

    @classmethod
    def increment_body_error(cls):
        cls.body_error += 1

    @classmethod
    def increment_merge_error(cls):
        cls.merge_error += 1

    @classmethod
    def increment_title_scope_error(cls):
        cls.title_scope_error += 1

    @classmethod
    def error_report(cls):
        if not (cls.title_error + cls.body_error + cls.merge_error):
            print(SUCCESS)
        else:
            print(FAILED)
            print(f"Errors found: {cls.title_error + cls.body_error + cls.merge_error}")
            if cls.title_error > 0:
                print(TITLE_FAILED)
            if cls.body_error > 0:
                print(BODY_FAILED)
            if cls.merge_error > 0:
                print(MERGE_FAILED)
            if cls.title_scope_error > 0:
                print(COMMIT_TYPE_MUST_HAVE_SCOPE)
            if cls.title_scope_error_list:
                for scope_error in cls.title_scope_error_list:
                    print(scope_error)
            sys.exit(1)

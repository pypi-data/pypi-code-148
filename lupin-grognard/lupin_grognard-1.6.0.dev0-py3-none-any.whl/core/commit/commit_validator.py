import re

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_reporter import CommitReporter
from lupin_grognard.core.commit.commit_error import ErrorCount
from lupin_grognard.core.config import (
    INITIAL_COMMIT,
    EMOJI_CHECK,
    EMOJI_CROSS,
    PATTERN,
    COMMIT_TYPES,
    COMMIT_SCOPES,
    COMMIT_TYPE_MUST_NOT_HAVE_SCOPE,
)


class CommitValidator(Commit):
    def __init__(self, commit: str):
        super().__init__(commit=commit)
        self.reporter = CommitReporter(commit)
        self.error_count = ErrorCount

    def validate_commit_title(self) -> bool:
        if self._validate_commit_message(self.title, validate_scope=True):
            self.reporter.display_title_report(EMOJI_CHECK)
            return True
        self.reporter.display_title_report(EMOJI_CROSS)
        return False

    def validate_commit_body(self) -> bool:
        if self.body:
            message_error = []
            for message in self.body:
                if self._validate_commit_message(message):
                    message_error.append(message)
            if len(message_error) > 0:
                self.reporter.display_body_report(message_error)
                return False  # must not start with a conventional message
        return True

    def validate_commit_merge(self) -> bool:
        self.reporter.display_merge_report(approvers=self.approvers)
        if len(self.approvers) < 1:
            return False
        return True

    def _validate_commit_message(
        self, commit_msg: str, pattern: str = PATTERN, validate_scope: bool = False
    ):
        """By default, the function validates a commit message against the conventional commits format.
        With the validate_scope flag set to True, it will also validate the scope for the 'feat' type.
        The scope must be one of the following: add, change, remove"""
        if (
            commit_msg.startswith("Merge")
            or commit_msg.startswith("Revert")
            or commit_msg.startswith("fixup!")
            or commit_msg.startswith("squash!")
            or commit_msg in INITIAL_COMMIT
        ):
            return True
        match = re.match(pattern, commit_msg)
        validated_message = bool(match)
        # only validates add/change/remove scopes for only feat type
        if validate_scope:
            if match:
                group1, group2, *_ = match.groups()
                if group1 in COMMIT_TYPES:
                    if group2 is None or group2 not in COMMIT_SCOPES:
                        self.error_count.increment_title_scope_error()
                        validated_message = False
                    else:
                        validated_message = True
                elif group1 not in COMMIT_TYPES:
                    if group2 is None:
                        validated_message = True
                    else:
                        self.error_count.title_scope_error_list.append(
                            COMMIT_TYPE_MUST_NOT_HAVE_SCOPE.format(
                                group1, (group1 + ":")
                            )
                        )
                        validated_message = False
        return validated_message

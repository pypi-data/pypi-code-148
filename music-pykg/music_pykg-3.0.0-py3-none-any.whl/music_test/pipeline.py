from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .runs import TestRunException
from .term import (
    TERMCOLOR_BLUE,
    TERMCOLOR_DEFAULT,
    TERMCOLOR_GREEN,
    TERMCOLOR_RED,
    TERMCOLOR_YELLOW,
    Chars,
    CharsBase,
    CharsWithAsciiAlternate,
    Message,
    NullMsg,
    StrMsg,
    TermBase,
    err_msg,
    warn_msg,
)
from .test import ConcreteTest
from .utils import Timer

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Dict, Optional, Sequence

    from .cmake_builder import BuildOutcome
    from .dirs import TestsOutputDirectory


@dataclass(frozen=True, eq=True)
class Outcome:
    label: str
    symbol: str
    ascii_symbol: str
    termcolor: str
    stops_pipeline: bool
    changed: bool
    is_failure: bool

    @property
    def char(self) -> CharsWithAsciiAlternate:
        return CharsWithAsciiAlternate(
            self.symbol,
            self.ascii_symbol,
            self.termcolor,
        )


PASS = Outcome(
    label="Passed",
    symbol="✔",
    ascii_symbol=".",
    termcolor=TERMCOLOR_GREEN,
    stops_pipeline=False,
    changed=True,
    is_failure=False,
)

REUSE = Outcome(
    label="Reused",
    symbol="♻",
    ascii_symbol="o",
    termcolor=TERMCOLOR_BLUE,
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

FAIL = Outcome(
    label="Failed",
    symbol="✗",
    ascii_symbol="!",
    termcolor=TERMCOLOR_RED,
    stops_pipeline=True,
    changed=True,
    is_failure=True,
)

SKIP = Outcome(
    label="Skipped",
    symbol="⮞",
    ascii_symbol=">",
    termcolor=TERMCOLOR_YELLOW,
    stops_pipeline=True,
    changed=False,
    is_failure=False,
)

NA = Outcome(
    label="N/A",
    symbol="-",
    ascii_symbol="-",
    termcolor=TERMCOLOR_DEFAULT,
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

ALL_OUTCOMES = [PASS, REUSE, FAIL, SKIP, NA]


class TestsTally:
    def __init__(self, tests: Sequence[ConcreteTest], stages: Sequence[str]):
        self.tests = tests
        self.stages = stages

        self._outcomes: Dict[ConcreteTest, Dict[str, Outcome]] = {
            t: {} for t in tests
        }  # outcome[test][stage]

    def register(self, test: ConcreteTest, stage: str, outcome: Outcome) -> None:
        assert stage in self.stages
        assert stage not in self._outcomes[test]
        self._outcomes[test][stage] = outcome

    def _finalize_matrix(self) -> None:
        for test in self.tests:
            for i, stage in enumerate(self.stages):
                if stage not in self._outcomes[test]:
                    assert i > 0
                    prev_outcome = self._outcomes[test][self.stages[i - 1]]
                    assert prev_outcome.stops_pipeline
                    self._outcomes[test][stage] = SKIP

    def print_report_to(self, term: TermBase, print_key: bool = True) -> None:
        self._finalize_matrix()
        cols: Sequence[CharsBase] = [Chars(f"{' ':40}")] + [
            Chars(f"{stage:^13s}") for stage in self.stages
        ]
        term.print_line_of_chars(cols)
        sym_pad = Chars((13 - 1) // 2 * " ")
        for test in self.tests:
            cols = [Chars(f"{test.name:40}")]
            for stage in self.stages:
                cols += [sym_pad, self._outcomes[test][stage].char, sym_pad]
            term.print_line_of_chars(cols)

        if print_key:
            term.print_line("\nKey:")
            for outcome in ALL_OUTCOMES:
                term.print_line_of_chars(
                    [outcome.char, Chars(f" : {outcome.label}")], indent=1
                )

    def count_failures(self) -> int:
        """Count number of tests that have at least one failure in their pipeline"""
        self._finalize_matrix()
        return sum(
            any(self._outcomes[test][stage].is_failure for stage in self.stages)
            for test in self.tests
        )

    @property
    def num_tests(self) -> int:
        return len(self.tests)


@dataclass(frozen=True)
class StageResult:
    outcome: Outcome
    message: Message = NullMsg()
    timing: Optional[float] = None

    @property
    def stops_pipeline(self) -> bool:
        return self.outcome.stops_pipeline

    @property
    def is_failure(self) -> bool:
        return self.outcome.is_failure

    @property
    def changed(self) -> bool:
        return self.outcome.changed

    def log_to(self, term: TermBase, header: str, indent: int = 0) -> None:
        timer_str = f" [{self.timing:.2f} s]" if self.timing is not None else ""
        StrMsg(
            f"{self.outcome.label}{timer_str}: {header}",
            termcolor=self.outcome.termcolor,
        ).print_to(term, indent)
        self.message.print_to(term, indent + 1)


class PipelineBase(ABC):
    @abstractmethod
    def process(self, tests: Sequence[ConcreteTest], term: TermBase) -> TestsTally:
        """Run a sequence of tests."""


@dataclass(frozen=True)
class PipelineByTest(PipelineBase):
    stages: Sequence[PipelineStage]

    def process(self, tests: Sequence[ConcreteTest], term: TermBase) -> TestsTally:
        tally = TestsTally(tests, [stage.describe() for stage in self.stages])
        # Loop over tests
        for test in tests:
            StrMsg(f"Test={test.name}").print_to(term, 1)

            # Loop over stages for this test
            force_downstream_update = False
            for stage in self.stages:
                result = stage.execute(test, force_downstream_update)
                force_downstream_update = result.changed
                tally.register(test, stage.describe(), result.outcome)
                result.log_to(term, f"{stage.describe()}({test.name})", indent=2)
                if result.stops_pipeline:
                    break  # Break from pipeline stage loop

        return tally


@dataclass(frozen=True)
class PipelineByStage(PipelineBase):
    stages: Sequence[PipelineStage]

    def process(self, tests: Sequence[ConcreteTest], term: TermBase) -> TestsTally:
        tally = TestsTally(tests, [stage.describe() for stage in self.stages])

        force_downstream_update = {test: False for test in tests}
        pipeline_stopped = {test: False for test in tests}

        # Loop over stages
        for stage in self.stages:
            StrMsg(f"Stage={stage.describe()}").print_to(term, 1)

            # Loop over tests
            for test in tests:
                if pipeline_stopped[test]:
                    continue

                result = stage.execute(test, force_downstream_update[test])
                force_downstream_update[test] = result.changed
                tally.register(test, stage.describe(), result.outcome)
                result.log_to(term, f"{stage.describe()}({test.name})", indent=2)
                pipeline_stopped[test] = result.stops_pipeline

        return tally


class PipelineStage(ABC):
    @abstractmethod
    def describe(self) -> str:
        """Short description of the stage."""

    @abstractmethod
    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        raise NotImplementedError


@dataclass(frozen=True)
class BuildCheckStage(PipelineStage):
    build_outcome: BuildOutcome
    tests_out_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Build-check"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if not self.build_outcome.built_targets.includes(test.build_targets):
            return StageResult(FAIL)

        bdir = self.tests_out_dir.builds_directory
        run_path = self.tests_out_dir.run_path(test)
        if all(
            (
                (local_link := run_path / tgt.name).exists()
                and bdir.target_path(tgt).samefile(local_link)
            )
            for tgt in test.build_targets
        ):
            return StageResult(REUSE)

        return StageResult(PASS)


@dataclass(frozen=True)
class RunStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory
    reuse_if_ready: bool
    verbose: bool

    def describe(self) -> str:
        return "Run"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        run_dir = self.tests_out_dir.test_run_directory(test)
        attempt_reuse = (not force_exec) and self.reuse_if_ready

        if attempt_reuse and run_dir.is_ready():
            return StageResult(REUSE)

        try:
            timer = Timer()
            run_dir.run(verbose=self.verbose)
            return StageResult(PASS, timing=timer.time())

        except TestRunException as err:
            return StageResult(FAIL, message=err_msg(str(err)))


@dataclass(frozen=True)
class SelfCheckStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Self-check"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if test.self_check is None:
            return StageResult(NA)

        timer = Timer()
        run_dir = self.tests_out_dir.test_run_directory(test)
        result = test.self_check.check_run(run_dir.path)
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())


@dataclass(frozen=True)
class CompareStage(PipelineStage):
    music_dir: Path
    tests_out_dir: TestsOutputDirectory
    ref_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Comparison"

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        if test.comparison_check is None:  # Test prescribes no comparison
            return StageResult(NA)

        ref_run_dir = self.ref_dir.test_run_directory(test)
        if not ref_run_dir.is_ready():  # No matching run in ref output dir
            return StageResult(
                SKIP,
                message=warn_msg(
                    f"reference run directory '{ref_run_dir.path}' not found"
                ),
            )

        timer = Timer()
        run_dir = self.tests_out_dir.test_run_directory(test)
        result = test.comparison_check.compare_run_to_ref(
            self.music_dir, run_dir.path, ref_run_dir.path
        )
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())


@dataclass(frozen=True)
class FakeStage(PipelineStage):
    name: str
    result: StageResult

    def describe(self) -> str:
        return self.name

    def execute(self, test: ConcreteTest, force_exec: bool) -> StageResult:
        return self.result

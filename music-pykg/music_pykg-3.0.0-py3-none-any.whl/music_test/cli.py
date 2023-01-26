#!/usr/bin/env python3

import argparse
from argparse import Namespace
from pathlib import Path

from .cmake_builder import CmakeBuilder, NoCacheFoundError
from .dirs import TestsOutputDirectory
from .pipeline import (
    SKIP,
    BuildCheckStage,
    CompareStage,
    FakeStage,
    PipelineByStage,
    PipelineByTest,
    PipelineStage,
    RunStage,
    SelfCheckStage,
    StageResult,
)
from .repo import (
    TestRepository,
    TestRepositoryBase,
    TestsMatchingPatterns,
    TestsWithAllTags,
    TestsWithAnyTag,
)
from .runs import MusicRun
from .source_tree import GitRepository, MusicSourceTree, NoOpRepository, Repository
from .term import (
    TERMCOLOR_GREEN,
    LogFile,
    Message,
    StrMsg,
    TeeTerm,
    Term,
    TermBase,
    err_msg,
    info_msg,
    warn_msg,
)
from .utils import Timer


def parse_cmdline_args() -> Namespace:
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        description="""Automate compilation, execution and validation of MUSIC tests problems.
        Without arguments, processes all available tests in the tests repository.
        Specific test names or shell-like glob patterns may also be passed as positional arguments,
        see TEST_NAME.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    group = parser.add_argument_group("Test selection options")
    group.add_argument(
        "tests",
        metavar="TEST_NAME",
        nargs="*",
        help=(
            "Individual test name to run, see `--list` for a list of tests. "
            "Supports shell-like glob patters, e.g. '2dim/vortex*'. "
            "If not specified, defaults to all available tests."
        ),
    )
    group.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List tests for current selection and exit",
    )
    tag_group = group.add_mutually_exclusive_group()
    tag_group.add_argument(
        "-t",
        "--tags-all",
        metavar="TAG",
        nargs="+",
        help=(
            "Restrict selection to tests with ALL of these tags; use '~tag' to negate tag."
            " See `--list` for tests and their tags."
        ),
    )
    tag_group.add_argument(
        "-T",
        "--tags-any",
        metavar="TAG",
        nargs="+",
        help="Restrict selection to tests with ANY of these tags.",
    )

    group = parser.add_argument_group("Base directory options")
    group.add_argument(
        "-o",
        "--output",
        metavar="TESTS_OUTPUT_DIR",
        default=Path("tests_out"),
        type=Path,
        help="Path to the tests output base directory",
    )
    group.add_argument(
        "--repo",
        metavar="TESTS_REPO_DIR",
        default=Path("tests"),
        type=Path,
        help="Path to the tests repository",
    )
    group.add_argument(
        "--music",
        metavar="MUSIC_SOURCE_DIR",
        default=Path(),
        type=Path,
        help="Path to the MUSIC source tree",
    )
    group.add_argument(
        "-c",
        "--cache-from",
        metavar="CMAKE_BUILD_DIR",
        type=Path,
        help="Path to the CMake build directory whose cache should be reused",
    )

    group = parser.add_argument_group("Validation options")
    group.add_argument(
        "-r",
        "--ref",
        metavar="REF_TESTS_OUTPUT_DIR",
        default=Path("tests_out.ref"),
        type=Path,
        help="Tests output directory to use for comparison, if exists",
    )

    group = parser.add_argument_group("Behaviour control")
    group.add_argument(
        "-k",
        "--keep",
        action="store_true",
        help="Do not delete tests output base directory before running",
    )
    group.add_argument(
        "-b",
        "--build-only",
        action="store_true",
        help="Only build; don't consider the test pipeline itself.",
    )
    group.add_argument(
        "-s",
        "--by-stage",
        action="store_true",
        help=(
            "Group by stage: perform all runs first, then all checks, etc. "
            "By default, processing is done test by test."
        ),
    )

    group = parser.add_argument_group("Runtime environment options")
    group.add_argument(
        "--no-git",
        action="store_true",
        help="Disable calls to git; don't store VCS information in the test directory",
    )
    group.add_argument(
        "--with-music-self-tests",
        action="store_true",
        help="Run MUSIC self tests on top of regular tests (time consuming!)",
    )

    group = parser.add_argument_group("Logging and display control")
    group.add_argument(
        "-w",
        "--write-log",
        metavar="LOG_FILE",
        type=Path,
        help="Also write test system output to the given file; obeys `--ascii` flag",
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show output of code execution on standard output",
    )
    group.add_argument(
        "-C",
        "--no-color",
        action="store_true",
        help="Disable colored output on terminal",
    )
    group.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="Only use ASCII characters in test system outputs",
    )

    return parser.parse_args()


def main() -> int:

    options = parse_cmdline_args()

    term: TermBase = Term(has_color=not options.no_color, has_unicode=not options.ascii)
    if options.write_log is not None:
        term = TeeTerm(
            [term, LogFile(options.write_log, has_unicode=not options.ascii)]
        )

    music_path = options.music

    if not options.no_git:
        vcs_repo: Repository = GitRepository(music_path)
    else:
        vcs_repo = NoOpRepository()

    if options.with_music_self_tests:
        MusicRun.skip_self_tests_dflt = False

    music_tree = MusicSourceTree(music_path, vcs_repo)

    # Check that --output is not a parent of --repo or --music,
    # or we may run into trouble.
    output_path = options.output.resolve()
    for path in [options.repo, music_path]:
        if output_path in path.resolve().parents:
            raise ValueError(
                f"output directory '{options.output}' is a parent path of '{path}'"
            )

    # Prepare the output directory
    tests_out_dir = TestsOutputDirectory(music_tree, options.output)
    info_msg(f"using TestsOutputDirectory '{tests_out_dir.path}'").print_to(term, 0)

    builder = CmakeBuilder(
        music_dir=music_path,
        outdir=tests_out_dir,
        requested_cache=options.cache_from,
    )

    repo: TestRepositoryBase = TestRepository(options.repo, builder)
    info_msg(f"using TestRepoDirectory '{repo.path}'").print_to(term, 0)

    run_all_tests = True

    # Setup test repository and filters
    if options.tests:
        run_all_tests = False
        repo = TestsMatchingPatterns(repo, options.tests)

    if options.tags_any:
        run_all_tests = False
        repo = TestsWithAnyTag(repo, options.tags_any)

    if options.tags_all:
        run_all_tests = False
        repo = TestsWithAllTags(repo, options.tags_all)

    if options.list:
        if run_all_tests:
            term.print_line("Selected tests (all):\n")
        else:
            term.print_line("Selected tests:\n")
        repo.print_tests()
        return 0

    # From now on, we're committed to run and may change things to disk

    timer = Timer()

    tests_out_dir.prepare(wipe=not options.keep)

    # Build necessary binaries
    try:
        build_outcome = builder.build_targets(repo.targets(), output_to=term, indent=1)
    except NoCacheFoundError:
        err_msg(
            "Could not find any existing build tree, please create one",
            "and/or indicate its path with `-c|--cache-from`.",
        ).print_to(term, 1)
        return 1
    except Exception:
        err_msg("Build of test presets failed.", "The encountered error was:").print_to(
            term, 1
        )
        raise
    if build_outcome.all_successful:
        build_msg: Message = StrMsg(
            f"Built all necessary presets in {timer.time_str()}.",
            termcolor=TERMCOLOR_GREEN,
        )
    else:
        build_msg = warn_msg(
            f"Some builds failed, build phase took {timer.time_str()}."
        )
    build_msg.print_to(term, 1)

    if options.build_only:
        return 0 if build_outcome.all_successful else 1

    def make_comparison_stage() -> PipelineStage:
        """Build an appropriate PipelineStage object for the comparison stage"""
        # Reference repository and comparison
        out_path = options.output
        ref_path = options.ref

        if ref_path.is_dir() and ref_path.resolve() != out_path.resolve():
            # Reference directory was specified, and is different from output directory
            ref_dir = TestsOutputDirectory(music_tree, ref_path)
            info_msg(f"using ReferenceOutputDirectory '{options.ref}'").print_to(
                term, 0
            )
            return CompareStage(music_tree.path, tests_out_dir, ref_dir)

        # Reference directory not specified: skip all comparisons
        warn_msg(
            f"ReferenceOutputDirectory '{options.ref}' not found, comparisons disabled"
        ).print_to(term, 0)
        return FakeStage(name="Comparison", result=StageResult(SKIP))

    # Assemble pipeline
    stages = [
        BuildCheckStage(
            build_outcome,
            tests_out_dir,
        ),
        RunStage(
            tests_out_dir,
            reuse_if_ready=options.keep,
            verbose=options.verbose,
        ),
        SelfCheckStage(
            tests_out_dir,
        ),
        make_comparison_stage(),
    ]

    pipeline = PipelineByStage(stages) if options.by_stage else PipelineByTest(stages)

    timer.reset()

    # Run the pipeline
    tally = pipeline.process(repo.tests(), term)

    # Report results
    term.print_line("")
    tally.print_report_to(term)
    term.print_line("")

    num_failures = tally.count_failures()
    msg = info_msg if num_failures == 0 else err_msg
    msg(
        f"Processed {tally.num_tests} test(s) in {timer.time_str()}, "
        f"{num_failures} failure(s)"
    ).print_to(term, 0)

    term.close()

    if num_failures > 0:
        return 1

    return 0

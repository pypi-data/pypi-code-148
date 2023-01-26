from __future__ import annotations

import shutil
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from .source_tree import MusicSourceTree
from .test import ConcreteTest

if typing.TYPE_CHECKING:
    from .cmake_builder import Target


@dataclass(frozen=True)
class TestRunDirectory:
    test: ConcreteTest
    path: Path
    builds_dir: BuildsDirectory

    @property
    def _run_tag_path(self) -> Path:
        return self.path / "run_successful.tag"

    def is_ready(self) -> bool:
        return self._run_tag_path.is_file()

    def run(self, verbose: bool = False) -> None:
        # Start with fresh run directory
        shutil.rmtree(self.path, ignore_errors=True)
        self.path.mkdir(parents=True)

        # Setup files required for run, coming from
        # ... the build
        for tgt in self.test.build_targets:
            # hardlink here enables BuildCheckStage to verify
            # whether the build artefacts changed
            self.builds_dir.target_path(tgt).link_to(self.path / tgt.name)
        # ... the test problem
        self.test.setup_dir_for_run(self.path)

        # Run the test
        self.test.run_in_dir(self.path, verbose=verbose)

        # Touch the run successful flag
        self._run_tag_path.touch()


@dataclass(frozen=True)
class BuildsDirectory:
    path: Path

    def preset_path(self, preset: str) -> Path:
        return self.path / preset

    def target_path(self, target: Target) -> Path:
        return self.preset_path(target.preset) / target.name


@dataclass(frozen=True)
class TestsOutputDirectory:
    music_tree: MusicSourceTree
    path: Path

    def prepare(self, wipe: bool = True) -> None:
        if wipe and self.path.is_dir():
            shutil.rmtree(self.path)
        self.builds_directory.path.mkdir(parents=True, exist_ok=True)

        # Capture VCS revision and diff
        self.music_tree.store_vcs_info(
            vcs_head_fname=self.path / "git_head.log",
            vcs_diff_fname=self.path / "git_diff.log",
        )

    @cached_property
    def builds_directory(self) -> BuildsDirectory:
        """Location of builds with given preset."""
        return BuildsDirectory(self.path / "builds")

    def run_path(self, test: ConcreteTest) -> Path:
        """Location of the run for a given path."""
        return self.path / "runs" / test.name

    def test_run_directory(self, test: ConcreteTest) -> TestRunDirectory:
        return TestRunDirectory(
            test=test,
            path=self.run_path(test),
            builds_dir=self.builds_directory,
        )

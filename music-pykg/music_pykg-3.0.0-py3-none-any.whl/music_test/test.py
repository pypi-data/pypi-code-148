from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional, Tuple, Union

    from .cmake_builder import Target, TargetCollection
    from .comparison_checks import ComparisonCheck
    from .runs import Run
    from .self_checks import SelfCheck


@dataclass(frozen=True)
class Test:
    """A test to run"""

    build_targets: Union[Target, TargetCollection]
    run: Run
    self_check: Optional[SelfCheck]
    comparison_check: Optional[ComparisonCheck]
    description: str
    tags: Tuple[str, ...]

    def with_name_and_path(self, name: str, path: Path) -> ConcreteTest:
        return ConcreteTest(
            build_targets=self.build_targets,
            run=self.run,
            self_check=self.self_check,
            comparison_check=self.comparison_check,
            description=self.description,
            tags=self.tags,
            name=name,
            path=path,
        )


@dataclass(frozen=True)
class ConcreteTest(Test):
    name: str
    path: Path

    def setup_dir_for_run(self, dst_path: Path) -> None:
        """Setup given path for this test's run"""
        self.run.setup_run_dir_from_template(self.path, dst_path)

    def run_in_dir(self, path: Path, verbose: bool) -> None:
        self.run.execute(path, verbose=verbose)

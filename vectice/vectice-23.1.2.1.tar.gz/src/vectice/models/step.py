from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.http_error_handlers import VecticeException

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api.json.iteration import IterationStepArtifact
    from vectice.models import Iteration, Phase, Project, Workspace


_logger = logging.getLogger(__name__)


class Step:
    """Model a Vectice step.

    Steps define the logical sequence of steps required to complete
    the phase along with their expected outcomes.
    """

    def __init__(
        self,
        id: int,
        iteration: Iteration,
        name: str,
        index: int,
        description: str | None = None,
        completed: bool = False,
        artifacts: list[IterationStepArtifact] | None = None,
    ):
        """
        Initialize a step.

        Parameters:
            id: The step identifier.
            iteration: The iteration to which the step belongs.
            name: The name of the step.
            index: The index of the step.
            description: The description of the step.
            completed: Whether the step is completed.
            artifacts: The artifacts linked to the steps.
        """
        self._id = id
        self._iteration: Iteration = iteration
        self._name = name
        self._index = index
        self._description = description
        self._client = self._iteration._client
        self._completed = completed
        self._artifacts = artifacts

        if completed:
            _logger.warning(f"The Step {name} is completed!")

    def __repr__(self):
        return f"Step(name='{self.name}', id={self.id}, description='{self._description}', completed={self.completed})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    @property
    def name(self) -> str:
        """The step's name.

        Returns:
            The step's name.
        """
        return self._name

    @property
    def id(self) -> int:
        """The step's id.

        Returns:
            The step's id.
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        """Set the step's id.

        Parameters:
            step_id: The id to set.
        """
        self._id = step_id

    @property
    def index(self) -> int:
        """The step's index.

        Returns:
            The step's index.
        """
        return self._index

    @property
    def properties(self) -> dict:
        """The step's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id` and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def artifacts(self) -> list[IterationStepArtifact] | None:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: list[IterationStepArtifact]):
        self._artifacts = artifacts

    def next_step(self, message: str | None = None) -> Step | None:
        """Advance to the next step.

        Close the current step (mark it completed) and return the next
        step to complete if another open step exists. Otherwise return None.

        Note that steps are not currently ordered, and so the concept
        of "next" is rather arbitrary.

        Parameters:
            message: The message to use when closing the current step.

        Returns:
            The next step.
        """
        try:
            self.close(message)
        except VecticeException:
            _logger.info("The step is closed!")
            return None
        steps_output = self._client.list_steps(self._iteration._phase.id, self._iteration.index)
        open_steps = sorted(
            [
                Step(item.id, self._iteration, item.name, item.index, item.description)
                for item in steps_output
                if not item.completed
            ],
            key=lambda x: x.index,
        )
        if not open_steps:
            _logger.info("There are no active steps.")
            return None
        next_step = open_steps[0]
        _logger.info(f"Next step : {repr(next_step)}")
        return next_step

    def close(self, message: str | None = None):
        """Close the current step, marking it completed.

        Parameters:
            message: The message to use when closing the step.
        """
        self._client.close_step(self.id, message)
        _logger.info(f"'{self.name}' was successfully closed.")
        self._completed = True

    @property
    def connection(self) -> Connection:
        """The connection to which this step belongs.

        Returns:
            The connection to which this step belongs.
        """
        return self._iteration.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this step belongs.

        Returns:
            The workspace to which this step belongs.
        """
        return self._iteration.workspace

    @property
    def project(self) -> Project:
        """The project to which this step belongs.

        Returns:
            The project to which this step belongs.
        """
        return self._iteration.project

    @property
    def phase(self) -> Phase:
        """The phase to which this step belongs.

        Returns:
            The phase to which this step belongs.
        """
        return self._iteration.phase

    @property
    def iteration(self) -> Iteration:
        """The iteration to which this step belongs.

        Returns:
            The iteration to which this step belongs.
        """
        return self._iteration

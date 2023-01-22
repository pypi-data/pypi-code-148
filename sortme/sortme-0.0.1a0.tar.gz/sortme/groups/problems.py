import typing
from dataclasses import dataclass

from sortme.group import Group
import sortme.errors as errors

PREFIX = "/problems"


@dataclass
class Problem:
    id: int
    name: str

    @dataclass
    class Statement:
        legend: typing.Optional[str]
        input: typing.Optional[str]
        output: typing.Optional[str]
        protocol: typing.Optional[str]
        scoring: typing.Optional[str]
        note: typing.Optional[str]

    statement: Statement

    @dataclass
    class Sample:
        stdin: str
        stdout: str

    samples: list[Sample]

    @dataclass
    class Subtask:
        points: int
        depends: list[int]
        description: str

    subtasks: typing.Optional[list[Subtask]]

    @dataclass
    class Limits:
        time: int
        memory: int

    limits: Limits

    category: typing.Optional[int]
    difficulty: typing.Optional[int]
    can_edit: bool


class Statement(typing.TypedDict):
    legend: typing.Optional[str]
    input: typing.Optional[str]
    output: typing.Optional[str]
    protocol: typing.Optional[str]
    scoring: typing.Optional[str]
    note: typing.Optional[str]


class Problems(Group):
    def __init__(self, token, lang):
        super().__init__(token, lang)

    def get_by_id(self, id: int = 0) -> Problem:
        """
        Return general info about user by ID.

        :param id: ID of user. If not provided, get info about current logged-in user.
        """

        if id <= 0:
            raise errors.ParamError("id must be a positive integer")

        return self._make_request("GET", f"{PREFIX}/getByID", {"id": id}, data_class=Problem)

    def create(self) -> int:
        """
        Create new problem and get its ID.
        """
        response = self._make_request("POST", f"{PREFIX}/create", {})

        return response['id']

    def set_statement(self, problem_id: int,
                      name: str,
                      legend: str,
                      input: str,
                      output: str,
                      samples: typing.List[typing.Union[typing.Tuple[str, str], list[Problem.Sample]]],
                      scoring: str = "",
                      note: str = ""):
        """
        Set the problem statement.
        """

        if isinstance(samples[0], tuple) or isinstance(samples[0], list):
            samples = [{"in": s[0], "out": s[1]} for s in samples]

        self._make_request("POST", f"{PREFIX}/setStatement", {}, body={
            "problem_id": problem_id,
            "statement": {
                "name": name,
                "legend": legend,
                "input": input,
                "output": output,
                "scoring": scoring,
                "samples": samples,
                "note": note,
            },
        })

        return

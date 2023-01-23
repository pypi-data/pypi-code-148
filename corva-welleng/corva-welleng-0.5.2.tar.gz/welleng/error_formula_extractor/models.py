from typing import Callable, List, Optional

from pydantic import BaseModel, Field

from welleng.error_formula_extractor.enums import Propagation, VectorType
from welleng.error_formula_extractor.formula_utils import (
    convert_source_code_to_function,
)


class ErrorTerm(BaseModel):
    sequence_no: int
    term_name: str
    formula: List[str]
    error_function: Optional[List[Callable]] = Field(default=None, exclude=True)
    arguments: List[List[str]]
    func_string: List[str]
    magnitude: List[float]
    units: List[str]
    tie_type: List[Propagation]
    vector_type: List[VectorType]

    # class Config:
    #     # TODO: Propagation and VectorType are enums, and we should use their names instead of values
    #     # In addition, since the value of the Vector Type is its dict, we can't use this.
    #     use_enum_values = True

    def __init__(self, **data):
        super().__init__(**data)

        if not self.error_function and self.formula:
            self.error_function = [
                convert_source_code_to_function(formula) for formula in self.formula
            ]

        self.make_function_args_unique()

    def __add__(self, other: "ErrorTerm") -> "ErrorTerm":
        if not isinstance(other, ErrorTerm):
            raise TypeError(f"Cannot concatenate {type(other)} to ErrorTerm")

        if self.term_name != other.term_name:
            raise ValueError(
                f"Cannot concatenate ErrorTerm with different term_name: "
                f"{self.term_name} and {other.term_name}"
            )

        self.formula += other.formula
        self.error_function += other.error_function
        self.magnitude += other.magnitude
        self.units += other.units
        self.tie_type += other.tie_type
        self.vector_type += other.vector_type
        self.arguments += other.arguments
        self.func_string += other.func_string

        self.make_function_args_unique()

        return self

    def make_function_args_unique(self):
        self.arguments = [list(set(args_set)) for args_set in self.arguments]


class SurveyToolErrorModel(BaseModel):
    survey_tool_id: str
    survey_tool_name: str
    sequence_no: int
    error_terms: List[ErrorTerm]
    start_depth: float
    end_depth: float

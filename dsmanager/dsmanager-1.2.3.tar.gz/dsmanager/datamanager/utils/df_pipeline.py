"""@Author: Rayane AMROUCHE

DataFrame Pipeline class.
"""

import json

from typing import Any, List, Generator, Callable, Tuple

import pandas as pd  # type: ignore

from dsmanager.controller.logger import Logger


Logger.update_logger(name="df_pipeline")


class DfPipeline:
    """DataFrame Pipeline class."""

    def __init__(self, steps: List[Tuple[Callable, Any, Any]], env: dict) -> None:
        Logger.update_logger(name="df_pipeline")
        self.env = env
        self.steps = steps

    @staticmethod
    def pipe_step(func: Any, *args, **kwargs) -> Any:
        """Function that prepare a pipe_steps call.

        Args:
            func (Any): Function wrapped for the pipe_steps call.

        Returns:
            Any: Tuple of parameters for a pipe_steps call.
        """
        return func, args, kwargs

    @staticmethod
    def _loop_pipe(
        df_: pd.DataFrame,
        generator: Generator[Tuple[Callable[..., Any], Any, Any], None, None],
        **kwargs
    ) -> pd.DataFrame:
        cur_args = []
        cur_kwargs = {}
        try:
            cur = next(generator)
            if isinstance(cur, tuple):
                cur_func = cur[0]
                cur_args = cur[1]
                cur_kwargs = cur[2]
            else:
                cur_func = cur
        except StopIteration:
            return df_

        if isinstance(cur_func, str):
            cur_func = getattr(DfPipeline._loop_pipe(df_, generator), cur_func)
            cur_func = Logger.log_func("df_pipeline")(cur_func)

            if cur_args:
                return cur_func(*cur_args, **cur_kwargs)
            return cur_func(**cur_kwargs)
        cur_func = Logger.log_func("df_pipeline")(cur_func)
        if cur_args:
            return cur_func(
                DfPipeline._loop_pipe(df_, generator), *cur_args, **cur_kwargs
            )
        return cur_func(DfPipeline._loop_pipe(df_, generator), **cur_kwargs)

    @staticmethod
    def pipe_steps(
        df_: pd.DataFrame, steps: List[Tuple[Callable, Any, Any]], **kwargs
    ) -> pd.DataFrame:
        """Wrap chain function to a DataFrame using a generator to apply multiple
            functions and theirs arguments in chain.

        Args:
            df_ (pd.DataFrame): DataFrame that will be piped.
            steps (List[Tuple[Callable, Any, Any]): List of functions and their
                respective keyword arguments.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        pipeline = DfPipeline(steps, kwargs)
        return pipeline(df_)

    @staticmethod
    def step(func: Any, *args, **kwargs) -> Any:
        """Function that prepare a pipe_steps call.

        Args:
            func (Any): Function wrapped for the pipe_steps call.

        Returns:
            Any: Tuple of parameters for a pipe_steps call.
        """
        return func, args, kwargs

    def add_step(self, func: Any, *args, **kwargs) -> Any:
        """Function that prepare a pipe_steps call.

        Args:
            func (Any): Function wrapped for the pipe_steps call.

        Returns:
            Any: Tuple of parameters for a pipe_steps call.
        """
        return self.steps.append(DfPipeline.step(func, args, kwargs))

    def add_var(self, name: Any, var: Any) -> None:
        """_summary_

        Args:
            name (Any): _description_
            var (Any): _description_
        """
        self.env[name] = var

    def get_var(self, name: Any) -> None:
        """_summary_

        Args:
            name (Any): _description_
            var (Any): _description_

        Returns:
            _type_: _description_
        """
        return self.env[name]

    def __call__(self, df_) -> Any:
        return DfPipeline._loop_pipe(df_, (element for element in reversed(self.steps)))

    def __repr__(self) -> str:
        arg_list = [
            (
                [str(param) for param in step[1]]
                + [f"{k}={v}" for k, v in step[2].items()]
            )
            for step in self.steps
        ]
        steps_repr = {
            i: {
                step[0]
                if isinstance(step[0], str)
                else step[0].__name__: f"({', '.join(arg_list[i])})",
            }
            for i, step in enumerate(self.steps)
        }
        return json.dumps(steps_repr, indent=4)

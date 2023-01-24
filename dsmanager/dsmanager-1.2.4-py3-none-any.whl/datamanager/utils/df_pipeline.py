"""@Author: Rayane AMROUCHE

DataFrame Pipeline class.
"""


from typing import Any, Generator

import pandas as pd  # type: ignore

from dsmanager.controller.logger import Logger


Logger.update_logger(name="df_pipeline")


class DfPipeline:
    """DataFrame Pipeline class."""

    def __init__(self, steps: Any = None, **kwargs) -> None:
        Logger.update_logger(name="df_pipeline")
        self.steps = [] if steps is None else steps
        self.env = kwargs

    def use_vars_as(
        self, env_vars: list, aliases: list, func: Any, *args, **kwargs
    ) -> Any:
        """use vars"""

        def func_wrapper(pipeline):
            def func_wrapped(df_, *args_, **kwargs_):
                kwargs_.update(
                    **{v: pipeline.env[k] for k, v in zip(env_vars, aliases)}
                )
                return func(df_, *args_, **kwargs_)

            return func_wrapped

        tuple_res = (func_wrapper(self), args, kwargs)
        self.steps.append(tuple_res)

    def add_var(self, name: str, value: Any) -> Any:
        """set var"""
        self.env[name] = value

    @staticmethod
    def step(func: Any, *args, **kwargs) -> Any:
        """create step"""
        return func, args, kwargs

    def add_step(self, func: Any, *args, **kwargs) -> None:
        """add step"""
        self.steps.append(DfPipeline.step(func, *args, **kwargs))

    def __call__(self, df_) -> Any:
        return self._loop_pipe(df_, (element for element in reversed(self.steps)))

    def __repr__(self) -> str:
        res = "DfPipeline:\n"
        res += "steps: [\n\t" + ",\n\t".join([str(step) for step in self.steps])
        res += "\n]\n"
        res += "env: " + str(self.env)
        return res

    def _loop_pipe(
        self, df_: pd.DataFrame, generator: Generator[Any, None, None]
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
            cur_func = getattr(self._loop_pipe(df_, generator), cur_func)
            cur_func = Logger.log_func("df_pipeline")(cur_func)
            return cur_func(*cur_args, **cur_kwargs)
        cur_func = Logger.log_func("df_pipeline")(cur_func)
        return cur_func(self._loop_pipe(df_, generator), **cur_kwargs)

    @staticmethod
    def pipe_steps(df_: pd.DataFrame, pipeline: Any) -> pd.DataFrame:
        """Wrap chain function to a DataFrame using a generator to apply multiple
            functions and theirs arguments in chain.

        Args:
            df_ (pd.DataFrame): DataFrame that will be piped.
            pipeline (Any): DfPipeline instance.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return pipeline(df_)

"""@Author: Rayane AMROUCHE

DataFrame Pipeline class.
"""

import collections

from typing import Any, Generator

import pandas as pd  # type: ignore

from dsmanager.controller.logger import Logger


Logger.update_logger(name="df_pipeline")


class DfPipeline:
    """DataFrame Pipeline class."""

    def __init__(self, **kwargs) -> None:
        """Init a pipeline with a list of steps and env vars as kwargs."""
        Logger.update_logger(name="df_pipeline")
        self.steps: collections.OrderedDict = collections.OrderedDict({})
        self.env = kwargs

    def add_vars(self, **kwargs) -> Any:
        """Add a var to the pipeline env.

        Returns:
            Any: Returns the updated pipeline.
        """
        self.env.update(**kwargs)
        return self

    def set_name(self, name: str) -> Any:
        """Change name of a step.

        Args:
            name (str): Name to give to a step.

        Returns:
            Any: Returns the updated pipeline.
        """
        last_step = next(reversed(self.steps))
        old_name = self.steps[last_step].name
        for _ in range(len(self.steps)):
            key_, value_ = self.steps.popitem(False)
            self.steps[name if old_name == key_ else key_] = value_
        self.steps[name].name = name
        return self

    def add_env_kwargs(self, var_aliases: dict) -> Any:
        """Add DfPipeline env variables in kwargs as given names.

        Args:
            var_aliases (dict): Dict with the key being the name of the var in the
                DfPipeline and value the name to put in kwargs.

        Returns:
            Any: Returns the updated pipeline.
        """
        last_step = next(reversed(self.steps))
        func = self.steps[last_step].func

        def enved_func(df_, *args_, **kwargs_):
            kwargs_.update(**{v: self.env[k] for k, v in var_aliases.items()})
            return func(df_, *args_, **kwargs_)

        enved_func.__qualname__ = func.__qualname__
        self.steps[last_step].func = enved_func
        return self

    class Step:
        """Step class."""

        def __init__(
            self,
            __is_leaf: bool,
            __output_name: Any,
            __func: Any,
            *args,
            **kwargs,
        ) -> None:
            """Init a step with a pipeline instance, a func and its args/kwargs.

            Args:
                __is_leaf (bool): Check whether step is a leaf.
                __output_name (Any): Name of the output in env.
                __func (Any): Function of the step.
                __name (Any): Name of the step.
            """
            self.is_leaf = __is_leaf
            self.output_name = __output_name
            self.func = __func
            self.args = args
            self.kwargs = kwargs
            self.name = "default"

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return (self.func, self.args, self.kwargs)

        def __str__(self) -> str:
            func_name = self.func if isinstance(self.func, str) else self.func.__name__
            return f"<{str(self.name)}> [{func_name}]"

    def add_step(self, __func: Any, *args, **kwargs) -> Any:
        """Add a step to a DfPipeline.

        Args:
            func (Any): Step function.

        Returns:
            Any: return the pipeline updated with the new step.
        """
        name = f"step_{len(self.steps)}"
        step = DfPipeline.Step(False, None, __func, *args, **kwargs)
        setattr(step, "name", name)
        self.steps[name] = step
        return self

    def add_leaf(self, __output_name: Any, __func: Any, *args, **kwargs) -> Any:
        """Add a step that does not return a dataframe to a DfPipeline.

        Args:
            func (Any): Step function.

        Returns:
            Any: return the pipeline updated with the new step.
        """
        name = f"step_{len(self.steps)}"
        step = DfPipeline.Step(True, __output_name, __func, *args, **kwargs)
        setattr(step, "name", name)
        self.steps[name] = step
        return self

    def __call__(self, df_) -> Any:
        steps = [v for _, v in self.steps.items()]
        return self._loop_pipe(df_, (element for element in reversed(steps)))

    def __repr__(self) -> str:
        res = "DfPipeline:\n"
        res += "Steps order: [\n\t"
        res += "\n\t-> ".join(str(v) for _, v in self.steps.items())
        res += "\n]\n"
        res += "Env vars: {\n\t"
        res += ",\n\t".join(f"{str(k)}: {str(v)}" for k, v in self.env.items())
        res += "\n}"
        return res

    def _loop_pipe(
        self, df_: pd.DataFrame, generator: Generator[Any, None, None]
    ) -> pd.DataFrame:
        try:
            cur = next(generator)
        except StopIteration:
            return df_

        tmp_func = cur.func
        jump_val = self._loop_pipe(df_, generator)
        if isinstance(tmp_func, str):
            tmp_func = getattr(jump_val, tmp_func)
            tmp_func = Logger.log_func("df_pipeline")(tmp_func)
            res = tmp_func(*cur.args, **cur.kwargs)
        else:
            tmp_func = Logger.log_func("df_pipeline")(tmp_func)
            res = tmp_func(jump_val, *cur.args, **cur.kwargs)
        if cur.is_leaf:
            if cur.output_name:
                self.env[cur.output_name] = res
            return jump_val
        return res

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

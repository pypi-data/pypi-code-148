"""
Approximate a function using OpenAI's API.
"""

import functools
import os
from dataclasses import dataclass
from dataclasses import field
from typing import *

import openai
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_random_exponential

openai.api_key = os.getenv("OPENAI_API_KEY")

create_completion = retry(
    wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6)
)(openai.Completion.create)


@dataclass(frozen=True)
class Arguments:
    """Arguments to a function"""

    args: tuple = field(default_factory=tuple)  # Positional arguments
    kwargs: dict = field(default_factory=dict)  # Keyword arguments

    @classmethod
    def call(cls, *args, **kwargs):
        """Create an Arguments object from a function call"""
        return cls(args=args, kwargs=kwargs)

    def as_code(self) -> str:
        return ", ".join(
            str(x)
            for x in self.args
            + tuple(f"{key}: {value}" for key, value in self.kwargs.items())
        )


@dataclass(frozen=True)
class FunctionExample:
    """Example of a function's behaviour"""

    arguments: Arguments = field(default=Arguments.call())  # Arguments to the function
    output: Any = field(default=None)  # Output of the function


def make_llmfn(
    *,
    examples: list[FunctionExample],  # Examples of the function's behaviour
    function_name: str = "f",  # Name of the function to approximate
    decoder: Callable[[str], Any] = lambda x: x,  # Function to decode the output
    engine: str = "text-davinci-003",  # OpenAI engine to use.
) -> Callable:  # The approximated function
    """Approximate the given function using OpenAI's API"""
    import textwrap

    base_prompt = textwrap.dedent(
        """
        Python 3.10.7 | packaged by conda-forge | (main, Nov 21 2022, 13:22:15) [Clang 14.0.6 ]
        Type 'copyright', 'credits' or 'license' for more information
    """
    ).strip()
    for example in examples:
        base_prompt += f"\n>>> {function_name}({example.arguments.as_code()})"
        base_prompt += f"\n{example.output}"

    @functools.wraps(make_llmfn)
    def approximator(*args, **kwargs) -> Callable:
        """Approximated function"""
        arguments = Arguments(args=args, kwargs=kwargs)
        prompt = base_prompt + f"\n>>> {function_name}({arguments.as_code()})\n"
        response = create_completion(
            engine=engine,
            prompt=prompt,
            max_tokens=4000,
            temperature=0.0,
            top_p=1.0,
            n=1,
            stream=False,
            logprobs=None,
            stop=["\n>>> "],
        )
        return decoder(response.choices[0].text)

    return approximator


def llmfn(
    *,
    examples: list[FunctionExample],  # Examples of the function's behaviour.
    function_name: str = "f",  # Name of the function to approximate
    decoder: Callable[[str], Any] = lambda x: x,  # Function to decode the output
    engine: str = "text-davinci-003",  # OpenAI engine to use.
) -> Callable:
    """Decorator to llmfn a function using OpenAI's API"""

    def decorator(func):
        return functools.wraps(func)(
            make_llmfn(
                examples=examples,
                decoder=decoder,
                function_name=function_name,
                engine=engine,
            )
        )

    return decorator

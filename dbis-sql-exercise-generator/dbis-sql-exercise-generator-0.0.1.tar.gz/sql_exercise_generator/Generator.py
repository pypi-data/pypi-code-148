from __future__ import annotations

from typeguard import typechecked

from excmanager.Task import SubTask
from jinja2 import Environment, FileSystemLoader

from pathlib import Path


@typechecked
def generate_exercise(
    subtask: SubTask,
    description: str,
    expression: str,
    *,
    correct_attributes_score_perc: float = 0.1,
) -> dict[str, str]:
    """
    Generate an exercise for the given subtask.

    Parameters
    ----------
    subtask : SubTask
        The subtask to generate the exercise for.
    description : str
        The description of the exercise.
    expression : str
        The expression to generate the exercise for. It is assumed that the string is a valid SQLite query.
    correct_attributes_score_perc : float, optional
        The percentage of the score that is given for correct attributes, by default 0.1

    Returns
    -------
    dict[str, str]
        A dictionary with the following keys
        - "title.md": The title of the exercise
        - "task.md": The task of the exercise
        - "submission.py": The submission code cell
        - "solution.py": The solution code cell
    """
    # create the data for jinja2
    data = dict()
    # subtask - view https://github.com/rwth-acis/dbis-exercise-manager
    task_num = subtask.task.task
    if "." in task_num:
        task_num = task_num.split(".")[0]
    data["subtask"] = {
        "task": {
            "task": task_num,
        },
        "subtask": subtask.subtask,
        "points": subtask.points,
    }
    # description
    data["description"] = description
    # sql expression
    data["correct_solution"] = expression
    # correct_attributes_score_perc
    data["correct_attributes_score_perc"] = correct_attributes_score_perc

    # load the templates from resources / templates
    abs_path = Path(__file__).parent.resolve() / "resources/templates"
    abs_path = str(abs_path)
    env = Environment(loader=FileSystemLoader(abs_path))
    # render the templates
    # title.md.jinja2
    title_md = env.get_template("title.md.jinja2").render(data)
    # task.md.jinja2
    task_md = env.get_template("task.md.jinja2").render(data)
    # submission.py.jinja2
    submission_py = env.get_template("submission.py.jinja2").render(data)
    # solution.py.jinja2
    solution_py = env.get_template("solution.py.jinja2").render(data)

    # return the rendered templates
    return {
        "title.md": title_md,
        "task.md": task_md,
        "submission.py": submission_py,
        "solution.py": solution_py,
    }

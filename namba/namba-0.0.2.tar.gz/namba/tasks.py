import json
import os
from typing import Dict, Any
from typing import Union
from typing import Optional
import string

import pathlib
from IPython.display import display, Markdown


class Task:
    class Fields:
        ID = "id"
        UNIT = "unit"
        TASK_TEXT = "task_text"
        TASK_SOLUTION_CODE_ANALYTICS = "task_solution_code_analytics"
        TASK_SOLUTION_CODE = "task_solution_code"

    def __init__(self, id: int = 0, unit: str = "test", task_text: str = "нет",
                 task_solution_code_analytics: str = "нет", task_solution_code: str = "нет"):
        self.id = id
        self.unit = unit
        self.task_text = task_text
        self.task_solution_code_analytics = task_solution_code_analytics
        self.task_solution_code = task_solution_code

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> 'Task':
        return Task(
            id=data.get(Task.Fields.ID),
            unit=data.get(Task.Fields.UNIT),
            task_text=data.get(Task.Fields.TASK_TEXT),
            task_solution_code_analytics=data.get(Task.Fields.TASK_SOLUTION_CODE_ANALYTICS),
            task_solution_code=data.get(Task.Fields.TASK_SOLUTION_CODE)
        )


def help():
    print('1. namba.find_by_words("любое количество слов")')
    print('2. namba.get_task_by_id(выбранный_id)')


def load_all_tasks():
    all_tasks = []
    with open(pathlib.Path(pathlib.Path(os.path.dirname(os.path.abspath(__file__)), "tasks_base.txt")),
              encoding="UTF8") as f:
        for row in f:
            all_tasks.append(Task.deserialize(json.loads(row)))
    return all_tasks


def get_task_by_id(id: int) -> Union[None, str]:
    all_tasks = load_all_tasks()
    for task in all_tasks:
        if task.id == id:
            eval(task.task_solution_code_analytics + "()")
            return

    return "fuck"


def find_by_words(words: str, unit: Optional[str] = None):
    words = words.split()
    words = [w.lower().replace("ё", "е") for w in words]
    all_tasks = load_all_tasks()
    counter = [0 for _ in range(max([task.id for task in all_tasks]) + 4)]
    for task in all_tasks:
        task_words = task.task_text.translate(str.maketrans('', '', string.punctuation))
        task_words = task_words.split(" ")
        task_words = [w.lower().replace("ё", "е") for w in task_words]
        for word in words:
            if word in task_words:
                counter[task.id] += 1
    all_tasks_by_id = {task.id: task for task in all_tasks}
    c = [[counter[i], i] for i in range(len(counter))]
    c.sort(reverse=True)
    for el in c:
        if el[0] > 0:
            i = el[1]
            task = all_tasks_by_id[i]
            text = task.task_text
            if unit:
                if task.unit == unit:
                    print(i, "\n".join([text[128 * i:128 * (i + 1)] for i in range(0, (len(text) - 1) // 128 + 1)]))
            else:
                print(i, "\n".join([text[128 * i:128 * (i + 1)] for i in range(0, (len(text) - 1) // 128 + 1)]))


def solve():
    display(Markdown(r"""
```
a = 5
b = 7
print(a + b)
```
 """))

def sample_and_sample_choice_function():
    display(Markdown(r"""
    $ n\hat{F(x)}  \sim Bin(n, F(x)); F(x) = \frac{x-a}{b-a} $  

$ a)P((\hat{F(6)}=\hat{F(8)}) = P(X_i  \nsubseteq [5,8]) = (1-\frac{2}{3})^6 \approx 0,0014$  

$ б) Y = 6\hat{F(7)}\sim Bin(6, \frac{2}{3})  $  
$ P(\hat{F(7)})=\frac{1}{2} = P(Y=3) = С^3_6 p^3 (1-p)^3 = \frac{4 \cdot 5 \cdot 6}{6} \cdot (\frac{2}{3})^3 \cdot (\frac{1}{3})^3  \approx 0,2195$  
    """))

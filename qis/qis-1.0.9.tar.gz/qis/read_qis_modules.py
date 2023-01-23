import qis.file_utils
this = dir(qis.file_utils)
print(this)
for x in this:
    if not any(y in x for y in ['__', 'Dict']):
        print(f"{x},")


print('##############################')
import inspect

all_functions = inspect.getmembers(qis.file_utils, inspect.isfunction)
for x in all_functions:
    if not any(y in x for y in ['run_unit_test', 'njit', 'NamedTuple', 'dataclass', 'skew', 'kurtosis', 'abstractmethod']):
        print(f"{x[0]},")
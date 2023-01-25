import subprocess
import inspect
from unittest.mock import Mock
import re
import os

script_file = 'tmp.sh'


def run(cmd):
    return subprocess.run(cmd)


def extract_function_code(file_contents, function_name):
    start_pos = file_contents.index(f'{function_name}()')
    end_pos = find_function_end(file_contents, start_pos)
    function_code = file_contents[start_pos:end_pos]
    return function_code


def get_content_from_file(filename):
    with open(filename, 'r') as f:
        file_contents = f.read()
    return file_contents


def find_function_end(file_contents, start_pos):
    stack = []
    end_pos = -1
    for i, c in enumerate(file_contents[start_pos:]):
        if c == '{':
            stack.append(c)
        elif c == '}':
            stack.pop()
            if not stack:
                end_pos = i + start_pos
                break
    if end_pos == -1:
        raise ValueError(f'Could not find end of function code')
    return end_pos + 1


def save_to_file(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)


def save_script(contents, function_name):
    run(['rm', '-f', 'mock_calls'])
    run(['rm', '-f', 'logs'])
    run(['touch', 'mocks.py'])
    header = '#!/bin/bash\n'
    footer = '{} "$@"'.format(function_name)
    contents = header + contents + '\n' + footer
    save_to_file(script_file, contents)
    run(['chmod', '+x', script_file])


def create_mock_function(name):
    lines = [
        '{}()'.format(name) + '{',
        '    echo "{} $@" >> mock_calls'.format(name),
        '    python3 -c "import mocks; mocks.{}()" $@'.format(name),
        '}\n',
    ]
    return '\n'.join(lines)


def execute(args):
    res = run(['./tmp.sh'] + args)
    result = {}
    result['mocks'] = get_mocks()
    result['stdout'] = res.stdout
    result['stderr'] = res.stderr
    read_file('logs')
    return result

def read_file(filename):
    f = open(filename, "r")
    print(f.read())

def get_mocks():
    calls_file = load_mock_calls()
    unique_calls = set()
    calls = []
    for call in calls_file.splitlines():
        [name, *args] = call.split()
        # print('Called {} with args {}'.format(name, args))
        unique_calls.add(name)
        call_dict = {
            'name': name,
            'args': args,
        }
        calls.append(call_dict)

    mocks = {}
    for unique_call in unique_calls:
        mocks[unique_call] = Mock()

    for call in calls:
        mock = mocks[call['name']]
        mock(*call['args'])

    return mocks


def load_mock_calls():
    with open('mock_calls', 'r') as f:
        return f.read()


def run_test(script_file, function_name, args=[], mocks=[]):
    file_contents = get_content_from_file(script_file)
    new_file_contents = get_new_content(mocks, file_contents)
    save_script(new_file_contents, function_name)
    res = execute(args)
    clean_up()
    return res

def clean_up():
    remove('mock_calls')
    remove('tmp.sh')
    remove('mocks.py')
    remove('logs')

def remove(filename):
    os.remove(filename)

def get_new_content(mocks, file_contents):
    new_file_contents = ''
    mocks_created = {}
    codes, names = get_functions(file_contents)
    for code, name in zip(codes, names):
        is_needed_to_be_mocked = any([name == mock['name'] for mock in mocks])
        if not is_needed_to_be_mocked:
            new_file_contents += code + '\n'
            continue

        mock = [mock for mock in mocks if mock['name'] == name][0]
        new_file_contents += create_mock_function(name)
        mocks_created[name] = True

    save_function_to_a_new_file('mocks.py', 'log', log, mode='w')
    for mock in mocks:
        if mock.get('effect', None):
            save_function_to_a_new_file(
                'mocks.py', mock['name'], mock['effect'])
        else:
            save_function_to_a_new_file('mocks.py', mock['name'], hello)
        if mock['name'] in mocks_created:
            continue
        new_file_contents += create_mock_function(
            mock['name'])
    return new_file_contents


def get_functions(file_contents):
    names = extract_function_names(file_contents)
    codes = []
    for name in names:
        code = extract_function_code(file_contents, name)
        codes.append(code)
    code = '\n'.join(codes)
    return codes, names


def extract_function_names(bash_script: str):
    # Use a regular expression to find all function definitions at the start of a line
    function_definitions = re.findall(
        r'^\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)', bash_script, re.MULTILINE)
    return function_definitions


def hello():
    import sys
    print(sys.argv)
    print('Hello world')


def log(*text):
    def get_caller_name():
        import inspect
        import traceback
        # Get the stack frame of the caller
        frame = inspect.stack()[2]
        # Get the name of the caller function
        name = frame[3]
        return name
    with open('logs', 'a') as f:
        print(get_caller_name(), text, file=f)


if __name__ == '__main__':
    result = run_test(
        mocks=[
            {
                'name': 'find',
            },
            {
                'name': 'sed',
            },
            {
                'name': 'escape_branch',
            },
        ],
        args=['arg1', 'arg2'],
        script_file='main.sh',
        function_name='update_module',
    )
    cool = result['mocks']['find'].call_args_list
    print()


def save_function_to_a_new_file(path, function_name, function, mode='a'):
    # Get the source code of the function
    source_code = inspect.getsource(function)
    source_code = source_code.replace(function.__name__, function_name)
    with open(path, mode) as f:
        # Write the function definition to the file
        # Write the source code of the function to the file
        f.write(source_code)

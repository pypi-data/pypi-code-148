__version__ = '0.2.5'
from google.colab import _message
import ast 
import re
import os 

def traverse_ast(tree_dict, code, tree):
  for node in tree.body:
      if isinstance(node, ast.Assign):
        value_source = ast.get_source_segment(code, node)
        # print("value_source: ", value_source)
        str_split = value_source.split("=", 1)
        key_val = str(str_split[0]).strip()
        value = str(str_split[1]).strip()
        tree_dict[key_val] = value_source
      elif isinstance(node, ast.ClassDef):
          # print(node.name)
          tree_dict[node.name.strip()] = ast.get_source_segment(code, node)
      elif isinstance(node, ast.FunctionDef):
          # print(node.name)
          tree_dict[node.name.strip()] = ast.get_source_segment(code, node)
      elif isinstance(node, ast.Import):
          value_source = ast.get_source_segment(code, node)
          for name in node.names:
            tree_dict[name.name] = value_source
      elif isinstance(node, ast.ImportFrom):
          value_source = ast.get_source_segment(code, node)
          for name in node.names:
            tree_dict[name.name] = value_source



def get_dependencies(code_segment_list):
    dep_modules = []
    # Run function in a sandbox and catch ImportErrors
    print("new list")
    try:
        for code_segment in code_segment_list:
          print("code_segment: ", code_segment)
          exec(code_segment)
          # func()  # Try to run function in the sandbox
    except Exception as e:
        print(e)
        if hasattr(e, 'name'):
          print(e.name)
          dep_modules.append(e.name)  # Add module that caused error
        else:
            text = e.args[0]
            match = re.search(r"'(.*)'", text)
            if match:
                quoted_text = match.group(1)
                print(quoted_text)
                dep_modules.append(quoted_text)
    return dep_modules

def get_dependencies_exec(import_statements, parent_dependencies, code_segment_list):
    dep_modules = []
    # Run function in a sandbox and catch ImportErrors
    print("new list")
    try:
        for import_statement in import_statements:
          exec(import_statement)
        for parent_dependency in parent_dependencies:
          exec(parent_dependency)
        for code_segment in code_segment_list:
          print("code_segment: ", code_segment)
          exec(code_segment)
          # func()  # Try to run function in the sandbox
    except Exception as e:
        print(e)
        # print(import_statements)
        # print(parent_dependencies)
        # print(code_segment_list)
        with open("fail.py", 'w') as f: 
          for import_statement in import_statements:
            f.write(import_statement + "\n")
          for parent_dependency in parent_dependencies:
            f.write(parent_dependency + "\n")
          for code_segment in code_segment_list:
            print("code_segment: ", code_segment)
            f.write(code_segment + "\n")
        if hasattr(e, 'name'):
          print(e.name)
          dep_modules.append(e.name)  # Add module that caused error
        else:
            text = e.args[0]
            match = re.search(r"'(.*)'", text)
            if match:
                quoted_text = match.group(1)
                print("quoted_text in dep exec: ", quoted_text)
                dep_modules.append(quoted_text)
    return dep_modules

def run_loop(code_list, tree_dict):
  for i in range(20):
    print(i)
    dependencies = get_dependencies(code_list)
    if len(dependencies) == 0:
      break
    for dependency in dependencies:
      # print("dependency: ", dependency)
      code = tree_dict[dependency]
      # print("dependency parent_dependency: ", parent_dependency)
      code_list.insert(0, code)
  return code_list

def save_requirements():
  try:
    from pip._internal.operations import freeze
  except ImportError:
      from pip.operations import freeze
  
  x = "\n".join(list(freeze.freeze()))
  f = open("requirements.txt", "w")
  f.write(x)
  f.close()

def deploy():
  # assume you're in a google colab 

  # save the requirements to a requirements.txt file 
  save_requirements
  # Obtain the notebook JSON as a string
  notebook_json_string = _message.blocking_request('get_ipynb', request='', timeout_sec=5)

  # save to temporary file
  lines = []
  for cell in notebook_json_string["ipynb"]["cells"]:
    print("cell source: ", cell["source"])
    for line in cell["source"]:
      if not line.startswith("!"):
        print("line: ", line)
        lines.append(line)
  
  f = open("temp.py", "w")
  for line in lines:
    f.write(line + "\n")
  f.close()
  
  # find the executing line
  agent_executing_line = "agent.run("
  
  with open("./temp.py") as f:
      lines = f.readlines()
  
  with open("./temp.py") as f:
      code = f.read()

  tree = ast.parse(code)
  tree_dict = {}
  # traverse the file and create a dictionary
  traverse_ast(tree_dict, code, tree)
  print("tree_dict: ", tree_dict)
  import_statements = []
  for line in lines:
    if agent_executing_line in line:
      print(line)
      agent_executing_line = line # find the executing line 
    elif "import" in line:
      import_statements.append(line)

  run_loop(import_statements, tree_dict)
  print(import_statements)

  parent_dependencies = []
  
  for key in tree_dict:
    if "os" in key:
      parent_dependencies.append(tree_dict[key])
  
  print("parent_dependencies: ", parent_dependencies)
  
  run_loop(parent_dependencies, tree_dict)

      
  code_segment_list = [agent_executing_line]
  
  # run_loop(code_segment_list, tree_dict)
  for i in range(30): 
    dependencies = get_dependencies_exec(import_statements, parent_dependencies, code_segment_list) # find it's dependencies 
    print("len(code_segment_list): ", len(code_segment_list))
    if len(dependencies) == 0:
      break
    print("dependencies: ", dependencies)
    for dependency in dependencies:
      code_segment = tree_dict[dependency]
      # print("dependency code segment: ", code_segment)
      code_segment_list.insert(0, code_segment)

  with open("clean_file.py", 'w') as f: 
    for code_segment in code_segment_list: 
        f.write(code_segment + "\n") 
  
  print("Done!")
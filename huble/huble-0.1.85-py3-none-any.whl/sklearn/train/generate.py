from jinja2 import Environment, FileSystemLoader
from .templates import return_function 
import os


def generate_script(steps_list):
    """
    Generate script for training data.
    """
    print(os.getcwd())
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'template')
    file_loader = FileSystemLoader(filename)
    env = Environment(loader=file_loader)
    template = env.get_template("train.j2")
    # node_map,edge_map = convert_graph(graph)
    # steps_list = generate_steps(node_map, edge_map)
    parameters = {
        "steps_list": steps_list
    }
    output = template.render(parameters)
    return output

from jinja2 import Environment, FileSystemLoader
from .metrics import log_metrics
from huble.sklearn.process.templating import return_function as preprocess_generate
from huble.sklearn.train.templates import return_function as train_generate
from huble.sklearn.essentials.templates import return_function as essentials_generate
from collections import defaultdict
 
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list) 
        self.V = vertices 

    def addEdge(self, u, v):
        self.graph[u].append(v)
 
    def topologicalSortUtil(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
        stack.append(v)

    def topologicalSort(self):
        visited = [False]*self.V
        stack = []
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
        return(stack[::-1]) 
 
def generate_file(graph, target_column, task_type, colab=False):
    g = Graph(len(graph['nodes']))
    map = {}
    j=0
    while j <(len(graph['nodes'])):
        for i in graph['nodes']:
            map[(i['id'])]=j
            j+=1
    map2 = {y: x for x, y in map.items()}
    for i in graph['edges']:
        g.addEdge(map[i['source']], map[i['target']])
    res=g.topologicalSort()
    steps=[]
    for i in res:
        steps.append(map2[i])
    steps_list={}
    for i in steps:
        for j in range(len(graph['nodes'])):
            if i == graph['nodes'][j]['id']:
                steps_list[(graph['nodes'][j]['data']['name'])]=graph['nodes'][j]['data']['node_type']

    with open("/content/output.py", "w") as f:
        f.write("import huble\n")
        
        for i in steps_list:
            for node in graph['nodes']:
                if i == node['data']['name']:
                    if steps_list[i]=='preprocess':
                        f.write(preprocess_generate(node))
                        f.write("\n")
                    elif steps_list[i] == 'model':
                        f.write(train_generate(node))
                        f.write("\n")
                    elif steps_list[i] == 'essential':
                        f.write(essentials_generate(node))
                        f.write("\n")
                    elif steps_list[i] == 'evaluate_model':
                        f.write(f"metrics = huble.util.evaluate_model(model=Model, test_dataset=test_dataset, target_column= '{target_column}, task_type='{task_type}' )")
                        f.write("\n")
                    elif steps_list[i] == 'primary_dataset':
                        f.write(f"data=huble.util.load_dataset('{node['data']['url']}')")
                        f.write("\n")






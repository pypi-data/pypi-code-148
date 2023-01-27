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
 
def generate_file(url, graph, colab=False):
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
                        f.write("metrics = huble.util.evaluate_model(model=model, test_dataset=test_dataset, 'classification' )")
                        f.write("\n")
                    elif steps_list[i] == 'primary_dataset':
                        f.write(f"data=huble.util.load_dataset({node['data']['url']})")
                        f.write("\n")








# def generate_file(url,graph,colab=False):

#     preprocess_template = preprocess_generate(graph)
#     train_template = temp_logistic_regression()
#     #output_template = preprocess_template + train_template
#     with open("/content/output.py", "w") as f:
#         f.write("import huble\n")
#         f.write("from sklearn.model_selection import train_test_split\n")
#         f.write(f"data=huble.util.load_dataset({url})")
#         f.write(preprocess_template)
#         f.write("\nX = data.drop(columns = ['survived'],axis = 1)\n")
#         f.write("y = data['survived']\n")
#         f.write("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n")
#         f.write(train_template)
#         f.write("\nmodel.fit(X,y)\n")
#         f.write("y_pred = model.predict(X_test)\n")
#         #metrics template
#         f.write("metrics = huble.sklearn.metrics.log_metrics(y_test, y_pred,'classification')\n")
#         f.write("huble.sklearn.metrics.upload(metrics)\n")
        

#     #print(output_template)


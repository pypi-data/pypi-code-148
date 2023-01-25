
import colorsys
import random as rn
from itertools import permutations, combinations
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import graphviz_layout

class system:
    """
    x = system(n_nodes, edge, ..., edges=0, weight=0.1)
    Instantiate a power system. It will automatically calculate the colonization matrix of the system.

    Arguments:

        n_nodes:    int, the number of nodes in the system (the first node will be node 0)

        edge, ...:  (optional) tuples of the form (out, in, weight) that define single edges:
                        out:    int, the out node of the edge
                        in:     int, the in node of the edge
                        weight: float between 0 and 1 (both excluded), the weight of the edge

        edges:      (optional) int, the number of random edges to add (you can use this argument
                    when the previous edge argument is empty, otherwise it will be ignored)

        weight:     (optional) float between 0 and 1 (both excluded), the weight of the random 
                    edges (default 0.1)

    Properties:

        system.graph:           networkx.DiGraph()

        system.n:               int, the number of nodes

        system.edge_list:       list of tuples of the form (out, in, weight)

        system.adjacency:       list of lists which contains the adjacency matrix

        system.colonization:    list of lists which contains the colonization matrix. 
                                The colonization of node X in node Y is system.colonization[X][Y]

        system.hierarchy:       float

        system.mutualism:       float

        system.freedom:         float

        system.cooperation:     float

    Methods:

        system.show():          It shows a figure with adjacency graph, histogram of colonizations and 
                                donut of properties.
                                layout: (optional) string. Admitted values:
                                "circular", "random", "shell", "spring", "spectral", "spiral", "tree" 
                                (default: "random")
    """

    def __init__(self, n_nodes: int, *edges, **kwargs):
        self.n = n_nodes
        if not edges:
            if "edges" not in kwargs:
                kwargs["edges"] = 0         # Set default edges
            if "weight" not in kwargs:
                kwargs["weight"] = 0.1      # Set default weight
            self.graph = self.generate(self.n, kwargs["edges"], kwargs["weight"])
        else:
            self.graph = self.generate_custom(self.n, list(edges))
        self.normalize()
        self.adjacency = self.adj()
        self.colonization = self.col()
        self.mutualism, self.cooperation, self.hierarchy = self.properties()
        self.freedom = 1 - self.cooperation

    def generate(self, n_nodes: int, n_edges: int, weight: float):
        """ 
        Generate a power system with random edges (to be used only by __init__)
        """
        K=nx.DiGraph()
        HSV_tuples = [(x*1.0/n_nodes, 0.7, 0.8) for x in range(n_nodes)]
        RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
        for node in range(n_nodes):
            K.add_node(node, color=RGB_tuples[node])
        edge_list=list(permutations(list(range(n_nodes)), 2))
        rn.shuffle(edge_list)
        edge_list = edge_list[slice(n_edges)]
        self.edge_list = [(*edge, weight) for edge in edge_list]
        self.edge_list.sort()
        for edge in edge_list:
            K.add_weighted_edges_from ([ (edge[0],edge[1], weight) ])
        return K

    def generate_custom(self, n_nodes:int , edge_list:list):
        """
        Generate a power system with custom edges (to be used only by __init__)
        """
        self.edge_list = edge_list
        K=nx.DiGraph()
        HSV_tuples = [(x*1.0/n_nodes, 0.7, 0.8) for x in range(n_nodes)]
        RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
        for node in range(n_nodes):
            K.add_node(node, color=RGB_tuples[node])
        if len(edge_list[0])==2:
            for edge in edge_list:
                K.add_weighted_edges_from([(edge[0],edge[1], rn.random() ) ])
        else:
            K.add_weighted_edges_from(edge_list)
        return K

    def normalize(self):
        """
        Change the graph in order to have the sum of the weights of the in-edges of every node less than 1
        (to be used only by __init__)
        """
        for node in self.graph.nodes():
            in_sum=0
            for in_node in self.graph.predecessors(node):
                in_sum = in_sum + self.graph[in_node][node]['weight']
            if (in_sum >= 1):
                for in_node in self.graph.predecessors(node):
                    new_weight = self.graph[in_node][node]['weight']/(in_sum+0.001)
                    index = self.edge_list.index((in_node, node, self.graph[in_node][node]['weight']))
                    self.edge_list[index] = (in_node, node, new_weight)
                    self.graph[in_node][node]['weight'] = new_weight

    def adj(self):
        adjacency = [[0] * self.n for x in range(self.n)]
        for edge in self.edge_list:
            adjacency[edge[0]] [edge[1]] = edge[2]
        return adjacency

    def edge_ind(self, n, a, b):
        """
        It calculates the position of an edge in the sequence of all edges.
        (to be used only by internal functions)
        """
        return a*(n-1)+b-(1 if b>a else 0)

    def col(self):
        """
        It calculates the colonization array of the system (to be used only by internal functions)
        """
        n=self.n
        N=n*(n-1)
        f_arr=[[0]*N for t in range(N)]
        for i in range(N):
            f_arr[i][i] = 1
        k_arr=[0]*N
        edges = list(self.graph.edges.data("weight"))
        for edge in edges:
            if edge[0]==edge[1]:
                ran = list(range(n))
                ran.remove(edge[0])
                for i in [self.edge_ind(n, edge[0], x) for x in ran]:
                    f_arr[i][i] = 1-edge[2]
            else:
                ind=self.edge_ind(n, edge[1], edge[0])
                k_arr[ind] = edge[2]
                ran = list(range(n))
                ran.remove(edge[0])
                for i in [self.edge_ind(n, edge[0], x) for x in ran]:
                    f_arr[ind][i] = edge[2]
                ran = list(range(n))
                ran.remove(edge[0])
                ran.remove(edge[1]) 
                for x in ran:
                    f_arr[self.edge_ind(n, edge[1], x)][self.edge_ind(n, edge[0], x)] = -edge[2]
        col_list = np.linalg.solve(f_arr, k_arr).tolist()
        node_col_list=list(col_list)
        for node in range(n):
            freedom=1-sum(col_list[node*(n-1) : (node+1)*(n-1)])
            node_col_list.insert(node*(n+1), freedom)
        node_col_list=np.array(node_col_list).reshape((n,n)).transpose().tolist()
        return node_col_list

    def properties(self):
        """
        It returns the mutualism, hierarchy, freedom indices of the system.
        """
        cooperation = 0
        hierarchy = 0
        for i in list(combinations(range(self.n), 2)):
            c1=self.colonization[i[0]][i[1]]
            c2=self.colonization[i[1]][i[0]]
            cooperation += c1 + c2
            hierarchy += abs( c1 - c2 )
        cooperation = cooperation/(self.n-1)
        hierarchy = hierarchy/(self.n-1)
        mutualism = cooperation - hierarchy
        return mutualism, cooperation, hierarchy

    def donut(self):
        """
        It draws the donut graph of mutualism, hierarchy and freedom.
        """
        plt.subplot(133)
        plt.title("Donut")
        plt.pie([self.mutualism, self.hierarchy, self.freedom], wedgeprops=dict(width=0.5), startangle=0, center=(100,-50))
        plt.legend(labels = ['mutualism' , 'hierarchy' , 'freedom'],loc='lower right', bbox_to_anchor=(0.6, -0.1, 0.5, 0.5))

    def draw(self, layout="random"):
        """
        It draws the graph of the adjacencies.

        layout: (optional) a string, the position of the nodes. Admitted values:
                "circular", "random", "shell", "spring", "spectral", "spiral", "tree"
                (default: random)
        """
        n_size=self.degrees()
        n_size=[element * 300 for element in n_size]
        e_widths = [self.graph[u][v]['weight'] for u,v in self.graph.edges]
        if layout=="circular":
            ps=nx.circular_layout(self.graph)
        if layout=="random":
            ps=nx.random_layout(self.graph)
        if layout=="shell":
            ps=nx.shell_layout(self.graph)
        if layout=="spring":
            ps=nx.spring_layout(self.graph)
        if layout=="spectral":
            ps=nx.spectral_layout(self.graph)
        if layout=="spiral":
            ps=nx.spiral_layout(self.graph)
        if layout=="tree":
            ps=graphviz_layout(self.graph, prog="dot")
        #F = plt.figure(num=current_figure, figsize=(4, 4), layout="constrained")
        #current_figure +=1
        plt.subplot(131, rasterized=False)
        plt.title("Adjacency Graph")
        #list(nx.get_node_attributes(K,'color').values())
        nx.draw_networkx(self.graph, pos=ps, node_size= n_size, 
                        node_color='0.8', 
                        width= e_widths, 
                        connectionstyle='arc3, rad = 0.1', 
                        with_labels=True)

    def degrees(self):
        """
        It returns a list with the total power of every node
        """
        return [sum(self.colonization[node]) for node in range(self.n)]

    def histogram(self):
        """
        It draws the histogram of colonizations
        """
        labels=[]
        bottom_sum=[]
        for node in self.graph.nodes:
            labels.append(str(node))
            bottom_sum.append(0)
        plt.subplot(132)
        for node in self.graph.nodes:
            plt.bar(labels, 
                    self.colonization[node], 
                    bottom=bottom_sum, 
                    color=nx.get_node_attributes(self.graph,'color')[node], 
                    label=str(node))
            bottom_sum=list(np.add(bottom_sum, self.colonization[node]))
        #print ( 'Libertà media: {:.1f}%'.format(freedom_sum/K.number_of_nodes()*100) )
        plt.title('Colonization Spectra')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    def show(self, layout="random"):
        """
        It shows a figure with adjacency graph, histogram of colonizations and donut of properties
        """
        plt.figure(num=1, figsize=(15, 5), layout='constrained')
        self.draw(layout)
        self.histogram()
        self.donut()
        plt.show()


import colorsys
import random as rn
from itertools import permutations, combinations
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import graphviz_layout

class p_system:
    """
    x = p_system(n_nodes, edge, ..., edges=0, weight=0.1)
    Instantiate a power system. It will automatically calculate the colonization matrix of the system.
    Arguments:
        n_nodes:    int, the number of nodes in the system (the first node will be node 0)
        edge, ...:  (optional) tuples of the form (out, in, weight) that define single edges:
                        out: int, the out node of the edge
                        in: int, the in node of the edge
                        weight: float between 0 and 1 (both excluded), the weight of the edge
        edges:      (optional) int, the number of random edges to add (you can use this argument
                    when the previous edge argument is empty, otherwise it will be ignored)
        weight:     (optional) float between 0 and 1 (both excluded), the weight of the random 
                    edges (default 0.1)
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
        self.colonization = self.col()
        self.mutualism, self.cooperation, self.hierarchy = self.properties()

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
        for edge in edge_list[slice(n_edges)]:
            K.add_weighted_edges_from ([ (edge[0],edge[1], weight) ])
        return K

    def generate_custom(self, n_nodes:int , edge_list:list):
        """
        Generate a power system with custom edges (to be used only by __init__)
        """
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
                in_sum= in_sum + self.graph[in_node][node]['weight']
            if (in_sum >= 1):
                for in_node in self.graph.predecessors(node):
                    self.graph[in_node][node]['weight'] = self.graph[in_node][node]['weight']/(in_sum+0.001)

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
        It shows the donut graph of mutualism, hierarchy and freedom.
        """
        global current_figure
        plt.figure(num=current_figure)
        current_figure +=1
        plt.subplots(figsize=(4, 4), layout='constrained')
        plt.pie([self.mutualism, self.hierarchy, (1-self.cooperation)], wedgeprops=dict(width=0.5), startangle=0)
        plt.legend(labels = ['mutualism' , 'hierarchy' , 'freedom'],loc='center', bbox_to_anchor=(1, 1.1))
        plt.show(block=True)

    def draw(self, layout="random"):
        """
        It shows the graph of the system.

        layout: (optional) a string, the position of the nodes. Admitted values:
                "circular", "random", "shell", "spring", "spectral", "spiral", "tree"
                (default: random)
        """
        global current_figure
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
        plt.figure(current_figure)
        current_figure +=1
        plt.subplots(figsize=(4, 4), layout='constrained')
        #list(nx.get_node_attributes(K,'color').values())
        nx.draw_networkx(self.graph, pos=ps, node_size= n_size, 
                        node_color='0.8', 
                        width= e_widths, 
                        connectionstyle='arc3, rad = 0.1', 
                        with_labels=True)
        #nx.draw_networkx_nodes(K, pos=ps, nodelist=[0], node_color='red' , node_size=n_size[0])
        #nx.draw_networkx_edges(K, pos=ps, edgelist=[(0,1)], edge_color='red',connectionstyle='arc3, rad = 0.1' )
        plt.show(block=True)

    def degrees(self):
        """
        It returns a list with the total power of every node
        """
        p_arr=[]
        for node in range(self.n):
            p_arr.append(sum(self.colonization[node]))
        return p_arr

    def histogram(self):
        """
        It shows the histogram of colonizations
        """
        labels=[]
        bottom_sum=[]
        for node in self.graph.nodes:
            labels.append(str(node))
            bottom_sum.append(0)
        global current_figure
        plt.figure(num=current_figure)
        current_figure +=1
        plt.subplots(figsize=(4, 4), layout='constrained')
        for node in self.graph.nodes:
            plt.bar(labels, 
                    self.colonization[node], 
                    bottom=bottom_sum, 
                    color=nx.get_node_attributes(self.graph,'color')[node], 
                    label=str(node))
            bottom_sum=list(np.add(bottom_sum, self.colonization[node]))
        #print ( 'Libertà media: {:.1f}%'.format(freedom_sum/K.number_of_nodes()*100) )
        plt.title('Spectra')
        plt.ylabel('Colonization')
        plt.xlabel('Nodes')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show(block=True)

    def cournot(self, a=20 , b=1 , c=1):
        """
        It applies the system to a Cournot game. Inverse demand function: P = a - b*Q
        P is the price; Q is the supply.
        Utility function of the firms: u = (P - c)*q
        c is the (constant) cost of production.
        """
        n = self.n
        C = self.colonization
        if a==0:
            a=n**3
        array=[]
        known=[]
        for i in range(n):
            partial=[]
            known.append( (a - c) * C[i][i] )
            for j in range(n):
                if j == i:
                    partial.append( 2 * C[i][i] * b )
                else:
                    partial.append( (C[j][i] + C[i][i]) * b )
            array.append(partial)
        quantity = np.linalg.solve(array, known).tolist()
        print ( "Supply: " , quantity)
        qm = (a-c)/(2*b)
        print ( "Monopoly supply: " , qm)
        price = a - sum(quantity) * b
        print ( "Price: " , price)
        profit = [ (price - c) * quantity[x] for x in range(n) ]
        print ( "Profits: " , profit) 
        pm = qm*(a-b*qm-c)
        print ( "Monopoly profit: " , pm)
        global current_figure
        plt.figure(num=current_figure)
        current_figure +=1
        #   Profits Histogram
        plt.subplots(figsize=(4, 4), layout='constrained')
        nodes = [str (x) for x in range (n)]
        plt.bar(nodes, profit, color = "peru")
        left, right = plt.xlim()
        plt.plot([left, right], [pm/n] * 2 , "b")
        plt.title('Cournot Model')
        plt.annotate('monopoly / {}'.format(n) , (0,pm/n+1))
        if plt.ylim()[1]<pm/n+5:
            plt.ylim(0,pm/n+5)
        plt.ylabel('Profits')
        plt.xlabel('Nodes')
        plt.show(block=False)
        #   Prices Histogram
        plt.figure(num=current_figure)
        current_figure +=1
        plt.subplots(figsize=(2.5, 4), layout='constrained')
        plt.bar([""], price, color = "tab:purple", width = 0.6)
        plt.xlim(-1,1)
        left, right = plt.xlim()
        pricemon = a - qm * b
        plt.plot([left, right], [pricemon]*2 , "b")
        plt.annotate('monopoly', (-0.8,pricemon+1))
        plt.plot([left, right], [c]*2 , "r")
        plt.annotate('perfect competition', (-0.8,c+1))
        plt.title('Cournot Model')
        if plt.ylim()[1]<pricemon+5:
            plt.ylim(0,pricemon+5)
        plt.ylabel('Price')
        plt.show(block=True)

    def landowner(self , a=20 , b=1 , c=1):
        """
        It applies the system to a Landowner game. Inverse demand and
        utility function are the same of cournot() (see). Here node 0
        is the landowner.
        """
        n = self.n
        C = self.colonization
        if a==0:
            a=n**3
        array=[]
        known=[]
        for i in range(1,n):
            partial=[]
            known.append( (a - c) * C[i][i] + C[0][i])
            for j in range(1,n):
                if j == i:
                    partial.append( 2 * C[i][i] * b )
                else:
                    partial.append( (C[j][i] + C[i][i]) * b )
            array.append(partial)
        quantity = np.linalg.solve(array, known).tolist()
        print ( "Labor supply: " , quantity)
        qm = (a-c)/(2*b)
        print ( "Labor monopoly supply: " , qm)
        price = a - sum(quantity) * b
        print ( "Wage: " , price)
        profit = [ (price - c) * quantity[x] for x in range(n-1) ]
        print ( "Profits of peasants: " , profit) 
        pm = qm*(a-b*qm-c)
        print ( "Monopoly profit: " , pm)
        global current_figure
        plt.figure(num=current_figure)
        current_figure +=1
        #   Profits Histogram
        plt.subplots(figsize=(5, 4), layout='constrained')
        nodi = [str (x) for x in range (0,n)]
        profit.insert(0, 0)
        plt.bar(nodi, profit, color = "peru")
        plt.bar(0,sum(quantity), color = "tab:olive")
        left, right = plt.xlim()
        plt.plot([-left, right], [pm/(n-1)] * 2 , "b")
        #plt.title('Landowner Game')
        plt.annotate('max utility / {}'.format(n-1) , (2,pm/(n-1)+1))
        qc = (a - c)/b
        plt.plot([left, -left-0.1], [qc]*2 , "r")
        plt.annotate('max Q', (-0.3,qc+1))
        plt.plot([left, -left-0.1], [qm]*2 , "r")
        plt.annotate('min Q', (-0.3,qm+1))
        if plt.ylim()[1]<pm/(n-1)+5:
            plt.ylim(0,pm/(n-1)+5)
        plt.ylabel('Utility')
        plt.xlabel('Nodes')
        plt.show(block=False)
        #   Prices Histogram
        plt.figure(num=current_figure)
        current_figure +=1
        plt.subplots(figsize=(1, 4), layout='constrained')
        plt.bar([""], price, color = "tab:purple", width = 0.6)
        plt.xlim(-1,1)
        left, right = plt.xlim()
        pricemon = a - qm * b
        plt.plot([left, right], [pricemon]*2 , "b")
        plt.annotate('max wage', (-0.8,pricemon+0.5))
        plt.plot([left, right], [c]*2 , "r")
        plt.annotate('min wage', (-0.8,c+0.5))
        #plt.title('Landowner Game')
        if plt.ylim()[1]<pricemon+5:
            plt.ylim(0,pricemon+5)
        plt.ylabel('Wage')
        plt.show(block=True)


current_figure=0


#plt.show(block=True)
J=p_system(10, edges=5)
J.draw("tree")
plt.close(0)
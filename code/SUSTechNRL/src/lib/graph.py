import networkx as nx
import pickle as pkl
import numpy as np
import scipy.sparse as sp

class Graph(object):
    def __init__(self):
        self.G = None
        self.look_up_dict = {}
        self.look_back_list = []
        self.node_size = 0
        self.adjMat = None
    
    def encode_node(self):
        look_up = self.look_up_dict
        look_back = self.look_back_list
        for node in self.G.nodes():
            look_up[node] = self.node_size
            look_back.append(node)
            self.node_size += 1
            self.G.nodes[node]['status'] = ''

    def read_adjlist(self, filename):
        self.G = nx.read_adjlist(filename, create_using=nx.DiGraph())
        for i, j in self.G.edges():
            self.G[i][j]['weight'] = 1.0
        self.encode_node()
        self.adjacent_matrix()

    def read_edgelist(self, filename, weighted=False, directed=False):
        self.G = nx.DiGraph()
        if directed:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = 1.0
            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = float(w)
        else:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = 1.0
                self.G[dst][src]['weight'] = 1.0
            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = float(w)
                self.G[dst][src]['weight'] = float(w)
        fin = open(filename, 'r')
        func = read_unweighted
        if weighted:
            func = read_weighted
        while True:
            l = fin.readline()
            if l == '':
                break
            func(l)
        fin.close()
        self.encode_node()
        self.adjacent_matrix()

    def read_node_label(self, filename):
        fin = open(filename, 'r')
        while True:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G.nodes[vec[0]]['label'] = vec[1:]
        fin.close()
    
    def read_node_features(self, filename):
        fin = open(filename, 'r')
        while True:
            l = fin.readline()
            if l =='':
                break
            vec = l.split()
            self.G.nodes[vec[0]]['feature'] = np.array([float(x) for x in vec[1:]])
        fin.close()

    def read_node_status(self, filename):
        fin = open(filename, 'r')
        while True:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G.nodes[vec[0]]['status'] = vec[1]
        fin.close()
    
    def read_edge_label(self, filename):
        fin = open(filename, 'r')
        while True:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G[vec[0]][vec[1]]['label'] == vec[2]
        fin.close()
    
    def adjacent_matrix(self):
        look_up = self.look_up_dict
        self.adjMat = np.zeros((self.node_size, self.node_size))
        for edge in self.G.edges():
            self.adjMat[look_up[edge[0]]][look_up[edge[1]]] = 1.0
            self.adjMat[look_up[edge[1]]][look_up[edge[0]]] = 1.0
        # self.adjMat = np.matrix(self.adjMat/np.sum(self.adjMat, axis=1))

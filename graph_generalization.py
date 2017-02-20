from scipy import *
from pylab import *
import numpy as np
import networkx as nx
import random

###########
#Create a list of all possible partitons of the graph (O(2^n) - will take legit forever for big graphs... needs work)
###########
def all_partitions(G):
    array = nx.nodes(G)
    n = nx.number_of_nodes(G)
    partitions = []
    for partition_index in range(2 ** (n-1)):
        partition = []
        subset = []
        for position in range(n):
            subset.append(array[position])
            if 1 << position & partition_index or position == n-1:
                partition.append(subset)
                subset = []
        #print(partition)
        partitions.append(partition)
    return partitions

###########
#Iterate over all the different sets of partitions, and return those where every partition is of size >= k 
###########
def all_partitions_k(G, k):
    k_partitions = []
    for graph in G:
        flag = 0
        for partiton in graph: 
            if len(partiton) < k:
                flag = 1
                break
        if flag == 0:
            k_partitions.append(graph)
    return k_partitions 
   
def generalize(k):
    graph = nx.read_graphml('graphs/graph.xml')
    k_partitions = all_partitions_k(all_partitions(graph), k)
    #print(*k_partitions, sep='\n')

    rand = ceil(random.uniform(0, len(k_partitions) - 1))
    partition = k_partitions[int(rand)] #Do gradient descent algorithm here!!
    print(partition)
    origin_centrality = nx.closeness_centrality(graph)
    origin_diameter = nx.diameter(graph)

    gen_graph = nx.MultiGraph()
    buffer_graph = nx.MultiGraph()
    for i in range(0, len(partition)):
        subgraph = nx.subgraph(graph, partition[i])
        buffer_graph.add_node(subgraph, index=i)
        gen_graph.add_node(i, nodes=subgraph.number_of_nodes(), edges=subgraph.number_of_edges())

    #Create a list of all the edges, and the index of the partition each vertex is contained in
    edge_list = []
    for (u,v) in graph.edges():
        for i in range(0, len(partition)):
            if u in partition[i]:
                u_loc = i
            if v in partition[i]:
                v_loc = i
        edge_list.append([u, v, u_loc, v_loc])

    for edge in edge_list:
        if edge[2] != edge[3]:
            gen_graph.add_edge(edge[2], edge[3])

    nx.write_graphml(gen_graph, 'graphs/gen_graph.xml')                
    nx.draw_circular(gen_graph)
    savefig('images/gen_graph.png')
    print(graph.number_of_edges(), ":", gen_graph.number_of_edges())
    print(graph.number_of_nodes(), ":", gen_graph.number_of_nodes())

    gen_centrality = nx.closeness_centrality(gen_graph)
    gen_diameter = nx.diameter(gen_graph)

    #print(origin_centrality, ":", gen_centrality)
    #print(origin_diameter, ":", gen_diameter)
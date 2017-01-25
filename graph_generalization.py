from scipy import *
import numpy as np
import networkx as nx

def generalize(Ga, k):
    
    
    return V

###########
#Create a list of all possible partitons of the graph (O(2^n) - will take legit forever for big graphs... needs work)
##########
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
            
graph = nx.read_graphml('graph.xml')
all_partitions = all_partitions(graph)
k_partitions = all_partitions_k(all_partitions, 3)
print(*k_partitions, sep='\n')
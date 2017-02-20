from scipy import *
from pylab import *
import numpy as np
import networkx as nx

gen_graph = nx.read_graphml('graphs/gen_graph.xml')
print(gen_graph.number_of_nodes(), ":", gen_graph.number_of_edges())
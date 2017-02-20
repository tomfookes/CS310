from plrg import generate
from graph_generalization import generalize 
import sys

if sys.argv[1] == "--help":
    print("anonymize.py takes 3 arguments: \n 1 - Number of nodes in the graph to generate \n 2 - a true/false argument for wether or not to plot the distribution \n 3 - the anonymization constant K > 1")
else:
    if int(sys.argv[1]) > 0:
        generate(int(sys.argv[1]), bool(sys.argv[2]))

    if int(sys.argv[3]) > 1:
        generalize(int(sys.argv[3]))
    
    
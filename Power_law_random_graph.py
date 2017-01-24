from pylab import *
from scipy import *
from scipy import optimize
import numpy as np
import networkx as nx
import random

# Define function for calculating a power law
# Increasing amp increases max height of dist. Index -> -infinty causes sharper dist. gradient 
powerlaw = lambda x, amp, index: amp * (x**index)

##########
# Generate data points with noise
##########
#num_points will correspind to the number of nodes in the graph
num_points = 20
# Note: all positive, non-zero data
# Array of integers from 1 to the number of points
xdata = linspace(1, num_points, num_points).astype(int)
#simulated perfect data
ydata = powerlaw(xdata, (num_points/2), -0.5)
# simulated errors (10%)
yerr = 0.2 * ydata
# simulated noisy data
ydata += randn(num_points) * yerr
#Print out of all the sets of data (for error checking)
#print("xData: ", xdata, "\n yData: ", ydata, "\n yError: ", yerr)

##########
# Fitting the data -- Least Squares Method
##########
# Power-law fitting is best done by first converting
# to a linear equation and then fitting to a straight line.
#
# y = a * x^b
# log(y) = log(a) + b*log(x)

logx = log10(xdata)
logy = log10(ydata)
logyerr = yerr / ydata

# define our (line) fitting function
fitfunc = lambda p, x: p[0] + p[1] * x   
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

pinit = [1.0, -1.0]
out = optimize.leastsq(errfunc, pinit,
                       args=(logx, logy, logyerr), full_output=1)

pfinal = out[0]
covar = out[1]
#print(pfinal)
#print(covar)

index = pfinal[1]
amp = 10.0**pfinal[0]

#check similarity of index & amp to original values (should be kinda the same)
#print(index, amp)

indexErr = sqrt( covar[0][0] ) 
ampErr = sqrt( covar[1][1] ) * amp

##########
# Plotting data
# Not really useful, but graphically shows the power law distribution used to determine degree distribution
##########
clf()
subplot(2, 1, 1)
plot(xdata, powerlaw(xdata, amp, index))     # Power_Law fit line
#errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Original data with error bar (really hard to see for large number of nodes)
title('Best Fit Power Law')
xlabel('X')
ylabel('Y')
xlim(1, num_points)

subplot(2, 1, 2)
loglog(xdata, powerlaw(xdata, amp, index))
errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
xlabel('X (log scale)')
ylabel('Y (log scale)')
xlim(1.0, num_points)

savefig('plrg.png')

##########
# Generate graph with degree dist. following the power law generated above 
##########
graph = nx.Graph()
degrees = list()
#populate the graph with all the nodes so edges can be added
for x in xdata:
    graph.add_node(x)
    #Can assume this always works because each element in xdata is distinct (if its ever not its gonna break)
    num_arcs = ydata[np.where(xdata == x)]
    num_arcs_ceiling = int(ceil(num_arcs[0]))
    degrees.append([x, num_arcs_ceiling])
print(degrees)
#add number of edges to each node according to PL dist. where each edge has an equal probability of being added (edges can only exist once in networkx i.e only 1 edge between 2 nodes) 
int_sum = 0
index = 0
for x in xdata:
    max_degree = degrees[index][1]
    index += 1
    for i in range(0, max_degree):
        rand_node = x
        while(rand_node == x):
            rand_node = random.randint(1, num_points)
        if(graph.degree(rand_node) < degrees[rand_node - 1][1]):
            print(x, ': ', rand_node)
            graph.add_edge(x, rand_node)
        
print(graph.number_of_nodes(), graph.number_of_edges())
nx.write_graphml(graph, 'graph.xml') 
    
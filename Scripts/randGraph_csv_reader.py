
from igraph import *
import pandas as pd
from random import *

#Input: n an integer that represents the number of nodes the graph will have.
#Output: l a list of lists that represent the graph using the sparse matrix nodeA||nodeB||weight where A and B are adjacent nodes.
def gen_graph(n: int) -> list:
    l = [] #This will be the output
    lp = []#List to check for multiple edges, is a list of the edges in the graph
    v = list(range(1,n+1)) #Names of the edges
    root = choice(v)
    v.remove(root)
    pred = [root] #List of nodes in the graph

    while len(v) != 0: #Creates a graph with n-1 edges
        n1 = choice(pred) #Random node already in the graph
        n2 = choice(v) # Node not in the graph
        tp = [n1, n2]
        tp.sort() #To prevent multiple edges we add the other possible way of representing the same edge  lp.
        t = [n1, n2, randint(1, 15)] #nodeA||nodeB||weight where A and B are adjacent nodes.
        if tp not in lp: #if tp its a new edge then:
            l.append(t) #add edge-representation to the graph
            lp.append(tp) #Add edge to the list of edges
            pred.append(n2) #Add node to the list of nodes in the graph
            v.remove(n2) #Remove n2 from the list of nodes not in the graph
    while len(l) != int(n+n/2): #Adds edges till meeting the requierement of (n+n)/2 edges in the graph
        #The following code is similiar as the one above
        n1 = choice(pred)
        n2 = choice(pred) #Random node already in the graph
        tp = [n1, n2]
        tp.sort() 
        t = [n1, n2, randint(1, 15)]
        if n1 != n2 and tp not in lp and t not in l: #if the edge doesnt exist in the graph then it adds it
            l.append(t)
            lp.append(tp)
    return l #graph represented with the sparse matrix
#-------------------------------------------GRAFO Y CSV------------------------------------------------------
#Input: t sparse matrix of a graph nodeA||nodeB||weight where A and B are adjacent nodes.
#Output: None in python, but creates a file named 'graph.csv' in the same directory as the code
def graph2csv(t:list) -> None: #Saca el grafo creado en un csv
    df = pd.DataFrame(t)
    df = df.set_axis(['Node A', 'Node B', 'Cost'], axis=1, inplace=False)
    df.to_csv('./paths/graph.csv', index=False)

#Input: name the string of the name of the file with the sparse matrix, that has the same characteristics as the one created above
#Output: list of lists representing the graph via a sparse matrix
def import_graph(name='graph.csv'):
    df = pd.read_csv(name)
    return df.values.tolist()
#-------------------------------------------GRAFO Y CSV------------------------------------------------------



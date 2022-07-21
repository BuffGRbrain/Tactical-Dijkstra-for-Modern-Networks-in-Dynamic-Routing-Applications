import pandas as pd
from igraph import *

errorss = 0

# Input: Graph L in dictionary format, initial node u, destiny node z.
# Ouput: r a list of the nodes form the origin to the destiny node.

def get_path(L, u, z, r=[]):
    lz = L[z][1]  # It selects the first edge of the destiny node.
    r.append(lz[-1])  # Here it appends the previous node of the destiny node.
    if u in r:
        return r  # It ends if the origin node enters in the list of the route edges. Returns the path from z to u.
    return get_path(L, u, lz[-1], r)  # If the origin node isn't in r, the procedure repeats with the obtained node.


# Input: Graph G in iGraph format, node x and node v of the graph.
# Output: The weight of the edge between these nodes.

def w(G, x, v):
    try:
        return G.es[G.get_eid(x, v)]["weight"]  # If an edge exists between the nodes this finds the weight of it.
    except:
        return float('inf')  # If there is no edge exists between the nodes this returns infinite.


# Input:G graph from igraph, u a node in L and L is a dictionary in which the keys are the nodes and the values are a weight and destiny node of the edge.
# Output: Path from U to each node in the graph using the function get_path in a dictionary where keys are the name of the nodes
# and the values are a list of 2 elements: 1.List of the path from u to z. 2 .Total weight of going from u to z using the given path.

def list_graph_path(G, u, L):
    print("DEPRECATED")
    all_paths = {}  # Dictionary with keys as the name of the node and values the path from u top that node.
    l = list(G.vs['name'])  # List in which we have all the nodes of the graph.
    l.remove(str(u))  # Delete the initial node from the nodes to check.

    for i in l:
        path = get_path(L, str(u), str(i), [])  # Find paths from u to all the nodes with get_path.
        path = path[::-1]  # It inverse the path, this because geth_path returns the route list backwards.
        path.append(i)  # Appends the destiny node to the list because get_path makes the list without him.
        # if L[i][0] == 0: #Float(inf). If the weight of the path is 0 is because there isn't any.
        #    path = []

        all_paths[i] = [path, L[i][0]]  # Assign a path and a weight to their respective nodes.
    return all_paths


def to_disperse_matrix(t: list, L: dict) -> list:
    # Input : t : list of tuples (source, destination, weight) from original graph. L : dictionary of the graph.
    # Output : list of lists of weights to disperse matrix.

    bt = {tuple(sorted((i[0], i[1]))): i[2] for i in t}
    nt = []
    for i in L:
        try:
            pred = L[i][1][0]
        except:
            continue

        edge = sorted([int(i), int(pred)])
        weight = bt[tuple(edge)]
        tmp = [*edge, weight]
        nt.append(tmp)
    return nt


def get_routing_table(t: list, L: dict, u: str):
    bt = {tuple(sorted((i[0], i[1]))): i[2] for i in t}
    rt = {"Source": [], "Destination": [], "Predecessor": [], "Weight": []}
    for i in L:
        try:
            if not (int(i) == int(u)):
                rt["Source"].append(int(u))
                rt["Destination"].append(int(i))
                rt["Weight"].append(int(L[i][0]))
                rt["Predecessor"].append(int(L[i][1][0]))
        except:
            continue
    return pd.DataFrame(data=rt)


def Dijkstra(G: Graph, u: str, iterations: int = 0, affected_nodes: list = [], old_S: list = [], old_L: dict = {}) -> (
dict, list, int):
    # Input: G graph from iGraph.
    #        u : node in the graph.
    #        iterations : number of iterations.
    # Output: L a list of lists that represent the graph using the sparse matrix nodeA||nodeB||weight where A and B are adjacent nodes.
    #         S a list of nodes that are in the shortest path from u to all the nodes in the graph.
    #         iterations the number of iterations that the algorithm has done.

    global errorss
    L = {i: [float('inf'), []] for i in G.vs["name"]}  # Initializes all distances from u to any node in infinite.
    L[str(u)] = [0, []]  # Changes value of distance from u to u to 0.
    start2 = False
    if not old_S:
        S = [str(u)]  # Now we append u to the list of checked nodes.
        start = True
    else:
        # affected_nodes = [str(i) for i in affected_nodes]
        start = False
        # When we have to recalculate due to changes we use this case in which affected nodes is a set({}) of the affected nodes

        S = []
        for i in old_L:
            if i in affected_nodes:
                L[i] = [float('inf'), []]
        for i in old_S:
            if L[i][0] != float('inf'):
                S.append(i)
        start2 = True

    while 1:
        L_S = {i: L[i][0] for i in L if i not in S}  # Append to L_S all the nodes in L that have not been checked.
        # print(f"LS: {L_S} PUTA LISTA")
        if not L_S:  # If all nodes have been checked, it breaks, if not it continues.
            break
        if start:  # If we are in the first node, we asign u to x.
            x = u  # x will be the node whose edges will be checked.
            start = False  # Changing start to 0 because we will no longer be in the first node.
        elif start2:
            x = S[-1]
            start2 = False
        else:
            x = min(L_S, key=L_S.get)  # Selects the minimum of the weights and select that node to move to him
            if L[x][0] == float('inf'):
                raise Exception("No path found")
            S.append(x)  # Indicates that this node is checked now.

        for v in G.vs["name"]:  # For all the nodes in G.
            iterations += 1
            if v not in S:  # If v hasn't been checked.
                if L[str(v)][0] > L[str(x)][0] + w(G, str(x),
                                                   str(v)):  # If the weight that are in L is greater than the route for a node we replace that.
                    try:
                        L[str(v)][1].pop()
                    except:
                        pass
                    L[str(v)][1].append(str(x))  # If they are connected, we append in the predecessor list of v x.
                    L[str(v)][0] = L[str(x)][0] + w(G, str(x),
                                                    str(v))  # Updates weight of the edge and adds the route
    return L, S, iterations


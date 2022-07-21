from matplotlib.pyplot import plot
from igraph import *
from DJ import Dijkstra, to_disperse_matrix, get_routing_table
import pandas as pd
import json
import random
import randGraph_csv_reader as randgraph
import time


def plot_graph(g: Graph, path: str, name: str) -> None:
    # Input: g: graph from igraph, path: path to the file, name: name of the file.
    # Output: None
    # Plots the graph in the path with the name
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]
    layout = g.layout("kk")
    plot(g, layout=layout, target=f"./{path}/{name}.png")


def update_graph(t: list, count='initial') -> (Graph, list, list):
    # Input: t list of tuples with the graph
    # Output: G graph from igraph, old_graph_weights and new_graph_weights to see the changes
    # Updates the graph and returns the new graph and the old and new weights of the edges.
    old_graph_weights = [i[2] for i in t]
    to_change = random.sample(t, random.randint(1,
                                                len(t) // 3))  # random number  between 0 and a third of the number of nodes the graph has
    for i in to_change:  # Changes the weights randomly of the random sized sample created in ae
        index = t.index(i)
        t[index] = [i[0], i[1], random.randint(1, 15)]
    new_graph_weights = [i[2] for i in t]
    G = format_graph(t)

    if bool(config["plot"]):
        plot_graph(G, "graphs", f"Graph {count}")
    return G, old_graph_weights, new_graph_weights

def loop_update(t: list, changes: int) -> int:
    # Input: G graph from igraph, changes int number of random updates in the graph
    # Output: None in python.
    # Loops the update function for the number of changes specified, saving states in excel files.

    iterations = 0
    G = format_graph(t)
    a = random.sample(G.vs['name'], 1)  # Picks a random node in the graph
    old_L, old_S, iterations = Dijkstra(G, a[0])  # First dijkstra to know the state of the graph
    count = 0

    # Excel 
    graphs = pd.ExcelWriter(f'./simulations/Graph_N{len(G.vs)}_C{changes}.xlsx', engine='xlsxwriter')
    trees = pd.ExcelWriter(f'./simulations/Tree_N{len(G.vs)}_C{changes}.xlsx', engine='xlsxwriter')
    rts = pd.ExcelWriter(f'./simulations/RT_N{len(G.vs)}_C{changes}.xlsx', engine='xlsxwriter')

    df_graph = pd.DataFrame(t)
    df_graph.set_axis(['Node A', 'Node B', 'Cost'], axis=1, inplace=False)
    df_route, df_tree = print_route_tables(t, old_L, a[0])

    df_graph.to_excel(graphs, sheet_name='original')
    df_tree.to_excel(trees, sheet_name='original')
    df_route.to_excel(rts, sheet_name='original')

    while count < changes:  # Here the graph is updated and the routing tables are recalculeted
        G, old, new = update_graph(t,
                                   count + 1)  # Changes the weights on some of the edges of the graph and saves the old and the new weights.
        # From here we detect the changes on the graph and make the correspondent calculations
        diff = [i for i in range(len(old)) if old[i] != new[i]]  # Compare the old and the new weights to find the indices of the weights that changed and using this, we can find what edges changed
        # Now we use the indices to find the correspondent edges and with them we save both of the nodes connected to that edge to the a set to know whitch vertices route should be recalculated
        dv = [G.es[i] for i in diff]
        affected_nodes_rep = []
        affected_nodes = []

        for i in dv:
            affected_nodes_rep.append(G.vs[i.source]['name'])
            affected_nodes_rep.append(G.vs[i.target]['name'])

        for i in affected_nodes_rep:
            if i not in affected_nodes:
                affected_nodes.append(i)

        print('-----------------')
        if a[0] in affected_nodes:
            old_L, old_S, iterations = Dijkstra(G, a[0], iterations)
        else:
            old_L, old_S, iterations = Dijkstra(G, a[0], iterations, affected_nodes, old_S, old_L)  # Uses DIjkstra but keeping the past calculations that where not affected by the update. Only recalculating on the affected vertices.
        count += 1  # Another recalculation was made

        # Excel
        df_graph = pd.DataFrame(t)
        df_graph.set_axis(['Node A', 'Node B', 'Cost'], axis=1, inplace=False)
        df_route, df_tree = print_route_tables(t, old_L, a[0], count)

        df_graph.to_excel(graphs, sheet_name=f'it_{count}')
        df_tree.to_excel(trees, sheet_name=f'it_{count}')
        df_route.to_excel(rts, sheet_name=f'it_{count}')

    trees.save()
    trees.close()
    graphs.save()
    graphs.close()
    rts.save()
    rts.close()
    return iterations


def print_route_tables(t: list, L: dict, u: str, count='initial') -> (pd.DataFrame, pd.DataFrame):
    # Input: t list of tuples with the graph, L dictionary with the L Dijkstra output, u string with the node to
    # start from
    # Output: df_route pd.DataFrame with the routing table, df_tree pd.DataFrame with the tree graph
    # Prints and saves the routing table (and saves the tree graph)

    print(f"--- Routing Table {count}-----")
    df_rt = get_routing_table(t, L, u)
    print(df_rt.to_markdown())
    tree = to_disperse_matrix(t, L)
    df_tree = pd.DataFrame(t)
    df_tree.set_axis(['Node A', 'Node B', 'Cost'], axis=1, inplace=False)
    if bool(config["plot"]):
        g = format_graph(tree)
        plot_graph(g, "paths", f"Tree {count}")
    return df_rt, df_tree


def format_graph(t: list) -> Graph:
    # Input: t list of tuples with the graph
    # Output: G Graph from igraph
    new_t = [(str(i[0]), str(i[1]), i[2]) for i in t]
    return Graph.TupleList(new_t, weights=True)


def simulations() -> None:
    # Input: None
    # Output: None
    # Runs the simulations
    global config
    config = {"plot": False}
    graph_sizes = [i for i in range(20, 720, 20)]
    changes_ids = [i for i in range(10, 110, 10)]
    times_reg = []
    nodes_reg = []
    changes_reg = []
    iterations_reg = []

    for changes in changes_ids:
        for nodes in graph_sizes:
            start_time = time.time()
            print(
                f"-----------------------\n--------- Nodos: {nodes} Cambios: {changes}------------\n---------------------------------")
            t = randgraph.gen_graph(nodes)
            iterations = loop_update(t, changes)
            nodes_reg.append(nodes)
            changes_reg.append(changes)
            times_reg.append(time.time() - start_time)
            iterations_reg.append(iterations)

    df = pd.DataFrame(
        data={'# Nodes': nodes_reg, '# Changes': changes_reg, 'Time': times_reg, 'Iterations': iterations_reg})
    df.to_csv('Data.csv')


def main() -> None:
    # Input: None
    # Output: None
    # Runs the main program
    start_time = time.time()
    with open("config.json") as file:
        global config
        config = json.load(file)
        print("Current config:")
        for i in config:
            print(f"{i}: {config[i]}")

    if bool(config["generate_graph"]):
        print("Generating graph...")
        t = randgraph.gen_graph(config["nodes"])
        print("Graph generated")
    else:
        print("Loading graph...")
        t = randgraph.import_graph(config["graph_path"])
        print("Graph loaded")

    g = format_graph(t)
    if bool(config["plot"]):
        plot_graph(g, "graphs", "Graph initial")
    iterations = loop_update(t, config["changes"])
    print(f"Time: {time.time() - start_time}")
    print(f"Total Iterations: {iterations}")

if __name__ == '__main__':
    # main()
    simulations()

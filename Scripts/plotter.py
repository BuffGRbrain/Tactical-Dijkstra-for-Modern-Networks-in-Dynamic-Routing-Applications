import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plt.plot(nodes, time)
# plt.title("Nodos vs. Tiempo de ejecucion")
# plt.xlabel("Nodos")
# plt.ylabel("Tiempo (Segs)")
# plt.savefig('./plots/nodevtime.png')

def nodevit(ccdf : pd.DataFrame):
    nodes = ccdf["# Nodes"].to_numpy()
    iterations = ccdf["Iterations"].to_numpy()

    plt.plot(nodes, iterations)
    plt.title("Nodes vs. Iterations. (10 Changes)")
    plt.xlabel("Nodes")
    plt.ylabel("Iterations")
    plt.savefig('./plots/nodevit.png')

def nodevtime(ccdf : pd.DataFrame):
    nodes = ccdf["# Nodes"].to_numpy()
    time = ccdf["Time"].to_numpy()

    plt.plot(nodes, time)
    plt.title("Nodes vs. Execution time. (10 Changes)")
    plt.xlabel("Nodos")
    plt.ylabel("Time (Segs)")
    plt.savefig('./plots/nodevtime.png')

def changesvtime(cndf : pd.DataFrame):
    changes = cndf["# Changes"].to_numpy()
    time = cndf["Time"].to_numpy()
    plt.plot(changes, time)
    plt.title("Changes vs. Execution time. (200 Nodes)")
    plt.xlabel("Changes")
    plt.ylabel("Time (Segs)")
    plt.savefig('./plots/changesvtime.png')

def main():
    df = pd.read_csv('Data.csv')
    ccdf = df[df['# Changes'] == 10]
    cndf = df[df['# Nodes'] == 200]
    nodevit(ccdf)
    plt.clf()
    nodevtime(ccdf)
    plt.clf()
    changesvtime(cndf)
    # print(sum(df['Tiempo']))

if "__main__" == __name__:
    main()

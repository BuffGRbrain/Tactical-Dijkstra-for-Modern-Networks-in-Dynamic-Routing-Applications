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

def bigplot(df : pd.DataFrame):
    changes = [20,50,80,100]
    css = [df[df['# Changes'] == i] for i in changes]
    # 4 x 1 sub plot nodes vs iterations
    fig, axs = plt.subplots(1, 4, figsize=(16,7))
    for i, ax in enumerate(axs):
        ax.plot(css[i]['# Nodes'], css[i]['Iterations'])
        ax.set_title(f"{changes[i]} Changes.", pad = 10)
        ax.set_xlabel("Nodes")
        ax.set_ylabel("Iterations")
    # get the max time
    max_time = round(max([max(css[i]['Time']) for i in range(4)]))
    # Name the figure
    fig.suptitle("Nodes vs. Iterations. (20,50,80,100 Changes)")
    # add a footnote
    fig.text(0.5, 0.01, f"Max time {max_time//60} Minutes {max_time%60} Seconds", ha='center', fontsize=10)
    plt.savefig('./plots/bigplot.png')


def main():
    df = pd.read_csv('Data.csv')
    #ccdf = df[df['# Changes'] == 10]
    #cndf = df[df['# Nodes'] == 200]
    #nodevit(ccdf)
    #plt.clf()
    #nodevtime(ccdf)
    #plt.clf()
    #changesvtime(cndf)
    ## print(sum(df['Tiempo']))
    bigplot(df)

if "__main__" == __name__:
    main()
    # bigplot()

import numpy as np
import sys
from pathlib import Path
data_folder = Path("data")

def createH(inputFile):
    text = None
    with open(data_folder/inputFile, 'r') as f:
        text = f.read()
        lines = text.splitlines()
        nodes_count = int(lines.pop(0))
        H = np.zeros((nodes_count,nodes_count))
        x = 0
        for line in lines:
            elems = line.split(' ')
            for elem in elems:
                if elem == '': break
                split = elem.split(':')
                y = int(split[0])
                outlinks_cnt = int(split[1])
                H[x,y] = outlinks_cnt/len(elems)
            x=x+1
    print("H:\n{}\n".format(H))
    return(H)

def createS(H):
    S = H.copy()
    for i, row in enumerate(S):
        if row.sum() == 0:
            S[i] = np.full(len(row),1/len(row))
    print("S:\n{}\n".format(S))
    return(S)

def createG(S,alpha):
    size = S.shape[0]
    G = alpha*S + np.full((size,size),1)*(1 - alpha)/size
    print("G:\n{}\n".format(G))
    return(G)


def computePR(M, iterations):
    size = M.shape[0]
    pagerank = np.zeros(size)
    pagerank[0] = 1

    for i in range(iterations):
        pagerank = pagerank.transpose() @ M

    return pagerank


if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit('Gimme input file from data folder')
    inputFile = sys.argv[1]
    alpha = 0.85
    iterations = 16
    H = createH(inputFile)
    print("Pagerank(H):")
    print(computePR(H, iterations))
    print('\n'+("#"*30)+'\n')

    S = createS(H)
    print("Pagerank(S):")
    print(computePR(S, iterations))

    print('\n'+("#"*30)+'\n')
    G = createG(S,alpha)
    print("Pagerank(G):")
    print(computePR(G, iterations))
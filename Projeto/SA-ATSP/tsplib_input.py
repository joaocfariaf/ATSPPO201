import sys, atsp
import os as os

def tsplib(content, f=1, r=None, learning_plot=False):
    idx = content.index('DIMENSION:') + 1
    n = int(content[idx])
    idx = content.index('EDGE_WEIGHT_FORMAT:') + 1
    if content[idx] != 'FULL_MATRIX':
        return [], 0
    idx = content.index('EDGE_WEIGHT_SECTION') + 1
    inf = int(content[idx])
    data = []
    for i in range(n):
        if len(content) > idx + n:
            data.append(list(map(int, content[idx:idx + n])))
        else:
            return [], 0
        idx += n

    for j in range (len(data)):
        print(data[j])
        print('\n')
    

    _atsp = atsp.SA(data, initial_fitness=f, infinity=inf, regularization_bound=r, learning_plot=learning_plot)
    return _atsp.solve()


for file in os.listdir("../Exemplos"):
    filex = "../Exemplos/" + file
    with open(filex, 'r') as fp:
        print(filex)
        file_content = fp.read().split()
        res = tsplib(file_content, learning_plot=True)
        solutionFile = "Sols/" + file.split('.')[0] + ".sol"
        sol = open(solutionFile, 'a')
        sol.write(str(res[1]))
        sol.write('\n')
        sol.write(str(res[0]))
        sol.write('\n')
        sol.close()
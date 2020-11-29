from itertools import combinations, product
import os as os

def tsplib(content):
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

    # for j in range(len(data)):
    #     print(data[j])
    #     print('\n')
    return data
    # _atsp = atsp.SA(data, initial_fitness=f, infinity=inf, regularization_bound=r, learning_plot=learning_plot)
    # return _atsp.solve()

# Retorna a distância entre as cidades 1 e 2 - basta pegar na posição
def TSPdistance(distanceMatrix, city1, city2, cheap = -1):
    ATSPsize = len(distanceMatrix)
    if (abs(city1 - city2) == ATSPsize):
        return cheap
    elif (city1 >= ATSPsize and city2 < ATSPsize):
        return distanceMatrix[city1 - ATSPsize][city2]
    elif (city2 >= ATSPsize and city1 < ATSPsize):
        return distanceMatrix[city2 - ATSPsize][city1]
    else:
        return 99999

for file in os.listdir("../Exemplos"):
    filex = "../Exemplos/" + file
    with open(filex, 'r') as fp:
        file_content = fp.read().split()
        data = tsplib(file_content)

        # Dicionario com as distâncias entre cidades
        TSPdimension = 2 * (len(data))
        capitals = list(range(TSPdimension))
        dist = {(c1, c2): TSPdistance(data, c1, c2) for c1, c2 in product(capitals, capitals) if c1 != c2}

        dist = {}
        for c1, c2 in product(capitals, capitals):
            d = TSPdistance(data, c1, c2)
            if (c1 != c2):
                dist[(c1, c2)] = d

        tspFile = "ConvertedToTSP/" + file.split('.')[0] + ".tsp"
        f = open(tspFile, "w")
        f.write("NAME:%6s" % file.split('.')[0]+" \nTYPE: TSP\nCOMMENT: NO_COMMENT\n")
        f.close()
        f = open(tspFile, "a")
        f.write("DIMENSION:")
        f.write('%4s' % str(TSPdimension))
        f.write("\nEDGE_WEIGHT_TYPE: EXPLICIT\nEDGE_WEIGHT_FORMAT: FULL_MATRIX\nDISPLAY_DATA_TYPE: NO_DISPLAY\nEDGE_WEIGHT_SECTION\n")
        for i in range(TSPdimension):
            for k in range(TSPdimension):
                f.write('%6s' % str(TSPdistance(data, i, k)))
            f.write("\n")

        f.write("EOF")
        f.close()
        # Roda o concorde e guarda a solução apenas num lugar específico
        os.system("./concorde -x -o Sols/" + file.split('.')[0] + "sol " + tspFile)
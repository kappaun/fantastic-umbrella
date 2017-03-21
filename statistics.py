import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def plot_heatmap(filename):
    pass
if __name__ == "__main__":

    '''
        lendo os resultados e armazenando em um dicionario
    '''
    data = []
    # f = open("Results/result_new_omd.csv")
    f = open("result_sts.csv")
    for line in f:
        vec = line.split(";")
        vec[2] = float(vec[2])
        vec[3] = float(vec[3])
        data.append(vec)
    data_points = {}
    for d in data:
        try:
            data_points[d[0]+'_'+d[1]][0].append(d[2])
            data_points[d[0]+'_'+d[1]][1].append(d[3])
        except KeyError:
            data_points[d[0]+'_'+d[1]] = [[],[]]
            data_points[d[0]+'_'+d[1]][0].append(d[2])
            data_points[d[0]+'_'+d[1]][1].append(d[3])


    for key in data_points:
        aux_array = np.array(data_points[key])
        if key.split('_')[1] == '0.1':
            print key.split('_'), stats.ttest_rel(aux_array[0], aux_array[1])[1]

from ctypes import cdll
import sklearn
from numpy.ctypeslib import ndpointer
import numpy as np
import ctypes
import random
from pyswarm import pso
from sklearn.svm import SVC
import pandas as pd

report = open("report","w")

def init():
    lib = cdll.LoadLibrary('./libopt.so')
    lib.object_function.argtypes = [ctypes.c_int, ctypes.c_float]
    lib.object_function.restype = ctypes.c_double
    return lib

def data_preparation(Xfile, yfile):
    Xf = open(Xfile)
    yf = open(yfile)
    X = []
    y = []
    for line in Xf:
        temp = [int(x) for x in line.split(',')]
        X.append(temp)
    y = yf.readline().replace('\n','').split(',')

    X = np.array(X)
    y = np.array(y)

    positions = range(len(X))

    sample = list(random.sample(positions, int(0.7*len(X))))
    sample.sort()

    X_train = X[sample]
    y_train = y[sample]

    complement = [x for x in range(len(X)) if x not in sample]

    X_test = X[complement]
    y_test = y[complement]

    wX = open("temp_data/X_train", 'w')
    wy = open("temp_data/y_train", 'w')
    wXt = open("temp_data/X_test", 'w')
    wyt = open("temp_data/y_test", 'w')

    for x in X_train:
        wX.write(','.join([str(i) for i in list(x)])+'\n')
    for x in X_test:
        wXt.write(','.join([str(i) for i in list(x)])+'\n')
    wy.write(','.join(y_train))
    wyt.write(','.join(y_test))

    wX.close()
    wXt.close()
    wy.close()
    wyt.close()


def object_function(point):
    arg1, arg2 = int(point[0]), point[1]
    value = lib.object_function(arg1, arg2)
    r = str(arg1)+';'+str(arg2)+';'+str(value)+'\n'
    report.write(r)
    report.flush()
    return value



if __name__ == '__main__':
    data_preparation("data/imdb_cpp_X.csv", "data/imdb_cpp_y.csv")
    lib = init()
    # print lib.object_function(28,0.1)
    pso(object_function, [2,0.01], [32,0.99], processes = 1, maxiter=40, swarmsize = 20)
    # df1 = pd.read_csv("temp_data/X_train",header=None)
    # df2 = pd.read_csv("temp_data/y_train",header=None)
    # X = np.array(df1)
    # y = list(np.array(df2)[0])
    # print object_function_svm([])

    # pso(object_function_svm, [2,0.01], [32,0.99], processes = 4, maxiter=40, swarmsize = 20)



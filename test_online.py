from ctypes import cdll
from numpy.ctypeslib import ndpointer
import numpy as np
import ctypes
import time
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pickle



# exit(0)

def init():
    lib = cdll.LoadLibrary('./libopt.so')

    lib.object_function.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int]
    lib.object_function.restype = ctypes.c_double

    lib.get_position_ypred_global.argtypes = [ctypes.c_int]
    lib.get_position_ypred_global.restype = ctypes.c_char_p
    
    lib.get_position_y_global.argtypes = [ctypes.c_int]
    lib.get_position_y_global.restype = ctypes.c_char_p

    lib.get_pred_size.argtypes = []
    lib.get_pred_size.restype = ctypes.c_int

    lib.get_time_train.argtypes = []
    lib.get_time_train.restype = ctypes.c_double

    lib.get_time_predict.argtypes = []
    lib.get_time_predict.restype = ctypes.c_double

    return lib

if __name__ == '__main__':

    try:
        pkl_file = open('data.pkl', 'rb')
        real, pred = pickle.load(pkl_file)
        print "file found!"
    except:   
        print "file not found!" 
        pfile = open('data.pkl', 'wb')
        # time1 = time.time()
        lib = init()
        real = []
        pred = []
        print lib.object_function(18, 0.0981351353166, 0.4, 39, 2679)
        size = lib.get_pred_size()
        # print 'size: ', size
        # print lib.get_position_ypred_global(1)
        # print lib.get_position_y_global(0)
        for i in xrange(size):
            pred.append(lib.get_position_ypred_global(i))
            real.append(lib.get_position_y_global(i))

        print 'general accuracy: ',  accuracy_score(real, pred)

        print lib.get_time_train()/size, "<-- time train"
        print lib.get_time_predict()/size, "<-- time predict"


        pickle.dump((real, pred), pfile)

    accs = []
    for i in xrange(2,len(pred),10):
        try:
            accs.append(  accuracy_score(real[i-50:i], pred[i-50:i] ) )
        except:
            accs.append(  accuracy_score(real[:i], pred[:i] ) )

    # print accs
    plt.xlabel("Iteration", fontsize = 16)
    plt.ylabel("Accuracy", fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.plot(np.arange(len(accs))*10, accs, c="gray")
    plt.show()
    print 'overal accuracy: ', accuracy_score(real, pred )
    time_train = lib.get_time_train()/size
    time_predict = lib.get_time_predict()/size
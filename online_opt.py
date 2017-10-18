from ctypes import cdll
from numpy.ctypeslib import ndpointer
import numpy as np
import ctypes
from pyswarm import pso

report = open("report_online2","w")
def init():
    lib = cdll.LoadLibrary('./libopt.so')
    lib.object_function.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int]
    lib.object_function.restype = ctypes.c_double
    return lib

def object_function(point):
    arg1, arg2, arg3, arg4, arg5 = int(point[0]), point[1], point[2], int(point[3]), int(point[4])
    value = lib.object_function(arg1, arg2, arg3, arg4, arg5)
    # print value
    r = str(arg1)+';'+str(arg2)+';'+str(arg3)+';'+str(arg4)+';'+str(arg5)+';'+str(value)+'\n'
    report.write(r)
    report.flush()
    return -value

if __name__ == '__main__':
    lib = init()
    # object_function([32,0.99,0.99,50,3000])
    pso(object_function, [2,0.01,0.01,2,900], [32,0.7,0.5,50,3000], processes = 1, maxiter=10, swarmsize = 40)

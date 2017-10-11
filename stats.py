import numpy as np
from ctypes import cdll
import ctypes
import sklearn
from sklearn.svm import SVC
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import time

baseline = 0

def linear_svm_evaluation():
    print 'Starting SVM...'
    global baseline 

    df1 = pd.read_csv("temp_data/X_test",header=None)
    df2 = pd.read_csv("temp_data/y_test",header=None)

    X = np.array(df1)
    y = list(np.array(df2)[0])

    baseline = y.count(1)/float(y.count(1) + y.count(-1))

    accs = []
    timetrain = []
    timetest = []
    for i in xrange(100):

        svm = SVC(kernel = 'linear')
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y,test_size=0.05)

        time1 = time.time()
        svm.fit(X_train,y_train)
        timetrain.append(time.time() - time1)
        print "svm training: ", timetrain[-1]

        time1 = time.time()
        ypred = svm.predict(X_test)
        timetest.append(time.time() - time1)

        accuracy = sklearn.metrics.accuracy_score(y_test, ypred)
        accs.append(accuracy)

    return accs, timetrain, timetest

def nb_evaluation():
    print 'Starting Naive Bayes...'

    df1 = pd.read_csv("temp_data/X_test",header=None)
    df2 = pd.read_csv("temp_data/y_test",header=None)

    X = np.array(df1)
    y = list(np.array(df2)[0])


    accs = []
    timetrain = []
    timetest = []
    for i in xrange(100):

        nb = MultinomialNB()
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y,test_size=0.05)

        time1 = time.time()
        nb.fit(X_train,y_train)
        timetrain.append(time.time() - time1)
        print "naive bayes training: ", timetrain[-1]

        time1 = time.time()
        ypred = nb.predict(X_test)
        timetest.append(time.time() - time1)

        accuracy = sklearn.metrics.accuracy_score(y_test, ypred)
        accs.append(accuracy)

    return accs, timetrain, timetest

def init():
    lib = cdll.LoadLibrary('./libopt.so')
    lib.testing.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_int]
    lib.testing.restype = ctypes.c_double
    lib.getdev.argtypes = []
    lib.getdev.restype = ctypes.c_double
    lib.gettime.argtypes = []
    lib.gettime.restype = ctypes.c_double
    lib.gettimepredict.argtypes = []
    lib.gettimepredict.restype = ctypes.c_double
    return lib

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.4f' % float(height),
                ha='center', va='bottom',fontsize=16)


if __name__ == '__main__':
    

    f = open("report2")
    res = []
    for line in f:
        vec = line.split(';')
        vec[0] = int(vec[0])
        vec[1] = float(vec[1])
        vec[2] = float(vec[2])
        res.append(vec)

    res = np.array(res)
    bestmaxvalue = 0
    values = []
    for i in xrange(len(res)):
        maxvalue = max(res[:i+1,2])
        values.append(maxvalue)
        if maxvalue > bestmaxvalue:
            bestmaxvalue = maxvalue
            optimum = res[i]

    lib = init()

    print optimum

    # accnew = lib.testing(int(optimum[0]), float(optimum[1]),1)
    accnew = lib.testing(int(optimum[0]), float(optimum[1]),1)
    devnew = lib.getdev()
    traintimenew = lib.gettime()
    testtimenew = lib.gettimepredict()
    # print timenew

    accclassic = lib.testing(int(optimum[0]), float(optimum[1]),0)
    devlassic = lib.getdev()
    traintimeclassic = lib.gettime()
    testtimeclassic = lib.gettimepredict()
    # print timeclassic

    out = linear_svm_evaluation()
    accs = out[0]
    traintimesvm = np.mean(out[1])
    testtimesvm = np.mean(out[2])

    accsvm, devsvm = np.mean(accs), np.std(accs)

    out = nb_evaluation()
    accs = out[0]
    traintimenb = np.mean(out[1])
    testtimenb = np.mean(out[2])


    accnb, devnb = np.mean(accs), np.std(accs)

    accuracy_list = [accnew, accclassic, accsvm, accnb]
    std_list = [devnew, devlassic, devsvm, devnb]
    print "STD: ", std_list



    bar_width = 0.35
    print baseline
    baseline = max([baseline, 1.0 - baseline])
    print baseline
    plt.figure(figsize=(7,5))
    plt.axhline(baseline, color='black', ls='dashed', label = 'Baseline', linewidth = 3, alpha = 0.5)
    rects = plt.bar(range(0,4),[accnew, accclassic, accsvm, accnb], 0.5, color='gray')
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.xticks(np.arange(0,4), ('WiSARD-i', 'WiSARD', 'SVM', 'Naive Bayes'))
    plt.title("IMDB Dataset", fontsize = 20)
    plt.xlabel("Models", fontsize = 16)
    plt.ylabel("Accuracy", fontsize = 16)
    plt.ylim(0,1)
    plt.errorbar(range(0,4), [rect.get_height() for rect in rects], yerr=std_list, fmt='o', c= 'black', alpha=0.6)
    params = {'legend.fontsize': 15}
    plt.rcParams.update(params)
    legend = plt.legend(loc=3)
    autolabel(rects)

    plt.show()

    plt.figure(figsize=(7,5))
    plt.title("Optimization: IMDB Dataset", fontsize = 20)
    plt.xlabel("Iteration", fontsize = 16)
    plt.ylabel("Accuracy", fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=15)

    data = [values[i] for i in xrange(0,len(values),20)]
    plt.plot(range(len(data)), [values[i] for i in xrange(0,len(values),20)], linewidth = 2, c='gray')
    plt.show()

print "Model Order: ", "new | classic | svm | nb"
print "Training Times: %f, %f, %f, %f"%(traintimenew * 10**(-9), traintimeclassic * 10**(-9), traintimesvm, traintimenb)
print "Testing Times: %f, %f, %f, %f"%(testtimenew * 10**(-9), testtimeclassic * 10**(-9), testtimesvm, testtimenb)
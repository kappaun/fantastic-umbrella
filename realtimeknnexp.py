from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import accuracy_score
import numpy as np
import time

data = []
y = []
def read():
    f1 = open("data/spam_nominal_X.csv")
    f2 = open("data/spam_nominal_y.csv")
    global data
    global y
    y = f2.readline()
    y = [int(x) for x in y.split(',')]
    # i = 0
    for line in f1:
        # i+=1
        line = [int(x) for x in line.split(',')]
        data.append(line)
        # if i == 200:
        #     break
        
    print 'Finished to read data'

    
def object_function(param):
    init_pos = 2611
    window_size = param[0]
    k = param[1]
    inital_set = data[:init_pos]
    targets = y[:init_pos]
    preds = []
    times = []
    for i in xrange(init_pos, len(data)):
        clf = KNN(k)
        clf.fit(inital_set[-window_size:], targets[-window_size:])
        time1 = time.time()
        pred = clf.predict([data[i]])[0]
        times.append( time.time() - time1)
        preds.append(pred)
        inital_set.append(data[i])
        targets.append(pred)

    return accuracy_score(y[init_pos:], preds), np.mean(times)


if __name__ == '__main__':
    read()
    w = 1000
    k = 10
    result = object_function([w, k])
    fileoutput = open("realtimeonlineknnresults2.csv","w")
    fileoutput.write(str(w)+';'+str(k)+';'+str(result[0])+';'+str(result[1])+'\n')

    # window = range(2,20)
    # for w in window:
    #     for k in range(1,w+1):
    #         print w, k, ' iteration!'
    #         try:
    #             result = object_function([w, k])
    #             fileoutput.write(str(w)+';'+str(k)+';'+str(result[0])+';'+str(result[1])+'\n')
    #         except Exception as e:
    #             print e

    # print object_function([])

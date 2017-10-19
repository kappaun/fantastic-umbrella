from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import accuracy_score

data = []
y = []
def read():
    f1 = open("data/spam_nominal_X.csv")
    f2 = open("data/spam_nominal_y.csv")
    global data
    global y
    y = f1.readline()
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
    for i in xrange(init_pos, len(data)):
        clf = KNN(k)
        clf.fit(inital_set[-window_size:], targets[-window_size:])
        pred = clf.predict([data[i]])[0]
        preds.append(pred)
        inital_set.append(data[i])
        targets.append(pred)
    return accuracy_score(y[init_pos:], preds)


if __name__ == '__main__':
    read()
    pso(object_function, [10,2], [2611,1000], processes = 4, maxiter=10, swarmsize = 40)
    # print object_function([])

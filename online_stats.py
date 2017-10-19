import numpy as np

f = open("report_online2")

data = []
for line in f:
    line = line.split(';')
    # extern "C" double object_function(int numBitsAddr, 
    #                                  float confidenceThreshold, 
    #                                  float ssthreshold, 
    #                                  int onlineMax,
    #                                  int init_size)
    line[0] = int(line[0])
    line[1] = float(line[1])
    line[2] = float(line[2])
    line[3] = int(line[3])
    line[4] = int(line[4])
    line[5] = float(line[5])
    data.append(line)

data = np.array(data)

print np.argmax(data[:,5])
best = data[np.argmax(data[:,5])]
print 'Number of Bits: ', int(best[0])
print 'confidenceThreshold: ', float(best[1])
print 'ssthreshold: ', float(best[2])
print 'onlineMax: ', int(best[3])
print 'Inital size: ', int(best[4])
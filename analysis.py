import numpy as np

f = open("report_online2")
data = []
res = []
for line in f:
	line = line.split(';')
	res.append(float(line[-1]))
	data.append(line[:-1])

for i in xrange(len(res)):
	if res[i] > 0.53:
		print res[i], data[i]

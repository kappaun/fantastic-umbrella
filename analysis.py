import numpy as np
import matplotlib.pyplot as plt

f = open("report_online2")
data = []
res = []
for line in f:
	line = line.split(';')
	res.append(float(line[-1]))
	data.append(line[:-1])

amax = 0
opt = []
for i in xrange(0,len(res),40):
	m = max(res[i:i+40])
	if m > amax:
		opt.append(m)
		amax = m
	else:
		opt.append(amax)

plt.figure(figsize=(7,5))
plt.title("Optimization: Online Spam Dataset Classification", fontsize = 20)
plt.xlabel("Iteration", fontsize = 16)
plt.ylabel("Accuracy", fontsize = 16)
plt.tick_params(axis='both', which='major', labelsize=15)

# data = [values[i] for i in xrange(0,len(values),20)]

plt.plot(range(len(opt)), opt, linewidth = 2, c='gray')
plt.show()
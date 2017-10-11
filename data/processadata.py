f = open("cpp_usenet_recurrent3.3.data")
Xf = open("usenet_X.csv",'w')
yf = open("usenet_y.csv",'w')
d = {}

for linha in f:
    vec = linha.split(",")
    target = vec[-1]
    data = vec[:-1]
    Xf.write(",".join(data))
    Xf.write("\n")
    y = target.replace('\n','')
    try:
        d[y] += 1
    except:
        d[y] = 1

    if y == 'yes':
        yf.write('1')
    elif y == 'no':
        yf.write('0')
    else:
        print 'erro'
    yf.write(',')

print d
Xf.close()
yf.close()
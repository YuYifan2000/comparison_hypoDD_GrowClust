from datetime import datetime
import numpy as np

input = '../hypodd/event.sel'
output = './evlist.txt'
f1 = open(input, 'r')
f2 = open(output,'w')
contents = f1.readlines()
for i in contents:
	content = i.split()
	yr = int(content[0])//10000
	mo = (int(content[0])%10000)//100
	day = (int(content[0])%10000)%100
	hr = int(content[1])//1000000
	min = (int(content[1])%100000)//10000
	sec = float((int(content[1])%100000)%10000)/100.
	la = content[2]
	lo = content[3]
	dep = content[4]
	mag = content[5]
	evid = content[9]
	setence = f'{yr} {mo} {day} {hr} {min} {sec} {la} {lo} {dep} {mag} 0.000 0.000 0.000 {evid}\n'
	f2.write(setence)
f1.close()
f2.close()

# form station.dat
f = open('./station.dat', 'w+')
stas = np.load('../o_station.npy')
num_sta = len(stas)
for i in range(0, num_sta):
    sta = 'ST' + str(i)
    lat = stas[i,0]
    lon = stas[i,1]
    ele = stas[i,2]
    f.write(f'{sta:4s} {lat:7.4f} {lon:8.4f} {ele:4.0f}\n')
f.close()


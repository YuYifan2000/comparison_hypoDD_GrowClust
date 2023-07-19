import numpy as np
import matplotlib.pyplot as plt

f = open('vjma2001', 'r')
Lines = f.readlines()
v = []
d = []
vs = []
for i in range(0,60):
	line = Lines[i].split()
	d.append(float(line[2]))
	v.append(float(line[0]))
	vs.append(float(line[1]))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(v,d,label='Vp')
ax.plot(vs,d,label='Vs')
ax.set_xlabel('Velocity(m/s)')
ax.set_ylabel('Depth (km)')
ax.invert_yaxis()
ax.legend()
ax.set_xlim(2.5,7.2)
ax.set_ylim(32,0)
plt.savefig('1dvelo.png', dpi=500)
plt.close()


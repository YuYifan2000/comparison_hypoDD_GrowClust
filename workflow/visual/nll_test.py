import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
matplotlib.use('agg')
stations = np.load('../o_station.npy')
sources = np.load('../o_source.npy')
sources[:,2] = sources[:,2]/1000.
# NLL
f = open('../NLL/loc/alaska.sum.grid0.loc.hyp', 'r')
Lines = f.readlines()
f.close()
nll_lat = []
nll_lon = []
nll_dep = []
for line in Lines:
    if 'GEOGRAPHIC' in line:
        nll_lat.append(float(line.split()[9]))
        nll_lon.append(float(line.split()[11]))
        nll_dep.append(float(line.split()[13]))
print(len(nll_lat))
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])

ax = fig.add_subplot(gs[0,0])
for i in range(0, len(sources[:100])):

    ax.quiver(sources[i,1], sources[i,0], nll_lon[i]-sources[i,1], nll_lat[i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.002)

ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(sources[:100])):
    ax.quiver(sources[i,2], sources[i,0], nll_dep[i]-sources[i,2], nll_lat[i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.003)

ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(sources[:100])):
    ax.quiver(sources[i,1], sources[i,2], nll_lon[i]-sources[i,1], nll_dep[i]-sources[i,2],angles='xy', scale_units='xy', scale=1, width=0.001)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./nll.png', dpi=300)
plt.close()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
matplotlib.use('agg')

stations = np.load('../o_station.npy')
sources = np.load('../o_source.npy')
catalog_gc = pd.read_csv(f"../out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_vele = pd.read_csv("../hypoDD.loc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
# hypoinverse
catalog_hypoinverse = pd.read_csv("../catOut.sum", sep="\s+")
catalog_hypoinverse["time"] = (catalog_hypoinverse['DATE']+catalog_hypoinverse["TIME"]).apply(lambda x: datetime.strptime(x, "%Y/%m/%d%H:%M"))
# NLL
f = open('../NLL/loc/sum.hyp', 'r')
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
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['LAT', 'LON', 'DEPTH'])


# original locations
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(sources[:, 1], sources[:,0], s=4, c='k')
ax.scatter(stations[:,1], stations[:,0], s=11, marker='^')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(sources[:,2], sources[:,0], s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(sources[:,1], sources[:,2], s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_sources_stations.png', dpi=300)
plt.close()

# velest

fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(catalog_vele['LON'], catalog_vele['LAT'], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(catalog_vele['DEPTH'], catalog_vele['LAT'], s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(catalog_vele['LON'], catalog_vele['DEPTH'], s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./velest.png', dpi=300)
plt.close()


# hypodd
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(catalog_dd['DEPTH'], catalog_dd['LAT'], s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(catalog_dd['LON'], catalog_dd['DEPTH'], s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./dd.png', dpi=300)
plt.close()

# growclust

fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(catalog_gc['depR'], catalog_gc['latR'], s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(catalog_gc['lonR'], catalog_gc['depR'], s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./gc.png', dpi=300)
plt.close()


# original v.s. velest
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])

ax = fig.add_subplot(gs[0,0])
for i in range(0, len(catalog_vele)):
    ax.quiver(sources[catalog_vele['ID'][i]-1,1], sources[catalog_vele['ID'][i]-1,0], catalog_vele['LON'][i]-sources[catalog_vele['ID'][i]-1,1], catalog_vele['LAT'][i]-sources[catalog_vele['ID'][i]-1,0],angles='xy', scale_units='xy', scale=1, width=0.002,headwidth=3)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(catalog_vele)):
    ax.quiver(sources[catalog_vele['ID'][i]-1,2], sources[catalog_vele['ID'][i]-1,0], catalog_vele['DEPTH'][i]-sources[catalog_vele['ID'][i]-1,2], catalog_vele['LAT'][i]-sources[catalog_vele['ID'][i]-1,0],angles='xy', scale_units='xy', scale=1, width=0.003,headwidth=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(catalog_vele)):
    ax.quiver(sources[catalog_vele['ID'][i]-1,1], sources[catalog_vele['ID'][i]-1,2], catalog_vele['LON'][i]-sources[catalog_vele['ID'][i]-1,1], catalog_vele['DEPTH'][i]-sources[catalog_vele['ID'][i]-1,2],angles='xy', scale_units='xy', scale=1, width=0.002,headwidth=3)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_velest.png', dpi=300)
plt.close()


# original v.s. hypoDD
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])

ax = fig.add_subplot(gs[0,0])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == i+1
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,0], tmp['LON']-sources[i,1], tmp['LAT']-sources[i,0],angles='xy', scale_units='xy', scale=1,width=0.002)
    else:
        ax.scatter(sources[i,1], sources[i,0], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == i+1
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,2], sources[i,0], tmp['DEPTH']-sources[i,2], tmp['LAT']-sources[i,0],angles='xy', scale_units='xy', scale=1,width=0.003)
    else:
        ax.scatter(sources[i,2], sources[i,0], s=3, c='k')
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == i+1
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,2], tmp['LON']-sources[i,1], tmp['DEPTH']-sources[i,2],angles='xy', scale_units='xy', scale=1,width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,2], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_hypodd.png', dpi=300)
plt.close()

# original v.s. growclust
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])

ax = fig.add_subplot(gs[0,0])
for i in range(0, len(sources)):
    if i+1 == catalog_gc['evid'][i]:
        ax.quiver(sources[i,1], sources[i,0], catalog_gc['lonR'][i]-sources[i,1], catalog_gc['latR'][i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.002)
    else:
        ax.scatter(sources[i,1], sources[i,0], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(sources)):
    if i+1 == catalog_gc['evid'][i]:
        ax.quiver(sources[i,2], sources[i,0], catalog_gc['depR'][i]-sources[i,2], catalog_gc['latR'][i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.003)
    else:
        ax.scatter(sources[i,2], sources[i,0], s=3, c='k')
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(sources)):
    if i+1 == catalog_gc['evid'][i]:
        ax.quiver(sources[i,1], sources[i,2], catalog_gc['lonR'][i]-sources[i,1], catalog_gc['depR'][i]-sources[i,2],angles='xy', scale_units='xy', scale=1, width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,2], s=3, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_gc.png', dpi=300)
plt.close()

# NLL

fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(nll_lon, nll_lat, s=4, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(nll_dep, nll_lat, s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(nll_lon, nll_dep, s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./nll.png', dpi=300)
plt.close()



# original v.s nll

fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
for i in range(0, len(sources)):
    ax.quiver(sources[i,1], sources[i,0], nll_lon[i]-sources[i,1], nll_lat[i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.002)

ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(sources)):
    ax.quiver(sources[i,2], sources[i,0], nll_dep[i]-sources[i,2], nll_lat[i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.003)

ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(sources)):
    ax.quiver(sources[i,1], sources[i,2], nll_lon[i]-sources[i,1], nll_dep[i]-sources[i,2],angles='xy', scale_units='xy', scale=1, width=0.001)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_NLL.png', dpi=300)
plt.close()



# 
# hypoinverse
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])
ax = fig.add_subplot(gs[0,0])
ax.scatter(catalog_hypoinverse['LON'], catalog_hypoinverse['LAT'], s=4, c='k')
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
#ax.tick_params(axis='x', labelsize=20)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
ax.scatter(catalog_hypoinverse['DEPTH'], catalog_hypoinverse['LAT'], s=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
ax.scatter(catalog_hypoinverse['LON'], catalog_hypoinverse['DEPTH'], s=2)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./hypoinverse.png', dpi=300)
plt.close()


# original v.s. hypoinverse
fig = plt.figure(figsize=[10,7])
gs = gridspec.GridSpec(2, 2,width_ratios= [3, 1], height_ratios=[3,1])

ax = fig.add_subplot(gs[0,0])

for i in range(0, len(catalog_hypoinverse)):
    ax.quiver(sources[i,1], sources[i,0], catalog_hypoinverse['LON'][i]-sources[i,1], catalog_hypoinverse['LAT'][i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.002,headwidth=3)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([35.45, 36.2])
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude')

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(catalog_hypoinverse)):
    ax.quiver(sources[i,2], sources[i,0], catalog_hypoinverse['DEPTH'][i]-sources[i,2], catalog_hypoinverse['LAT'][i]-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.003,headwidth=3)
ax.set_ylim([35.45, 36.2])
ax.set_xlim([0, 15])
ax.set_xlabel('Depth (km)')
ax.yaxis.tick_right()


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(catalog_hypoinverse)):
    ax.quiver(sources[i,1], sources[i,2], catalog_hypoinverse['LON'][i]-sources[i,1], catalog_hypoinverse['DEPTH'][i]-sources[i,2],angles='xy', scale_units='xy', scale=1, width=0.002,headwidth=3)
ax.set_xlim([-117.9, -117.2])
ax.set_ylim([0, 15])
ax.invert_yaxis()
ax.set_ylabel('Depth (km)')
ax.set_xlabel('Longitude')

plt.tight_layout()
plt.savefig('./original_hypoinverse.png', dpi=300)
plt.close()

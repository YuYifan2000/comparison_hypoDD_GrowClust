import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
matplotlib.use('agg')
import matplotlib.colors as colors

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
f = open('../NLL/loc/ridgecrest.sum.grid0.loc.arc', 'r')
Lines  = f.readlines()
f.close()
nll_lat = []
nll_lon = []
nll_dep = []
for line in Lines:
    if (line[:2] != 'ST') & (line!='\n'):
        nll_lat.append(float(line[16:18])+float(line[19:23])/6000.)
        nll_lon.append(-(float(line[23:26])+float(line[27:31])/6000.))
        nll_dep.append(float(line[32:36])/100.)
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['LAT', 'LON', 'DEPTH'])

# plot parameter
map_lat = [35.47, 36.13]
map_lon = [-117.91, -117.305]
size = 0.2
title_fontsize = 8


# original distribution
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
#ax.set_title('True Location', fontsize=title_fontsize, fontweight="bold")
#ax.scatter(stations[:,1], stations[:,0], s=7, marker='v', alpha=0.7)
ax.scatter(sources[:, 1], sources[:,0], s=size, c='green')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./true_location_mapview.png', dpi=300, transparent=True)
plt.close()

# hypoDD
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
#ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c=catalog_dd['CID'], cmap='Dark2', norm=colors.Normalize(vmin=1, vmax=4))
ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./dd_location_mapview.png', dpi=300, transparent=True)
plt.close()


# growclust
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c='red')
#ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c=catalog_gc['cID'], cmap='tab10', norm=colors.Normalize(vmin=1, vmax=20))
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./gc_location_mapview.png', dpi=300, transparent=True)
plt.close()


# velest
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(catalog_vele['LON'], catalog_vele['LAT'], s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./ve_location_mapview.png', dpi=300, transparent=True)
plt.close()


# hypoinverse
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(catalog_hypoinverse['LON'], catalog_hypoinverse['LAT'], s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./hypo_location_mapview.png', dpi=300, transparent=True)
plt.close()


# Non Lin Loc
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(nll_lon, nll_lat, s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./nll_location_mapview.png', dpi=300, transparent=True)
plt.close()


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
from obspy.geodetics.base import gps2dist_azimuth
matplotlib.use('agg')
import matplotlib.colors as colors
import matplotlib.ticker as ticker

def project_profile(lat, lon):
    lat1 = 36.1
    lon1 = -117.9
    lat2 = 35.5
    lon2 = -117.32
    _,az1, baz1 = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    dist, az2, baz2 = gps2dist_azimuth(lat1, lon1, lat, lon)
    theta = abs(az1 - az2)
    return dist * np.cos(np.deg2rad(theta)) / 1000.



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



# profile
fig = plt.figure(figsize=[9,4], constrained_layout=True)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.001)

map_dist = [0, 90]
map_dep = [15, 0]
size = 0.5
title_fontsize = 8

# original distribution
ax = fig.add_subplot(gs[0,0])
ax.set_title('True Location', fontsize=title_fontsize, fontweight="bold")
for source in sources:
    dist = project_profile(source[0], source[1])
    ax.scatter(dist, source[2], s=size, c='k')
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
#ax.axes.get_xaxis().set_ticklabels([])

# hypoDD
ax = fig.add_subplot(gs[0,1])
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")
for i in range(0, len(catalog_dd)):
    dist = project_profile(catalog_dd.iloc[i]['LAT'], catalog_dd.iloc[i]['LON'])
    #ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='k')
    ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c=catalog_dd.iloc[i]['CID'], cmap='Dark2', norm=colors.Normalize(vmin=1, vmax=4))
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])

# growclust
ax = fig.add_subplot(gs[0,2])
ax.set_title('GrowClust',fontsize=title_fontsize, fontweight="bold")
for i in range(0, len(catalog_gc)):
    dist = project_profile(catalog_gc.iloc[i]['latR'], catalog_gc.iloc[i]['lonR'])
    #ax.scatter(dist, catalog_gc.iloc[i]['depR'], s=size, c='k')
    ax.scatter(dist, catalog_gc.iloc[i]['depR'], s=size, c=catalog_gc.iloc[i]['cID'], cmap='tab10', norm=colors.Normalize(vmin=1, vmax=20))
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])

# velest
ax = fig.add_subplot(gs[1,0])
ax.set_title('VELEST',fontsize=title_fontsize, fontweight="bold")
for i in range(0, len(catalog_vele)):
    dist = project_profile(catalog_vele.iloc[i]['LAT'], catalog_vele.iloc[i]['LON'])
    ax.scatter(dist, catalog_vele.iloc[i]['DEPTH'], s=size, c='k')
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])

# hypoinverse
ax = fig.add_subplot(gs[1,1])
ax.set_title('HypoInverse',fontsize=title_fontsize, fontweight="bold")
for i in range(0, len(catalog_hypoinverse)):
    dist = project_profile(catalog_hypoinverse.iloc[i]['LAT'], catalog_hypoinverse.iloc[i]['LON'])
    ax.scatter(dist, catalog_hypoinverse.iloc[i]['DEPTH'], s=size, c='k')
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# Non Lin Loc
ax = fig.add_subplot(gs[1,2])
ax.set_title('Non_Lin_Loc',fontsize=title_fontsize, fontweight="bold")
for i in range(len(nll_lon)):
    dist = project_profile(nll_lat[i], nll_lon[i])
    ax.scatter(dist, nll_dep[i], s=size, c='k')
ax.set_xlim(map_dist)
ax.set_ylim(map_dep)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])

plt.savefig('./profile.pdf', transparent=True, dpi=300)
plt.close()

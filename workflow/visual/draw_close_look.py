import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
matplotlib.use('agg')
import matplotlib.ticker as ticker
from obspy.geodetics.base import gps2dist_azimuth
def project_profile(lat, lon):
    lat1 = 36.1
    lon1 = -117.9
    lat2 = 35.8
    lon2 = -117.6
    _,az1, baz1 = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    dist, az2, baz2 = gps2dist_azimuth(lat1, lon1, lat, lon)
    theta = abs(az1 - az2)
    return dist * np.cos(np.deg2rad(theta)) / 1000.


sources = np.load('../o_source.npy')
#sources = np.load('../test_source.npy')
catalog_gc = pd.read_csv(f"../out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])

lat_range = [35.78, 36.1]
lon_range = [-117.9, -117.58]
dep_range = [0, 15]
size = 0.3
title_fontsize = 8

idx = np.arange(1, 1001).reshape(1000,1)
sources = np.hstack([sources,idx])
catalog_dd = catalog_dd[catalog_dd['LAT']>lat_range[0]]
catalog_gc = catalog_gc[catalog_gc['latR']>lat_range[0]]
sources = sources[sources[:,0]>lat_range[0]]

fig = plt.figure(figsize=[9,5])
gs = gridspec.GridSpec(2, 4,width_ratios= [2.5, 1.5,2.5,1.5], height_ratios=[2,1.2], hspace=0.1, wspace=0.1)
ax = fig.add_subplot(gs[0,0])
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")
ax.scatter(sources[:, 1], sources[:,0], s=size, c='k')
ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c='crimson')
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
#ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])

ax = fig.add_subplot(gs[0,1])
ax.scatter(sources[:, 2], sources[:,0], s=size, c='k')
ax.scatter(catalog_dd['DEPTH'], catalog_dd['LAT'], s=size, c='crimson')
ax.set_ylim(lat_range)
ax.set_xlim(dep_range)
ax.set_xlabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.tick_right()
ax.axes.get_yaxis().set_ticklabels([])
ax.xaxis.set_tick_params(labelsize=6)


ax = fig.add_subplot(gs[1,0])
ax.scatter(sources[:, 1], sources[:,2], s=size, c='k')
ax.scatter(catalog_dd['LON'], catalog_dd['DEPTH'], s=size, c='crimson')
ax.set_xlim(lon_range)
ax.set_ylim(dep_range)
ax.invert_yaxis()
ax.set_ylabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
#ax.axes.get_xaxis().set_ticks(ticks)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)

# growclust
ax = fig.add_subplot(gs[0,2])
ax.set_title('Growclust', fontsize=title_fontsize, fontweight="bold")
ax.scatter(sources[:, 1], sources[:,0], s=size, c='k')
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c='royalblue')
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.axes.get_yaxis().set_ticklabels([])
ax.axes.get_xaxis().set_ticklabels([])

ax = fig.add_subplot(gs[0,3])
ax.scatter(sources[:, 2], sources[:,0], s=size, c='k')
ax.scatter(catalog_gc['depR'], catalog_gc['latR'], s=size, c='royalblue')
ax.set_ylim(lat_range)
ax.set_xlim(dep_range)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.set_xlabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.yaxis.set_label_position('right')
ax.yaxis.tick_right()
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)

ax = fig.add_subplot(gs[1,2])
ax.scatter(sources[:, 1], sources[:,2], s=size, c='k')
ax.scatter(catalog_gc['lonR'], catalog_gc['depR'], s=size, c='royalblue')
ax.set_xlim(lon_range)
ax.set_ylim(dep_range)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.invert_yaxis()
ax.axes.get_yaxis().set_ticklabels([])
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_tick_params(labelsize=6)


plt.savefig('./north_part.pdf', dpi=500, transparent = True)
plt.close()

# profile and mapview
fig = plt.figure(figsize=[9,5])
gs = gridspec.GridSpec(2, 6,width_ratios= [0.5, 3, 0.5, 0.5, 3,0.5], height_ratios=[2,1.2], hspace=0.2, wspace=0.2)
ax = fig.add_subplot(gs[0,1])
ax.text(-117.9, 36.08, 'B', fontsize=7, fontweight='bold', rotation=45)
ax.text(-117.6, 35.8, 'B\'', fontsize=7, fontweight='bold', rotation=45)
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")
ax.scatter(sources[:, 1], sources[:,0], s=size, c='k')
ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c='crimson')
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
#ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.set_xlabel('Longitude', labelpad=0.1, fontsize=8)
#ax.axes.get_xaxis().set_ticklabels([])

ax = fig.add_subplot(gs[0,4])
ax.set_title('Growclust', fontsize=title_fontsize, fontweight="bold")
ax.scatter(sources[:, 1], sources[:,0], s=size, c='k')
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c='royalblue')
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.set_xlabel('Longitude', labelpad=0.1, fontsize=8)

ax = fig.add_subplot(gs[1,:3])
for source in sources:
    dist = project_profile(source[0], source[1])
    ax.scatter(dist, source[2], s=size, c='k')
for i in range(0, len(catalog_dd)):
    dist = project_profile(catalog_dd.iloc[i]['LAT'], catalog_dd.iloc[i]['LON'])
    #ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='k')
    ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='crimson')
#ax.set_xlim()
ax.set_ylim([13,0])
ax.set_ylabel('Depth (km)',labelpad=0.1, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.set_xlabel('Distance (km)', labelpad=0.1, fontsize=8)


ax = fig.add_subplot(gs[1,3:])
for source in sources:
    dist = project_profile(source[0], source[1])
    ax.scatter(dist, source[2], s=size, c='k')
for i in range(0, len(catalog_gc)):
    dist = project_profile(catalog_gc.iloc[i]['latR'], catalog_gc.iloc[i]['lonR'])
    #ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='k')
    ax.scatter(dist, catalog_gc.iloc[i]['depR'], s=size, c='royalblue')
#ax.set_xlim()
ax.set_ylim([13,0])
#ax.set_ylabel('Depth (km)')
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.set_xlabel('Distance (km)', labelpad=0.1, fontsize=8)
ax.axes.get_yaxis().set_ticklabels([])
plt.savefig('./profile_north_part.png', dpi=300, transparent = True)
plt.close()











fig = plt.figure(figsize=[9,5])
gs = gridspec.GridSpec(2, 4,width_ratios= [2.5, 2,2.5,2], height_ratios=[2,1.2], hspace=0.1, wspace=0.1)
ax = fig.add_subplot(gs[0,0])
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")

for i in range(0, len(sources)):
    index = catalog_dd['ID'] == sources[i,4]
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,0], tmp['LON']-sources[i,1], tmp['LAT']-sources[i,0],angles='xy', scale_units='xy', scale=1,width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,0], s=3, c='k')

ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
#ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.axes.get_xaxis().set_ticklabels([])

ax = fig.add_subplot(gs[0,1])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == sources[i,4]
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,2], sources[i,0], tmp['DEPTH']-sources[i,2], tmp['LAT']-sources[i,0],angles='xy', scale_units='xy', scale=1,width=0.001)
    else:
        ax.scatter(sources[i,2], sources[i,0], s=3, c='k')
ax.set_ylim(lat_range)
ax.set_xlim(dep_range)
ax.set_xlabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.tick_right()
ax.axes.get_yaxis().set_ticklabels([])
ax.xaxis.set_tick_params(labelsize=6)


ax = fig.add_subplot(gs[1,0])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == sources[i,4]
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,2], tmp['LON']-sources[i,1], tmp['DEPTH']-sources[i,2],angles='xy', scale_units='xy', scale=1,width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,2], s=3, c='k')
ax.set_xlim(lon_range)
ax.set_ylim(dep_range)
ax.invert_yaxis()
ax.set_ylabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
#ax.axes.get_xaxis().set_ticks(ticks)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)

# growclust
ax = fig.add_subplot(gs[0,2])
ax.set_title('Growclust', fontsize=title_fontsize, fontweight="bold")
for i in range(0, len(sources)):
    index = catalog_gc['evid'] == sources[i,4]
    tmp = catalog_gc.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,0], tmp['lonR']-sources[i,1], tmp['latR']-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,0], s=3, c='k')

ax.set_xlim(lon_range)
ax.set_ylim(lat_range)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.axes.get_yaxis().set_ticklabels([])
ax.axes.get_xaxis().set_ticklabels([])

ax = fig.add_subplot(gs[0,3])
for i in range(0, len(sources)):
    index = catalog_gc['evid'] == sources[i,4]
    tmp = catalog_gc.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,2], sources[i,0], tmp['depR']-sources[i,2], tmp['latR']-sources[i,0],angles='xy', scale_units='xy', scale=1, width=0.001)
    else:
        ax.scatter(sources[i,2], sources[i,0], s=3, c='k')
ax.set_ylim(lat_range)
ax.set_xlim(dep_range)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.set_xlabel('Depth (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Latitude', labelpad=0.05, fontsize=8)
ax.yaxis.set_label_position('right')
ax.yaxis.tick_right()
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)

ax = fig.add_subplot(gs[1,2])
for i in range(0, len(sources)):
    index = catalog_gc['evid'] == sources[i,4]
    tmp = catalog_gc.where(index).dropna()
    if not tmp.empty:
        ax.quiver(sources[i,1], sources[i,2], tmp['lonR']-sources[i,1], tmp['depR']-sources[i,2],angles='xy', scale_units='xy', scale=1, width=0.001)
    else:
        ax.scatter(sources[i,1], sources[i,2], s=3, c='k')
ax.set_xlim(lon_range)
ax.set_ylim(dep_range)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.invert_yaxis()
ax.axes.get_yaxis().set_ticklabels([])
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
ax.xaxis.set_tick_params(labelsize=6)


plt.savefig('./vector_north_part.pdf', dpi=500, transparent = True)
plt.close()

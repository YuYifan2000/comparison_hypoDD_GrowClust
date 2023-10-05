import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
matplotlib.use('agg')
import matplotlib.colors as colors
from obspy.geodetics.base import gps2dist_azimuth
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
catalog_gc = pd.read_csv(f"../growclust/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypodd/hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
# velest
velest_lat = []
velest_lon = []
velest_dep = []
f = open('../velest/hypocenter_.CNV', 'r')
lines = f.readlines()
f.close()
for line in lines:
    if line[0] == ' ':
        velest_lat.append(float(line.split()[3][:-1]))
        velest_lon.append(-float(line.split()[4][:-1]))
        velest_dep.append(float(line.split()[5]))
velest = np.stack((np.array(velest_lat).T, np.array(velest_lon).T, np.array(velest_dep).T), axis=1)
catalog_vele = pd.DataFrame(velest, columns=['LAT', 'LON', 'DEPTH'])
# hypoinverse
catalog_hypoinverse = pd.read_csv("../hypoinverse/catOut.sum", sep="\s+")
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
# for xcorloc
catalog_xcloc = pd.read_csv(f"../xcorloc/out.loc_xcor", sep="\s+", names=["qID", "yr","mon","day", "hr","min","sec","lat","lon","dep","mag","pair", "pick_used", "erx", "ery", "erz", "ert", "rms_phs", "rms_dif", "type"])

# for hyposvi
catalog_hyposvi = pd.read_csv(f"../hyposvi/data/catalog_svi9.csv_svi")

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

# profile parameter setup
profile_figsize = [8, 3]
size2 = 0.5
fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for source in sources:
    dist = project_profile(source[0], source[1])
    ax.scatter(dist, source[2], s=size2, c='green')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./true_location_profile.png', dpi=300, transparent=True)
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

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_dd)):
    dist = project_profile(catalog_dd.iloc[i]['LAT'], catalog_dd.iloc[i]['LON'])
    #ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='k')
    ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./dd_location_profile.png', dpi=300, transparent=True)
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

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_gc)):
    dist = project_profile(catalog_gc.iloc[i]['latR'], catalog_gc.iloc[i]['lonR'])
    ax.scatter(dist, catalog_gc.iloc[i]['depR'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./gc_location_profile.png', dpi=300, transparent=True)
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

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_vele)):
    dist = project_profile(catalog_vele.iloc[i]['LAT'], catalog_vele.iloc[i]['LON'])
    ax.scatter(dist, catalog_vele.iloc[i]['DEPTH'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./ve_location_profile.png', dpi=300, transparent=True)
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

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_hypoinverse)):
    dist = project_profile(catalog_hypoinverse.iloc[i]['LAT'], catalog_hypoinverse.iloc[i]['LON'])
    ax.scatter(dist, catalog_hypoinverse.iloc[i]['DEPTH'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./hypo_location_profile.png', dpi=300, transparent=True)
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

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(len(nll_lon)):
    dist = project_profile(nll_lat[i], nll_lon[i])
    ax.scatter(dist, nll_dep[i], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./nll_location_profile.png', dpi=300, transparent=True)
plt.close()


# xcorloc
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(catalog_xcloc['lon'], catalog_xcloc['lat'], s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./xcorloc_location_mapview.png', dpi=300, transparent=True)
plt.close()

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_xcloc)):
    dist = project_profile(catalog_xcloc.iloc[i]['lat'], catalog_xcloc.iloc[i]['lon'])
    ax.scatter(dist, catalog_xcloc.iloc[i]['dep'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./xcorloc_location_profile.png', dpi=300, transparent=True)
plt.close()


# hyposvi
fig = plt.figure(figsize=[3,4], constrained_layout=True)
ax = fig.add_subplot(111)
ax.scatter(catalog_hyposvi['longitude'], catalog_hyposvi['latitude'], s=size, c='red')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=6)
ax.set_ylabel('Latitude', fontsize=6, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=5)
ax.yaxis.set_tick_params(labelsize=5)
plt.savefig('./svi_location_mapview.png', dpi=300, transparent=True)
plt.close()

fig = plt.figure(figsize=profile_figsize, constrained_layout = True)
ax = fig.add_subplot(111)
for i in range(0, len(catalog_hyposvi)):
    dist = project_profile(catalog_hyposvi.iloc[i]['latitude'], catalog_hyposvi.iloc[i]['longitude'])
    ax.scatter(dist, catalog_hyposvi.iloc[i]['depth'], s=size2, c='red')
ax.set_xlim([0, 80])
ax.set_ylim([15,0])
ax.set_xlabel('Distance (km)', labelpad=0.05, fontsize=8)
ax.set_ylabel('Depth (km)', fontsize=8, labelpad=0.1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
plt.savefig('./svi_location_profile.png', dpi=300, transparent=True)
plt.close()
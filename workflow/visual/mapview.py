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
catalog_gc = pd.read_csv(f"../growclust/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypodd/hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])

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

# mapview containing six
fig = plt.figure(figsize=[11,7], constrained_layout=True)
gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.01)

map_lat = [35.47, 36.13]
map_lon = [-117.91, -117.305]
size = 0.2
title_fontsize = 8


# original distribution
ax = fig.add_subplot(gs[0,0])
ax.set_title('True Location', fontsize=title_fontsize, fontweight="bold")
#ax.scatter(stations[:,1], stations[:,0], s=7, marker='v', alpha=0.7)
ax.plot([-117.9, -117.32], [36.1, 35.5], linestyle='--', linewidth=2, marker='x', c=(140./255,21./255,21./255), dashes=(10,55))
ax.text(-117.9, 36.1, 'A', fontsize=7, fontweight='bold', rotation=45)
ax.text(-117.32, 35.51, 'A\'', fontsize=7, fontweight='bold', rotation=45)
ax.scatter(sources[:, 1], sources[:,0], s=size, c='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
ax.set_ylabel('Latitude', fontsize=8, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)
#ax.axes.get_xaxis().set_ticklabels(xticklabel[::-1], fontsize=6)
#ax.axes.get_yaxis().set_ticklabels(yticklabel, fontsize=6)


# hypoDD
ax = fig.add_subplot(gs[0,1])
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c='k')
#ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c=catalog_dd['CID'], cmap='Dark2', norm=colors.Normalize(vmin=1, vmax=4))
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# growclust
ax = fig.add_subplot(gs[0,2])
ax.set_title('GrowClust', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c='k')
#ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c=catalog_gc['cID'], cmap='tab10', norm=colors.Normalize(vmin=1, vmax=20))
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# velest
ax = fig.add_subplot(gs[1,0])
ax.set_title('VELEST', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_vele['LON'], catalog_vele['LAT'], s=size, c='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# hypoinverse
ax = fig.add_subplot(gs[1,1])
ax.set_title('HypoInverse', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_hypoinverse['LON'], catalog_hypoinverse['LAT'], s=size, c='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# Non Lin Loc
ax = fig.add_subplot(gs[1,2])
ax.set_title('Non_Lin_Loc', fontsize=title_fontsize, fontweight="bold")
ax.scatter(nll_lon, nll_lat, s=size, c='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])

# Xcorloc
ax = fig.add_subplot(gs[0,3])
ax.set_title('XCorLoc', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_xcloc['lon'], catalog_xcloc['lat'], s=size, c='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


# hyposvi
ax = fig.add_subplot(gs[1,3])
ax.set_title('HypoSVI', fontsize=title_fontsize, fontweight="bold")
ax.scatter(catalog_hyposvi['longitude'], catalog_hyposvi['latitude'], s=size,c ='k')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


#plt.tight_layout()
plt.savefig('./mapview.png', dpi=300)
#plt.savefig('./mapview.png', dpi=300, transparent=True)
plt.close()

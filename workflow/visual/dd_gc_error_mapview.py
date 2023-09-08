import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
matplotlib.use('agg')
import matplotlib.colors as colors

h_df = pd.read_csv('relative_error_hori.csv')
z_df = pd.read_csv('relative_error_depth.csv')

sources = np.load('../o_source.npy')
catalog_gc = pd.read_csv(f"../out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])

fig = plt.figure(figsize=[10,6], constrained_layout=True)

map_lat = [35.47, 36.13]
map_lon = [-117.91, -117.305]
size = 1
title_fontsize = 8

# hypoDD
ax = fig.add_subplot(121)
ax.set_title('HypoDD', fontsize=title_fontsize, fontweight="bold")
#ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c='k')
sc = ax.scatter(catalog_dd['LON'], catalog_dd['LAT'], s=size, c=z_df['hypoDD'], cmap='viridis', norm=colors.Normalize(vmin=0, vmax=1.5))
cbar = fig.colorbar(sc, ax=ax)
cbar.ax.set_title('Error (km)')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
ax.set_ylabel('Latitude', fontsize=8, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)


# growclust
ax = fig.add_subplot(122)
ax.set_title('GrowClust', fontsize=title_fontsize, fontweight="bold")
#ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size, c='k')
sc = ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], s=size,c=z_df['growclust'], cmap='viridis', norm=colors.Normalize(vmin=0, vmax=1.5))
cbar = fig.colorbar(sc, ax=ax)
cbar.ax.set_title('Error (km)')
ax.set_xlim(map_lon)
ax.set_ylim(map_lat)
ax.set_xlabel('Longitude', labelpad=0.05, fontsize=8)
ax.set_ylabel('Latitude', fontsize=8, labelpad=0.3)
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)

plt.savefig('./gc_dd_dep_hori_error_mapview.png', dpi=300, transparent=True)
plt.close()

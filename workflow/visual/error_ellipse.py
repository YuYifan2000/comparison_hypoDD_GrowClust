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
    lat2 = 35.8
    lon2 = -117.6
    _,az1, baz1 = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    dist, az2, baz2 = gps2dist_azimuth(lat1, lon1, lat, lon)
    theta = abs(az1 - az2)
    return dist * np.cos(np.deg2rad(theta)) / 1000.

lat_range = [35.78, 36.1]
lon_range = [-117.9, -117.58]
dep_range = [0, 15]
# hypoinverse
catalog_hypoinverse = pd.read_csv("../catOut.sum", sep="\s+")
catalog_hypoinverse["time"] = (catalog_hypoinverse['DATE']+catalog_hypoinverse["TIME"]).apply(lambda x: datetime.strptime(x, "%Y/%m/%d%H:%M"))
catalog_hypoinverse = catalog_hypoinverse[catalog_hypoinverse['LAT']>lat_range[0]]

fig = plt.figure(figsize=[9,5])

ax = fig.add_subplot(111)
ax.set_title('Error Ellipse', fontsize=8, fontweight="bold")
for i in range(0, len(catalog_hypoinverse)):
    dist = project_profile(catalog_hypoinverse.iloc[i]['LAT'], catalog_hypoinverse.iloc[i]['LON'])
    #ax.scatter(dist, catalog_dd.iloc[i]['DEPTH'], s=size, c='k')
    ax.errorbar(dist, catalog_hypoinverse.iloc[i]['DEPTH'], catalog_hypoinverse.iloc[i]['ERH'] * 2.4, catalog_hypoinverse.iloc[i]['ERZ'] * 2.4, fmt='.k', capsize=1, elinewidth=0.5,capthick=0.5)
ax.invert_yaxis()
ax.set_ylabel('Depth (km)',labelpad=0.1, fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)
ax.set_xlabel('Distance (km)', labelpad=0.1, fontsize=8)

plt.savefig('./error_ellipse.png', dpi=400, transparent = True)
plt.close()
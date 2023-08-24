import matplotlib.pyplot as plt
import mplstereonet
from obspy.geodetics.base import gps2dist_azimuth
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')


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
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['LAT', 'LON', 'DEPTH'])

# velest
fig = plt.figure()
ax = fig.add_subplot(111, projection='stereonet')
for i in range(0, len(catalog_vele)):
    lat1 = sources[catalog_vele['ID'][i]-1,0]
    lon1 = sources[catalog_vele['ID'][i]-1,1]
    lat2 = catalog_vele['LAT'][i]
    lon2 = catalog_vele['LON'][i]
    dist, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    plunge = np.arctan((sources[catalog_vele['ID'][i]-1,2]-catalog_vele['DEPTH'][i])*1000. / dist) *180/np.pi
    if plunge < 0:
        ax.line(-plunge, az, c='blue', linewidth=1)
    else:
        ax.line(plunge, az, c='red', linewidth=1)
ax.grid()
plt.savefig('./velest_stereo.png', dpi=300)
plt.close()
# hypoinverse
fig = plt.figure()
ax = fig.add_subplot(111, projection='stereonet')
for i in range(0, len(catalog_hypoinverse)):
    lat1 = sources[i,0]
    lon1 = sources[i,1]
    dep1 = sources[i,2]
    lat2 = catalog_hypoinverse['LAT'][i]
    lon2 = catalog_hypoinverse['LON'][i]
    dist, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    plunge = np.arctan((dep1-catalog_hypoinverse['DEPTH'][i])*1000. / dist) *180/np.pi
    if plunge < 0:
        ax.line(-plunge, az, c='blue', linewidth=1)
    else:
        ax.line(plunge, az, c='red', linewidth=1)
ax.grid()
plt.savefig('./hypoinverse_stereo.png', dpi=300)
plt.close()
# NonLinLoc
fig = plt.figure()
ax = fig.add_subplot(111, projection='stereonet')
for i in range(0, len(catalog_nll)):
    lat1 = sources[i,0]
    lon1 = sources[i,1]
    dep1 = sources[i,2]
    lat2 = catalog_nll['LAT'][i]
    lon2 = catalog_nll['LON'][i]
    dist, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    plunge = np.arctan((dep1-catalog_nll['DEPTH'][i])*1000. / dist) *180/np.pi
    if plunge < 0:
        ax.line(-plunge, az, c='blue', linewidth=1)
    else:
        ax.line(plunge, az, c='red', linewidth=1)
ax.grid()
plt.savefig('./nonlinloc_stereo.png', dpi=300)
plt.close()

# hypoDD

fig = plt.figure()
ax = fig.add_subplot(111, projection='stereonet')
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == i+1
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        lat1 = sources[i, 0]
        lon1 = sources[i, 1]
        dep1 = sources[i, 2]
        lat2 = tmp.iloc[0]['LAT']
        lon2 = tmp.iloc[0]['LON']
        dist, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
        plunge = np.arctan((dep1-tmp.iloc[0]['DEPTH'])*1000. / dist) *180/np.pi
        if plunge < 0:
            ax.line(-plunge, az, c='blue', linewidth=0.1)
        else:
            ax.line(plunge, az, c='red', linewidth=0.1)
ax.grid()
plt.savefig('./hypodd_stereo.png', dpi=300)
plt.close()

# growclust
fig = plt.figure()
ax = fig.add_subplot(111, projection='stereonet')
for i in range(0, len(sources)):
    if i+1 == catalog_gc['evid'][i]:
        lat1 = sources[i, 0]
        lon1 = sources[i, 1]
        dep1 = sources[i, 2]
        lat2 = catalog_gc['latR'][i]
        lon2 = catalog_gc['lonR'][i]
        dep2 = catalog_gc['depR'][i]
        dist, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
        plunge = np.arctan((dep1-dep2)*1000. / dist) *180/np.pi
        if plunge < 0:
            ax.line(-plunge, az, c='blue', linewidth=1)
        else:
            ax.line(plunge, az, c='red', linewidth=1)
ax.grid()
plt.savefig('./growclust_stereo.png', dpi=300)
plt.close()
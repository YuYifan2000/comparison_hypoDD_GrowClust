
from datetime import datetime
import numpy as np
import pandas as pd
from obspy.geodetics.base import gps2dist_azimuth

sources = np.load('../o_source.npy')
catalog_gc = pd.read_csv(f"../out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"../hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])

velest_lat = []
velest_lon = []
velest_dep = []
f = open('../hypocenter_.CNV', 'r')
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
# for xcorloc
catalog_xcloc = pd.read_csv(f"../out.loc_xcor", sep="\s+", names=["qID", "yr","mon","day", "hr","min","sec","lat","lon","dep","mag","pair", "pick_used", "erx", "ery", "erz", "ert", "rms_phs", "rms_dif", "type"])
# for hyposvi
catalog_hyposvi = pd.read_csv(f"../hyposvi_cat.csv")


# statistics horizontal movement and vertical

# original v.s. velest
velest_hori = np.zeros([len(catalog_vele),])
velest_vert = np.zeros([len(catalog_vele),])
for i in range(0, len(catalog_vele)):
    lat1 = catalog_vele['LAT'][i]
    lon1 = catalog_vele['LON'][i]
    lat0 = sources[i,0]
    lon0 = sources[i,1]
    dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
    velest_hori[i] = abs(dist)/1000.
    velest_vert[i] = abs(catalog_vele['DEPTH'][i] - sources[i,2])

# original v.s. hypoinverse
hypoinverse_hori = np.zeros([len(catalog_hypoinverse),])
hypoinverse_vert = np.zeros([len(catalog_hypoinverse),])
for i in range(0, len(catalog_hypoinverse)):
    lat1 = catalog_hypoinverse['LAT'][i]
    lon1 = catalog_hypoinverse['LON'][i]
    lat0 = sources[i,0]
    lon0 = sources[i,1]
    dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
    hypoinverse_hori[i] = abs(dist) / 1000.
    hypoinverse_vert[i] = abs(catalog_hypoinverse['DEPTH'][i] - sources[i, 2])


# original v.s. nll
nll_hori = np.zeros([len(sources), ])
nll_vert = np.zeros([len(sources), ])
for i in range(0, len(sources)):
    lat1 = catalog_nll['LAT'][i]
    lon1 = catalog_nll['LON'][i]
    lat0 = sources[i,0]
    lon0 = sources[i,1]
    dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
    nll_hori[i] = abs(dist) / 1000.
    nll_vert[i] = abs(catalog_nll['DEPTH'][i] - sources[i, 2])

# original v.s. hypodd
dd_hori = np.zeros([len(sources),])
dd_vert = np.zeros([len(sources),])
for i in range(0, len(sources)):
    index = catalog_dd['ID'] == i+1
    tmp = catalog_dd.where(index).dropna()
    if not tmp.empty:
        #sources[i,1], sources[i,0], tmp['LON']-sources[i,1], tmp['LAT']-sources[i,0]
        lat1 = tmp.iloc[0]['LAT']
        lon1 = tmp.iloc[0]['LON']
        lat0 = sources[i,0]
        lon0 = sources[i,1]
        dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
        dd_hori[i] = abs(dist / 1000.)
        dd_vert[i] = abs(tmp.iloc[0]['DEPTH'] - sources[i, 2])

# original v.s. growclust
gc_hori = np.zeros([len(sources), ])
gc_vert = np.zeros([len(sources), ])
for i in range(0, len(sources)):
    if i+1 == catalog_gc['evid'][i]:
        lat1 = catalog_gc['latR'][i]
        lon1 = catalog_gc['lonR'][i]
        lat0 = sources[i,0]
        lon0 = sources[i,1]
        dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
        gc_hori[i] = abs(dist / 1000.)
        gc_vert[i] = abs(catalog_gc['depR'][i] - sources[i, 2])

# original v.s. xcorloc
xc_hori = np.zeros([len(sources), ])
xc_vert = np.zeros([len(sources), ])
for i in range(0, len(sources)):
    lat1 = catalog_xcloc['lat'][i]
    lon1 = catalog_xcloc['lon'][i]
    lat0 = sources[i,0]
    lon0 = sources[i,1]
    dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
    xc_hori[i] = abs(dist/1000.)
    xc_vert[i] = abs(catalog_xcloc['dep'][i] - sources[i,2])

# original v.s. hyposvi
svi_hori = np.zeros([len(sources), ])
svi_vert = np.zeros([len(sources), ])
for i in range(0, len(sources)):
    lat1 = catalog_hyposvi['LAT'][i]
    lon1 = catalog_hyposvi['LON'][i]
    lat0 = sources[i,0]
    lon0 = sources[i,1]
    dist, az, baz = gps2dist_azimuth(lat0, lon0, lat1, lon1)
    svi_hori[i] = abs(dist/1000.)
    svi_vert[i] = abs(catalog_hyposvi['DEPTH'][i] - sources[i,2])

h_data = np.stack([velest_hori, nll_hori, hypoinverse_hori, dd_hori, gc_hori, xc_hori, svi_hori], axis=1)
z_data = np.stack([velest_vert, nll_vert, hypoinverse_vert, dd_vert, gc_vert, xc_vert, svi_vert], axis=1)


h_df = pd.DataFrame(h_data, columns=['velest', 'NonLinLoc', 'hypoinverse', 'hypoDD', 'growclust', 'xcorloc', 'HypoSVI'])
z_df = pd.DataFrame(z_data, columns=['velest', 'NonLinLoc', 'hypoinverse', 'hypoDD', 'growclust', 'xcorloc', 'HypoSVI'])
print(h_df.mean())
print(z_df.mean())
h_df.to_csv('absolute_error_hori.csv', index=False)
z_df.to_csv('absolute_error_depth.csv', index=False)
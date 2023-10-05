from datetime import datetime
import numpy as np
import pandas as pd
from obspy.geodetics.base import gps2dist_azimuth

def hori_(source1, source2):
    return np.sqrt((source1[0]-source2[0])**2 + (source1[1]-source2[1])**2) / 1000.

def catalog_distance(lat1, lon1, dep1, lat2, lon2, dep2):
    h_e,az,baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    v_e = abs(dep1-dep2)
    return h_e/1000., v_e

def pairup():
    df = pd.DataFrame(columns=['idx1', 'idx2', 'hori', 'vert'])
    sources = np.load('source.npy')

    for i in range(0,len(sources)):
        print(i)
        for j in range(i,len(sources)):
            hori_dist = hori_(sources[i], sources[j])
            vert_dist = abs(sources[i,2]-sources[j,2]) / 1000.
            if ((hori_dist < 2.) and (vert_dist < 2.)):
                tmp = pd.DataFrame(data={'idx1':i, 'idx2':j, 'hori':hori_dist, 'vert':vert_dist}, index=[0])
                df = pd.concat([df,tmp], ignore_index=True)
    df.to_csv('relative.csv', index=False)
    return df
# read all location file
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
sources = np.load('../source.npy')
# for xcorloc
catalog_xcloc = pd.read_csv(f"../out.loc_xcor", sep="\s+", names=["qID", "yr","mon","day", "hr","min","sec","lat","lon","dep","mag","pair", "pick_used", "erx", "ery", "erz", "ert", "rms_phs", "rms_dif", "type"])
# for hyposvi
catalog_hyposvi = pd.read_csv(f"../hyposvi_cat.csv")

# pairup()
df = pd.read_csv('relative.csv')
velest_hori = np.zeros([len(catalog_vele),])
velest_vert = np.zeros([len(catalog_vele),])
hypoinverse_hori = np.zeros([len(catalog_hypoinverse),])
hypoinverse_vert = np.zeros([len(catalog_hypoinverse),])
nll_hori = np.zeros([len(sources), ])
nll_vert = np.zeros([len(sources), ])
dd_hori = np.zeros([len(sources),])
dd_vert = np.zeros([len(sources),])
gc_hori = np.zeros([len(sources), ])
gc_vert = np.zeros([len(sources), ])
xc_hori = np.zeros([len(sources), ])
xc_vert = np.zeros([len(sources), ])
svi_hori = np.zeros([len(sources), ])
svi_vert = np.zeros([len(sources), ])
for i in range(0, 1000):
    print(i)
    tmp = df.loc[(df['idx1']==i)|(df['idx2']==i)]
    l = len(tmp)
    for j in range(0,l):
        evid1 = int(tmp.iloc[j]['idx1'] + 1)
        evid2 = int(tmp.iloc[j]['idx2'] + 1)
        o_hori = tmp.iloc[j]['hori']
        o_vert = tmp.iloc[j]['vert']

        # velest
        vele1 = catalog_vele.loc[evid1-1]
        vele2 = catalog_vele.loc[evid2-1]
        vele_h, vele_v = catalog_distance(catalog_vele.iloc[evid1-1]['LAT'], catalog_vele.iloc[evid1-1]['LON'], catalog_vele.iloc[evid1-1]['DEPTH'], catalog_vele.iloc[evid2-1]['LAT'],catalog_vele.iloc[evid2-1]['LON'], catalog_vele.iloc[evid2-1]['DEPTH'])
        velest_hori[i] += (vele_h-o_hori) **2 / l
        velest_vert[i] += (vele_v-o_vert) **2 / l
        
        # hypodd
        dd1 = catalog_dd.loc[catalog_dd['ID'] == evid1]
        dd2 = catalog_dd.loc[catalog_dd['ID'] == evid2]
        dd_h, dd_v = catalog_distance(dd1.iloc[0]['LAT'], dd1.iloc[0]['LON'], dd1.iloc[0]['DEPTH'], dd2.iloc[0]['LAT'], dd2.iloc[0]['LON'], dd2.iloc[0]['DEPTH'])
        dd_hori[i] += (dd_h-o_hori) **2 / l
        dd_vert[i] += (dd_v-o_vert) **2 / l

        # growclust
        gc1 = catalog_gc.loc[catalog_gc['qID']==evid1]
        gc2 = catalog_gc.loc[catalog_gc['qID']==evid2]
        gc_h, gc_v = catalog_distance(gc1.iloc[0]['latR'], gc1.iloc[0]['lonR'], gc1.iloc[0]['depR'], gc2.iloc[0]['latR'], gc2.iloc[0]['lonR'], gc2.iloc[0]['depR'])
        gc_hori[i] += (gc_h-o_hori) **2 / l
        gc_vert[i] += (gc_v-o_vert) **2 / l

        # xcorloc
        xc1 = catalog_xcloc.loc[catalog_xcloc['qID']==evid1]
        xc2 = catalog_xcloc.loc[catalog_xcloc['qID']==evid2]
        xc_h, xc_v = catalog_distance(xc1.iloc[0]['lat'], xc1.iloc[0]['lon'], xc1.iloc[0]['dep'], xc2.iloc[0]['lat'], xc2.iloc[0]['lon'], xc2.iloc[0]['dep'])
        xc_hori[i] += (xc_h-o_hori) **2 / l
        xc_vert[i] += (xc_v-o_vert) **2 / l

        # hypoinverse
        hypo_h, hypo_v = catalog_distance(catalog_hypoinverse.iloc[evid1-1]['LAT'], catalog_hypoinverse.iloc[evid1-1]['LON'], catalog_hypoinverse.iloc[evid1-1]['DEPTH'], catalog_hypoinverse.iloc[evid2-1]['LAT'], catalog_hypoinverse.iloc[evid2-1]['LON'], catalog_hypoinverse.iloc[evid2-1]['DEPTH'])
        hypoinverse_hori[i] += (hypo_h-o_hori) **2 / l
        hypoinverse_vert[i] += (hypo_v-o_vert) **2 / l

        # NLL
        nll_h, nll_v = catalog_distance(catalog_nll.iloc[evid1-1]['LAT'], catalog_nll.iloc[evid1-1]['LON'], catalog_nll.iloc[evid1-1]['DEPTH'], catalog_nll.iloc[evid2-1]['LAT'],catalog_nll.iloc[evid2-1]['LON'], catalog_nll.iloc[evid2-1]['DEPTH'])
        nll_hori[i] += (nll_h-o_hori) **2 / l
        nll_vert[i] += (nll_v-o_vert) **2 / l

        #hyposvi
        svi_h, svi_v = catalog_distance(catalog_hyposvi.iloc[evid1-1]['LAT'], catalog_hyposvi.iloc[evid1-1]['LON'], catalog_hyposvi.iloc[evid1-1]['DEPTH'], catalog_hyposvi.iloc[evid2-1]['LAT'],catalog_hyposvi.iloc[evid2-1]['LON'], catalog_hyposvi.iloc[evid2-1]['DEPTH'])
        svi_hori[i] += (svi_h-o_hori) **2 / l
        svi_vert[i] += (svi_v-o_vert) **2 / l

h_data = np.stack([velest_hori, nll_hori, hypoinverse_hori, dd_hori, gc_hori, xc_hori, svi_hori], axis=1)
z_data = np.stack([velest_vert, nll_vert, hypoinverse_vert, dd_vert, gc_vert, xc_vert, svi_vert], axis=1)
h_data = np.sqrt(h_data)
z_data = np.sqrt(z_data)

h_df = pd.DataFrame(h_data, columns=['velest', 'NonLinLoc', 'hypoinverse', 'hypoDD', 'growclust', 'xcorloc', 'HypoSVI'])
z_df = pd.DataFrame(z_data, columns=['velest', 'NonLinLoc', 'hypoinverse', 'hypoDD', 'growclust', 'xcorloc', 'HypoSVI'])
print(h_df.mean())
print(z_df.mean())
h_df.to_csv('relative_error_hori.csv', index=False)
z_df.to_csv('relative_error_depth.csv', index=False)
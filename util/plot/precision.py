import pandas as pd
import numpy as  np
import pymap3d as pm

def distance(origin1lat,origin1lon,origin1dep, origin2lat,origin2lon, origin2dep,result1lat, result1lon,result1dep, result2lat, result2lon,result2dep):
    set1 = pm.geodetic2enu(origin1lat,origin1lon,origin1dep,origin2lat,origin2lon,origin2dep)
    set2 = pm.geodetic2enu(result1lat,result1lon,result1dep,result2lat,result2lon,result2dep)
    return np.array(set1), np.array(set2)

dd = pd.read_csv('./hypodd.csv')
sources = np.load('./o_source.npy')
xc = pd.read_csv('./xcorloc.csv')
gc = pd.read_csv('./growclust.csv')
# pairup()
df = pd.read_csv('relative.csv')
gc_count = 0
gc_yes = 0
xc_count = 0
xc_yes = 0
dd_count = 0
dd_yes = 0
for i in range(0, 1000):
    print(i)
    tmp = df.loc[(df['idx1']==i)|(df['idx2']==i)]
    l = len(tmp)
    for j in range(0,l):
        evid1 = int(tmp.iloc[j]['idx1'] + 1)
        evid2 = int(tmp.iloc[j]['idx2'] + 1)
        # hypodd
        # dd1 = dd.loc[dd['ID'] == evid1]
        # dd2 = dd.loc[dd['ID'] == evid2]
        # set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], dd1.iloc[0]['LAT'], dd1.iloc[0]['LON'], dd1.iloc[0]['DEPTH'], dd2.iloc[0]['LAT'], dd2.iloc[0]['LON'], dd2.iloc[0]['DEPTH'])

        # growclust
        gc1 = gc.loc[gc['qID'] == evid1]
        gc2 = gc.loc[gc['qID'] == evid2]
        set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], gc1.iloc[0]['latR'], gc1.iloc[0]['lonR'], gc1.iloc[0]['depR'], gc2.iloc[0]['latR'], gc2.iloc[0]['lonR'], gc2.iloc[0]['depR'])
        erx = np.sqrt(gc1.iloc[0]['eh']**2 + gc2.iloc[0]['eh']**2)/0.7*3.08
        ery = np.sqrt(gc1.iloc[0]['eh']**2 + gc2.iloc[0]['eh']**2)/0.7*3.08
        erz = np.sqrt(gc1.iloc[0]['ez']**2 + gc2.iloc[0]['ez']**2)/0.7*3.08
        gc_count += 1
        if np.abs(set1[0]-set2[0])<erx*1000.:
            gc_yes +=1
        # xcorloc
        xc1 = xc.loc[xc['qID'] == evid1]
        xc2 = xc.loc[xc['qID'] == evid2]
        set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], xc1.iloc[0]['lat'], gc1.iloc[0]['lon'], gc1.iloc[0]['dep'], gc2.iloc[0]['lat'], gc2.iloc[0]['lon'], gc2.iloc[0]['dep'])
        erx = np.sqrt(xc1.iloc[0]['erx']**2 + xc2.iloc[0]['erx']**2)/0.7*3.08
        ery = np.sqrt(xc1.iloc[0]['ery']**2 + xc2.iloc[0]['ery']**2)/0.7*3.08
        erz = np.sqrt(xc1.iloc[0]['erz']**2 + xc2.iloc[0]['erz']**2)/0.7*3.08
        xc_count += 1
        if np.abs(set1-set2)<np.array([erx,ery,erz]):
            xc_yes +=1
print('Growclust')
print(gc_yes/ gc_count)
print('XCORLOC')
print(xc_yes/xc_count)

dd_count = 0
dd_yes = 0
for i in range(0, 100):
    tmp = df.loc[(df['idx1']==i)|(df['idx2']==i)]
    l = len(tmp)
    for j in range(0,l):
        evid1 = int(tmp.iloc[j]['idx1'] + 1)
        evid2 = int(tmp.iloc[j]['idx2'] + 1)
        if (evid1>100 | evid2 > 100):
            continue
        # hypodd
        dd1 = dd.loc[dd['ID'] == evid1]
        dd2 = dd.loc[dd['ID'] == evid2]
        set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], dd1.iloc[0]['LAT'], dd1.iloc[0]['LON'], dd1.iloc[0]['DEPTH'], dd2.iloc[0]['LAT'], dd2.iloc[0]['LON'], dd2.iloc[0]['DEPTH'])
        erx = np.sqrt(dd1.iloc[0]['EX']**2 + xc2.iloc[0]['EX']**2)*2.8
        ery = np.sqrt(dd1.iloc[0]['EY']**2 + xc2.iloc[0]['EY']**2)*2.8
        erz = np.sqrt(dd1.iloc[0]['EZ']**2 + xc2.iloc[0]['EZ']**2)*2.8
        dd_count += 1
        if np.abs(set1-set2)<np.array([erx,ery,erz]):
            dd_yes +=1
print('HypoDD')
print(dd_yes/dd_count)
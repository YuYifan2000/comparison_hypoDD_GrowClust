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
velest = pd.read_csv('./velest.csv')
svi = pd.read_csv('./hyposvi.csv')
inverse = pd.read_csv('./hypoinverse.csv')
nll = pd.read_csv('./nll.csv')
# pairup()
df = pd.read_csv('relative.csv')
gc_count = 0
gc_yes = 0
xc_count = 0
xc_yes = 0
dd_count = 0
dd_yes = 0
velest_count = 0
velest_yes = 0
svi_count = 0
svi_yes = 0
inverse_count = 0
inverse_yes = 0
nll_count = 0
nll_yes = 0
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
        erx = np.sqrt(gc1.iloc[0]['eh']**2 + gc2.iloc[0]['eh']**2)/0.7*np.sqrt(3.08)
        ery = np.sqrt(gc1.iloc[0]['eh']**2 + gc2.iloc[0]['eh']**2)/0.7*np.sqrt(3.08)
        erz = np.sqrt(gc1.iloc[0]['ez']**2 + gc2.iloc[0]['ez']**2)/0.7*np.sqrt(3.08)
        gc_count += 1
        if (np.abs(set1-set2)<np.array([erx,ery,erz])*1000.).all():
        #if np.abs(set1[0]-set2[0])<erx*1000.:
            gc_yes +=1
        # xcorloc
        xc1 = xc.loc[xc['qID'] == evid1]
        xc2 = xc.loc[xc['qID'] == evid2]
        set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], xc1.iloc[0]['lat'], xc1.iloc[0]['lon'], xc1.iloc[0]['dep'], xc2.iloc[0]['lat'], xc2.iloc[0]['lon'], xc2.iloc[0]['dep'])
        erx = np.sqrt(xc1.iloc[0]['erx']**2 + xc2.iloc[0]['erx']**2)/0.7*np.sqrt(3.08)
        ery = np.sqrt(xc1.iloc[0]['ery']**2 + xc2.iloc[0]['ery']**2)/0.7*np.sqrt(3.08)
        erz = np.sqrt(xc1.iloc[0]['erz']**2 + xc2.iloc[0]['erz']**2)/0.7*np.sqrt(3.08)
        xc_count += 1
        #if np.abs(set1[0]-set2[0])<erx:
        if (np.abs(set1-set2)<np.array([erx,ery,erz])).all():
            xc_yes +=1

        # velest
        velest1 = velest.loc[[evid1-1]]
        velest2 = velest.loc[[evid2-1]]
        set1,set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], velest1.iloc[0]['LAT'], velest1.iloc[0]['LON'], velest1.iloc[0]['DEPTH'], velest2.iloc[0]['LAT'], velest2.iloc[0]['LON'], velest2.iloc[0]['DEPTH'])
        erx = np.sqrt(velest1.iloc[0]['ERX']**2 + velest2.iloc[0]['ERX']**2)
        ery = np.sqrt(velest1.iloc[0]['ERY']**2 + velest2.iloc[0]['ERY']**2)
        erz = np.sqrt(velest1.iloc[0]['ERZ']**2 + velest2.iloc[0]['ERZ']**2)
        velest_count += 1
        #if np.abs(set1[0]-set2[0])<erx:
        if (np.abs(set1-set2)/1000.<np.array([erx,ery,erz])).all():
            velest_yes +=1

        # hyposvi
        svi1 = svi.iloc[[evid1-1]]
        svi2 = svi.iloc[[evid2-1]]
        set1,set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], svi1.iloc[0]['latitude'], svi1.iloc[0]['longitude'], svi1.iloc[0]['depth'], svi2.iloc[0]['latitude'], svi2.iloc[0]['longitude'], svi2.iloc[0]['depth'])
        erx = np.sqrt(svi1.iloc[0]['unc_h_max']**2 + svi2.iloc[0]['unc_h_max']**2)*np.sqrt(2.8)
        ery = np.sqrt(svi1.iloc[0]['unc_h_min']**2 + svi2.iloc[0]['unc_h_min']**2)*np.sqrt(2.8) 
        erz = np.sqrt(svi1.iloc[0]['unc_z']**2 + svi2.iloc[0]['unc_z']**2)*np.sqrt(2.8) 
        svi_count += 1
        #if np.abs(set1[0]-set2[0])<erx:
        if (np.abs(set1-set2)/1000.<np.array([erx,ery,erz])).all():
            svi_yes +=1

        # hypoinverse
        inverse1 = inverse.iloc[[evid1-1]]
        inverse2 = inverse.iloc[[evid2-1]]
        set1,set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], inverse1.iloc[0]['LAT'], inverse1.iloc[0]['LON'], inverse1.iloc[0]['DEPTH'], inverse2.iloc[0]['LAT'], inverse2.iloc[0]['LON'], inverse2.iloc[0]['DEPTH'])
        erx = np.sqrt(inverse1.iloc[0]['ERH']**2 + inverse2.iloc[0]['ERH']**2)*np.sqrt(2.80)
        ery = np.sqrt(inverse1.iloc[0]['ERH']**2 + inverse2.iloc[0]['ERH']**2)*np.sqrt(2.80)
        erz = np.sqrt(inverse1.iloc[0]['ERZ']**2 + inverse2.iloc[0]['ERZ']**2)*np.sqrt(2.80)
        inverse_count += 1
        #if np.abs(set1[0]-set2[0])<erx:
        if (np.abs(set1-set2)/1000.<np.array([erx,ery,erz])).all():
            inverse_yes +=1
        # nll
        nll1 = nll.iloc[[evid1-1]]
        nll2 = nll.iloc[[evid2-1]]
        set1,set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], nll1.iloc[0]['LAT'], nll1.iloc[0]['LON'], nll1.iloc[0]['DEPTH'], nll2.iloc[0]['LAT'], nll2.iloc[0]['LON'], nll2.iloc[0]['DEPTH'])
        erx = np.sqrt((nll1.iloc[0]['xx'] + nll2.iloc[0]['xx'])*2.80)
        ery = np.sqrt((nll1.iloc[0]['yy'] + nll2.iloc[0]['yy'])*2.80)
        erz = np.sqrt((nll1.iloc[0]['zz'] + nll2.iloc[0]['zz'])*2.80)
        nll_count += 1
        if (np.abs(set1-set2)/1000.<np.array([erx,ery,erz])).all():
            nll_yes +=1
print('Growclust')
print(gc_yes/ gc_count)
print('XCORLOC')
print(xc_yes/gc_count)
print('VELEST')
print(velest_yes/velest_count)
print('svi')
print(svi_yes/svi_count)
print('hypoinverse')
print(inverse_yes/inverse_count)
print('nll')
print(nll_yes/nll_count)
dd_count = 0
dd_yes = 0
for i in range(0, 1000):
    tmp = df.loc[(df['idx1']==i)|(df['idx2']==i)]
    l = len(tmp)
    for j in range(0,l):
        evid1 = int(tmp.iloc[j]['idx1'] + 1)
        evid2 = int(tmp.iloc[j]['idx2'] + 1)
        # hypodd
        dd1 = dd.loc[dd['ID'] == evid1]
        dd2 = dd.loc[dd['ID'] == evid2]
        try:
            set1, set2 = distance(sources[evid1-1,0], sources[evid1-1,1], sources[evid1-1,2], sources[evid2-1,0], sources[evid2-1,1],sources[evid2-1,2], dd1.iloc[0]['LAT'], dd1.iloc[0]['LON'], dd1.iloc[0]['DEPTH'], dd2.iloc[0]['LAT'], dd2.iloc[0]['LON'], dd2.iloc[0]['DEPTH'])
        except:
            print(dd1)
            print(dd2)
            print(evid1)
            print(evid2)
        erx = np.sqrt(dd1.iloc[0]['EX']**2 + dd2.iloc[0]['EX']**2)
        ery = np.sqrt(dd1.iloc[0]['EY']**2 + dd2.iloc[0]['EY']**2)
        erz = np.sqrt(dd1.iloc[0]['EZ']**2 + dd2.iloc[0]['EZ']**2)
        dd_count += 1
        if (np.abs(set1-set2)<np.array([erx,ery,erz])).all():
            dd_yes +=1
print('HypoDD')
print(dd_yes/dd_count)

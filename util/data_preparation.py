import pandas as pd
import numpy as np

# prepare the data from each program for the uncertainty quantification
# save as csv with location, 95% confidence interval ellipsoid parameters,

# growclust
catalog_gc = pd.read_csv(f"./growclust/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","Lat","Lon","Dep","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_gc['unc_x'] = catalog_gc['eh'].apply(lambda x: x/0.7*np.sqrt(3.08))
catalog_gc['unc_z'] = catalog_gc['ez'].apply(lambda x: x/0.7*np.sqrt(3.08))
catalog_gc = catalog_gc[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_gc.to_csv('./data/growclust.csv', index=False)


# HypoDD
catalog_dd = pd.read_csv(f"./hypodd/hypoDD.reloc", sep="\s+", names=["ID", "Lat", "Lon", "Dep", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_dd['unc_x'] = catalog_dd.apply(lambda x: np.sqrt(x['EX']**2+ x['EY']**2)/1000.*2.8, axis=1)
catalog_dd['unc_z'] = catalog_dd.apply(lambda x: x['EZ']/1000.*2.8, axis=1)
catalog_dd = catalog_dd[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_dd.to_csv('./data/hypodd.csv', index=False)


# XCORLOC
catalog_xcloc = pd.read_csv(f"./data/out.loc_xcor", sep="\s+", names=["qID", "yr","mon","day", "hr","min","sec","Lat","Lon","Dep","mag","pair", "pick_used", "erx", "ery", "erz", "ert", "rms_phs", "rms_dif", "type"])
catalog_xcloc['unc_x'] = catalog_xcloc.apply(lambda x: np.sqrt(x['erx']**2 + x['ery']**2)/0.7*3.08, axis=1)
catalog_xcloc['unc_z'] = catalog_xcloc.apply(lambda x: x['erz']/0.7*3.08, axis=1)
catalog_xcloc = catalog_xcloc[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_xcloc.to_csv('./data/xcorloc.csv', index=False)


# hyposvi
catalog_hyposvi = pd.read_csv(f"./hyposvi/data/catalog_svi9.csv_svi").rename(columns={'latitude': 'Lat', 'longitude': 'Lon', 'depth': 'Dep'})
catalog_hyposvi['unc_x'] = catalog_hyposvi.apply(lambda x: np.sqrt(x['unc_h_max']**2 + x['unc_h_min']**2 )*np.sqrt(7.81), axis=1)
catalog_hyposvi['unc_z'] = catalog_hyposvi['unc_z'] * np.sqrt(7.81)
data = catalog_hyposvi[['Lat', 'Lon','Dep','unc_x', 'unc_z']]
data.to_csv('./hyposvi.csv', index=False)


# hypoinverse
catalog_hypoinverse = pd.read_csv("./data/catOut.sum", sep="\s+").rename(columns={'LAT': 'Lat', 'LON': 'Lon', 'DEPTH': 'Dep'})
catalog_hypoinverse['unc_x'] = catalog_hypoinverse['ERH'].apply(lambda x: 2.4 * x)
catalog_hypoinverse['unc_z'] = catalog_hypoinverse['ERZ'].apply(lambda x: 2.4 * x)
catalog_hypoinverse = catalog_hypoinverse[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_hypoinverse.to_csv('./data/hypoinverse.csv', index=False)


# nonlinloc
f = open('./data/ridgecrest.sum.grid0.loc.hyp', 'r')
Lines  = f.readlines()
f.close()
nll_lat = []
nll_lon = []
nll_dep = []
nll_xx = []
nll_yy = []
nll_zz = []
for line in Lines:
    try:
        if (line.split()[0] == 'STATISTICS'):
            nll_xx.append(np.sqrt(float(line.split()[8])*8.02))
            nll_yy.append(np.sqrt(float(line.split()[14])*8.02))
            nll_zz.append(np.sqrt(float(line.split()[18])*8.02))
        if (line.split()[0] == 'FOCALMECH'):
            nll_lat.append(float(line.split()[2]))
            nll_lon.append(float(line.split()[3]))
            nll_dep.append(float(line.split()[4]))
    except:
        continue
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T,np.array(nll_xx).T, np.array(nll_yy).T, np.array(nll_zz).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['Lat', 'Lon', 'Dep', 'erx', 'ery', 'unc_z'])
catalog_nll['unc_x'] = catalog_nll.apply(lambda x: np.sqrt(x['erx']**2+x['ery']**2) , axis=1)
catalog_nll = catalog_nll[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_nll.to_csv('./data/NLL.csv', index=False)


# nonlinloc ssst
# first sort out the event sequence
f = open('./data/YifanYu_2024.sum.grid0.loc.hyp', 'r')
Lines  = f.readlines()
f.close()
nll_lat = []
nll_lon = []
nll_dep = []
nll_xx = []
nll_yy = []
nll_zz = []
nll_order = []
for line in Lines:
    try:
        if (line.split()[0] == 'GEOGRAPHIC'):
            nll_order.append(float(line.split()[4])*10000 + float(line.split()[5])*100 + float(line.split()[6]))
        if (line.split()[0] == 'STATISTICS'):
            nll_xx.append(np.sqrt(float(line.split()[8])*8.02))
            nll_yy.append(np.sqrt(float(line.split()[14])*8.02))
            nll_zz.append(np.sqrt(float(line.split()[18])*8.02))
        if (line.split()[0] == 'FOCALMECH'):
            nll_lat.append(float(line.split()[2]))
            nll_lon.append(float(line.split()[3]))
            nll_dep.append(float(line.split()[4]))
    except:
        continue
arr1inds = np.array(nll_order).argsort()
nll_lat = np.array(nll_lat)[arr1inds]
nll_lon = np.array(nll_lon)[arr1inds]
nll_dep = np.array(nll_dep)[arr1inds]
nll_xx = np.array(nll_xx)[arr1inds]
nll_yy = np.array(nll_yy)[arr1inds]
nll_zz = np.array(nll_zz)[arr1inds]
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T,np.array(nll_xx).T, np.array(nll_yy).T, np.array(nll_zz).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['Lat', 'Lon', 'Dep', 'erx', 'ery', 'unc_z'])
catalog_nll['unc_x'] = catalog_nll.apply(lambda x: np.sqrt(x['erx']**2+x['ery']**2) , axis=1)
catalog_nll = catalog_nll[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_nll.to_csv('./data/NLL_SSST.csv', index=False)


# velest
velest_lat = []
velest_lon = []
velest_dep = []
velest_erx = []
velest_ery = []
velest_erz = []
f = open('./velest/hypocenter_.CNV', 'r')
lines = f.readlines()
f.close()
for line in lines:
    if line[0] == ' ':
        velest_lat.append(float(line.split()[3][:-1]))
        velest_lon.append(-float(line.split()[4][:-1]))
        velest_dep.append(float(line.split()[5]))
f = open('./velest/sin.cnv', 'r')
Lines = f.readlines()
f.close()
flag = 0
for line in Lines:
     if len(line.split()) < 2:
          continue
     if line.split()[1] == 'ERX':
          flag = 1
          continue
     if flag == 1:
          velest_erx.append(float(line.split()[0])*np.sqrt(2.8))
          velest_ery.append(float(line.split()[1])*np.sqrt(2.8))
          velest_erz.append(float(line.split()[2])*np.sqrt(2.8))
          flag = 0
velest = np.stack((np.array(velest_lat).T, np.array(velest_lon).T, np.array(velest_dep).T, np.array(velest_erx).T, np.array(velest_ery).T, np.array(velest_erz).T), axis=1)
catalog_vele = pd.DataFrame(velest, columns=['Lat', 'Lon', 'Dep','ERX', 'ERY', 'unc_z'])
catalog_vele['unc_x'] = catalog_vele.apply(lambda x: np.sqrt( x['ERX']**2 + x['ERY']**2 ), axis=1)
catalog_vele = catalog_vele[['Lat', 'Lon', 'Dep', 'unc_x', 'unc_z']]
catalog_vele.to_csv('./data/velest.csv', index=False)









# # hypoinverse
# catalog_hypoinverse = pd.read_csv("./hypoinverse/ERC_1_catOut.sum", sep="\s+")
# f = open('./hypoinverse/prtOut.prt', 'r')
# lines = f.readlines()
# count = 0
# l1 = []
# az = []
# dip = []
# l2 = []
# l3 = []
# for line in lines:
#     try:
#         if line.split()[0] == 'ERROR':
#             l1.append(float(line.split()[5]))
#             az.append(float(line.split()[6]))
#             dip.append(float(line.split()[7].strip('>-<')))
#             l2.append(float(line.split()[8]))
#             l3.append(float(line.split()[11]))
#             count += 1
#     except:
#         continue
# catalog_hypoinverse['l1'] = l1   
# catalog_hypoinverse['l2'] = l2
# catalog_hypoinverse['l3'] = l3
# catalog_hypoinverse['az'] = az
# catalog_hypoinverse['dip'] = dip
# print('Hypoinverse')
# print(count)
# data = catalog_hypoinverse[['LAT', 'LON', 'DEPTH', 'l1','l2', 'l3','az','dip', 'ERH', 'ERZ']]
# data.to_csv('./hypoinverse.csv',index=False)

# # NonLinLoc
# f = open('./lomax/loc_ALomax/ridgecrest.sum.grid0.loc.hyp', 'r')
# # NLL_SSST
# #f = open('./YifanYu_2024.sum.grid0.loc.hyp','r')
# Lines  = f.readlines()
# f.close()
# nll_lat = []
# nll_lon = []
# nll_dep = []
# nll_l1 = []
# nll_l2 = []
# nll_l3 = []
# nll_az = []
# nll_dip = []
# nll_rota = []
# nll_xx = []
# nll_yy = []
# nll_zz = []
# for line in Lines:
#     try:
#         if (line.split()[0] == 'QML_ConfidenceEllipsoid'):
#             nll_l1.append(float(line.split()[2]))
#             nll_l2.append(float(line.split()[6]))
#             nll_l3.append(float(line.split()[4]))
#         if (line.split()[0] == 'STATISTICS'):
#             nll_dip.append(float(line.split()[28]))
#             nll_az.append(float(line.split()[26]))
#             nll_xx.append(np.sqrt(float(line.split()[8])*8.02))
#             nll_yy.append(np.sqrt(float(line.split()[14])*8.02))
#             nll_zz.append(np.sqrt(float(line.split()[18])*8.02))
#         if (line.split()[0] == 'FOCALMECH'):
#             nll_lat.append(float(line.split()[2]))
#             nll_lon.append(float(line.split()[3]))
#             nll_dep.append(float(line.split()[4]))
#     except:
#         continue
# nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T, np.array(nll_l1).T, np.array(nll_l2).T, np.array(nll_l3).T, np.array(nll_az).T, np.array(nll_dip).T,np.array(nll_xx).T, np.array(nll_yy).T, np.array(nll_zz).T) , axis=1)
# catalog_nll = pd.DataFrame(nll, columns=['LAT', 'LON', 'DEPTH', 'l1', 'l2','l3','az','dip', 'erx', 'ery', 'erz'])
# catalog_nll.to_csv('./nll.csv', index=False)

# velest

# velest_lat = []
# velest_lon = []
# velest_dep = []
# velest_erx = []
# velest_ery = []
# velest_erz = []
# f = open('./velest/hypocenter_.CNV', 'r')
# lines = f.readlines()
# f.close()
# for line in lines:
#     if line[0] == ' ':
#         velest_lat.append(float(line.split()[3][:-1]))
#         velest_lon.append(-float(line.split()[4][:-1]))
#         velest_dep.append(float(line.split()[5]))
# f = open('./velest/_sin.cnv', 'r')
# Lines = f.readlines()
# f.close()
# flag = 0
# for line in Lines:
#      if len(line.split()) < 2:
#           continue
#      if line.split()[1] == 'ERX':
#           flag = 1
#           continue
#      if flag == 1:
#           velest_erx.append(float(line.split()[0])*np.sqrt(2.8))
#           velest_ery.append(float(line.split()[1])*np.sqrt(2.8))
#           velest_erz.append(float(line.split()[2])*np.sqrt(2.8))
#           flag = 0
# velest = np.stack((np.array(velest_lat).T, np.array(velest_lon).T, np.array(velest_dep).T, np.array(velest_erx).T, np.array(velest_ery).T, np.array(velest_erz).T), axis=1)
# catalog_vele = pd.DataFrame(velest, columns=['LAT', 'LON', 'DEPTH','ERX', 'ERY', 'ERZ'])
# catalog_vele.to_csv('./velest.csv', index=False)

# hyposvi
# catalog_hyposvi = pd.read_csv(f"./hyposvi/data/catalog_svi9.csv_svi")
# data = catalog_hyposvi[['latitude', 'longitude','depth','unc_h_max','unc_h_min', 'unc_z']]
# data.to_csv('./hyposvi.csv', index=False)

import pandas as pd
import numpy as np

# prepare the data from each program for the uncertainty quantification
# save as csv with location, 95% confidence interval ellipsoid parameters,

# hypoinverse
catalog_hypoinverse = pd.read_csv("./hypoinverse/ERC_1_catOut.sum", sep="\s+")
f = open('./hypoinverse/prtOut.prt', 'r')
lines = f.readlines()
count = 0
l1 = []
az = []
dip = []
l2 = []
l3 = []
for line in lines:
    try:
        if line.split()[0] == 'ERROR':
            l1.append(float(line.split()[5]))
            az.append(float(line.split()[6]))
            dip.append(float(line.split()[7].strip('>-<')))
            l2.append(float(line.split()[8]))
            l3.append(float(line.split()[11]))
            count += 1
    except:
        continue
catalog_hypoinverse['l1'] = l1   
catalog_hypoinverse['l2'] = l2
catalog_hypoinverse['l3'] = l3
catalog_hypoinverse['az'] = az
catalog_hypoinverse['dip'] = dip
print('Hypoinverse')
print(count)
data = catalog_hypoinverse[['LAT', 'LON', 'DEPTH', 'l1','l2', 'l3','az','dip', 'ERH', 'ERZ']]
data.to_csv('./hypoinverse.csv',index=False)

# NonLinLoc
f = open('./lomax/loc_ALomax/ridgecrest.sum.grid0.loc.hyp', 'r')
Lines  = f.readlines()
f.close()
nll_lat = []
nll_lon = []
nll_dep = []
nll_l1 = []
nll_l2 = []
nll_l3 = []
nll_az = []
nll_dip = []
nll_rota = []
nll_xx = []
nll_yy = []
nll_zz = []
for line in Lines:
    try:
        if (line.split()[0] == 'QML_ConfidenceEllipsoid'):
            nll_l1.append(float(line.split()[2]))
            nll_l2.append(float(line.split()[6]))
            nll_l3.append(float(line.split()[4]))
        if (line.split()[0] == 'STATISTICS'):
            nll_dip.append(float(line.split()[28]))
            nll_az.append(float(line.split()[26]))
            nll_xx.append(float(line.split()[8]))
            nll_yy.append(float(line.split()[14]))
            nll_zz.append(float(line.split()[18]))
        if (line.split()[0] == 'FOCALMECH'):
            nll_lat.append(float(line.split()[2]))
            nll_lon.append(float(line.split()[3]))
            nll_dep.append(float(line.split()[4]))
    except:
        continue
nll = np.stack((np.array(nll_lat).T, np.array(nll_lon).T, np.array(nll_dep).T, np.array(nll_l1).T, np.array(nll_l2).T, np.array(nll_l3).T, np.array(nll_az).T, np.array(nll_dip).T,np.array(nll_xx).T, np.array(nll_yy).T, np.array(nll_zz).T) , axis=1)
catalog_nll = pd.DataFrame(nll, columns=['LAT', 'LON', 'DEPTH', 'l1', 'l2','l3','az','dip', 'xx', 'yy', 'zz'])
catalog_nll.to_csv('./nll.csv', index=False)

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
f = open('./velest/_sin.cnv', 'r')
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
catalog_vele = pd.DataFrame(velest, columns=['LAT', 'LON', 'DEPTH','ERX', 'ERY', 'ERZ'])
catalog_vele.to_csv('./velest.csv', index=False)

# hyposvi
catalog_hyposvi = pd.read_csv(f"./hyposvi/data/catalog_svi9.csv_svi")
data = catalog_hyposvi[['latitude', 'longitude','depth','unc_h_max','unc_h_min', 'unc_z']]
data.to_csv('./hyposvi.csv', index=False)

# hypodd
# empty_df = pd.DataFrame()
# for i in range(1,11):
#     catalog_dd = pd.read_csv(f"./hypodd/{i}.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
# "NCTS", "RCC", "RCT", "CID"])
#     empty_df = pd.concat([empty_df, catalog_dd])
# catalog_dd = empty_df.sort_values('ID')
# catalog_dd.to_csv('./hypodd/result.csv',index=False)
catalog_dd = pd.read_csv('./hypodd/result.csv')
data = catalog_dd[['LAT','LON','DEPTH','EX','EY','EZ','ID']]
data.to_csv('./hypodd.csv', index=False)


# growclust
catalog_gc = pd.read_csv(f"./growclust/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
data = catalog_gc[['latR','lonR','depR','eh','ez','et','qID']]
data.to_csv('./growclust.csv', index=False)

# xcorloc
catalog_xcloc = pd.read_csv(f"./xcorloc/out.loc_xcor", sep="\s+", names=["qID", "yr","mon","day", "hr","min","sec","lat","lon","dep","mag","pair", "pick_used", "erx", "ery", "erz", "ert", "rms_phs", "rms_dif", "type"])
data = catalog_xcloc[['lat','lon','dep','erx','ery','erz','ert','qID']]
data.to_csv('./xcorloc.csv', index=False)

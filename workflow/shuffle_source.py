import pandas as pd
import numpy as np
import pymap3d as pm

catalog = pd.read_csv(f"./ridgecrest_qtm.cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

idx = catalog.cID.value_counts()
database = catalog[catalog.cID.isin(idx.index[idx.gt(400)])]
data = database.sample(n=1000, random_state=1)
o_lat = 35.4
o_lon = -117.956
sources = data[["latR", "lonR", "depR", "cID"]].to_numpy()
np.save('o_source.npy', sources)
for source in sources:
    x,y,z = pm.geodetic2enu(source[0], source[1], source[2]*1000, o_lat, o_lon, 0)
    source[0] = x
    source[1] = y
    source[2] = z
np.save('source.npy', sources)
import numpy as np
import pandas as pd
# for stations
stations = np.load('../o_station.npy')
print(stations.shape)
f = open('./gmt/stations.txt', 'w')
for sta in stations:
    f.write(f'{sta[1]:.3f}')
    f.write(' ')
    f.write(f'{sta[0]:.3f}')
    f.write('\n')
f.close()

# for sources
catalog = pd.read_csv(f"./gmt/ridgecrest_qtm.cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

idx = catalog.cID.value_counts()
database = catalog[catalog.cID.isin(idx.index[idx.gt(400)])]
print(len(database))
sources = database[['lonR', 'latR', 'depR']]
sources.to_csv('./gmt/source.csv', index=False)
import pandas as pd
import json
import numpy as np
svi_lat = []
svi_lon = []
svi_dep = []


with open('./Events2/Catalogue.json') as f:
    d = json.load(f)
for i in d.keys():
    print(i)
    try:
        a = d[i]['location']['Hypocentre']
    except:
        continue
    if a[0] != a[0]:
        continue
        print(d[i]['Picks']['X'])
    svi_lat.append(a[1])
    svi_lon.append(a[0])
    svi_dep.append(a[2])



svi = np.stack((np.array(svi_lat).T, np.array(svi_lon).T, np.array(svi_dep).T), axis=1)
catalog_vele = pd.DataFrame(svi, columns=['LAT', 'LON', 'DEPTH'])
catalog_vele.to_csv('./hyposvi_cat.csv', index=False)

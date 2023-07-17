import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

stations = np.load('sta.npy')
sources = np.load('source.npy')
catalog_hypoDD = pd.read_csv(f"./hypoDD/hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_gc = pd.read_csv(f"./growclust/OUT/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

fig = plt.figure(figsize=[14,10])
ax = fig.add_subplot(projection='3d')
ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue')
ax.scatter(catalog_hypoDD['LAT'], catalog_hypoDD['LON'], catalog_hypoDD['DEPTH'], zdir='z', label='hypoDD', marker='*', c='red')
ax.scatter(catalog_gc['latR'], catalog_gc['lonR'], catalog_gc['depR'], zdir='z', label='GrowClust', marker='*', c='green')
ax.legend()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Z')
ax.invert_zaxis()
ax.view_init(elev=20., azim=-35, roll=0)

plt.show()
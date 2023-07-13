import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

stations = np.load('sta.npy')
sources = np.load('source.npy')
catalog_hypoDD = pd.read_csv(f"./hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
fig = plt.figure(figsize=[12,6])
ax = fig.add_subplot(projection='3d')
ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue')
ax.scatter(catalog_hypoDD['LAT'], catalog_hypoDD['LON'], catalog_hypoDD['DEPTH'], zdir='z', label='result', marker='*', c='red')
ax.legend()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Z')
ax.invert_zaxis()
ax.view_init(elev=20., azim=-35, roll=0)

plt.show()
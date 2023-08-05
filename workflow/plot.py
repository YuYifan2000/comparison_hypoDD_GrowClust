import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation
def rotate(angle):
    ax.vie_init(azim=angle)

stations = np.load('station.npy')
sources = np.load('source.npy')
catalog_gc = pd.read_csv(f"./out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
catalog_dd = pd.read_csv(f"./hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_vele = pd.read_csv("./hypoDD.loc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])

fig = plt.figure(figsize=[8,10])
ax = fig.add_subplot(projection='3d')
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue', s=2.5)
ax.scatter(catalog_vele["LAT"], catalog_vele["LON"], catalog_vele["DEPTH"], zdir="z", label="velest", marker="*", c="red", s=2.5)
ax.legend()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Z')
ax.invert_zaxis()
ax.grid(False)

rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0,362,2),interval=100)
rot_animation.save('rotation.gif', dpi=200, writer='imagemagick')
plt.close()

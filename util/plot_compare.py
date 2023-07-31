import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation

stations = np.load('sta.npy')
sources = np.load('source.npy')
n = len(sources[:,2])
catalog_hypoDD = pd.read_csv(f"./hypoDD/hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_gc = pd.read_csv(f"./growclust/OUT/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

fig = plt.figure(figsize=[14,10])
ax = fig.add_subplot(projection='3d')
ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
#ax.scatter(sources[:,0]+(np.random.rand(n)-0.5)/10., sources[:,1]+(np.random.rand(n)-0.5)/10., sources[:,2]+(np.random.rand(n)-0.5)*1.2, zdir='z', label='random', s=2)
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue', s=2.5)
ax.scatter(catalog_hypoDD['LAT'], catalog_hypoDD['LON'], catalog_hypoDD['DEPTH'], zdir='z', label='hypoDD',  c='red', s=2.5)
ax.set_zlim([0,20])
ax.scatter(catalog_gc['latR'], catalog_gc['lonR'], catalog_gc['depR'], zdir='z', label='GrowClust', c='green', s=2.5)
ax.legend()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Z')
ax.invert_zaxis()

def init():
    ax.view_init(elev=10., azim=0)
    return fig,
def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=10, blit=True)
anim.save('ana.mp4', fps=20, extra_args=['-vcodec', 'libx264'])

plt.close()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(sources[:,1], sources[:,0], label='sources', marker = "*", c='blue', s=4.5)
ax.scatter(catalog_hypoDD['LON'], catalog_hypoDD['LAT'], label='hypoDD',  c='red', s=4.5)
ax.scatter(catalog_gc['lonR'], catalog_gc['latR'], label='GrowClust',  c='green', s=4.5)
ax.scatter(stations[:,1], stations[:,0], marker='^', s=8)
ax.legend()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
#ax.set_xlim([30, 30.8])
#ax.set_ylim([120, 120.8])
plt.show()
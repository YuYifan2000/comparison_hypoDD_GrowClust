import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation

stations = np.load('sta.npy')
sources = np.load('source.npy')
catalog_hypoDD = pd.read_csv(f"./hypoDD/hypoDD.reloc", sep="\s+", names=["ID", "LAT", "LON", "DEPTH", "X", "Y", "Z", "EX", "EY", "EZ", "YR", "MO", "DY", "HR", "MI", "SC", "MAG", "NCCP", "NCCS", "NCTP",
"NCTS", "RCC", "RCT", "CID"])
catalog_gc = pd.read_csv(f"./growclust/OUT/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

fig = plt.figure(figsize=[14,10])
ax = fig.add_subplot(projection='3d')
ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
ax.scatter(sources[:,0]+(np.random.rand(1)[0]-0.5)/10., sources[:,1]+(np.random.rand(1)[0]-0.5)/10.,sources[:,2]+(np.random.rand(1)[0]-0.5), zdir='z', label='random', marker="*")
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue')
ax.scatter(catalog_hypoDD['LAT'], catalog_hypoDD['LON'], catalog_hypoDD['DEPTH'], zdir='z', label='hypoDD', marker='*', c='red')
# ax.scatter(catalog_gc['latR'], catalog_gc['lonR'], catalog_gc['depR'], zdir='z', label='GrowClust', marker='*', c='green')
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


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=300, interval=20, blit=True)
anim.save('ana.mp4', fps=20, extra_args=['-vcodec', 'libx264'])

plt.close()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(sources[:,0], sources[:,1], label='sources', marker = "*", c='blue')
ax.scatter(catalog_hypoDD['LAT'], catalog_hypoDD['LON'], label='hypoDD', marker='*', c='red')
ax.scatter(catalog_gc['latR'], catalog_gc['lonR'], label='GrowClust', marker='*', c='green')
ax.legend()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
plt.show()
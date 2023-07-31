import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation

stations = np.load('sta.npy')
sources = np.load('source.npy')
n = len(sources[:,2])
catalog_gc = pd.read_csv(f"./growclust/OUT/out.growclust_cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])

fig = plt.figure(figsize=[14,10])
ax = fig.add_subplot(projection='3d')
ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*", c='blue', s=2.5)
ax.set_zlim([0,20])
ax.scatter(catalog_gc['latC'], catalog_gc['lonC'], catalog_gc['depC'], zdir='z', label='Velest', c='red', s=2.5)
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
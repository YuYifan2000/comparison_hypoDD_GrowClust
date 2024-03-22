import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors

def get_cmp():
    f = open('./roma.cpt', 'r')
    Lines = f.readlines()
    vals = np.ones((len(Lines)-3, 4))
    for i in range(0, len(Lines)-3):
        line = Lines[i].split()
        vals[i,0] = float(line[1].split('/')[0]) / 256
        vals[i,1] = float(line[1].split('/')[1])/ 256
        vals[i,2] = float(line[1].split('/')[2])/256
    newcmp = mcolors.ListedColormap(vals)
    return newcmp
nz = 441
nx = 701
ny = 1001
dx = 0.1
dz = 0.05
dy = 0.1

x1 = np.linspace(0, dx*(nx-1),nx)
y1 = np.linspace(0, dy*(ny-1),ny)
z1 = np.linspace(0, dz*(nz-1),nz)

  
data = np.load('./vk_ele_vel_p.npy')/1000.
air = np.load('./air.npy')
for point in air:
    data[tuple(point[:3].astype('int'))] = np.nan
# np.save('./alter_velo.npy', data)
# data = np.load('./ele_vel_p.npy')
# cross file in Y = 70
profile = data[:,450,0:]
#profile = data[40,:,0:45]
#profile = profile[::-1,:]
print(profile.shape)
#fig = plt.figure(figsize = [6,5], constrained_layout=True)
fig = plt.figure()
ax = fig.add_subplot(111)

cmap = get_cmp()
# cmap.set_under('white')
c = ax.imshow(profile.T, origin='upper', cmap=cmap, vmin=2, vmax=7, extent=[0,70,20, -2], aspect='equal')
ax.set_ylim([20,-2])
cbar = fig.colorbar(c, ax=ax, shrink=0.3,location='top')
cbar.locator = plt.MaxNLocator(4)
cbar.update_ticks()
ax.set_xlabel('Distance (km)',fontweight='bold')
ax.set_ylabel('Elevation (km)',fontweight='bold')
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
ax.yaxis.set_major_locator(plt.MaxNLocator(5))
plt.savefig('./cross_profile.png',dpi=300, transparent=True)
plt.close()
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import animation
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
z1 = np.linspace(-dz*(400),0,nz)

  
data = np.load('./vk_ele_vel_p.npy')/1000.
#print(data.shape)
#air = np.load('./air.npy')
# f = open('../ucvm/target/test_results.log', 'r')
# z = np.zeros([nx,ny])
# for i in range(0, nx):
#     print(i)
#     for j in range(0,ny):
#         for k in range(40,nz):
#             line = f.readline()
#             if k == 40:
#                 elevation = float(line.split()[3])
#                 z[i,j] = elevation
# np.save('ele.npy', z)
# velocity
z = np.load('ele.npy')

X, Y = np.meshgrid(x1,y1)
print(Y.shape)
velo = np.zeros_like(z)
for i in range(0, nx):
    for j in range(0, ny):
        velo[i,j] = data[i,j,int(40-np.floor(z[i,j]/1000./dz))]

minv, maxv = velo.min(), velo.max()
norm = matplotlib.colors.Normalize(2.5, 7)
m = plt.cm.ScalarMappable(norm=norm, cmap=get_cmp())
m.set_array([])
fcolors = m.to_rgba(velo.T)
print(fcolors.shape)
# plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.grid(False)
surf = ax.plot_surface(X,Y,z.T, facecolors=fcolors, vmin=minv, vmax=maxv, shade=False)
ax.set_xlabel('x (km)',fontweight='bold')
ax.set_aspect('equalxy')
ax.set_ylabel('y (km)',fontweight='bold')
ax.set_zlabel('Elevation (m)',fontweight='bold')
ax.set_zlim([200, 2500])

#cbar = fig.colorbar(m, shrink=0.5,  fraction=0.1, label='Velocity (km/s)')
cbar = fig.colorbar(m, shrink=0.5,  fraction=0.1)
cbar.locator = plt.MaxNLocator(4)
cbar.update_ticks()
ax.xaxis.set_major_locator(plt.MaxNLocator(3))
ax.yaxis.set_major_locator(plt.MaxNLocator(3))
ax.zaxis.set_major_locator(plt.MaxNLocator(3))

ax.view_init(elev=60, azim=-150)
plt.savefig('./3d_ele.png',dpi=300, transparent=True)
plt.close()
import numpy as np
import matplotlib.pyplot as plt
import pymap3d as pm
import matplotlib
import matplotlib.gridspec as gridspec

matplotlib.use('agg')
np.random.seed(0)
sample = 20

# the velocity structure used in the location inversion
velo_1d = np.array([4.746, 4.793, 4.799, 5.045, 5.721, 5.879, 6.604, 6.708, 6.725, 7.80])
velo_depth = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 30.])
vel = np.load('../vk_ele_vel_p.npy')
# the origin coordinates in 3d model
o_lat = 35.4
o_lon = -117.956
dx = 100
dz = 50
dy = 100
# choose the two regions 
# return the corresponding x & y indices which will be used in retreiving data
# 1. northwestern part, depth vary a lot
lat_1 = 35.8
lat_2 = 36.1
lon_1 = -117.9
lon_2 = -117.6
x1, y1, z1 = pm.geodetic2enu(lat_1, lon_1, 0, o_lat, o_lon,0)
x2, y2, z2 = pm.geodetic2enu(lat_2, lon_2, 0, o_lat, o_lon,0)
x1_index = x1 // dx
y1_index = y1 // dy
x2_index = x2 // dx
y2_index = y2 // dy
select_x = np.random.randint(x1_index, high=x2_index, size=sample)
select_y = np.random.randint(y1_index, y2_index, size=sample)

select_velo_1 = vel[select_x, select_y, 40:341:20] / 1000.
print(select_velo_1.shape)
# 2. southeastern part, depth is quite correct
lat_1 = 35.54
lat_2 = 35.78
lon_1 = -117.6
lon_2 = -117.4
x1, y1, z1 = pm.geodetic2enu(lat_1, lon_1, 0, o_lat, o_lon,0)
x2, y2, z2 = pm.geodetic2enu(lat_2, lon_2, 0, o_lat, o_lon,0)
x1_index = x1 // dx
y1_index = y1 // dy
x2_index = x2 // dx
y2_index = y2 // dy
select_x = np.random.randint(x1_index, high=x2_index, size=sample)
select_y = np.random.randint(y1_index, y2_index, size=sample)

select_velo_2 = vel[select_x, select_y, 40:341:20] / 1000.
# plot the velocity comparison
depth = np.linspace(0, 15, 16)

fig = plt.figure(figsize=[10,6], constrained_layout=True)
gs = gridspec.GridSpec(1, 2, figure=fig, hspace=0.1)
ax = fig.add_subplot(gs[0,0])
ax.set_title('Misfit Area', fontsize=8, fontweight="bold")
ax.plot(velo_1d, velo_depth, c='k', linewidth=2,label='1D structure')
for i in range(0, sample):
    ax.plot(select_velo_1[i, :], depth, c='gray', linewidth=0.5)
ax.plot(np.mean(select_velo_1, axis=0), depth, c='blue', linewidth=1,label='mean')
ax.plot([1,1],[1,1],c='gray',linewidth=0.5,label='3D slice')
ax.set_xlabel('Velocity (km/s)')
ax.set_ylabel('Depth (km)')
#ax.invert_yaxis()
ax.set_ylim([15,0])
ax.set_xlim([3,8])
ax.legend()
ax = fig.add_subplot(gs[0,1])
ax.set_title('Accurate Area', fontsize=8, fontweight="bold")
ax.plot(velo_1d, velo_depth, c='k', linewidth=2,label='1D structure')
for i in range(0, sample):
    ax.plot(select_velo_2[i, :], depth, c='gray', linewidth=0.5)
ax.plot(np.mean(select_velo_2, axis=0), depth, c='blue', linewidth=1,label='mean')
ax.plot([1,1],[1,1],c='gray',linewidth=0.5,label='3D slice')

ax.set_xlabel('Velocity (km/s)')
ax.set_ylabel('Depth (km)')
ax.legend()
#ax.invert_yaxis()
ax.set_ylim([15,0])
ax.set_xlim([3,8])

plt.savefig('./velocity_comparion.png', dpi=300)

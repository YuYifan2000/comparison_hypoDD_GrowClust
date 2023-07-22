import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt

nz = 31
nx = 201
ny = 221
dx = 1
dz = 1
dy = 1

v_in = np.array([[0., 4.6], [6., 5.8], [15., 7.0], [23., 8.0], [28., 8.5], [30., 8.3]])
all_depth = np.linspace(0, 30, 31)
vz = np.interp(all_depth, v_in[:,0], v_in[:,1])
v = np.expand_dims(vz,1)
h = np.ones([1,nx])
vel = np.multiply(v,h,dtype='float32') #z,x
vel3d=np.zeros([nz,nx,ny],dtype='float32')
for ii in range(ny):
	vel3d[:,:,ii]=vel
vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
p_vel_structure = vxyz.flatten(order='F')
source = np.array([1,1,10])
tp = fmm.eikonal(p_vel_structure,xyz=source,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
print(tp[100,100,0])

fd = np.loadtxt('time')

ekfmm = tp[:,:,0]

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow((ekfmm-fd)*1000, cmap='seismic', vmin=-20, vmax=20)
ax.set_title('At surface')
ax.set_xlabel('X (grid point)')
ax.set_ylabel('Y (grid point)')
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('pyekfmm-FD (ms)')
plt.savefig('validation_grid_point.png', dpi=500)
plt.close()
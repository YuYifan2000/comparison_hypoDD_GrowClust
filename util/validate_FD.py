import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt
import pykonal

nz = 401
nx = 601
ny = 601
dx = 0.1
dz = 0.1
dy = 0.1
'''
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
'''
p_vel_structure = np.load('p_vel.npy')
source = np.array([30.,30.,16.])

# pykonal
# initialize the solver
'''
solver = pykonal.EikonalSolver(coord_sys="cartesian")
solver.velocity.min_coords = 0, 0, 0
solver.velocity.node_intervals = dx, dy, dz
solver.velocity.npts = nx, ny, nz
solver.velocity.values = vxyz
src_idx = source[0], source[1], source[2]
solver.traveltime.values[src_idx] = 0
solver.unknown[src_idx] = False
solver.trial.push(*src_idx)

# Solve the system.
solver.solve()
print(solver.traveltime.values[100, 100, 0])
'''
# fmm
tp = fmm.eikonal(p_vel_structure,xyz=source,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
print(tp[100,100,0])

fd = np.loadtxt('time')

ekfmm = tp[:,:,0]

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow((tp[:,:,0] - fd)*1000, cmap='seismic', vmin=-100, vmax=100)
ax.set_title('At surface')
ax.set_xlabel('X (grid point)')
ax.set_ylabel('Y (grid point)')
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('PYEKFMM-FD (ms)')
plt.savefig('pyekfmm-fd_grid_point.png', dpi=500)
plt.close()
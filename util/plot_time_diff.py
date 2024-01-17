import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt


nz = 401
nx = 601
ny = 601
dx = 0.1
dz = 0.05
dy = 0.1


print(f'Range: in x direction {(nx-1)*dx} in y direction {(ny-1)*dy} in z direction {(nz-1)*dz}')

# load velocity
#p_vel_structure, s_vel_structure = genearte_velocity(nx,ny,nz,dx,dy,dz)
p_vel_structure = np.load('p_vel.npy')
s_vel_structure = np.load('s_vel.npy')

source1 = np.array([30, 30, 13])
source2 = np.array([30, 30, 10])

p1 = fmm.eikonal(p_vel_structure,xyz=source1,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
p2 = fmm.eikonal(p_vel_structure,xyz=source2,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')

s1 = fmm.eikonal(s_vel_structure,xyz=source1,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
s2 = fmm.eikonal(s_vel_structure,xyz=source2,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')

fig = plt.figure(figsize=[12,6])
ax = fig.add_subplot(121)
im = ax.imshow(p1[:,:,0]-p2[:,:,0], vmin=-0.5, vmax=0.5)
cbar = fig.colorbar(im, ax=ax, fraction=0.1,orientation="horizontal")
cbar.set_label('Time(s)')
ax.set_title('P traveltime difference')
ax.set_xlabel('X(grid point)')
ax.set_ylabel('Y(grid point)')

ax = fig.add_subplot(122)
im = ax.imshow(s1[:,:,0]-s2[:,:,0], vmin=-0.5, vmax=0.5)
cbar = fig.colorbar(im, ax=ax, fraction=0.1,orientation="horizontal")
cbar.set_label('Time(s)')
ax.set_title('S traveltime difference')
ax.set_xlabel('X(grid point)')
ax.set_ylabel('Y(grid point)')

plt.show()
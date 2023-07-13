import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt


v1=1;
v2=3;
nz=100;
nx=501;
ny=501;
dx=1;
dz=0.2;
dy=1;
# vel=3.0*np.ones([101*101,1],dtype='float32'); #velocity axis must be x,y,z respectively
v=np.linspace(v1,v2,nz);
v=np.expand_dims(v,1);
h=np.ones([1,nx])
vel=np.multiply(v,h,dtype='float32'); #z,x

vel3d=np.zeros([nz,nx,ny],dtype='float32');
for ii in range(ny):
	vel3d[:,:,ii]=vel
# plt.figure();
# plt.imshow(vel3d[:,:,0]);
# plt.jet();plt.show()

vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2);
t=fmm.eikonal(vxyz.flatten(order='F'),xyz=np.array([200,200,12]),ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2);
print(t.shape)
time=t.reshape(nx,ny,nz,order='F');#first axis (vertical) is x, second is z
print(time.shape)
print(time[0][:][0])
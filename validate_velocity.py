import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from scipy.signal import detrend
from scipy.fft import fft2, fftfreq, ifft2, fftn, ifftn, fftshift,fft
import pyekfmm as fmm

def von_Karman_3d_velo(nx,ny,nz,delta_x, delta_y, delta_z, ar, az, kappa, epsilon):

	Vs = 2 * np.random.rand(nx, ny, nz)-1

	# 3D FFT
	Y2 = fftn(Vs)
	# whiten
	Y2 = np.exp(1j * np.angle(Y2))
	# define the wavenumber scale in X and Z
	kx = fftfreq(nx, delta_x)*2*np.pi
	ky = fftfreq(ny, delta_y)*2*np.pi
	kz = fftfreq(nz, delta_z)*2*np.pi
	kx_, ky_, kz_ = np.meshgrid(ky,kx,kz)
	K_sq = ky_**2 * ar**2 + kx_**2 * ar**2 + kz_**2 * az**2
	d = 3.
	# Von Karman distribution
	#P_K = (np.power(2,d) * np.power(np.pi,d/2) * np.power(epsilon, 2) * ar * ar * az * gamma(kappa+d/2)) / (gamma(abs(kappa)) * np.power(1+K_sq,kappa+d/2.))
	P_K = (np.power(2,d) * np.power(np.pi,d/2.) * ar * ar * az * gamma(kappa+d/2)) / (gamma(abs(kappa)) * np.power(1+K_sq,kappa+d/2.))
	Y2 = Y2 * np.sqrt(P_K)
	# ifft
	dV = np.real(ifftn(Y2))
	dV = detrend(dV, type='constant')
	dV = epsilon / np.std(dV) * dV
	return dV

def genearte_velocity(nx,ny,nz,dx,dy,dz):
	depth = 10.
	dV = von_Karman_3d_velo(nx,ny,int(depth/dz),dx,dy,dz,0.5,0.1,0.04,0.107)
	# set up velocity structure
	# for P velocity
	f = open('./vjma2001', 'r')
	tmp = f.readlines()
	f.close()
	v = []
	for i in tmp[:nz]:
		v.append(float(i.split()[0]))
	v = np.array(v)
	v = np.expand_dims(v,1)
	h = np.ones([1,nx])
	vel = np.multiply(v,h,dtype='float32') #z,x
	vel3d=np.zeros([nz,nx,ny],dtype='float32')
	for ii in range(ny):
		vel3d[:,:,ii]=vel
	vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
	origin = vxyz.flatten(order='F')
	vxyz[:,:,:int(depth/dz)] *= (1+dV)
	p_vel_structure = vxyz.flatten(order='F')


	return p_vel_structure, origin


p_velo = np.load('p_vel_array.npy')
print(p_velo.shape)
a = p_velo[1,:,2]
fig = plt.figure(figsize=[7,8])

f2 = fft(a)
ax = fig.add_subplot(311)

ax.set_ylabel('PSD')
ax.set_yscale('log')
ax.set_xlim([0.5,80])
ax.set_xscale('log')
ax.plot(fftfreq(a.size,0.1)[:a.size//2]*np.pi*2, np.abs(fft(a))[:a.size//2]**2, label='y-direction', linewidth=1.5)
ax.legend()
a = p_velo[1,1,:]
ax = fig.add_subplot(313)

ax.set_ylabel('PSD')
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlim([0.5,80])
ax.set_xlabel('wavenumber radian/km')
ax.plot(fftfreq(a.size,0.05)[:a.size//2]*np.pi*2, np.abs(fft(a))[:a.size//2]**2, label='z-direction', linewidth=1.5)
ax.legend()
a = p_velo[:,1,1]
ax = fig.add_subplot(312)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(fftfreq(a.size,0.1)[:a.size//2]*np.pi*2, np.abs(fft(a))[:a.size//2]**2, label='x-direction', linewidth=1.5)

ax.set_ylabel('PSD')
ax.legend()
ax.set_xlim([0.5,80])
plt.savefig('scatter_fft.png', dpi=500)
plt.close()
'''
# check scatter velocity effects on the travel time calculator
nz = 400
nx = 500
ny = 500
dx = 0.1
dz = 0.05
dy = 0.1
p1, p0 = genearte_velocity(nx,ny,nz,dx,dy,dz)
source = np.array([15, 15, 16.2])
tp1 = fmm.eikonal(p1,xyz=source,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
tp0 = fmm.eikonal(p0,xyz=source,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')

fig = plt.figure(figsize=[12,6])
ax = fig.add_subplot(131)
im = ax.imshow(tp1[:,:,0], vmin=2, vmax=7)
cbar = fig.colorbar(im, ax=ax, fraction=0.1,orientation="horizontal")
cbar.set_label('Time(s)')
ax.set_title('with von Karman velocity')
ax.set_xlabel('X(grid point)')
ax.set_ylabel('Y(grid point)')

ax = fig.add_subplot(132)
im = ax.imshow(tp0[:,:,0], vmin=2, vmax=7)
cbar = fig.colorbar(im, ax=ax, fraction=0.1, orientation="horizontal")
cbar.set_label('Time(s)')
ax.set_title('without von Karman velocity')
ax.set_xlabel('X(grid point)')
ax.set_ylabel('Y(grid point)')

ax = fig.add_subplot(133)
im = ax.imshow(tp0[:,:,0]-tp1[:,:,0], cmap='seismic', vmin=-1.5, vmax=1.5)
cbar = fig.colorbar(im, ax=ax, fraction=0.1, orientation="horizontal")
cbar.set_label('Time(s)')
ax.set_title('Difference')
ax.set_xlabel('X(grid point)')
ax.set_ylabel('Y(grid point)')

plt.savefig('scatter_velocity.png', dpi=500)
plt.close()
'''
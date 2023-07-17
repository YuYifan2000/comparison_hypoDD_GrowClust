import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft2, fftfreq, ifft2, fftn, ifftn
from scipy.special import gamma

def scatter_velocity_perturbation(M, N, delta, ax, az, sigma, k):
	# double the size
	M = 2 * M
	N = 2 * N
	Vs = 2 * np.random.rand(M, N)-1

	# 2D FFT
	Y2 = fft2(Vs)
	# define the wavenumber scale in X and Z
	kx = fftfreq(M, delta)*2*np.pi
	kz = fftfreq(N, delta)*2*np.pi
	kx_, kz_ = np.meshgrid(kz, kx)

	K_sq = kx_**2 * ax**2 + kz_**2 * az**2
	# Von Karman distribution
	P_K = (4 * np.pi * gamma(k+1) * (ax*az)) / (gamma(abs(k)) * np.power(1+K_sq, k+1))
	Y2 = Y2 * np.sqrt(P_K)

	# ifft
	newV = ifft2(Y2)
	test = np.real(newV[:M, :N])
	test = sigma / np.std(test) * test
	m_mid = np.floor(M/4).astype('int')
	m_stop = (np.floor(M/4)+np.floor(M/2)).astype('int')
	n_mid = np.floor(N/4).astype('int')
	n_stop = (np.floor(N/4)+np.floor(N/2)).astype('int')
	dV = test[m_mid:m_stop, n_mid : n_stop]
	return dV

def von_Karman_3d_velo(nx,ny,nz,delta_x, delta_y, delta_z, ar, az, kappa, epsilon):
	N_x = nx * 2
	N_y = ny * 2
	N_z = nz * 2
	Vs = 2 * np.random.rand(N_x, N_y, N_z)-1

	# 3D FFT
	Y2 = fftn(Vs)
	print('done fftn')
	# define the wavenumber scale in X and Z
	kx = fftfreq(N_x, delta_x)*2*np.pi
	ky = fftfreq(N_y, delta_y)*2*np.pi
	kz = fftfreq(N_z, delta_z)*2*np.pi
	kx_, ky_, kz_ = np.meshgrid(ky,kx,kz)
	print('done mesh')
	K_sq = ky_**2 * ar**2 + kx_**2 * ar**2 + kz_**2 * az**2
	d = 3.
	# Von Karman distribution
	#P_K = (np.power(2,d) * np.power(np.pi,d/2) * np.power(epsilon, 2) * ar * ar * az * gamma(kappa+d/2)) / (gamma(abs(kappa)) * np.power(1+K_sq,kappa+d/2.))
	P_K = (np.power(2,d) * np.power(np.pi,d/2) * ar * ar * az * gamma(kappa+d/2)) / (gamma(abs(kappa)) * np.power(1+K_sq,kappa+d/2.))
	Y2 = Y2 * np.sqrt(P_K)
	# ifft
	newV = ifftn(Y2)
	print('done ifft')
	test = np.real(newV[:N_x, :N_y, :N_z])
	test = epsilon / np.std(test) * test
	x_mid = np.floor(N_x/4).astype('int')
	x_stop = np.floor(N_x/4+nx).astype('int')
	y_mid = np.floor(N_y/4).astype('int')
	y_stop = np.floor(N_y/4+ny).astype('int')
	z_mid = np.floor(N_z/4).astype('int')
	z_stop = np.floor(N_z/4+nz).astype('int')
	
	dV = test[x_mid:x_stop, y_mid:y_stop, z_mid : z_stop]
	return dV

def plot_velocity(vel3d):
	fig = plt.figure()
	ax = fig.add_subplot(121)
	ax.set_title('Depth at shallow, heterogeneity')
	ax.imshow(vel3d[10,:,:], cmap='jet')
	ax = fig.add_subplot(122)
	ax.set_title('Depth at deeper, constant')
	ax.imshow(vel3d[50,:,:], cmap='jet')
	plt.savefig('velocity.png', dpi=500)
	plt.close()
	

nz = 61
nx = 401
ny = 401
dx = 0.5
dz = 0.5
dy = 0.5
dV = von_Karman_3d_velo(nx,ny,int(10/dz),dx,dy,dz,0.5,0.1,0.04,0.107)

dvxyz = np.swapaxes(dV, 0, 2)

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
vel3d[:int(10/dz),:,:] += dvxyz
vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
p_vel_structure = vxyz.flatten(order='F')

plot_velocity(vel3d)

f = open('./vjma2001', 'r')
tmp = f.readlines()
f.close()
v = []
for i in tmp[:nz]:
    v.append(float(i.split()[1]))
v = np.array(v)
v = np.expand_dims(v,1)
h = np.ones([1,nx])
vel = np.multiply(v,h,dtype='float32') #z,x
vel3d=np.zeros([nz,nx,ny],dtype='float32')
for ii in range(ny):
    vel3d[:,:,ii]=vel
vel3d[:int(10/dz),:,:] += dvxyz
vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
s_vel_structure = vxyz.flatten(order='F')

np.save('p_vel', p_vel_structure)
np.save('s_vel', s_vel_structure)
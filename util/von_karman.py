import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftfreq, ifft2, fftn, ifftn, fftshift
from scipy.special import gamma
from scipy.signal import detrend

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
	dV = dV - np.mean(dV)
	dV = epsilon / np.std(dV) * dV
	fig = plt.figure()
	ax = fig.add_subplot(111)
	im = ax.imshow(dV[:,:,0], cmap='seismic')
	fig.colorbar(im, ax=ax)
	plt.show()
	return dV


nz = 500
nx = 500
ny = 500
dx = 0.1
dz = 0.1
dy = 0.1
depth = 4.
dV = von_Karman_3d_velo(nx,ny,nz,dx,dy,dz,0.5,0.1,0.04,0.107)
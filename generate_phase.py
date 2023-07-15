import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft2, fftfreq, ifft2
from scipy.special import gamma
from math import asin, atan2, cos, degrees, radians, sin

def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)

def plot_source_station(stations,sources):
	fig = plt.figure(figsize=[12,6])
	ax = fig.add_subplot(projection='3d')
	ax.scatter(stations[:,0], stations[:,1], zs=0, zdir='z', label='station', marker="^")
	ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', marker = "*")
	ax.legend()
	ax.set_xlabel('Latitude')
	ax.set_ylabel('Longitude')
	ax.set_zlabel('Z')
	ax.invert_zaxis()
	ax.view_init(elev=20., azim=-35, roll=0)
	plt.savefig('source_station.png', dpi=500)
	#plt.show()
	plt.close()

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
	print(Y2.shape)
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
	ax.imshow(vel3d[:,:,0], cmap='jet')
	ax = fig.add_subplot(122)
	ax.set_title('Depth at deeper, constant')
	ax.imshow(vel3d[:,:,10], cmap='jet')
	plt.savefig('velocity.png', dpi=500)
	plt.close()

# set up basic parameters

nz = 61
nx = 201
ny = 201
dx = 0.5
dz = 0.5
dy = 0.5
print(f'Range: in x direction {(nx-1)*dx} in y direction {(ny-1)*dy} in z direction {(nz-1)*dz}')

# set up velocity structure
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
vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
s_vel_structure = vxyz.flatten(order='F')

# set up stations

stations = [[100,100], [50,100], [150,100], [100,50], [100, 150], [50,50], [150,150], [150,50], [30,130], [60,60]]

# set up sources
# fit a line which goes from [100,50,12] to [120,80,14]
np.random.seed(0)
a = np.random.rand(50,1)
x = 100 + 20*a
y = 50 + 30*a
z = 12 + 2*a
sources = np.hstack([x,y,z])


# change the sources to earth coordinates
o_lat = 30
o_lon = 10
o_sources = []
for source in sources:
	lat,lon = get_point_at_distance(o_lat, o_lon, np.sqrt((source[0]*dx)**2+(source[1]*dy)**2), np.arctan(source[0]*dx/(source[1]*dy)))
	o_sources.append([lat,lon, source[2]])

# change the stations to earth coordinates
o_stations = []
for station in stations:
	lat, lon = get_point_at_distance(o_lat, o_lon, np.sqrt((station[0]*dx)**2+(station[1]*dy)**2), np.arctan(station[0]*dx/(station[1]*dy)))
	o_stations.append([lat,lon])
	
# write hypoDD file
# write station.dat
f = open('station.dat', 'w')
for i in range(0,len(o_stations)):
    f.write(f'ST{i} {o_stations[i][0]:5.3f} {o_stations[i][1]:6.3f}\n')
f.close()

np.save('sta', np.array(o_stations))
np.save('source', np.array(o_sources))

plot_source_station(np.array(o_stations), np.array(o_sources))

# write pha file
# save the travel time at the same time for the future reference for dt.cc

p_time_table = np.zeros([len(o_sources), len(o_stations)])
s_time_table = np.zeros([len(o_sources), len(o_stations)])
f = open('test.pha', 'w+')
f2 = open('benchmark_station.txt', 'w')

for i in range(0, len(o_sources)):
	print(i)
	random_lat = o_sources[i][0]+np.random.rand(1)[0]/10.
	random_lon = o_sources[i][1]+np.random.rand(1)[0]/10.
	f.write(f"# 2000 12 13 15 00 23.48 {random_lat:6.3f} {random_lon:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	f2.write(f"# 2000 12 13 15 00 23.48 {o_sources[i][0]:5.3f} {o_sources[i][1]:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	for j in range(0, len(stations)):
		t = fmm.eikonal(p_vel_structure,xyz=sources[i],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')[:,:,0]
		travel_time = t[stations[j][0]][stations[j][1]]
		p_time_table[i][j] = travel_time
		f.write(f"ST{j}    {travel_time:4.2f}0  1.000    P \n")

		t = fmm.eikonal(s_vel_structure,xyz=sources[i],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')[:,:,0]
		travel_time = t[stations[j][0]][stations[j][1]]
		s_time_table[i][j] = travel_time
		f.write(f"ST{j}    {travel_time:4.2f}0  1.000    S \n")
f.close()
f2.close()
np.save('tt_P',p_time_table)
np.save('tt_S',s_time_table)


# 
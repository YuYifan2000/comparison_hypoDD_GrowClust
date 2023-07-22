import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt

from obspy.geodetics.base import locations2degrees
from scipy.signal import detrend
from scipy.fft import fftfreq, fftn, ifftn, fftshift
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
	ax.scatter(sources[:,0], sources[:,1], sources[:,2], zdir='z', label='sources', s=1)
	ax.legend()
	ax.set_xlabel('Latitude')
	#ax.set_xlim([30, 31.5])
	ax.set_ylabel('Longitude')
	#ax.set_ylim([120, 121.5])
	ax.set_zlabel('Z')
	ax.set_zlim([0, 30])
	ax.invert_zaxis()
	ax.view_init(elev=30., azim=-45)
	plt.savefig('source_station.png', dpi=500)
	#plt.show()
	plt.close()

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

def plot_velocity(vel3d):
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[12,6])
	axes[0].set_title('Depth at shallow, heterogeneity')
	im = axes[0].imshow(vel3d[:,:,6], cmap='seismic')
	axes[0].set_xlabel('dx')
	axes[0].set_ylabel('dy')
	cbar = fig.colorbar(im, ax=axes[0], orientation="horizontal")
	cbar.set_label('Vp (m/s)')
	axes[1].set_title('Depth at deeper, constant')
	im = axes[1].imshow(vel3d[:,:,300], cmap='seismic')
	axes[1].set_xlabel('dx')
	axes[1].set_ylabel('dy')
	cbar = fig.colorbar(im, ax=axes[1], orientation="horizontal")
	cbar.set_label('Vp (m/s)')
	plt.savefig('velocity.png', dpi=1000)
	plt.close()

def genearte_velocity(nx,ny,nz,dx,dy,dz):
	depth = 10.
	dV = von_Karman_3d_velo(nx,ny,int(depth/dz),dx,dy,dz,0.5,0.1,0.04,0.107)
	# set up velocity structure
	# for P velocity
	f = open('./vjma2001', 'r')
	tmp = f.readlines()
	f.close()
	v = []
	vs = []
	for i in tmp[:nz]:
		v.append(float(i.split()[0]))
		vs.append(float(i.split()[1]))
	v = np.array(v)
	vs = np.array(vs)
	v = np.expand_dims(v,1)
	vs = np.expand_dims(vs, 1)
	h = np.ones([1,nx])
	vel = np.multiply(v,h,dtype='float32') #z,x
	vels = np.multiply(vs, h ,dtype='float32')
	vel3d=np.zeros([nz,nx,ny],dtype='float32')
	vels3d = np.zeros([nz,nx,ny], dtype='float32')
	for ii in range(ny):
		vel3d[:,:,ii]=vel
		vels3d[:,:,ii] = vels
	vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
	vsxyz = np.swapaxes(np.swapaxes(vels3d,0,1),1,2)
	vxyz[:,:,:int(depth/dz)] *= (1+dV)
	vsxyz[:,:,:int(depth/dz)] *= (1+dV)
	np.save('p_vel_array', vxyz)
	np.save('s_vel_array', vsxyz)
	p_vel_structure = vxyz.flatten(order='F')
	s_vel_structure = vsxyz.flatten(order='F')
	plot_velocity(vxyz)

	np.save('p_vel', p_vel_structure)
	np.save('s_vel', s_vel_structure)
	return p_vel_structure, s_vel_structure

# set up basic parameters

nz = 401
nx = 601
ny = 601
dx = 0.1
dz = 0.05
dy = 0.1
print(f'Range: in x direction {(nx-1)*dx} in y direction {(ny-1)*dy} in z direction {(nz-1)*dz}')

# load velocity
p_vel_structure, s_vel_structure = genearte_velocity(nx,ny,nz,dx,dy,dz)
#p_vel_structure = np.load('p_vel.npy')
#s_vel_structure = np.load('s_vel.npy')

# set up stations

stations = [[1,1], [600,1], [1,600], [600,600], [300,300], [150,300], [450, 300], [300, 150], [300,450], [100, 400], [400,400], [100,100], [400, 100]]

# set up sources
# fit a line which goes from [200,200,12] to [200,190,14]

np.random.seed(0)
x = 300 + (np.random.rand(50,1) - 0.5) * 30
y = 300 - (np.random.rand(50,1) - 0.5) * 40
z = 12 + 0.1 * (x-110) + 0.2 * (y-100)
sources = np.hstack([x*dx,y*dy,z*dz])

# change the sources to earth coordinates
o_lat = 30
o_lon = 120
o_sources = []
for source in sources:
	lat,lon = get_point_at_distance(o_lat, o_lon, np.sqrt((source[0])**2+(source[1])**2), np.arctan(source[0]/(source[1]))/np.pi*180.)
	o_sources.append([lat,lon, source[2]])

# change the stations to earth coordinates
o_stations = []
for station in stations:
	lat, lon = get_point_at_distance(o_lat, o_lon, np.sqrt((station[0]*dx)**2+(station[1]*dy)**2), np.arctan(station[0]*dx/(station[1]*dy))/np.pi*180.)
	o_stations.append([lat,lon])
	
# write hypoDD file
# write station.dat
f = open('./hypoDD/station.dat', 'w')
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
f = open('./hypoDD/test.pha', 'w+')
f2 = open('benchmark_station.txt', 'w')

for i in range(0, len(o_sources)):
	print(i)
	#random_lat = o_sources[i][0]+(np.random.rand(1)[0]-0.5) / 5.
	#random_lon = o_sources[i][1]+(np.random.rand(1)[0]-0.5) / 5.
	#random_dep = sources[i][2]+(np.random.rand(1)[0]-0.5) * 1.2
	random_lat = o_sources[i][0]
	random_lon = o_sources[i][1]
	random_dep = sources[i][2]
	f.write(f"# 2000 12 13 15 00 1.00 {random_lat:6.3f} {random_lon:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	f2.write(f"# 2000 12 13 15 00 1.00 {o_sources[i][0]:5.3f} {o_sources[i][1]:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	tp = fmm.eikonal(p_vel_structure,xyz=sources[i],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
	tp = tp[:,:,0]
	ts = fmm.eikonal(s_vel_structure,xyz=sources[i],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
	ts = ts[:,:,0]
	for j in range(0, len(stations)):
		travel_time = tp[stations[j][0], stations[j][1]]
		p_time_table[i][j] = travel_time
		f.write(f"ST{j}    {travel_time:4.2f}0  1.000    P \n")
	
		travel_time = ts[stations[j][0]][stations[j][1]]
		s_time_table[i][j] = travel_time
		f.write(f"ST{j}    {travel_time:4.2f}0  1.000    S \n")
f.close()
f2.close()
np.save('./hypoDD/tt_P',p_time_table)
np.save('./hypoDD/tt_S',s_time_table)

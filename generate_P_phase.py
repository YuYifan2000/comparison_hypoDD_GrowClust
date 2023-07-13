import pyekfmm as fmm
import numpy as np
import matplotlib.pyplot as plt

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

# plt.figure()
# plt.imshow(vel3d[:,:,0])
# plt.jet();plt.show()
vxyz=np.swapaxes(np.swapaxes(vel3d,0,1),1,2)
vel_structure = vxyz.flatten(order='F')

# set up stations

stations = [[100,100], [90,100], [110,100], [100,90], [100, 110], [80,100], [120,100], [100,120], [100,80], [60,60]]

# set up sources
# fit a line which goes from [20,10,12] to [40,10,14]
np.random.seed(0)
x = 20 + 20*np.random.rand(50,1)
y = np.ones([50,1]) * 10.
z = 12 + 2*np.random.rand(50,1) + np.random.rand(50,1)/5
sources = np.hstack([x,y,z])


# change the sources to earth coordinates
o_lat = 30
o_lon = 120
o_sources = []
for source in sources:
	lat,lon = get_point_at_distance(o_lat, o_lon, np.sqrt((source[0]*dx)**2+(source[1]*dy)**2), np.arctan(source[0]*dx/(source[1]*dy)))
	o_sources.append([lat,lon])

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

# write pha file
# save the travel time at the same time for the future reference for dt.cc

time_table = np.zeros([len(o_sources), len(o_stations)])
f = open('test.pha', 'w+')
f2 = open('benchmark_station.txt', 'w')

for i in range(0, len(o_sources)):
	random_lat = o_sources[i][0]+np.random.rand(1)[0]/10.
	random_lon = o_sources[i][1]+np.random.rand(1)[0]/10.
	f.write(f"# 2000 12 13 15 00 23.48 {random_lat:6.3f} {random_lon:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	f2.write(f"# 2000 12 13 15 00 23.48 {o_sources[i][0]:5.3f} {o_sources[i][1]:6.3f} {sources[i][2]:4.2f} 1 0 0 0 {i} \n")
	for j in range(0, len(stations)):
		t = fmm.eikonal(vel_structure,xyz=sources[i],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')[:,:,0]
		travel_time = t[stations[j][0]][stations[j][1]]
		time_table[i][j] = travel_time
		print(j)
		f.write(f"ST{j}    {travel_time:4.2f}0  1.000    P \n")
f.close()
f2.close()
np.save('tt_P',time_table)
# fast marching for travel time
#t = fmm.eikonal(vel_structure,xyz=sources[0],ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2)
#time = t.reshape(nx,ny,nz,order='F')[:,:,0]
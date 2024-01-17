from math import asin, atan2, cos, degrees, radians, sin
import geopy
from geopy.distance import distance
import numpy as np
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

nz = 401
nx = 601
ny = 601
dx = 0.1
dz = 0.05
dy = 0.1
o_lat = 35.5
o_lon = -117.9
origin = geopy.Point(o_lat, o_lon)
f = open('./test', 'w')
for i in range(0, nx):
    print(i)
    for j in range(0,ny):
        for k in range(0,nz):
            x = dx * i
            y = dy * j
            z = dz * k
            if y ==0 :
                latitude, longitude = get_point_at_distance(o_lat, o_lon,np.sqrt(x**2+y**2),90)
                #destination = distance(kilometers=np.sqrt(x**2+y**2)).destination(origin, 90)
            else:
                latitude, longitude = get_point_at_distance(o_lat, o_lon,np.sqrt(x**2+y**2),np.arctan(x/y)/np.pi*180.)
                #destination = distance(kilometers=np.sqrt(x**2+y**2)).destination(origin, np.arctan(x/y)/np.pi*180.)
            f.write(f"{longitude:.4f} {latitude:.4f} {int(z*1000.)}\n")
f.close()

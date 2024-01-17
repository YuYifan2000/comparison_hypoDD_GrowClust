import numpy as np
from shapely.geometry import Point,Polygon
import matplotlib.pyplot as plt
from obspy.geodetics import gps2dist_azimuth
def Random_Points_in_Polygon(polygon, number):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points

# northeast fault
x1 = -117.6
y1 = 35.6
x2 = -117.5
y2 = 35.67
x3 = -117.62
y3 = 35.64
x4 = -117.52
y4 = 35.7
polygon = Polygon([[x1,y1],[x3,y3],[x4,y4],[x2,y2]])
points = Random_Points_in_Polygon(polygon, 20)
sourc1 = np.zeros([20,4])

# Plot the list of points
xs = [point.x for point in points]
ys = [point.y for point in points]
#print(polygon.exterior.distance(points[1]))
#print(polygon.exterior.distance(points[2]))


# Plot the polygon
xp,yp = polygon.exterior.xy


# Plot the list of points
zmin = 3
zmax = 12
p1 = np.array([x1,y1])
p2 = np.array([x2,y2])
dmax = np.cross(p2-p1,np.array([x3,y3])-p1)/np.linalg.norm(p2-p1)
for i in range(0,len(points)):
    p3 = np.array([points[i].x, points[i].y])
    d=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    z = d/dmax * (zmax-zmin) + zmin
    print(z)
    sourc1[i, 0] = points[i].x
    sourc1[i, 1] = points[i].y
    sourc1[i, 2] = z
    sourc1[i, 3] = 1

# main fault
np.random.seed(0)
start = [-117.5, 35.7]
end = [-117.7, 35.9]
num = 20
r = np.random.rand(num,1)
sourc2_x = r * (start[0]-end[0]) + start[0]
sourc2_y = r * (start[1]-end[1]) + start[1]
sourc2_z = np.random.rand(num,1) * 10+1
sourc2 = np.hstack([sourc2_x, sourc2_y, sourc2_z, np.ones_like(sourc2_x)*2])
branch1_e = [-117.46, 35.55]
num = 20
r = np.random.rand(num,1)
sourc3_x = r * (start[0]-branch1_e[0]) + start[0]
sourc3_y = r * (start[1]-branch1_e[1]) + start[1]
sourc3_z = np.random.rand(num,1) * 10
sourc3 = np.hstack([sourc3_x, sourc3_y, sourc3_z, np.ones_like(sourc3_x)*3])

branch2_e = [-117.42, 35.54]

sources= np.vstack([sourc1,sourc2,sourc3])
o_lat = 35.5
o_lon = -117.9
for source in sources:
    print(source[0], source[1])
    dist,az,baz = gps2dist_azimuth(o_lat, o_lon, source[1], source[0])
    source[0] = dist * np.sin(az/180*np.pi) / 1000.
    source[1] = dist * np.cos(az/180*np.pi) / 1000.
    print(source[0], source[1])
np.save('source', sources)
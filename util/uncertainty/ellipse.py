import numpy as np
import pandas as pd
import pymap3d as pm

def point_coor(length, az, dip):
    alpha = np.deg2rad(az)
    theta = np.deg2rad(dip)
    return np.array([length*np.cos(theta)*np.sin(alpha), length*np.cos(theta)*np.cos(alpha),length*np.sin(theta)])
def rotate_points(az, dip, points, lengths):
    R_a = np.eye(3)
    R_a[0,0] = np.cos(np.deg2rad(az-90))
    R_a[0,1] = -np.sin(np.deg2rad(az-90))
    R_a[1,0] = np.sin(np.deg2rad(az-90))
    R_a[1,1] = np.cos(np.deg2rad(az-90))
    R_b = np.eye(3)
    R_b[0,0] = np.cos(np.deg2rad(dip))
    R_b[0,2] = np.sin(np.deg2rad(dip))
    R_b[2,0] = -np.sin(np.deg2rad(dip))
    R_b[2,2] = np.cos(np.deg2rad(dip))
    R_c = np.eye(3)
    R = R_a@R_b@R_c
    rotated = np.dot(R, points.T).T
    if (np.dot(rotated.T**2,1./(lengths**2)) > 1.):
        return 0
    else:
        return 1
def rotate_points_nll(az, dip, points, lengths):
    R_a = np.eye(3)
    R_a[0,0] = np.cos(np.deg2rad(az))
    R_a[0,1] = -np.sin(np.deg2rad(az))
    R_a[1,0] = np.sin(np.deg2rad(az))
    R_a[1,1] = np.cos(np.deg2rad(az))
    R_b = np.eye(3)
    R_b[0,0] = np.cos(np.deg2rad(dip))
    R_b[0,2] = np.sin(np.deg2rad(dip))
    R_b[2,0] = -np.sin(np.deg2rad(dip))
    R_b[2,2] = np.cos(np.deg2rad(dip))
    R_c = np.eye(3)
    R = R_a@R_b@R_c
    rotated = np.dot(R, points.T).T
    if (np.dot(rotated.T**2,1./(lengths**2)) > 1.):
        return 0
    else:
        return 1
# length, azimuth and dip
# length = np.array([0.27,0.24,0.16])
# length = length * 2.8
# az = np.array([62, 297, 154])
# dip = np.array([4, 82, 6])
# x1 = point_coor(length[0], az[0],dip[0])
# x2 = point_coor(length[1], az[1], dip[1])
# x3 = point_coor(length[2], az[2], dip[2])

# A = np.stack((x1**2,x2**2,x3**2))
# b = np.ones(3)

# abc = np.linalg.solve(A, b)


# rotated_point = rotate_points(az[0], dip[0], x2, length)
# print(rotated_point)

# load ground truth data
sources = np.load('./o_source.npy')
# load hypoinverse data
hypoinverse_df = pd.read_csv('./hypoinverse.csv')
sum = 0
for i in range(0,len(hypoinverse_df)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], hypoinverse_df.iloc[i]['LAT'], hypoinverse_df.iloc[i]['LON'], hypoinverse_df.iloc[i]['DEPTH'])
    lengths = np.array([hypoinverse_df.iloc[i]['l1'],hypoinverse_df.iloc[i]['l2'],hypoinverse_df.iloc[i]['l3'] ])
    a = rotate_points(hypoinverse_df.iloc[i]['az'], hypoinverse_df.iloc[i]['dip'], np.array([e,n,u])/1000.,lengths*np.sqrt(2.80))
    sum += a
print('Hypoinverse')
print(sum)

# load NonLinLoc
nll = pd.read_csv('./nll.csv')
sum = 0
for i in range(0, len(nll)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], nll.iloc[i]['LAT'], nll.iloc[i]['LON'], nll.iloc[i]['DEPTH'])
    lengths = np.array([nll.iloc[i]['l1'],nll.iloc[i]['l2'],nll.iloc[i]['l3'] ])
    a = rotate_points_nll(nll.iloc[i]['az'], nll.iloc[i]['dip'], np.array([e,n,u])/1000.,lengths*np.sqrt(2.80))
    sum += a

print('NonLinLoc')
print(sum)

# load velest
velest = pd.read_csv('./velest.csv')
sum = 0
for i in range(0, len(velest)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], velest.iloc[i]['LAT'], velest.iloc[i]['LON'], velest.iloc[i]['DEPTH'])
    lengths = np.array([velest.iloc[i]['ERX'],velest.iloc[i]['ERY'],velest.iloc[i]['ERZ'] ])
    if np.dot((np.array([e,n,u])/1000.)**2, (1./lengths)**2) > 1:
        a = 0
    else:
        a = 1
    sum += a

print("VELEST")
print(sum)

# load hyposvi
hyposvi = pd.read_csv('./hyposvi.csv')
sum = 0
for i in range(0, len(hyposvi)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], hyposvi.iloc[i]['latitude'], hyposvi.iloc[i]['longitude'], hyposvi.iloc[i]['depth'])
    lengths1 = np.array([hyposvi.iloc[i]['unc_h_max'],hyposvi.iloc[i]['unc_h_min'],hyposvi.iloc[i]['unc_z'] ])*np.sqrt(2.8)
    lengths2 = np.array([hyposvi.iloc[i]['unc_h_min'],hyposvi.iloc[i]['unc_h_max'],hyposvi.iloc[i]['unc_z'] ])*np.sqrt(2.8)
    if np.dot((np.array([e,n,u]) /1000.)**2, (1./lengths1)**2) <= 1:
        a = 1
    elif np.dot((np.array([e,n,u]) /1000.)**2, (1./lengths2)**2) <= 1:
        a=1
    else:
        a=0
    sum += a

print("HYPOSVI")
print(sum)

# load growclust
gc = pd.read_csv('./growclust.csv')
sum = 0
for i in range(0, len(gc)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], gc.iloc[i]['latR'],gc.iloc[i]['lonR'], gc.iloc[i]['depR'])
    lengths = np.array([gc.iloc[i]['eh'], gc.iloc[i]['eh'], gc.iloc[i]['ez']])/0.7*np.sqrt(3.08)
    if np.dot((np.array([e,n,u])/1000.)**2, (1./lengths)**2) > 1:
        a = 0
    else:
        a = 1
    sum += a
print('GROWCLUST')
print(sum)
# xcorloc
xc = pd.read_csv('./xcorloc.csv')
sum = 0
for i in range(0, len(gc)):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], xc.iloc[i]['lat'],xc.iloc[i]['lon'], xc.iloc[i]['dep'])
    lengths = np.array([xc.iloc[i]['erx'], xc.iloc[i]['ery'], xc.iloc[i]['erz']])/1000./0.7*np.sqrt(3.08)
    if np.dot((np.array([e,n,u])/1000.)**2, (1./lengths)**2) > 1:
        a = 0
    else:
        a = 1
    sum += a
print('XCORLOC')
print(sum)

# hypodd
dd = pd.read_csv('./hypodd.csv')
sum = 0
for i in range(0, 100):
    [e,n,u] = pm.geodetic2enu(sources[i,0], sources[i,1], sources[i,2], dd.iloc[i]['LAT'],dd.iloc[i]['LON'], dd.iloc[i]['DEPTH'])
    lengths = np.array([dd.iloc[i]['EX'], dd.iloc[i]['EY'], dd.iloc[i]['EZ']])/1000
    if np.dot((np.array([e,n,u])/1000.)**2, (1./lengths)**2) > 1:
        a = 0
    else:
        a = 1
    sum += a
print('dd')
print(sum)

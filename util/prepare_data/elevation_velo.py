import numpy as np

def sediment(elevation, height, vp_0):
    vp = vp_0 - 0.6 * height / 1000.
    vs = 0.7858 -1.2344*vp + 0.7949*vp**2 - 0.1238 * vp**3 + 0.0064*vp**4
    return vp, vs
def granite(elevation, height, vp_0):
    if elevation >= 1700:
        elevation = 1700
    vp = vp_0 - (2.9299 - 1.648 * elevation/1000.) * height/1000.
    vs = 0.7858 -1.2344*vp + 0.7949*vp**2 - 0.1238 * vp**3 + 0.0064*vp**4
    return vp, vs

def velocity_ele(elevation, height, vp_0):
    if vp_0 < 3.8:
        vp,vs = sediment(elevation, height, vp_0)
    elif vp_0 > 4.4:
        vp,vs = granite(elevation, height, vp_0)
    else:
        vp_s, vs_s = sediment(elevation, height, vp_0)
        vp_g, vs_g = granite(elevation, height, vp_0)
        vp = (abs(vp_0-3.8)*vp_g + abs(vp_0-4.4)*vp_s)/0.6
        vs = (abs(vp_0-3.8)*vs_g + abs(vp_0-4.4)*vs_s)/0.6
    return vp, vs

#nz = 401
nz = 441
dz = 50.
nx = 701
ny = 1001
vel_p = np.zeros([nx,ny,nz])
vel_s = np.zeros([nx,ny,nz])
idx_set = []
f = open('test_results.log', 'r')
for i in range(0, nx):
    print(i)
    for j in range(0,ny):
        for k in range(40,nz):
            line = f.readline()
            vp_0 = float(line.split()[6])/1000.
            elevation = float(line.split()[3])
            if k == 40:
                for kk in range(1, 41):
                    height = kk*dz
                    if height > elevation:
                        vp,vs = 0.001, 0.001
                        idx = [i,j, 40-kk, height, elevation]
                        idx_set.append(idx)
                    else:
                        vp, vs = velocity_ele(elevation, height, vp_0)
                    vel_p[i,j,40-kk] = vp * 1000.
                    vel_s[i,j,40-kk] = vs * 1000.
            vel_p[i,j,k] = float(line.split()[6])
            vel_s[i,j,k] = float(line.split()[7])
f.close()
np.save('air', np.array(idx_set))

np.save('ele_vel_p',vel_p)
np.save('ele_vel_s', vel_s)

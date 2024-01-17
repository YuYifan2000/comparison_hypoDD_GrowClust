import numpy as np
from scipy.io import FortranFile

#f = FortranFile('test.3d', 'w', header_dtype=np.dtype("f4"))

#f.write_record(np.array([1.,2.,3.], dtype=np.dtype("f4")))
#f.close()

vel = np.load('p_vel_array.npy')
print(vel.shape)
print(vel[:,0,0])
nx = vel.shape[0]
ny = vel.shape[1]
nz = vel.shape[2]
with open('test.3d', 'wb') as fout:
    for i in range(0,nz):
        for j in range(0, ny):
            fout.write(vel[:,j,i].astype('f4'))
a = np.fromfile('test.3d', dtype=np.dtype("f4"), count=-1)
print(a.shape)
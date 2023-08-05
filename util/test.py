import pykonal
import numpy as np

nz = 40
nx = 60
ny = 60
dx = 1
dz = 0.5
dy = 1


v1 = np.ones([nx,ny,int(nz/2)])*3
v2 = np.ones([nx,ny,int(nz/2)])*6
print(v1.shape)
v = np.concatenate((v1,v2), axis=2)
print(v.shape)
print(v[:,:,0])
source = [10,10,19]
solver = pykonal.EikonalSolver(coord_sys="cartesian")
solver.velocity.min_coords = 0, 0, 0
solver.velocity.node_intervals = dx, dy, dz
solver.velocity.npts = nx, ny, nz
solver.velocity.values = v
src_idx = int(source[0]/dx), int(source[1]/dy), 39
solver.traveltime.values[src_idx] = 0
solver.unknown[src_idx] = False
solver.trial.push(*src_idx)

# Solve the system.

solver.solve()
print(solver.traveltime.values[10, 10, 29])
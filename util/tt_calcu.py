import numpy as np
import pykonal
import pyekfmm as fmm
import matplotlib.pyplot as plt
import time
'''
nz = 401
nx = 601
ny = 601
dx = 0.1
dz = 0.05
dy = 0.1

p_vel_structure = np.load('p_vel.npy') / 1000.
source = np.array([30,30,16])

# pykonal
# initialize the solver

solver = pykonal.EikonalSolver(coord_sys="cartesian")
solver.velocity.min_coords = 0, 0, 0
solver.velocity.node_intervals = dx, dy, dz
solver.velocity.npts = nx, ny, nz
solver.velocity.values = p_vel_structure
src_idx = int(source[0]/dx), int(source[1]/dy), int(source[2]/dz)
solver.traveltime.values[src_idx] = 0
solver.unknown[src_idx] = False
solver.trial.push(*src_idx)

# Solve the system.
start = time.time()
solver.solve()
print(solver.traveltime.values[100, 100, 0])
print(time.time()-start)
np.save('fmmtime2', solver.traveltime.values[:,:,0])

t1 = solver.traveltime.values[:,:,0]

p_vel_structure = np.load('vel_p.npy') / 1000.
source = np.array([30,30,16])

# pykonal
# initialize the solver

solver = pykonal.EikonalSolver(coord_sys="cartesian")
solver.velocity.min_coords = 0, 0, 0
solver.velocity.node_intervals = dx, dy, dz
solver.velocity.npts = nx, ny, nz
solver.velocity.values = p_vel_structure
src_idx = int(source[0]/dx), int(source[1]/dy), int(source[2]/dz)
solver.traveltime.values[src_idx] = 0
solver.unknown[src_idx] = False
solver.trial.push(*src_idx)

# Solve the system.
start = time.time()
solver.solve()
print(solver.traveltime.values[100, 100, 0])
print(time.time()-start)
np.save('fmmtime3', solver.traveltime.values[:,:,0])
t2 = solver.traveltime.values[:,:,0]
'''
t1 = np.load('fmmtime2.npy')
t2 = np.load('fmmtime3.npy')

fig = plt.figure()
ax = plt.subplot(111)
im = ax.imshow((t2-t1).T * 1000, extent=[0,60,0,60], cmap='viridis', vmin=-100, vmax=500)
ax.set_xlabel('km')
ax.set_ylabel('km')
fig.colorbar(im, location='bottom', orientation='horizontal', label='ms', shrink=0.7)
fig.tight_layout()
plt.savefig('before_after_vonKarman.png', dpi=400,bbox_inches='tight')

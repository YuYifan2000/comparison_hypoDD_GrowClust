import gc
import pykonal
import numpy as np
from mpi4py import MPI
import time
import pymap3d as pm

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# set up basic parameters
nz = 401
nx = 701
ny = 1001
dx = 100
dz = 50
dy = 100

print(f'Grid Range: in x direction {(nx-1)*dx} km, in y direction {(ny-1)*dy} km, in z direction {(nz-1)*dz} km')

# load or build up velocity
p_vel_structure = np.load('p_vel.npy')
s_vel_structure = np.load('s_vel.npy')

# set up stations
stations = np.load('station.npy')
# set up sources
shared_sources = np.load('source.npy')
source_num = int(len(shared_sources) / size)
sources = shared_sources[rank*source_num:(rank+1)*source_num]
# change the sources to earth coordinates
o_lat = 35.4
o_lon = -117.956

if rank == 0:
    o_stations = []
    for station in stations:
        lat, lon, _ = pm.enu2geodetic(station[0], station[1], 0, o_lat, o_lon,0)
        o_stations.append([lat,lon])
    np.save('o_station', np.array(o_stations))


# write travel time file
p_time_table = np.zeros([len(sources), len(stations)])
s_time_table = np.zeros([len(sources), len(stations)])
for i in range(0, len(sources)):
    st = time.time()
    solver = pykonal.EikonalSolver(coord_sys="cartesian")
    solver.velocity.min_coords = 0, 0, 0
    solver.velocity.node_intervals = dx, dy, dz
    solver.velocity.npts = nx, ny, nz
    solver.velocity.values = p_vel_structure
    src_idx = int(sources[i,0]/dx), int(sources[i,1]/dy), int(sources[i,2]/dz)
    solver.traveltime.values[src_idx] = 0
    solver.unknown[src_idx] = False
    solver.trial.push(*src_idx)
    solver.solve()
    tp = solver.traveltime.values[:,:, 0].copy()
    del solver
    gc.collect()
    solver = pykonal.EikonalSolver(coord_sys="cartesian")
    solver.velocity.min_coords = 0, 0, 0
    solver.velocity.node_intervals = dx, dy, dz
    solver.velocity.npts = nx, ny, nz
    solver.velocity.values = s_vel_structure
    src_idx = int(sources[i,0]/dx), int(sources[i,1]/dy), int(sources[i,2]/dz)
    solver.traveltime.values[src_idx] = 0
    solver.unknown[src_idx] = False
    solver.trial.push(*src_idx)
    solver.solve()
    ts = solver.traveltime.values[:,:, 0].copy()
    print(rank,'consumes',time.time()-st)
    for j in range(0, len(stations)):
        p_time_table[i][j] = tp[int(stations[j][0]/dx), int(stations[j][1]/dy)]
        s_time_table[i][j] = ts[int(stations[j][0]/dx), int(stations[j][1]/dy)]

comm.barrier()
#mpi gather time table
recv_p = None
recv_s = None
if rank == 0:
    recv_p = np.empty([size, len(sources), len(o_stations)])
    recv_s = np.empty([size, len(sources), len(o_stations)])
comm.Gather(p_time_table, recv_p, root=0)
comm.Gather(s_time_table, recv_s, root=0)
if rank == 0:
    np.save('./tt_P',np.vstack(recv_p))
    np.save('./tt_S',np.vstack(recv_s))

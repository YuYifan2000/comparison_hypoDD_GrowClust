import pyekfmm as fmm
import numpy as np


nz = 200
nx = 300
ny = 200
dx = 0.1
dz = 0.05
dy = 0.1

p_vel_structure = np.load('')
source = np.array([1,1,1])
tp = fmm.eikonal(p_vel_structure,xyz=source,ax=[0,dx,nx],ay=[0,dy,ny],az=[0,dz,nz],order=2).reshape(nx,ny,nz,order='F')
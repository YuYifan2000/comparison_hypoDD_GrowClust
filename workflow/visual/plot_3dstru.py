from tvtk.api import tvtk
import numpy as np
from mayavi import mlab
  
  
nz = 401
nx = 701
ny = 1001
dx = 0.1
dz = 0.05
dy = 0.1

x1 = np.linspace(0, dx*(nx-1),nx)
y1 = np.linspace(0, dy*(ny-1),ny)
z1 = np.linspace(0, dz*(nz-1),nz)

  
data = np.load('../p_vel.npy')[:,:,::-1]/1000.
print(data.shape)
i = tvtk.RectilinearGrid()
i.point_data.scalars = data.ravel(order='F')
i.point_data.scalars.name = 'scalars'
i.dimensions = data.shape
i.x_coordinates = x1
i.y_coordinates = y1
i.z_coordinates = z1

mlab.pipeline.surface(i, colormap='seismic', vmin = 3, vmax=7.5)
mlab.colorbar(orientation='vertical')
ax1   = mlab.axes( color=(1,1,1), nb_labels=4 )
mlab.show()
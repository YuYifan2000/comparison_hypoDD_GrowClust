import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('agg')

dep = np.array([0., 1., 2. ,3., 4., 5., 6., 7., 8., 30.])
# 3d velocity
v_p = np.load('p_vel.npy')[::2,::2,:]
v_s = np.load('s_vel.npy')[::2, ::2, :]
idx = dep/0.05
# average
mean_p = np.mean(np.mean(v_p, axis=0),axis=0)
mean_s = np.mean(np.mean(v_s, axis=0),axis=0)

# shelly
shelly_p = np.array([4.74, 5.01, 5.35, 5.71, 6.07, 6.17, 6.27, 6.34, 6.39, 7.80])
shelly_s = np.array([2.74, 2.90, 3.09, 3.30, 3.51, 3.57, 3.62, 3.66, 3.69, 4.50])

# velest_all events
velest_p = np.array([4.49, 4.585, 4.848, 5.291, 5.657, 5.658, 6.596, 6.911, 6.912, 7.8])
velest_s = np.array([2.707, 2.724, 2.900, 3.082, 3.350, 3.351, 3.867, 4.064, 4.068, 4.500])

fig = plt.figure()
ax = fig.add_subplot(121)
ax.set_title('P velocity')
ax.plot(mean_p[idx.astype('int')], dep, label='3D Model Average')
ax.plot(shelly_p, dep, label='Shelly 2020')
ax.plot(velest_p, dep, label = 'velest')

ax.set_xlabel('Velocity (km/s)')
ax.set_xlim([0, 10])
ax.set_ylabel('Depth (km)')


ax = fig.add_subplot(122)
ax.set_title('S velocity')
ax.plot(mean_s[idx.astype('int')], dep, label='3D Model Average')
ax.plot(shelly_s, dep, label='Shelly 2020')
ax.plot(velest_s, dep, label = 'velest')

ax.set_xlabel('Velocity (km/s)')
ax.set_xlim([0, 10])
ax.set_ylabel('Depth (km)')


plt.tight_layout()
plt.savefig('velocity.png', dpi=500)
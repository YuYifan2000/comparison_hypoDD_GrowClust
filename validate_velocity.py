import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

p_velo = np.load('p_vel_array.npy')
print(p_velo.shape)
a = p_velo[1,1,:]
fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(fftfreq(a.size,0.1)[:a.size//2], np.abs(fft(a))[:a.size//2])
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fft2

p_velo = np.load('p_vel_array.npy')
print(p_velo.shape)
a = p_velo[1,2,:]
fig = plt.figure()
ax = fig.add_subplot(111)
f2 = fft(a)

ax.set_yscale('log')
ax.set_xscale('log')
ax.scatter(fftfreq(a.size,0.01)[:a.size//2], np.abs(fft(a))[:a.size//2]**2)
plt.show()
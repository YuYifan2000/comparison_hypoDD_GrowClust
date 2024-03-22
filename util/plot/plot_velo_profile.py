import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
import pandas as pd

def get_cmp():
    f = open('./roma.cpt', 'r')
    Lines = f.readlines()
    vals = np.ones((len(Lines)-3, 4))
    for i in range(0, len(Lines)-3):
        line = Lines[i].split()
        vals[i,0] = float(line[1].split('/')[0]) / 256
        vals[i,1] = float(line[1].split('/')[1])/ 256
        vals[i,2] = float(line[1].split('/')[2])/256
    newcmp = mcolors.ListedColormap(vals)
    return newcmp
cmap = get_cmp()

y_i = 450
cat = pd.read_csv(f"ridgecrest_qtm.cat", sep="\s+", names=["yr","mon","day", "hr","min","sec","evid","latR","lonR","depR","mag","qID","cID","nbrach","qnpair","qndiffP","qndiffS","rmsP","rmsS","eh","ez","et","latC","lonC","depC"])
# filter cat
cat = cat[(cat['lonR'] > -117.956) & (cat['lonR'] < -117.4)]
cat = cat[(cat['latR'] > 35.4+y_i/1100-0.05) & (cat['latR'] < 35.4+y_i/1100+0.05)]
sources = cat[['depR', 'lonR']].to_numpy()
print(sources.shape)

vp = np.load('./vel_p.npy')/1000.
ele = np.load('./ele.npy')

fig = plt.figure(figsize=[6,4], constrained_layout=True)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

# imshow the velocity

y = np.linspace(-20,0,401)
x = np.linspace(0, 70, 701)
c = ax1.imshow(vp[:,y_i,:].T,cmap=cmap, vmin=2., vmax=7, extent=[0,70,20, 0], aspect='equal')
cbar = fig.colorbar(c, ax=ax1, location='bottom', shrink=0.6)
cbar.set_label('P Velocity (km/s)')
cbar.locator = plt.MaxNLocator(4)
cbar.update_ticks()

ax1.scatter((sources[:,1]+117.956)*111,sources[:,0],c='k',s=0.1,marker='o')

ax2.plot(x,ele[:,y_i],c='red')

ax1.set_xlabel('Distance (km)',fontsize=14)
ax1.set_ylabel('Depth (km)',fontsize=14)
ax2.set_ylabel('Elevation (m)', c='red',fontsize=14)
ax2.set_ylim([-2000,2000])
ax2.tick_params(axis='y', colors='red')
ax2.set_yticks([0,500,1000,1500,2000])
ax1.set_yticks([0,5,10,15])
ax1.set_ylim([20,-20])

#plt.savefig('./velo_ele.png', dpi=400)
plt.savefig('./velo_ele.png',transparent=True,dpi=500)
plt.close()
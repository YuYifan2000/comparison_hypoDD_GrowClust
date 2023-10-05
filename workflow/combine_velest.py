import numpy as np

f = open('hypocenter.CNV', 'w')
tmp = []
for i in range(0,5):
    input = open(f'{i}_.cnv', 'r')
    contents = input.read()
    input.close()
    a = contents.split('\n\n')[:-1]
    tmp = tmp + a
    print(len(tmp))
idx = np.load('vel_idx.npy')
for i in range(0, 1000):
    index = np.where(idx==i)[0][0]
    f.write(tmp[index])
    f.write('\n\n')
f.close()

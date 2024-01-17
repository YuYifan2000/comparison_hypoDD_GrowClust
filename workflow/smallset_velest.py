import numpy as np
import random
random.seed(0)
f = open('velest.cnv', 'r')
contents = f.read()
f.close()
a = contents.split('\n\n')
print(a[-1])
x = random.sample(range(0,1000), 1000)
np.save('vel_idx', np.array(x))
for i in range(0, 5):
    output = open(f'{i}.cnv', 'w')
    for j in x[i*200:(i+1)*200]:
        output.write(a[j])
        output.write('\n')
        output.write('\n')
    output.close()
    
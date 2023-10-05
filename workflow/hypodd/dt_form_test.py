import numpy as np
source = np.load('../o_source.npy')
tt_p = np.load('../tt_P.npy')
tt_s = np.load('../tt_S.npy')
f = open('dt.ct','r')
output = open('dt.cc', 'w')
Lines = f.readlines()
f.close()
for line in Lines:
    if line[0] == '#':
        flag = 0
        event1 = int(line.split()[1])
        event2 = int(line.split()[2])
        if source[event1-1, 3] == source[event2-1, 3]:
            flag = 1
        output.write(f'# {event1}  {event2}   0\n')
    else:
        if flag == 1:
            content = line.split()
            station = int(content[0].strip('ST'))
            phase_type = content[4]
            if phase_type == 'P':
                output.write(f'{content[0]} {(tt_p[event1-1][station]-tt_p[event2-1][station] + np.random.laplace(0, 0.011,)):4.3f} 1.00 {phase_type} \n')
            if phase_type == 'S':
                output.write(f'{content[0]} {(tt_s[event1-1][station]-tt_s[event2-1][station]+ np.random.laplace(0, 0.011,)):4.3f} 1.00 {phase_type} \n')
        else:
            content = line.split()
            station = int(content[0].strip('ST'))
            phase_type = content[4]
            if phase_type == 'P':
                output.write(f'{content[0]} {(tt_p[event1-1][station]-tt_p[event2-1][station]+ np.random.laplace(0, 0.011,)):4.3f} 0.30 {phase_type} \n')
            if phase_type == 'S':
                output.write(f'{content[0]} {(tt_s[event1-1][station]-tt_s[event2-1][station]+ np.random.laplace(0, 0.011,)):4.3f} 0.30 {phase_type} \n')
output.close()


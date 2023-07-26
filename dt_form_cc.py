import numpy as np

tt_p = np.load('tt_P.npy')
tt_s = np.load('tt_S.npy')
f = open('dt.ct','r')
output = open('dt.cc', 'w')
Lines = f.readlines()
f.close()
for line in Lines:
    if line[0] == '#':
        event1 = int(line.split()[1])
        event2 = int(line.split()[2])
        output.write(f'# {event1}  {event2}   0\n')
    else:
        content = line.split()
        station = int(content[0].strip('STA'))
        phase_type = content[4]
        if phase_type == 'P':
            output.write(f'{content[0]} {(tt_p[event1-1][station]-tt_p[event2-1][station]):4.3f} 1.00 {phase_type} \n')
        if phase_type == 'S':
            output.write(f'{content[0]} {(tt_s[event1-1][station]-tt_s[event2-1][station]):4.3f} 1.00 {phase_type} \n')
output.close()
print('done cc')
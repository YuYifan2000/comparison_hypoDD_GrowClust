import numpy as np
from datetime import datetime, timedelta

# stations
f = np.load('../o_station.npy')
output = open('./data/station.csv', 'w')
output.write('network,station,latitude,longitude,elevation\n')
for i in range(0, len(f)):
    network = 'X'
    station = 'ST'+str(i)
    latitude = f[i][0]
    longitude = f[i][1]
    elevation = f[i][2]
    output.write(f'{network},{station},{latitude:.4f},{longitude:.4f},{elevation/1000.:.2f}\n')
output.close()

# catalog and phase file

f = open('../hypocenter.CNV', 'r')
Lines = f.readlines()
f.close()
cat = open('./data/pre_cat.csv','w')
cat.write('evid,latitude,longitude,depth,time,mag\n')
pha = open('./data/phase.csv', 'w')
pha.write('time,evid,arid,phase,network,station\n')
idx = 0

for line in Lines:
    if line[0] == '\n':
        continue
    line = line.strip('\n')
    if line[0] == ' ':
        idx += 1
        year = 2000 + int(line[:2])
        mon = int(line[2:4])
        day = int(line[4:6])
        tmp = line[7:11]
        hour = int(tmp[:2])
#        min = int(tmp[2:4])
        min = 0
        sec = float(line[12:17])
        eventtime = datetime.strptime(f'{year},{mon},{day}T{hour}:{min}:{sec}', '%Y,%m,%dT%H:%M:%S.%f')
        eventtime = eventtime + timedelta(minutes=idx)
        phase_count = 0
        latitude = line.split()[3].strip('N')
        longitude = line.split()[4].strip('W')
        depth = line.split()[5]
        mag = 1.0
        cat.write(f'{idx},{latitude},-{longitude},{depth},{eventtime.strftime("%Y-%m-%dT%H:%M:%S.%f")},{mag}\n')
    else:
        length = len(line)
        for i in range(0, length//12):
            tmp = line[i*12:(i+1)*12]
            sta = tmp[:4]
            phase = tmp[4]
            travel_time = tmp.split()[-1]
            time = eventtime + timedelta(seconds=float(travel_time))
            phase_count += 1
            pha.write(f'{time.strftime("%Y-%m-%dT%H:%M:%S.%f")},{idx},{phase_count},{phase},X,{sta}\n')


import numpy as np
from datetime import datetime, timedelta
# form phase file
output = open('./obs/phase.obs', 'w+')
f = open('../hypocenter.CNV', 'r')
Lines = f.readlines()
f.close()
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
        min = 10
        sec = float(line[12:17])
        eventtime = datetime.strptime(f'{year},{mon},{day}T{hour}:{min}:{sec}', '%Y,%m,%dT%H:%M:%S.%f')
#        eventtime = eventtime + timedelta(minutes=idx)
        output.write('\n')
    else:
        length = len(line)
        for i in range(0, length//12):
            tmp = line[i*12:(i+1)*12]
            sta = tmp[:4]
            phase = tmp[4]
            travel_time = tmp.split()[-1]
            time = eventtime + timedelta(seconds=float(travel_time))
            output.write(f'{sta.ljust(6," ")} ?    ?    ? {phase}      ? {time.strftime("%Y%m%d")} {time.strftime("%H%M")}   {time.strftime("%S.%f")[:-2]} GAU  4.00e-02 -1.00e+00 -1.00e+00 -1.00e+00\n')

output.close()
# form station.dat

f = open('./obs/station_coordinates.txt', 'w+')

f.write('#GTSRCE  label  type  lat  lon  z_srce  elev\n')
stas = np.load('../o_station.npy')
num_sta = len(stas)
for i in range(0, num_sta):
    sta = 'ST' + str(i)
    lat = stas[i,0]
    lon = stas[i,1]
    ele = stas[i,2]
    line = f"GTSRCE  {sta}  LATLON  {lat:7.4f}  {lon:8.4f}  0  {ele/1000.:.2f}"
    f.write(line+'\n')
f.close()

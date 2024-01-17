import numpy as np
from datetime import datetime, timedelta
flag = 0
in_file = open("../hypocenter.CNV", "r")
Lines = in_file.readlines()
in_file.close()
out_file = open("./hypoInput.arc", "w")
for line in Lines:
    if line[0] == ' ':
        if flag != 0:
            out_file.write('\n')
        else:
            flag = 1
        south = ' '
        east = ' '
        hour = line.split()[1]
        sec = line.split()[2]
        event_time = datetime.strptime(f'2000-12-13-{hour}T{sec}', '%Y-%m-%d-%H%MT%S.%f')
        lat = float(line.split()[3][:-1])
        lat_degree = int(lat)
        lat_min = (lat-lat_degree)*60*100
        lon = float(line.split()[4][:-1])
        lon_degree = int(lon)
        lon_min = (lon-lon_degree)*60*100
        depth = float(line.split()[5]) * 100.
        event_line = f"{event_time.strftime('%Y%m%d%H%M%S%f')[:-4]}{abs(lat_degree):2d}{south}{lat_min:4.0f}{abs(lon_degree):3d}{east}{abs(lon_min):4.0f}{depth:5.0f}"
        out_file.write(event_line + "\n")
    else:
        picks = map(''.join, zip(*[iter(line)]*12))
        for pick in picks:
            network = 'N'
            comp = ''
            channel = ''
            phase_weight = 2
            sta = pick[:4]
            phase_type = pick[4]
            pick_time = event_time + timedelta(seconds = float(pick[6:]))
            phase_time_minute = pick_time.strftime("%Y%m%d%H%M")
            phase_time_second = pick_time.strftime("%S%f")[:-4]
            tmp_line = f"{sta:<5}{network:<2} {comp:<1}{channel:<3}"
            if phase_type.upper() == 'P':
                pick_line = f"{tmp_line:<13} P {phase_weight:<1d}{phase_time_minute} {phase_time_second}"
            elif phase_type.upper() == 'S':
                pick_line = f"{tmp_line:<13}   4{phase_time_minute} {'':<12}{phase_time_second} S {phase_weight:<1d}"
            out_file.write(pick_line + "\n")
out_file.write('\n')
out_file.close()

# hyp1.40 station
stas = np.load('../o_station.npy')
num_sta = len(stas)
f = open('hyp_station.dat', 'w')

def decdeg2dms(dd):
    deg, mnt = divmod(dd*60.0, 60)
    return int(deg), mnt

for i in range(0, num_sta):
    network_code = 'N'
    comp_code = ''
    channel_code = ''
    station_weight = ' '
    sta = "ST" + str(i)
    lat_degree, lat_minute = decdeg2dms(abs(stas[i,0]))
    lng_degree, lng_minute = decdeg2dms(abs(stas[i,1]))
    west = "W"
    north = "N"
    elevation = stas[i,2]
    f.write(f'{sta:<5} {network_code:<2} {comp_code[:-1]:<1}{channel_code:<3} {station_weight}{abs(lat_degree):2.0f} {abs(lat_minute):7.4f}{north}{abs(lng_degree):3.0f} {abs(lng_minute):7.4f}{west}{elevation:4.0f}\n')
f.close()

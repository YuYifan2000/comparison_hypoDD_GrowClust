from obspy.geodetics.base import gps2dist_azimuth
import numpy as np

# station file
stations = np.load('../o_station.npy')
f = open('./stlist.in','w')
for i in range(0,len(stations)):
    st = 'ST'+str(i)
    lat = stations[i][0]
    lon = stations[i][1]
    dep = stations[i][2]
    f.write(f' X {st.ljust(6," ")} {lat:.5f}  {lon:.5f}   {-dep/1000.:.2f}\n')
f.close()

# event list file
f = open('../growclust/evlist.txt','r')
Lines = f.readlines()
f.close()
f = open('evlist.in','w')
for line in Lines:
	tmp = line.split()
	yr = tmp[0]
	mo = tmp[1]
	day = tmp[2]
	hr = tmp[3]
	mi = tmp[4]
	sec = tmp[5]
	lat = tmp[6]
	lon = tmp[7]
	dep = tmp[8]
	mag = tmp[9]
	id = tmp[-1]
	f.write(f'{id.rjust(10," ")} {yr} {mo.rjust(2," ")} {day.rjust(2, " ")} {hr.rjust(2, " ")} {mi.rjust(2, " ")} {float(sec):6.3f}  {lat.ljust(8, " ")}  {lon.ljust(10," ")}   {dep}  {mag}\n')
f.close()

# cc file
f = open('../hypodd/dt.cc','r')
Lines = f.readlines()
f.close()
f = open('xcorr_coef.in','w')
ev_list = open('evlist.in','r')
ev = ev_list.readlines()
ev_list.close()
st_file = open('stlist.in', 'r')
st_list = st_file.readlines()

for line in Lines:
	if line[0] == '#':
		ev1 = int(line.split()[1])
		ev2 = int(line.split()[2])
		f.write(f'#{str(ev1).rjust(11," ")}{str(ev2).rjust(11," ")}\n')
		mid_lat = (float(ev[ev1-1].split()[7]) + float(ev[ev2-1].split()[7])) / 2
		mid_lon = (float(ev[ev1-1].split()[8]) + float(ev[ev2-1].split()[8])) / 2
	else:
		st = line.split()[0]
		idx = int(st.strip('ST'))
		phase = line.split()[-1]
		time = str(-float(line.split()[1]))
		value = line.split()[2]
		sta_lat = float(st_list[idx].split()[2])
		sta_lon = float(st_list[idx].split()[3])
		dist = gps2dist_azimuth(mid_lat, mid_lon, sta_lat, sta_lon)[0]/1000.
		f.write(f' X {st.ljust(6," ")}{phase}  {time.rjust(6," ")}   {value}   {dist:4.1f}\n')
f.close()

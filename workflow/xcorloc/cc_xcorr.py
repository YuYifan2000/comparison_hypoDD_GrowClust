from obspy.geodetics.base import gps2dist_azimuth
f = open('dt.cc','r')
Lines = f.readlines()
f.close()
f = open('xcorr_coef.in','w')
ev_list = open('evlist.in','r')
ev = ev_list.readlines()
ev_list.close()
st_file = open('station.dat', 'r')
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
		time = line.split()[1]
		value = line.split()[2]
		sta_lat = float(st_list[idx].split()[1])
		sta_lon = float(st_list[idx].split()[2])
		dist = gps2dist_azimuth(mid_lat, mid_lon, sta_lat, sta_lon)[0]/1000.
		f.write(f' X {st.ljust(6," ")}{phase}  {time.rjust(6," ")}   {value}   {dist:4.1f}\n')
f.close()

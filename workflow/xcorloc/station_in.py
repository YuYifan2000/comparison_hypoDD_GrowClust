f = open('./station.dat', 'r')
lines = f.readlines()
f.close()
f = open('./stlist.in','w')
for line in lines:
	st = line.split()[0]
	lat = float(line.split()[1])
	lon = float(line.split()[2])
	f.write(f' X {st.ljust(6," ")} {lat:.5f}  {lon:.5f}   0.0\n')
f.close()

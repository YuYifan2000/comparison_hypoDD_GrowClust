f = open('evlist.txt','r')
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

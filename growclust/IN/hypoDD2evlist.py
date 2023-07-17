input = './hypoDD.loc'
output = './evlist.txt'
f1 = open(input, 'r')
f2 = open(output,'w')
contents = f1.readlines()
for i in contents:
	content = i.split()
	evid = content[0]
	la = content[1]
	lo = content[2]
	dep = content[3]
	yr = content[10]
	mo = content[11]
	day = content[12]
	hr = content[13]
	min = content[14]
	sec = content[15]
	mag = content[16]
	setence = f'{yr} {mo} {day} {hr} {min} {sec} {la} {lo} {dep} {mag} 0.000 0.000 0.000 {evid}\n'
	f2.write(setence)
f1.close()
f2.close()

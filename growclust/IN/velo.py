input = './vjma2001'
output = './vzmodel.txt'
f1 = open(input, 'r')
f2 = open(output,'w')
contents = f1.readlines()
for i in contents:
	content = i.split()
	if float(content[2])>30.:
		break
	setence = f'{content[2]} {content[0]} {content[1]}\n'
	f2.write(setence)
f1.close()
f2.close()

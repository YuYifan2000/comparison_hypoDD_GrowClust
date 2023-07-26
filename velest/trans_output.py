# translate hypocenter.CNV to hypoDD.pha
f = open('./hypocenter.CNV', 'r')
output = open('./velest.pha', 'w+')
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
        tmp = line.split()[1]
        hour = tmp[:2]
        min = tmp[2:4]
        sec = float(line.split()[2])
        lat = line.split()[3][:-1]
        lon = line.split()[4][:-1]
        dep = line.split()[5]
        output.write(f'# {year} {mon} {day} {hour} {min} {sec} {lat} {lon} {dep} 1 0 0 0 {idx}\n')
    else:
        length = len(line)
        for i in range(0, length//12):
            tmp = line[i*12:(i+1)*12]
            sta = tmp[:4]
            phase = tmp[4]
            time = tmp.split()[-1]
            output.write(f'{sta}   {time}   1.00   {phase}\n')

output.close()
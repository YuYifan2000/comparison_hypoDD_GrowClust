# translate input for velest

# model-file
'''
f = open('bv.mod', 'w+')

f.write("10     vel,depth,vdamp (f5.2,5x,f7.2,2x,f7.3,3x,a1)\n")
refer = open('../vjma2001', 'r')
Lines = refer.readlines()[:60]
refer.close()


for count in range(0, 60, 5):
    line = Lines[count]
    vel = float(line.split()[0])
    dep = float(line.split()[2])
    if count == 0:
        f.write(f"{vel:5.2f}     {dep:7.2f}  {001.00}  P-VELOCITY MODEL\n")
    else:
        f.write(f"{vel:5.2f}     {dep:7.2f}  {001.00}\n")

for count in range(0, 60, 5):
    line = Lines[count]
    vel = float(line.split()[1])
    dep = float(line.split()[2])
    if count == 0:
        f.write(f"{vel:5.2f}     {dep:7.2f}  {001.00}  S-VELOCITY MODEL\n")
    else:
        f.write(f"{vel:5.2f}     {dep:7.2f}  {001.00}\n")

f.close()
'''
# station - file
f = open('./bv.sta', 'w+')
f.write('(a4,f7.4,a1,1x,f8.4,a1,1x,i4,1x,i1,1x,i3,1x,f5.2,2x,f5.2)\n')
refer = open('../hypoDD/station.dat', 'r')
Lines = refer.readlines()
refer.close()
c = 0
for line in Lines:
    c += 1
    sta = line.split()[0]
    lat = float(line.split()[1])
    lon = float(line.split()[2])
    ele = 0.0
    pdelay = 0.00
    sdelay = 0.00
    imod = 1
    f.write(f'{sta:4s}{lat:7.4f}N {lon:8.4f}W {ele:4.0f} 1 {str(c).rjust(3,"0")} {pdelay:5.2f}  {sdelay:5.2f}   {imod:1.0f}\n')
f.close()

# earthquake data file
f = open('./bv.cnv', 'w+')
refer = open('../hypoDD/test.pha', 'r')
Lines = refer.readlines()
refer.close()
for line in Lines:
    if line[0] == '#':
        f.write('\n')
        year = line.split()[1]
        mon = line.split()[2]
        day = line.split()[3]
        hour = line.split()[4]
        min = line.split()[5]
        sec = float(line.split()[6])
        lat = float(line.split()[7])
        lon = float(line.split()[8])
        dep = float(line.split()[9])
        mag = 0.0
        f.write(f"{year[2:]}{mon.rjust(2,'0')}{day.rjust(2,'0')} {hour.rjust(2,' ')}{min.rjust(2,' ')} {sec:5.2f} {lat:7.4f}N {lon:8.4f}W {dep:8.4f} {mag:7.2f} 0\n")
        count = 0
    else:
        count += 1
        sta = line.split()[0]
        tt = float(line.split()[1])
        f.write(f"{sta.ljust(4,' ')}{line.split()[3]}0 {tt:5.2f}")
        if count == 6:
            count = 0
            f.write('\n')
        

f.close()
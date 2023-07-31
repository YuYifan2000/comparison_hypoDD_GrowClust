import numpy as np
# station - file
f = open('./velest.sta', 'w+')
f.write('(a4,f7.4,a1,1x,f8.4,a1,1x,i4,1x,i1,1x,i3,1x,f5.2,2x,f5.2)\n')
stas = np.load('station.npy')
num_sta = len(stas)
c = 0
for i in range(0, num_sta):
    sta = 'ST' + str(i)
    lat = stas[i,0]
    lon = stas[i,1]
    ele = 0.0
    pdelay = 0.00
    sdelay = 0.00
    imod = 1
    f.write(f'{sta:4s}{lat:7.4f}N {lon:8.4f}W {ele:4.0f} 1 {str(i).rjust(3,"0")} {pdelay:5.2f}  {sdelay:5.2f}   {imod:1.0f}\n')
f.close()

# earthquake data file
f = open('./velest.cnv', 'w+')
sources = np.load('source.npy')
tt_p = np.load('tt_P.npy')
tt_s = np.load('tt_S.npy')
for i in range(0, len(sources)):
    f.write('\n')
    year = '2000'
    mon = '12'
    day = '13'
    hour = '15'
    min = '10'
    sec = 1.0
    lat = sources[i, 0]
    lon = sources[i, 1]
    dep = sources[i, 2]
    mag = 5.0
    f.write(f"{year[2:]}{mon.rjust(2,'0')}{day.rjust(2,'0')} {hour.rjust(2,' ')}{min.rjust(2,' ')} {sec:5.2f} {lat:7.4f}N {lon:8.4f}W {dep:8.4f} {mag:7.2f} 0\n")
    count = 0
    for j in range(0, num_sta):
        count += 2
        sta = 'ST' + str(j)
        tt = tt_p[i,j]
        f.write(f"{sta.ljust(4,' ')}P0 {tt:5.2f}")
        tt = tt_s[i,j]
        f.write(f"{sta.ljust(4,' ')}S0 {tt:5.2f}")
        if count == 6:
            count = 0
            f.write('\n')
f.close()

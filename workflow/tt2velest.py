import numpy as np
from datetime import datetime, timedelta
def generate_outlier(start, end):
    num = np.random.uniform(-end, end)
    while -start <= num <= start:
        num = np.random.uniform(-end, end)
    return num

np.random.seed(1)
p_prob = 0.67
s_prob = 0.5
outlier_p = 0.01
outlier_s = 0.04
# station - file
f = open('./velest.sta', 'w+')
f.write('(a4,f7.4,a1,1x,f8.4,a1,1x,i4,1x,i1,1x,i3,1x,f5.2,2x,f5.2)\n')
stas = np.load('o_station.npy')
num_sta = len(stas)
c = 0
for i in range(0, num_sta):
    sta = 'ST' + str(i)
    lat = stas[i,0]
    lon = abs(stas[i,1])
    ele = stas[i,2]
    pdelay = 0.00
    sdelay = 0.00
    imod = 1
    f.write(f'{sta:4s}{lat:7.4f}N {lon:8.4f}W {ele:4.0f} 1 {str(i).rjust(3,"0")} {pdelay:5.2f}  {sdelay:5.2f}   {imod:1.0f}\n')
f.write('\n')
f.close()


# earthquake data file
f = open('./velest.cnv', 'w+')
sources = np.load('o_source.npy')
tt_p = np.load('tt_P.npy')
tt_s = np.load('tt_S.npy')
out_list = open('./outlier_list.txt','w')
out_list.write('event_num sta_num phase\n')
start_time = datetime.strptime('2000-12-13T15:10:1', '%Y-%m-%dT%H:%M:%S')
for i in range(0, 1000):
    if i > 0:
        f.write('\n')
    year = start_time.strftime("%Y")
    mon = start_time.strftime("%m")
    day = start_time.strftime("%d")
    hour = start_time.strftime("%H")
    min = start_time.strftime("%M")
    sec = float(start_time.second)
    start_time = start_time + timedelta(hours=1)
    lat = sources[i, 0]
    lon = abs(sources[i, 1])
    dep = sources[i, 2]
    mag = 5.0
    f.write(f"{year[2:]}{mon.rjust(2,'0')}{day.rjust(2,'0')} {hour.rjust(2,' ')}{min.rjust(2,' ')} {sec:5.2f} {lat:7.4f}N {lon:8.4f}W {dep:8.4f} {mag:7.2f} 0\n")
    count = 0
    #for j in range(0, 6):
    for j in range(0, num_sta):
        sta = 'ST' + str(j)
        # p
        prob = np.random.rand()
        if prob < p_prob:
            count += 1
            tt = tt_p[i,j] + np.random.laplace(0, 0.02,)# long tail==double exponential?
            prob_outlier = np.random.rand()
            if prob_outlier < outlier_p:
                tt = tt + generate_outlier(0.4, 1)
                out_list.write(f'{i} {j} P\n')
            f.write(f"{sta.ljust(4,' ')}P0 {round(tt, 2):5.2f}")

        if count == 6:
            count = 0
            f.write('\n')
        # s
        prob = np.random.rand()
        if prob < s_prob:
            count += 1
            tt = tt_s[i,j] + np.random.laplace(0, 0.04,)
            prob_outlier = np.random.rand()
            if prob_outlier < outlier_s:
                tt = tt + generate_outlier(0.4, 1.4)
                out_list.write(f'{i} {j} S\n')
            f.write(f"{sta.ljust(4,' ')}S0 {round(tt, 2):5.2f}")
        if count == 6:
            count = 0
            f.write('\n')
    if count != 0:
        f.write('\n')
f.close()

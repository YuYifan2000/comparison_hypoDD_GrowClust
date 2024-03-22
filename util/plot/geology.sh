# !/usr/bin/env bash
# plot elevation and satellite image
gmt begin 3d_ridgecrest
	R=-R-118.0/-117.0/35.3/36.15
	gmt set MAP_FRAME_TYPE plain
	gmt set FONT_ANNOT_PRIMARY 4p,Helvetica,black
	# preprocess fault 
	#gmt grdtrack $R -G@earth_relief_01s CA_fault_data.txt > faults.xyz
	# preprocess image
	# gmt which -Gl @earth_day_30s_p
	#gdal_translate -of GTIFF -projwin -118.1 36.15 -117.0 35.3 earth_day_30s_p.tif day.tif

	# plot satellite image 
	gmt grdview @earth_relief_01s $R/0/2500 -JM6c -JZ1c -N0+ggray -Gday.tif -Qi -Ba -Bz -BwSEnZ -p160/20
	#gmt grdview @earth_relief_01s -R-120/-117/35/36/-8000/3000 -JM10c -JZ4c  -Gday.tif -Qi -Ba -Bz -BwsENZ -p150/20
	# plot fault line
	# gmt plot3d faults.xyz -W1p,brown -p
	# gmt makecpt -Croma -T2/5/0.1 -Z
	# # plot velocity
	# gmt grdimage ./p_velocity.nc -p150/20/10000 -Bwsen -C
	# gmt colorbar -C -Ba+l'P Velocity (km/s)' -DJCT+o0/1c -p150/20/10000
	# plot QTM catalog
	# build up a colorbar
	gmt makecpt -Cviridis -T0/10/0.1 -Z -D
	awk '{if ($9<=-117.1 && $9>=-118.0 && $8>=35.5 && $8<=36.0) print $9,$8,600,$10}' ridgecrest_qtm.cat | gmt plot3d -Sc0.2p -C -p160/20
	# plot station
	#awk '{print $3,$2,$4}' station.dat | gmt plot3d -St7p -GPtest.jpg -p
	awk '{print $3,$2,$4}' station.dat | gmt plot3d -St5p -Gblue -p160/20 -W0.2p,white
	
	gmt colorbar -C -Ba+l'Depth (km)' -DJBC+o0/1c -p160/20/100
	gmt basemap -TdjRM+w0.8c+l+o-1c/-0.5c+f1 -p160/20/0
	gmt legend -DjRB+w0.9c/0.4c+o-1.c/-0.2c -F+p0.5p << EOF
G -0.1c
S - t 0.1c blue 0.2p - Station
S - c 0.1c - 0.2p - Event
EOF

gmt end show


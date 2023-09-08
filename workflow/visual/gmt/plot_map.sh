#!/usr/bin/env bash
gmt begin map pdf E300
gmt set FORMAT_GEO_MAP ddd.x
gmt set FONT_ANNOT 8p,Helvetica,black
gmt basemap -R-118/-117.2/35.4/36.31 -JX7c/8c -BWSen -Ba0.2
gmt makecpt -T-200/2500/200 -Cetopo1 -Z
#gmt grdimage @earth_relief_01s -R-118.0/-117.2/35.4/36.33 -JM8c -BWSen -Ba0.2 -C

awk {'print $1,$2'} source.csv | gmt plot -Sc+0.01i -Gblack
gmt plot -Sc+0.07i -Gblack -l"Event" << EOF
-119. 33
EOF
awk {'print $1,$2'} stations.txt | gmt plot -Si+0.09i -Gblue -l"Station" -t20
    gmt inset begin -DjTR+w2.0c/2.05c+o0.1c/0.1c -F+gwhite+p1p
        gmt coast -R-124/-112/31/41 -JM? -Df  -Glightbrown -A10000 -Slightblue
        echo -118.1 35.4 -117.2 36.4 | gmt plot -Sr+s -W0.5p,blue
    gmt inset end
gmt legend -DjBR+o0.1c/0.1c -F+p0.5p
gmt end show

cd ./hypoDD
ph2dt ph2dt.inp
python dt_form_cc.py
hypoDD hypodd_ct.inp

cp ./station.dat ../growclust/IN/stlist.txt
cp ./event.sel ../growclust/IN/
cp ./dt.cc ../growclust/IN/
cd ../growclust/IN
python event2evlist.py
cd ..
growclust ssprings.inp > gc.log
cd ..
python plot_compare.py

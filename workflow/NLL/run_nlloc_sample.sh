START=`date +%s`
echo "Script to run sample locations for NonLinLoc - Non-Global mode"
echo "Generate velocity grids "
# Vel2Grid ./nlloc_sample.in
echo "Generate and view the travel-time and take-off angle grids "
# Grid2Time ./nlloc_sample.in
# echo "Generate some synthetic arrival times "
# Time2EQ run/nlloc_sample.in
# more obs_synth/synth.obs
echo
echo "Do the event Location "
NLLoc ./nlloc_sample.in
#echo "Plot the first event location with GMT"
#echo "Plot the combined locations with GMT"
# LocSum loc/ridgecrest.sum.grid0.loc 1 loc/sum "loc/ridgecrest.*.*.grid0.loc"
END=`date +%s`
DIFF3=$(( $END - $START ))
echo "time:$DIFF3 s"
